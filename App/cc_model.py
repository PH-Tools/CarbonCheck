# -*- Python Version: 3.10 -*-

"""Main Application Model."""

from typing import Dict, get_type_hints, Any, Optional
from types import ModuleType
import enum
import json
import os
import pathlib

import xlwings as xw
from rich import print

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from PHX.xl import xl_app
from PHX.PHPP import phpp_app

from NBDM.model import project, team, site, building
from NBDM.model.project import NBDM_Project
from NBDM.to_Excel import report
from NBDM.from_PHPP import create_NBDM_BuildingSegment, create_NBDM_Team, create_NBDM_Site
from NBDM.to_JSON.write import NBDM_Project_to_json_file


def is_dict_field(_class: type) -> bool:
    """Return True if the class provided is a dataclass Dict field (has __origin__ attr)."""
    if getattr(_class, "__origin__", None) == dict:
        return True
    return False


def is_dataclass_type(_class: type) -> bool:
    """Return True if the class provided is a dataclass."""
    if not hasattr(_class, "__dataclass_fields__"):
        return False
    return True


def is_NBDM_class(_class: type) -> bool:
    """Return True if the class provided is an NBDM Type."""
    if not is_dataclass_type(_class):
        return False
    if "NBDM" not in _class.__name__.upper():
        return False
    return True


def is_enum(_class: type) -> bool:
    """Return True if the class provided is an enum.Enum"""
    return issubclass(_class, enum.Enum)


def get_formatted_field_name(_output_format: ModuleType, _obj: Any, _field_name: str) -> Optional[str]:
    """Return an NBDM Object field_name in a user-facing format (nice)."""
    format_class = getattr(_output_format, f"Format_{_obj.__class__.__name__}")
    return getattr(format_class, _field_name, None)


def replace_key_names(_data: Dict[str, str], _output_format: ModuleType, _obj: Any) -> Dict[str, str]:
    """Replace the user-facing keys in a treeView dict with the actual field names.
    
    Arguments:
    ----------
        * _data: (Dict[str, Any]) The dict to replace the keys in.
        * _output_format: (ModuleType) The module containing the user-facing names.
        * _obj: (Any) The NBDM Object to get the field names from.
    
    Returns:
    --------
        * (Dict[str, Any]) The dict with the user-facing keys replaced with the actual field names.
    """
    format_type = getattr(_output_format, f"Format_{_obj.__name__}")
    
    d_ = {}
    for k, v in _data.items():
        # -- Got through all the items in the source dict
        for dict_field_name, formatted_name in vars(format_type).items():
            if k != formatted_name:
                # -- Not not a valid NBDM object field, ignore...
                continue

            if isinstance(v, dict):
                # -- Is an NBDM field, get the type and recurse
                obj = get_type_hints(_obj)[dict_field_name]
                d_[dict_field_name] = replace_key_names(v, _output_format, obj)
            else:
                # -- Is an valid NBDM object field, add it to the new dict
                d_[dict_field_name] = v
    return d_


def NBDM_Object_from_treeView(_output_format: ModuleType, _data: Dict[str, Any], _obj: Any):
    """Create a NBDM_Team object from treeView dict data.
    
    Arguments:
    ----------
        * _output_format: (ModuleType) The module containing the user-facing names.
        * _data: (Dict[str, Any]) The dict to create the NBDM_Team from.
        * _obj: (Any) The NBDM Object to create.

    Returns:
    --------
        * (Any) The NBDM object created from the dict.
    """
    new_NBDM_obj = _obj.from_dict(replace_key_names(_data, _output_format, _obj))
    return new_NBDM_obj


class WorkerReadProjectData(qtc.QObject):
    """Thread Worker for loading Project Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        xl = xl_app.XLConnection(xl_framework=xw, output=print, xl_file_path=_filepath)
        phpp_conn = phpp_app.PHPPConnection(xl)

        with phpp_conn.xl.in_silent_mode():
            _project.team = create_NBDM_Team(phpp_conn)
            _project.site = create_NBDM_Site(phpp_conn)

        self.loaded.emit(_project)


class WorkerReadBaselineSegmentData(qtc.QObject):
    """Thread Worker for loading Baseline Segment Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        xl = xl_app.XLConnection(xl_framework=xw, output=print, xl_file_path=_filepath)
        phpp_conn = phpp_app.PHPPConnection(xl)

        with phpp_conn.xl.in_silent_mode():
            new_seg = create_NBDM_BuildingSegment(phpp_conn)
            _project.add_new_baseline_segment(new_seg)

        self.loaded.emit(_project)


class WorkerReadProposedSegmentData(qtc.QObject):
    """Thread Worker for loading Proposed Segment Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        xl = xl_app.XLConnection(xl_framework=xw, output=print, xl_file_path=_filepath)
        phpp_conn = phpp_app.PHPPConnection(xl)

        with phpp_conn.xl.in_silent_mode():
            new_seg = create_NBDM_BuildingSegment(phpp_conn)
            _project.add_new_proposed_segment(new_seg)

        self.loaded.emit(_project)


class WorkerWriteExcelReport(qtc.QObject):
    """Thread Worker for writing out the report to Excel."""

    written = qtc.pyqtSignal(NBDM_Project)

    @qtc.pyqtSlot(NBDM_Project)
    def run(self, _project: NBDM_Project):
        xl = xl_app.XLConnection(xl_framework=xw, output=print)
        output_report = report.OutputReport(_xl=xl, _autofit=True, _hide_groups=False)

        with xl.in_silent_mode():
            xl.activate_new_workbook()
            row_num = output_report.write_NBDM_Project(_nbdm_object=_project)
            row_num = output_report.write_NBDM_WholeBuilding(_nbdm_object=_project)
            row_num = output_report.write_NBDM_BuildingSegments(_nbdm_object=_project)
            output_report.remove_sheet_1()

        self.written.emit(_project)


class CCModel(qtw.QWidget):
    """CarbonCheck Model Class."""

    # -- Signals for passing data back to treeViews
    load_team_data = qtc.pyqtSignal(dict)
    load_site_data = qtc.pyqtSignal(dict)
    load_baseline_segments_data = qtc.pyqtSignal(dict)
    load_proposed_segments_data = qtc.pyqtSignal(dict)
    
    # -- Signals for reading data from the GUI treeViews
    read_treeView_team = qtc.pyqtSignal()
    read_treeView_site = qtc.pyqtSignal()
    read_treeView_proposed_segments = qtc.pyqtSignal()
    read_treeView_baseline_segments = qtc.pyqtSignal()

    # -- Thread workers for reading / writing PHPP data
    read_project_data_from_file = qtc.pyqtSignal(NBDM_Project, pathlib.Path)
    read_baseline_seg_data_from_file = qtc.pyqtSignal(NBDM_Project, pathlib.Path)
    read_proposed_seg_data_from_file = qtc.pyqtSignal(NBDM_Project, pathlib.Path)
    write_excel_report = qtc.pyqtSignal(NBDM_Project)

    def __init__(self, _output_format: ModuleType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_format = _output_format
        self.NBDM_project = NBDM_Project()
        self.configure_worker_threads()

    def configure_worker_threads(self):
        """Configure and start up all the worker threads for read/write."""
        self._create_workers()
        self._start_worker_threads()
        self._connect_worker_signals()

    def _create_workers(self):
        self.worker_read_proj_data = WorkerReadProjectData()
        self.worker_read_proj_data_thread = qtc.QThread()

        self.worker_read_baseline_seg_data = WorkerReadBaselineSegmentData()
        self.worker_read_baseline_seg_data_thread = qtc.QThread()

        self.worker_read_prop_seg_data = WorkerReadProposedSegmentData()
        self.worker_read_prop_seg_data_thread = qtc.QThread()

        self.worker_write_report = WorkerWriteExcelReport()
        self.worker_write_report_thread = qtc.QThread()

    def _start_worker_threads(self):
        self.worker_read_proj_data.moveToThread(self.worker_read_proj_data_thread)
        self.worker_read_proj_data_thread.start()

        self.worker_read_baseline_seg_data.moveToThread(
            self.worker_read_baseline_seg_data_thread
        )
        self.worker_read_baseline_seg_data_thread.start()

        self.worker_read_prop_seg_data.moveToThread(self.worker_read_prop_seg_data_thread)
        self.worker_read_prop_seg_data_thread.start()

        self.worker_write_report.moveToThread(self.worker_write_report_thread)
        self.worker_write_report_thread.start()

    def _connect_worker_signals(self):
        self.worker_read_proj_data.loaded.connect(self.set_NBDM_project)
        self.read_project_data_from_file.connect(self.worker_read_proj_data.run)

        self.worker_read_baseline_seg_data.loaded.connect(self.set_NBDM_project)
        self.read_baseline_seg_data_from_file.connect(
            self.worker_read_baseline_seg_data.run
        )

        self.worker_read_prop_seg_data.loaded.connect(self.set_NBDM_project)
        self.read_proposed_seg_data_from_file.connect(self.worker_read_prop_seg_data.run)

        self.worker_write_report.written.connect(self.set_NBDM_project)
        self.write_excel_report.connect(self.worker_write_report.run)

    def set_NBDM_project(self, _project: NBDM_Project) -> None:
        self.NBDM_project = _project
        self.update_treeview_team()
        self.update_treeview_baseline()
        self.update_treeview_proposed()

    def create_tree_data(self, _obj: Any) -> Dict[str, Any]:
        """Recursively build up a dict of string values for the Project Data TreeView."""
        # Note: cannot use dataclasses.fields() 'cus __future__ annotations
        # breaks it and all .type comes as str.
        d = {}
        for field_name, field_type in get_type_hints(_obj.__class__).items():
            # -- Exclude the Variants from the Project data view.
            if field_name == "variants":
                continue

            # -- Exclude whatever this is
            if is_dict_field(field_type):
                continue

            # -- Figure out the right view-name to use
            field_view_name = get_formatted_field_name(self.output_format, _obj, field_name)
            if not field_view_name:
                continue

            if is_NBDM_class(field_type):
                d[field_view_name] = self.create_tree_data(getattr(_obj, field_name))
            elif is_enum(field_type):
                d[field_view_name] = getattr(_obj, field_name).value
            else:
                d[field_view_name] = getattr(_obj, field_name)
        return d

    def output_dict_to_JSON_file(
        self, _filepath: pathlib.Path, config_data: Dict[str, Any]
    ) -> None:
        """Write out a dict to a JSON file."""
        try:
            with open(_filepath, "w") as write_file:
                json.dump(config_data, write_file, indent=2)
                return
        except Exception as ex:
            print(f"Error trying to write out to JSON file: {_filepath}")
            print(ex)
            return

    def update_treeview_team(self):
        """Build the treeView data dict from the Project and pass back to the view."""
        tree_project_data = {}
        tree_project_data.update(self.create_tree_data(self.NBDM_project.team))
        tree_project_data.update(self.create_tree_data(self.NBDM_project.site))
        self.load_team_data.emit(tree_project_data)

    def update_treeview_baseline(self):
        """Build the treeView data dict from the Project and pass back to the view."""
        baseline_segment_dict = {}
        for segment in self.NBDM_project.variants.baseline.building_segments:
            seg_name = f"BUILDING SEGMENT: {segment.segment_name}"
            baseline_segment_dict[seg_name] = self.create_tree_data(segment)
        self.load_baseline_segments_data.emit(baseline_segment_dict)

    def update_treeview_proposed(self):
        """Build the treeView data dict from the Project and pass back to the view."""
        proposed_segment_dict = {}
        for segment in self.NBDM_project.variants.proposed.building_segments:
            seg_name = f"BUILDING SEGMENT: {segment.segment_name}"
            proposed_segment_dict[seg_name] = self.create_tree_data(segment)
        self.load_proposed_segments_data.emit(proposed_segment_dict)

    def load_cc_project_from_file(self, _filepath: pathlib.Path):
        """Build up an NBDM_Project from a save file and set as the active."""
        data = self.load_json_file_as_dict(_filepath)
        self.NBDM_project = project.NBDM_Project.from_dict(data)

        self.update_treeview_team()
        self.update_treeview_baseline()
        self.update_treeview_proposed()

    def load_json_file_as_dict(self, _filepath: pathlib.Path) -> Dict:
        """Read in a dict from a JSON file."""
        try:
            if not os.path.exists(_filepath):
                print(f"Warning: No file named: {_filepath}")
                return {}

            with open(_filepath, "r") as read_file:
                return json.load(read_file)
        except Exception as ex:
            print(f"Error trying to read in JSON file: {_filepath}")
            print(ex)
            return {}

    def write_json_file(self, _filepath: pathlib.Path):
        # TODO: Collect new model from UI first...
        NBDM_Project_to_json_file(self.NBDM_project, _filepath)

    def set_project_from_gui(self):
        """Read in all the data in the GUI fields and build a new project."""
        print(">> 2) CCModel.set_project_from_gui()")
        self.read_treeView_team.emit()
        self.read_treeView_site.emit()
        self.read_treeView_proposed_segments.emit()
        self.read_treeView_baseline_segments.emit()

    @qtc.pyqtSlot(dict)
    def set_project_team_from_treeView_data(self, _data: Dict[str, str]) -> None:
        """Set the self.NBDM_project.team from the data in the treeView"""
        print(">>    3.1) CCModel.set_project_team_from_treeView_data(_data)")
        self.NBDM_project.team = NBDM_Object_from_treeView(self.output_format, _data, team.NBDM_Team)

    @qtc.pyqtSlot(dict)
    def set_project_site_from_treeView_data(self, _data: Dict[str, str]) -> None:
        """Set the self.NBDM_project.site from the data in the treeView"""
        print(">>    4.1) CCModel.set_project_site_from_treeView_data(_data)")
        self.NBDM_project.site = NBDM_Object_from_treeView(self.output_format, _data, site.NBDM_Site)

    @qtc.pyqtSlot(dict)
    def set_project_proposed_segments_from_treeView_data(self, _data: Dict[str, Any]) -> None:
        """Set the self.NBDM_project.variants.proposed from the data in the treeView"""
        print(">>    5.1) CCModel.set_project_proposed_segments_from_treeView_data(_data)")
        self.NBDM_project.variants.proposed.clear_variant_building_segments()
        for segment_data in _data.values():
            new_segment = NBDM_Object_from_treeView(self.output_format, segment_data, building.NBDM_BuildingSegment)
            self.NBDM_project.add_new_proposed_segment(new_segment)

    @qtc.pyqtSlot(dict)
    def set_project_baseline_segments_from_treeView_data(self, _data: Dict[str, Any]) -> None:
        """Set the self.NBDM_project.variants.baseline from the data in the treeView"""
        print(">>    6.1) CCModel.set_project_baseline_segments_from_treeView_data(_data)")
        self.NBDM_project.variants.baseline.clear_variant_building_segments()
        for segment_data in _data.values():
            new_segment = NBDM_Object_from_treeView(self.output_format, segment_data, building.NBDM_BuildingSegment)
            self.NBDM_project.add_new_baseline_segment(new_segment)