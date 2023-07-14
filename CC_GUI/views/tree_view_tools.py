# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions for working with Qt treeView Panels."""

import enum
import json
from typing import List, Dict, Any, Optional, Tuple, Union, get_type_hints
from types import ModuleType
from collections import namedtuple
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from ph_units.unit_type import Unit

from NBDM.model.serialization import build_NBDM_obj_from_treeView

treeView_dataItem = namedtuple("treeView_dataItem", ["row_value", "row_unit"])

# -----------------------------------------------------------------------------
# -- TreeView functions for GUI


def find_parent_treeView_index(_index: qtc.QModelIndex) -> qtc.QModelIndex:
    """Given a starting treeView QModelIndex (row), walk up the tree to find the parent QModelIndex (row).

    Arguments:
    ----------
        * _index: (PyQt6.QtCore.QModelIndex) The starting index to find the parent of

    Returns:
    --------
        * (PyQt6.QtCore.QModelIndex) The parent QModelIndex of the starting index
    """
    if not _index.parent().data():
        # -- If the .parent().data() of the index is 'None', this index is the top node
        return _index
    else:
        # -- If not, climb up one level and try again
        return find_parent_treeView_index(_index.parent())


def get_treeView_model_as_dict(
    _model: qtg.QStandardItemModel,
    _index_item: Optional[qtc.QModelIndex] = None,
) -> Dict:
    """Recursively walk through a TreeView Model building up a dict of the row data.

    Arguments:
    ----------
        * _model: (qtg.QStandardItemModel) The TreeView to turn into a Dict
        * _index_item: (Optional[PyQt6.QtCore.QModelIndex]) Default=None

    Returns:
    --------
        * (Dict[str, Any])
    """
    d = {}

    row_count = _model.rowCount(_index_item) if _index_item else _model.rowCount()

    for row_num in range(row_count):
        if _index_item:
            # -- A child item with data
            item_1 = _model.index(row_num, 0, _index_item)
            row_value = _model.data(_model.index(row_num, 1, _index_item))
            row_unit = _model.data(_model.index(row_num, 2, _index_item))
        else:
            # -- A heading item with children
            item_1 = _model.index(row_num, 0)
            row_value = _model.data(_model.index(row_num, 1))
            row_unit = _model.data(_model.index(row_num, 2))

        # -- Get the data from the TreeView
        row_title = _model.data(item_1)
        d[row_title] = treeView_dataItem(row_value, row_unit)

        # -- if the row has any children objects, do it again
        if _model.rowCount(item_1) != 0:
            d[row_title] = get_treeView_model_as_dict(_model, item_1)

    return d


def formatted_value(value: float) -> str:
    """Format a value for display in the treeView."""
    if -0.00001 <= value <= 0.00001:
        return "0"
    if -1.0 <= value <= 1.0:
        return f"{value :.3f}"
    else:
        return f"{value :,.1f}"


def set_treeView_model_data(
    rootNode: qtg.QStandardItem, _data: Dict[str, Union[Dict, List, str, float, Unit]]
) -> qtg.QStandardItem:
    """Recursively populate a QStandardItemModel.rootNode with a Dict of arbitrary data."""

    for data_item_name, data_item_value in _data.items():
        q_tree_item = qtg.QStandardItem(data_item_name)

        if isinstance(data_item_value, Dict):
            # -- If there is more child data, call this function again
            # -- Pad with two empty columns for the value and unit
            rootNode.appendRow(
                [
                    set_treeView_model_data(q_tree_item, data_item_value),
                    qtg.QStandardItem(),
                    qtg.QStandardItem(),
                ]
            )

        elif isinstance(data_item_value, List):
            continue

        else:
            # -- Otherwise, add the actual data to the TreeView
            if isinstance(data_item_value, Unit):
                val = formatted_value(data_item_value.value)
                unit = str(data_item_value.unit)
            else:
                val = str(data_item_value)
                unit = "-"

            rootNode.appendRow(
                [q_tree_item, qtg.QStandardItem(val), qtg.QStandardItem(unit)]
            )

    return rootNode


def build_treeView_model(_data: Dict[str, Any]) -> qtg.QStandardItemModel:
    """Create a new treeModel based on a Dict of data."""
    treeModel = qtg.QStandardItemModel(0, 3)  # rows=0, columns=2
    rootNode = treeModel.invisibleRootItem()
    set_treeView_model_data(rootNode, _data)
    return treeModel


class RightAlignedDelegate(qtw.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.column() == 1:
            option.displayAlignment = (
                qtc.Qt.AlignmentFlag.AlignRight | qtc.Qt.AlignmentFlag.AlignVCenter
            )


def build_treeView(
    _data: Dict[str, Any], _tree_view: qtw.QTreeView
) -> Tuple[qtg.QStandardItemModel, qtw.QTreeView]:
    """Create a default TreeView with standard view params."""

    # -- Build the treeView model data from the Dict
    _model = build_treeView_model(_data)

    # -- Configure the treeView's header
    _model.setHeaderData(0, qtc.Qt.Orientation.Horizontal, "Item")
    _model.setHeaderData(1, qtc.Qt.Orientation.Horizontal, "Value")
    _model.setHeaderData(2, qtc.Qt.Orientation.Horizontal, "Unit")
    _tree_view.setModel(_model)
    _tree_view.setHeaderHidden(False)
    _tree_view.header().setStretchLastSection(True)

    # Set a delegate for the second column to right-align the text
    delegate = RightAlignedDelegate()
    _tree_view.setItemDelegateForColumn(1, delegate)

    # -- Configure the treeView's rows
    _tree_view.expandAll()  # Expand before setting column width
    _tree_view.resizeColumnToContents(0)
    _tree_view.setColumnWidth(0, int(round(_tree_view.columnWidth(0) * 1.1, 0)))
    _tree_view.setAlternatingRowColors(True)
    _tree_view.collapseAll()

    return _model, _tree_view


# -----------------------------------------------------------------------------
# --- Building TreeView from NBDM Objects ---


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


def get_formatted_field_name(
    _output_format: ModuleType, _obj: Any, _field_name: str
) -> Optional[str]:
    """Return an NBDM Object field_name in a user-facing format (nice)."""
    format_class = getattr(_output_format, f"Format_{_obj.__class__.__name__}")
    return getattr(format_class, _field_name, None)


def replace_key_names(
    _data: Dict[str, Any], _output_format: ModuleType, _obj: Any
) -> Dict[str, Dict[str, str]]:
    """Replace the user-facing keys in a treeView dict with the actual field names.

    Arguments:
    ----------
        * _data: (Dict[str, Dict[str, str]]) The dict to replace the keys in.
        * _output_format: (ModuleType) The module containing the user-facing names.
        * _obj: (Any) The NBDM Object to get the field names from.

    Returns:
    --------
        * (Dict[str, Dict[str, str]]) The dict with the user-facing keys replaced with the actual field names.
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


def create_tree_data(_output_format, _obj: Any) -> Dict[str, Any]:
    """Recursively build up a dict of string values for the Project Data TreeView."""
    # Note: cannot use dataclasses.fields() 'cus __future__ annotations
    # breaks it and all .type comes as str.

    # with open(f"{_obj.__class__.__name__}.txt", "w") as f:
    #     f.write(str(_obj))
    #     f.write("\n")
    #     f.write(
    #         f"get_type_hints(_obj.__class__).keys()={str(get_type_hints(_obj.__class__).keys())}"
    #     )
    #     f.write("\n")

    d = {}
    for field_name, field_type in get_type_hints(_obj.__class__).items():
        # f.write(f"    {field_name}=type: {field_type}\n")
        # -- Exclude the Variants and Envelope from the Project data view.
        if field_name in ["variants", "envelope"]:
            # f.write(f"        '{field_name}' excluded. skipping....\n")
            continue

        # -- Exclude whatever this is
        if is_dict_field(field_type):
            # f.write(f"        '{field_name}' is dict field. skipping....\n")
            continue

        # -- Figure out the right view-name to use
        field_view_name = get_formatted_field_name(_output_format, _obj, field_name)
        # f.write(f"        '{field_name}' field_view_name: {field_view_name}\n")
        if not field_view_name:
            continue

        if is_NBDM_class(field_type):
            # f.write(f"        '{field_type}' is_NBDM_class. recursing....\n")
            d[field_view_name] = create_tree_data(
                _output_format, getattr(_obj, field_name)
            )
        elif is_enum(field_type):
            # f.write(f"        '{field_type}' is_enum. getting value....\n")
            d[field_view_name] = getattr(_obj, field_name).value
        else:
            # f.write(f"        '{field_type}' is simple type. getting value....\n")
            d[field_view_name] = getattr(_obj, field_name)
    return d


# -----------------------------------------------------------------------------
# -- Building NBDM Objects from TreeView ---


def NBDM_Object_from_treeView(
    _output_format: ModuleType, _data: Dict[str, Any], _obj: Any
) -> Any:
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
    new_NBDM_obj = build_NBDM_obj_from_treeView(
        _obj, replace_key_names(_data, _output_format, _obj)
    )
    return new_NBDM_obj
