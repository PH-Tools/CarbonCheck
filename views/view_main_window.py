# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Main Application View Class."""

from typing import List, Dict, Any, Optional
import pathlib

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

# -- Layout from QtDesigner
from views.ui_files.layout_app import Ui_MainWindow


# class StandardItem(qtg.QStandardItem):
#     def __init__(self, txt):
#         super().__init__()

#         # fnt = QFont(<span class="hljs-string">'Open Sans'</span>, font_size)
#         # fnt.setBold(set_bold)

#         # self.setEditable(<span class="hljs-literal">False</span>)
#         # self.setForeground(color)
#         # self.setFont(fnt)
#         self.setText(txt)


class CCMainWindow(qtw.QMainWindow):
    """Main Application View."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- UI Layout from QtDesigner
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def get_file_path(self, filter: str = "xl") -> Optional[pathlib.Path]:
        """Return a user-selected file path from a Dialog window."""

        if filter == "xl":
            filter = "Excel (*.xlsx *.xls *.xlsm)"
        elif filter == "json":
            filter = "JSON (*.json)"
        else:
            filter = ""

        file_name, selected_filter = qtw.QFileDialog.getOpenFileName(
            self, "Select a file...", filter=filter
        )

        if file_name is not "":  # "" returned on 'Cancel'
            return pathlib.Path(file_name)
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
    def set_site_tree_view(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Site Information."""
        return self._set_default_tree_view(_data, self.ui.tree_view_site_info)

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
