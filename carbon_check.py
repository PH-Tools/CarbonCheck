# -*- Python Version: 3.10 -*-

"""Main Application. Run to see GUI."""


import sys
from typing import List, Dict, get_type_hints
import enum

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_tree_data(self, _obj) -> Dict:
        """Recursively build up a dict of string values for the Project Data TreeView."""
        # Note: cannot use dataclasses.fields() 'cus __future__ annotations
        # breaks it and all .type comes as str.
        d = {}
        for field_name, field_type in get_type_hints(_obj.__class__).items():

            # -- Exclude the Variants from the Project data view.
            if field_name == "variants":
                continue

            if is_dict_field(field_type):
                print("is dict")
            elif is_NBDM_class(field_type):
                print("is NBDM")
                d[field_name] = self.create_tree_data(getattr(_obj, field_name))
            elif is_enum(field_type):
                d[field_name] = getattr(_obj, field_name).value
            else:
                d[field_name] = getattr(_obj, field_name)
        return d


class CCApp(qtw.QApplication):
    """CarbonCheck Application Controller."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- Create the View
        self.view = view_main_window.CCMainWindow()

        # -- Create the Model
        self.model = CCModel()

        # -- Setup the treeView
        new_project = project.NBDM_Project.default()
        tree_data = self.model.create_tree_data(new_project)
        self.view.set_tree_view(tree_data)


if __name__ == "__main__":
    app = CCApp(sys.argv)
    app.view.show()
    sys.exit(app.exec())
