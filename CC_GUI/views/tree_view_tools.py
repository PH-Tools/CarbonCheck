# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions for working with Qt treeView Panels."""

from typing import List, Dict, Any, Optional, Tuple

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc


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
            item_1 = _model.index(row_num, 0, _index_item)
            row_value = _model.data(_model.index(row_num, 1, _index_item))
        else:
            item_1 = _model.index(row_num, 0)
            row_value = _model.data(_model.index(row_num, 1))

        # -- Get the data from the TreeView
        row_title = _model.data(item_1)
        d[row_title] = row_value

        # -- if the row has any children objects, do it again
        if _model.rowCount(item_1) != 0:
            d[row_title] = get_treeView_model_as_dict(_model, item_1)

    return d


def set_treeView_model_data(
    rootNode: qtg.QStandardItem, _data: Dict[str, Any]
) -> qtg.QStandardItem:
    """Recursively populate a QStandardItemModel.rootNode with a Dict of data."""

    for field_name, field_value in _data.items():
        item = qtg.QStandardItem(field_name)
        if isinstance(field_value, Dict):
            rootNode.appendRow(set_treeView_model_data(item, field_value))
        elif isinstance(field_value, List):
            continue
        else:
            rootNode.appendRow([item, qtg.QStandardItem(str(field_value))])

    return rootNode


def build_treeView_model(_data: Dict[str, Any]) -> qtg.QStandardItemModel:
    """Create a new treeModel based on a Dict of data."""
    treeModel = qtg.QStandardItemModel(0, 2)  # rows=0, columns=2
    rootNode = treeModel.invisibleRootItem()
    set_treeView_model_data(rootNode, _data)
    return treeModel


def build_treeView(
    _data: Dict[str, Any], _tree_view: qtw.QTreeView
) -> Tuple[qtg.QStandardItemModel, qtw.QTreeView]:
    """Create a default TreeView with standard view params."""
    _tree_view.setHeaderHidden(True)
    _model = build_treeView_model(_data)
    _tree_view.setModel(_model)
    _tree_view.expandAll()  # Expand before setting column width
    _tree_view.resizeColumnToContents(0)
    _tree_view.setColumnWidth(0, int(round(_tree_view.columnWidth(0) * 1.1, 0)))
    _tree_view.setAlternatingRowColors(True)
    _tree_view.collapseAll()
    return _model, _tree_view
