# -*- Python Version: 3.10 -*-

"""Main Application. Run to see GUI."""


import sys
from typing import List, Dict, get_type_hints, Any, Optional
import enum
import json
import os
import pathlib

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from NBDM.model import project
from views import view_main_window


def is_dict_field(_type: type) -> bool:
    if getattr(_type, "__origin__", None) == dict:
        return True
    return False


def is_dataclass_type(_type: type) -> bool:
    if not hasattr(_type, "__dataclass_fields__"):
        return False
    return True


def is_NBDM_class(_type: type) -> bool:
    if not is_dataclass_type(_type):
        return False
    if "NBDM" not in _type.__name__.upper():
        return False
    return True


def is_enum(_type: type) -> bool:
    return issubclass(_type, enum.Enum)


class CCModel(qtw.QWidget):
    """CarbonCheck Model Class."""

    team_data_loaded = qtc.pyqtSignal(dict)
    site_data_loaded = qtc.pyqtSignal(dict)
    baseline_segments_data_loaded = qtc.pyqtSignal(dict)
    proposed_segments_data_loaded = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_tree_data(self, _obj) -> Dict[str, Any]:
        """Recursively build up a dict of string values for the Project Data TreeView."""
        # Note: cannot use dataclasses.fields() 'cus __future__ annotations
        # breaks it and all .type comes as str.
        d = {}
        for field_name, field_type in get_type_hints(_obj.__class__).items():

            # -- Exclude the Variants from the Project data view.
            if field_name == "variants":
                continue

            if is_dict_field(field_type):
                continue
            elif is_NBDM_class(field_type):
                d[field_name] = self.create_tree_data(getattr(_obj, field_name))
            elif is_enum(field_type):
                d[field_name] = getattr(_obj, field_name).value
            else:
                d[field_name] = getattr(_obj, field_name)
        return d

    def load_cc_project_from_file(self, _file_path: pathlib.Path):

        # -- Setup the treeView
        data = self.load_json_file_as_dict(_file_path)
        new_project = project.NBDM_Project.from_dict(data)

        tree_data_team = self.create_tree_data(new_project.team)
        self.team_data_loaded.emit(tree_data_team)

        tree_data_site = self.create_tree_data(new_project.site)
        self.site_data_loaded.emit(tree_data_site)

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


class CCApp(qtw.QApplication):
    """CarbonCheck Application Controller."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- Create the View
        self.view = view_main_window.CCMainWindow()

        # -- Create the Model
        self.model = CCModel()

        # -- Connect View and Model
        self.connect_signals()

    def connect_signals(self) -> None:
        """Hook up all the signals and slots."""
        # .connect( SLOT )
        self.view.ui.actionOpen.triggered.connect(self.on_click_menu_file_open)
        self.model.team_data_loaded.connect(self.view.set_team_tree_view)
        self.model.site_data_loaded.connect(self.view.set_site_tree_view)
        self.model.proposed_segments_data_loaded.connect(self.view.set_proposed_tree_view)
        self.model.baseline_segments_data_loaded.connect(self.view.set_baseline_tree_view)
        return None

    def load_cc_project_from_file(self, file_path: Optional[pathlib.Path]) -> None:
        """Load an existing CC Project from a JSON file."""
        if file_path:
            self.model.load_cc_project_from_file(file_path)
        return None

    def on_click_menu_file_open(self) -> None:
        """Get a CC Project file path and open it. Execute on Menu / File / Open..."""
        file_path = self.view.get_file_path(filter="json")
        self.load_cc_project_from_file(file_path)
        return None


if __name__ == "__main__":
    app = CCApp(sys.argv)
    app.view.show()
    sys.exit(app.exec())
