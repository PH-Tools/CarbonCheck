# -*- Python Version: 3.11 -*-

"""Main Application Model."""

import json
import logging
import os
import pathlib
import sys
from typing import Dict, get_type_hints, Any, Optional, List, Generator, Union
from types import ModuleType


try:
    from PyQt6 import QtGui as qtg
    from PyQt6 import QtWidgets as qtw
    from PyQt6 import QtCore as qtc
except Exception as e:
    raise Exception("Error importing PyQt6 library?", e)

try:
    from CC_GUI.cc_workers import (
        WorkerReadProjectData,
        WorkerReadBaselineSegmentData,
        WorkerReadProposedSegmentData,
        WorkerWriteExcelReport,
        WorkerSetPHPPBaseline,
        WorkerSetWUFIBaseline,
        WorkerReadBldgComponentData,
    )
    from CC_GUI.views.tree_view_tools import (
        create_tree_data,
        build_NBDM_obj_from_treeView,
        NBDM_Object_from_treeView,
    )
except Exception as e:
    raise Exception("Error importing App library?", e)

try:
    from NBDM.model import (
        project,
        team,
        site,
        building,
        envelope,
        appliances,
        dhw_systems,
        heating_systems,
        cooling_systems,
        renewable_systems,
    )
    from NBDM.model.project import NBDM_Project
    from NBDM.to_JSON.write import NBDM_Project_to_json_file
    from NBDM.model.serialization import build_NBDM_obj_from_treeView
except Exception as e:
    raise Exception("Error importing NBDM library?", e)

try:
    from ph_baseliner.codes.model import BaselineCode
    from ph_baseliner.codes.options import (
        ClimateZones,
        BaselineCodes,
        Use_Groups,
        PF_Groups,
    )
except Exception as e:
    raise Exception("Error importing ph_baseliner library?", e)


class CCModel(qtw.QWidget):
    """CarbonCheck Model Class."""

    # -- Signals for passing data back to treeViews
    sig_load_team_data = qtc.pyqtSignal(dict)
    sig_load_site_data = qtc.pyqtSignal(dict)
    sig_load_baseline_segments_data = qtc.pyqtSignal(dict)
    sig_load_proposed_segments_data = qtc.pyqtSignal(dict)
    sig_load_bldg_components_data = qtc.pyqtSignal(dict)

    # -- Signals for reading data from the GUI treeViews
    sig_read_treeView_team = qtc.pyqtSignal()
    sig_read_treeView_site = qtc.pyqtSignal()
    sig_read_treeView_proposed_segments = qtc.pyqtSignal()
    sig_read_treeView_baseline_segments = qtc.pyqtSignal()
    sig_read_treeView_envelope = qtc.pyqtSignal()
    sig_read_treeView_appliances = qtc.pyqtSignal()

    # -- Thread workers for reading / writing PHPP and WUFI data
    sig_read_project_data_from_file = qtc.pyqtSignal(NBDM_Project, pathlib.Path)
    sig_read_baseline_seg_data_from_file = qtc.pyqtSignal(NBDM_Project, pathlib.Path)
    sig_read_proposed_seg_data_from_file = qtc.pyqtSignal(NBDM_Project, pathlib.Path)
    sig_read_bldg_component_data_from_file = qtc.pyqtSignal(NBDM_Project, pathlib.Path)

    # -- Thread workers for writing NBDM data to Excel report
    sig_write_excel_report = qtc.pyqtSignal(NBDM_Project, pathlib.Path)
    sig_write_baseline = qtc.pyqtSignal(pathlib.Path, BaselineCode, dict)
    sig_write_PHPP_baseline = qtc.pyqtSignal(pathlib.Path, BaselineCode, dict)
    sig_write_WUFI_baseline = qtc.pyqtSignal(pathlib.Path, BaselineCode, dict)

    def __init__(
        self, _output_format: ModuleType, _application_path: pathlib.Path, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing CCModel.")

        self.output_format = _output_format
        self.NBDM_project = NBDM_Project()
        self._configure_worker_threads()
        self.application_path = _application_path

    @property
    def worker_threads(self) -> Generator[qtc.QThread, None, None]:
        """Return a Generator which yields each of the worker threads."""
        return (attr for attr in vars(self).values() if isinstance(attr, qtc.QThread))

    def _configure_worker_threads(self) -> None:
        """Configure and start up all the worker threads for read/write."""
        self.logger.debug("Configuring worker threads.")
        self._create_workers()
        self._start_worker_threads()
        self._connect_worker_signals()

    def _create_workers(self) -> None:
        """Create all the worker threads."""
        self.logger.debug("Creating worker threads.")

        self.worker_read_proj_data = WorkerReadProjectData()
        self.worker_read_proj_data.setObjectName("Worker: Read Project Data")
        self.worker_read_proj_data_thread = qtc.QThread()
        self.worker_read_proj_data_thread.setObjectName(
            "Worker Thread: Read Project Data"
        )

        self.worker_read_baseline_seg_data = WorkerReadBaselineSegmentData()
        self.worker_read_baseline_seg_data.setObjectName("Worker: Read Baseline Seg Data")
        self.worker_read_baseline_seg_data_thread = qtc.QThread()
        self.worker_read_baseline_seg_data_thread.setObjectName(
            "Worker Thread: Read Baseline Seg Data"
        )

        self.worker_read_prop_seg_data = WorkerReadProposedSegmentData()
        self.worker_read_prop_seg_data.setObjectName("Worker: Read Proposed Seg. Data")
        self.worker_read_prop_seg_data_thread = qtc.QThread()
        self.worker_read_prop_seg_data_thread.setObjectName(
            "Worker Thread: Read Proposed Seg. Data"
        )

        self.worker_write_report = WorkerWriteExcelReport()
        self.worker_write_report.setObjectName("Worker: Write Excel Report")
        self.worker_write_report_thread = qtc.QThread()
        self.worker_write_report_thread.setObjectName("Worker Thread: Write Excel Report")

        self.worker_set_baseline_PHPP = WorkerSetPHPPBaseline()
        self.worker_set_baseline_PHPP.setObjectName("Worker: Set PHPP Baseline")
        self.worker_set_baseline_phpp_thread = qtc.QThread()
        self.worker_set_baseline_phpp_thread.setObjectName(
            "Worker Thread: Set PHPP Baseline"
        )

        self.worker_set_baseline_WUFI = WorkerSetWUFIBaseline()
        self.worker_set_baseline_WUFI.setObjectName("Worker: Set WUFI Baseline")
        self.worker_set_baseline_WUFI_thread = qtc.QThread()
        self.worker_set_baseline_WUFI_thread.setObjectName(
            "Worker Thread: Set WUFI Baseline"
        )

        self.worker_read_bldg_compo_data = WorkerReadBldgComponentData()
        self.worker_read_bldg_compo_data.setObjectName("Worker: Read Bldg. Compo. Data")
        self.worker_read_bldg_compo_data_thread = qtc.QThread()
        self.worker_read_bldg_compo_data_thread.setObjectName(
            "Worker Thread: Read Bldg. Compo. Data"
        )

    def _start_worker_threads(self) -> None:
        """Start all the worker threads."""
        self.logger.debug("Starting worker threads.")

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

        self.worker_set_baseline_PHPP.moveToThread(self.worker_set_baseline_phpp_thread)
        self.worker_set_baseline_phpp_thread.start()

        self.worker_set_baseline_WUFI.moveToThread(self.worker_set_baseline_WUFI_thread)
        self.worker_set_baseline_WUFI_thread.start()

        self.worker_read_bldg_compo_data.moveToThread(
            self.worker_read_bldg_compo_data_thread
        )
        self.worker_read_bldg_compo_data_thread.start()

    def _connect_worker_signals(self) -> None:
        """Connect all the worker signals."""
        self.logger.debug("Connecting worker signals.")

        self.worker_read_proj_data.loaded.connect(self.set_NBDM_project)
        self.sig_read_project_data_from_file.connect(self.worker_read_proj_data.run)

        self.worker_read_baseline_seg_data.loaded.connect(self.set_NBDM_project)
        self.sig_read_baseline_seg_data_from_file.connect(
            self.worker_read_baseline_seg_data.run
        )

        self.worker_read_prop_seg_data.loaded.connect(self.set_NBDM_project)
        self.sig_read_proposed_seg_data_from_file.connect(
            self.worker_read_prop_seg_data.run
        )

        self.worker_write_report.written.connect(self.set_NBDM_project)
        self.sig_write_excel_report.connect(self.worker_write_report.run)

        self.sig_write_PHPP_baseline.connect(self.worker_set_baseline_PHPP.run)
        self.sig_write_WUFI_baseline.connect(self.worker_set_baseline_WUFI.run)

        self.worker_read_bldg_compo_data.loaded.connect(self.set_NBDM_project)
        self.sig_read_bldg_component_data_from_file.connect(
            self.worker_read_bldg_compo_data.run
        )

    def set_NBDM_project(self, _project: NBDM_Project) -> None:
        """Set the NBDM_Project object and update the treeViews."""
        self.logger.debug("Setting NBDM_Project object.")

        self.NBDM_project = _project
        self.update_treeview_team()
        self.update_treeview_baseline()
        self.update_treeview_proposed()
        self.update_treeview_bldg_components()

    def output_dict_to_JSON_file(
        self, _filepath: pathlib.Path, config_data: Dict[str, Any]
    ) -> None:
        """Write out a dict to a JSON file."""
        self.logger.debug(f"Writing out to JSON file: {_filepath}")

        try:
            with open(_filepath, "w") as write_file:
                json.dump(config_data, write_file, indent=2)
                return
        except Exception as ex:
            msg = f"Error trying to write out to JSON file: {_filepath}"
            self.logger.error(msg)
            self.logger.error(ex, exc_info=True)
            return

    def update_treeview_team(self) -> None:
        """Build the treeView data dict from the Project and pass back to the view."""
        self.logger.debug("Updating treeView team data.")

        tree_project_data = {}
        tree_project_data.update(
            create_tree_data(self.output_format, self.NBDM_project.team)
        )
        tree_project_data.update(
            create_tree_data(self.output_format, self.NBDM_project.site)
        )
        self.sig_load_team_data.emit(tree_project_data)

    def update_treeview_baseline(self) -> None:
        """Build the treeView data dict from the Project and pass back to the view."""
        self.logger.debug("Updating treeView baseline data.")

        baseline_segment_dict = {}
        for segment in self.NBDM_project.variants.baseline.building_segments:
            seg_name = f"BUILDING SEGMENT: {segment.segment_name}"
            baseline_segment_dict[seg_name] = create_tree_data(
                self.output_format, segment
            )
        self.sig_load_baseline_segments_data.emit(baseline_segment_dict)

    def update_treeview_proposed(self) -> None:
        """Build the treeView data dict from the Project and pass back to the view."""
        self.logger.debug("Updating treeView proposed data.")

        proposed_segment_dict = {}
        for segment in self.NBDM_project.variants.proposed.building_segments:
            seg_name = f"BUILDING SEGMENT: {segment.segment_name}"
            proposed_segment_dict[seg_name] = create_tree_data(
                self.output_format, segment
            )
        self.sig_load_proposed_segments_data.emit(proposed_segment_dict)

    def update_treeview_bldg_components(self) -> None:
        """Build the treeView data dict from the Project, and pass the dict back to the view."""
        self.logger.debug("Updating treeView building-component data.")

        self.logger.debug("- " * 25)
        self.logger.debug("Updating treeView baseline data.")
        self.logger.debug("- " * 25)

        # -- In this case, we want to iterate over all the assemblies and display each one
        tree_bldg_component_data = {"ASSEMBLIES": {}}
        for assembly in self.NBDM_project.envelope.assemblies.values():
            tree_bldg_component_data["ASSEMBLIES"][assembly.name] = create_tree_data(
                self.output_format, assembly
            )

        tree_bldg_component_data.update(
            create_tree_data(self.output_format, self.NBDM_project.appliances)
        )

        # -- Pass the dict back to the treeView
        self.sig_load_bldg_components_data.emit(tree_bldg_component_data)

    # -------------------------------------------------------------------------
    # -- Menu Commands

    def update_cc_software(self, _application_path: pathlib.Path) -> None:
        """Update the CarbonCheck software."""
        self.logger.info("Updating CarbonCheck software.")
        # TODO:
        # -- Figure out the OS version being used

        # -- Download the new CarbonCheck package

        # -- Unzip the package to the application path

        # -- will that work? Can I replace the exe while its running?

        print("_application_path=", _application_path)

    def load_cc_project_from_file(self, _filepath: pathlib.Path) -> None:
        """Build up an NBDM_Project from a save file and set as the active."""
        self.logger.info(f"Loading CarbonCheck data from file: {_filepath}")

        data = self.load_json_file_as_dict(_filepath)
        self.NBDM_project = project.NBDM_Project.from_dict(data)

        self.update_treeview_team()
        self.update_treeview_baseline()
        self.update_treeview_proposed()
        self.logger.info("Successfully loaded data from file.")

    def load_json_file_as_dict(self, _filepath: pathlib.Path) -> Dict:
        """Read in a dict from a JSON file."""
        self.logger.info(f"Reading in JSON file: {_filepath}")

        try:
            if not os.path.exists(_filepath):
                self.logger.info(f"Warning: No file named: {_filepath} found?")
                return {}

            with open(_filepath, "r") as read_file:
                return json.load(read_file)

        except Exception as e:
            self.logger.error(f"Error trying to read in JSON file: {_filepath}")
            self.logger.error(e, exc_info=True)
            return {}

    def write_json_file(self, _filepath: pathlib.Path) -> None:
        self.logger.info(f"Writing out JSON file: {_filepath}")
        self.set_project_from_gui()
        NBDM_Project_to_json_file(self.NBDM_project, _filepath)

    def set_project_from_gui(self) -> None:
        """Read in all the data in the GUI fields and build a new NBDM project."""
        print("- " * 50)
        self.logger.info("Updating all Project data.")
        self.sig_read_treeView_team.emit()
        self.sig_read_treeView_site.emit()
        self.sig_read_treeView_proposed_segments.emit()
        self.sig_read_treeView_baseline_segments.emit()
        self.sig_read_treeView_envelope.emit()
        self.sig_read_treeView_appliances.emit()

    # -------------------------------------------------------------------------
    # Slots

    @qtc.pyqtSlot(dict)
    def set_project_team_from_treeView_data(self, _data: Dict[str, str]) -> None:
        """Set the self.NBDM_project.team from the data in the treeView"""
        self.logger.info("Updating the Project Team data.")

        if not _data:
            self.logger.error("No data passed to set_project_team_from_treeView_data()")
            return

        self.NBDM_project.team = NBDM_Object_from_treeView(
            self.output_format, _data, team.NBDM_Team
        )

    @qtc.pyqtSlot(dict)
    def set_project_site_from_treeView_data(self, _data: Dict[str, str]) -> None:
        """Set the self.NBDM_project.site from the data in the treeView"""
        self.logger.info("Updating the Project Site data.")
        if not _data:
            self.logger.error("No data passed to set_project_site_from_treeView_data()")
            return

        self.NBDM_project.site = NBDM_Object_from_treeView(
            self.output_format, _data, site.NBDM_Site
        )

    @qtc.pyqtSlot(dict)
    def set_project_proposed_segments_from_treeView_data(
        self, _data: Dict[str, Any]
    ) -> None:
        """Set the self.NBDM_project.variants.proposed from the data in the treeView"""
        self.logger.info("Updating the Project Proposed Segments data.")
        if not _data:
            self.logger.error(
                "No data passed to set_project_proposed_segments_from_treeView_data()"
            )
            return

        self.NBDM_project.variants.proposed.clear_variant_building_segments()
        for segment_data in _data.values():
            new_segment = NBDM_Object_from_treeView(
                self.output_format, segment_data, building.NBDM_BuildingSegment
            )
            self.NBDM_project.add_new_proposed_segment(new_segment)

    @qtc.pyqtSlot(dict)
    def set_project_baseline_segments_from_treeView_data(
        self, _data: Dict[str, Any]
    ) -> None:
        """Set the self.NBDM_project.variants.baseline from the data in the treeView"""
        self.logger.info("Updating the Project Baseline Segments data.")
        if not _data:
            self.logger.error(
                "No data passed to set_project_baseline_segments_from_treeView_data()"
            )
            return

        self.NBDM_project.variants.baseline.clear_variant_building_segments()
        for segment_data in _data.values():
            new_segment = NBDM_Object_from_treeView(
                self.output_format, segment_data, building.NBDM_BuildingSegment
            )
            self.NBDM_project.add_new_baseline_segment(new_segment)

    @qtc.pyqtSlot(dict)
    def set_project_envelope_from_treeView_data(
        self, _data: Dict[str, Dict[str, Any]]
    ) -> None:
        """Set the self.NBDM_project.envelope from the data in the treeView"""
        self.logger.info("Updating the Project Envelope data.")
        if not _data:
            self.logger.error(
                "No data passed to set_project_envelope_from_treeView_data()"
            )
            return

        self.NBDM_project.envelope.clear_envelope_assemblies()
        for assembly_data in _data.get("ASSEMBLIES", {}).values():
            self.NBDM_project.envelope.add_envelope_assembly(
                NBDM_Object_from_treeView(
                    self.output_format, assembly_data, envelope.NBDM_EnvelopeAssembly
                )
            )

    @qtc.pyqtSlot(dict)
    def set_project_appliances_from_treeView_data(self, _data: Dict[str, str]) -> None:
        """Set the self.NBDM_project.appliances from the data in the treeView"""
        self.logger.info("Updating the Project Appliance data.")
        if not _data:
            self.logger.error(
                "No data passed to set_project_appliances_from_treeView_data()"
            )
            return

        self.NBDM_project.appliances = NBDM_Object_from_treeView(
            self.output_format, _data, appliances.NBDM_BuildingSegmentAppliances()
        )

    # -------------------------------------------------------------------------

    def remove_baseline_segment_by_name(self, _segment_name: str):
        """Remove a baseline building-segment from the project."""
        self.logger.debug(f"Removing baseline segment: {_segment_name}")
        self.NBDM_project.variants.baseline.remove_segment_by_name(_segment_name)
        self.update_treeview_baseline()

    def remove_proposed_segment_by_name(self, _segment_name: str):
        """Remove a proposed building-segment from the project."""
        self.logger.debug(f"Removing proposed segment: {_segment_name}")
        self.NBDM_project.variants.proposed.remove_segment_by_name(_segment_name)
        self.update_treeview_proposed()

    def load_baseline_code_file(
        self, _baseline_code_option: BaselineCodes
    ) -> Optional[BaselineCode]:
        """Load the baseline code file from the specified path. Return None if not found.

        Arguments:
        ---------
            baseline_code: BaselineCodes
                The Enum of the baseline code name to load.
        """

        baseline_code_file_name = f"{_baseline_code_option.name}.json"
        self.logger.debug(f"Loading baseline code file: {baseline_code_file_name}")

        # -- The file might be in a few different places on the system path.
        for p in sys.path:
            baseline_code_file_path = pathlib.Path(
                p, "ph_baseliner", "codes", baseline_code_file_name
            )
            self.logger.debug(
                f"Checking for baseline code file: {baseline_code_file_path}"
            )
            if baseline_code_file_path.exists():
                self.logger.info(
                    f"Loading the Baseline Code file: '{baseline_code_file_path}'"
                )
                break
        else:
            self.logger.info(
                f"Error: Baseline code file '{baseline_code_file_name}' not found on system path?"
            )
            return None

        # -- Load in the Baseline Code file as a model.
        baseline_code_model = BaselineCode.parse_file(baseline_code_file_path)
        return baseline_code_model

    def get_allowable_code_names(self) -> List[str]:
        """Return a list of allowable code names."""
        return BaselineCodes.as_list()

    def get_allowable_climate_zone_names(self) -> List[str]:
        """Return a list of allowable climate zone names."""
        return ClimateZones.as_list()

    def get_allowable_use_type_names(self) -> List[str]:
        """Return a list of allowable use type names."""
        return Use_Groups.as_list()

    def get_allowable_pf_group_names(self) -> List[str]:
        """Return a list of allowable use Projection-Factor Group names."""
        return PF_Groups.as_list()
