# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions for working with Qt treeView Panels."""

from typing import List, Dict, Any, Optional, Tuple, Union
from collections import namedtuple
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from ph_units.unit_type import Unit


treeView_dataItem = namedtuple("treeView_dataItem", ["row_value", "row_unit"])


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


def set_treeView_model_data(
    rootNode: qtg.QStandardItem, _data: Dict[str, Union[Dict, List, str, float, Unit]]
) -> qtg.QStandardItem:
    """Recursively populate a QStandardItemModel.rootNode with a Dict of arbitary data."""

    for data_item_name, data_item_value in _data.items():
        q_tree_item = qtg.QStandardItem(data_item_name)

        if isinstance(data_item_value, Dict):
            # -- If there is more child data, call this function again
            rootNode.appendRow(set_treeView_model_data(q_tree_item, data_item_value))

        elif isinstance(data_item_value, List):
            continue

        else:
            # -- Otherwise, add the actual data to the TreeView
            if isinstance(data_item_value, Unit):
                val = str(data_item_value.value)
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

    # -- Configure the treeView's rows
    _tree_view.expandAll()  # Expand before setting column width
    _tree_view.resizeColumnToContents(0)
    _tree_view.setColumnWidth(0, int(round(_tree_view.columnWidth(0) * 1.1, 0)))
    _tree_view.setAlternatingRowColors(True)
    _tree_view.collapseAll()

    return _model, _tree_view
