# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Main Application View Class."""

from enum import Enum
import pathlib
from typing import List, Dict, Any, Optional

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

# -- Layout from QtDesigner
from App.views.ui_files.layout_app import Ui_MainWindow


class file_type(Enum):
    NONE = ""
    JSON = "JSON (*.json)"
    XL = "Excel (*.xlsx *.xls *.xlsm)"


class CCMainWindow(qtw.QMainWindow):
    """Main Application View."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- UI Layout from QtDesigner
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def get_file_path(self, filter: file_type = file_type.XL) -> Optional[pathlib.Path]:
        """Return a user-selected file path from a Dialog window."""

        file_name, selected_filter = qtw.QFileDialog.getOpenFileName(
            self, "Select a file...", filter=filter.value
        )

        if file_name is not "":  # "" returned on 'Cancel'
            return pathlib.Path(file_name).resolve()
        else:
            return None

    def get_save_file_path(self) -> Optional[pathlib.Path]:
        """Return a user-specified file path from a Dialog window."""

        filter: file_type = file_type.JSON
        file_name, selected_filter = qtw.QFileDialog.getSaveFileName(
            self,
            caption="Save CarbonCheck Project...",
            initialFilter=filter.value,
            filter=filter.value,
        )
        if file_name:
            return pathlib.Path(file_name).resolve()
        else:
            return None

    def _set_default_tree_view(
        self, _data: Dict[str, Any], _tree_view: qtw.QTreeView
    ) -> qtw.QTreeView:
        """Create a default TreeView with standard view params."""
        _tree_view.setHeaderHidden(True)
        _tree_view.setModel(self.build_tree_model(_data))

        _tree_view.expandAll()  # Expand before setting column width
        _tree_view.resizeColumnToContents(0)
        _tree_view.setColumnWidth(0, int(round(_tree_view.columnWidth(0) * 1.1, 0)))
        _tree_view.collapseAll()

        _tree_view.setAlternatingRowColors(True)

        return _tree_view

    @qtc.pyqtSlot(dict)
    def set_team_tree_view(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Team Information."""
        return self._set_default_tree_view(_data, self.ui.tree_view_team_info)

    @qtc.pyqtSlot(dict)
    def set_proposed_tree_view(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Proposed Segment Data."""
        return self._set_default_tree_view(_data, self.ui.tree_view_proposed)

    @qtc.pyqtSlot(dict)
    def set_baseline_tree_view(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Baseline Segment Data"""
        return self._set_default_tree_view(_data, self.ui.tree_view_baseline)

    def populate_tree_model(
        self, rootNode: qtg.QStandardItem, _data: Dict[str, Any]
    ) -> qtg.QStandardItem:
        """Recursively populate a QStandardItemModel.rootNode with a Dict of data."""

        for field_name, field_value in _data.items():
            item = qtg.QStandardItem(field_name)
            if isinstance(field_value, Dict):
                rootNode.appendRow(self.populate_tree_model(item, field_value))
            elif isinstance(field_value, List):
                continue
            else:
                rootNode.appendRow([item, qtg.QStandardItem(str(field_value))])

        return rootNode

    def build_tree_model(self, _data: Dict[str, Any]) -> qtg.QStandardItemModel:
        """Create a new treeModel based on a Dict of data."""
        treeModel = qtg.QStandardItemModel(0, 2)  # rows=0, columns=2
        rootNode = treeModel.invisibleRootItem()
        self.populate_tree_model(rootNode, _data)
        return treeModel
