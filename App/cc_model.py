# -*- Python Version: 3.10 -*-

"""Main Application Model."""

from typing import Dict, get_type_hints, Any, Optional
from types import ModuleType
import enum
import json
import os
import pathlib

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from NBDM.model import project


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


class CCModel(qtw.QWidget):
    """CarbonCheck Model Class."""

    team_data_loaded = qtc.pyqtSignal(dict)
    site_data_loaded = qtc.pyqtSignal(dict)
    baseline_segments_data_loaded = qtc.pyqtSignal(dict)
    proposed_segments_data_loaded = qtc.pyqtSignal(dict)

    def __init__(self, _output_format: ModuleType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_format = _output_format

    def _get_formatted_field_name(self, _obj: Any, _field_name: str) -> Optional[str]:
        """Return a field_name in a user-facing format (nice)."""
        format_class = getattr(self.output_format, f"Format_{_obj.__class__.__name__}")
        return getattr(format_class, _field_name, None)

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
            field_view_name = self._get_formatted_field_name(_obj, field_name)
            if not field_view_name:
                continue

            if is_NBDM_class(field_type):
                d[field_view_name] = self.create_tree_data(getattr(_obj, field_name))
            elif is_enum(field_type):
                d[field_view_name] = getattr(_obj, field_name).value
            else:
                d[field_view_name] = getattr(_obj, field_name)
        return d

    def load_cc_project_from_file(self, _file_path: pathlib.Path):

        # -- Load the Project Data
        data = self.load_json_file_as_dict(_file_path)
        new_project = project.NBDM_Project.from_dict(data)

        # -- Setup the treeView sections
        # -- Project Data treeView
        tree_project_data = {}
        tree_project_data.update(self.create_tree_data(new_project.team))
        tree_project_data.update(self.create_tree_data(new_project.site))
        self.team_data_loaded.emit(tree_project_data)

        # -- Project BldgSegment Data treeView
        baseline_segment_dict = {}
        for segment in new_project.variants.baseline.building_segments:
            seg_name = f"BUILDING SEGMENT: {segment.segment_name}"
            baseline_segment_dict[seg_name] = self.create_tree_data(segment)
        self.baseline_segments_data_loaded.emit(baseline_segment_dict)

        proposed_segment_dict = {}
        for segment in new_project.variants.baseline.building_segments:
            seg_name = f"BUILDING SEGMENT: {segment.segment_name}"
            proposed_segment_dict[seg_name] = self.create_tree_data(segment)
        self.proposed_segments_data_loaded.emit(proposed_segment_dict)

    def load_json_file_as_dict(self, filepath: pathlib.Path) -> Dict:
        """Read in a dict from a JSON file."""
        try:
            if not os.path.exists(filepath):
                print(f"Warning: No file named: {filepath}")
                return {}

            with open(filepath, "r") as read_file:
                return json.load(read_file)
        except Exception as ex:
            print(f"Error trying to read in JSON file: {filepath}")
            print(ex)
            return {}

    def output_dict_to_JSON_file(
        self, filepath: pathlib.Path, config_data: Dict[str, Any]
    ) -> None:
        """Write out a dict to a JSON file."""
        try:
            with open(filepath, "w") as write_file:
                json.dump(config_data, write_file, indent=2)
                return
        except Exception as ex:
            print(f"Error trying to write out to JSON file: {filepath}")
            print(ex)
            return
