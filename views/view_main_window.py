# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Main Application View Class."""

from typing import List, Dict, Any

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from views.ui_files.layout_app import Ui_MainWindow  # -- From QtDesigner


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

    data = {
        "key_1": "val_1",
        "key_2": "val_2",
        "obj_1": {"obj_arr_1": "obj_val_1", "obj_arr_2": "obj_val2"},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- UI Layout from QtDesigner
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def populate_tree_model(
        self, rootNode: qtg.QStandardItem, _data: Dict[str, Any]
    ) -> qtg.QStandardItem:
        """Recursively populate a QStandardItem Tree from a Dict of data"""

        for k, v in _data.items():
            item = qtg.QStandardItem(k)
            if isinstance(v, Dict):
                rootNode.appendRow(self.populate_tree_model(item, v))
            elif isinstance(v, List):
                continue
            else:
                rootNode.appendRow([item, qtg.QStandardItem(str(v))])

        return rootNode

    def build_tree_model(self, _data: Dict[str, Any]) -> qtg.QStandardItemModel:
        """Create a new treeModel based on a Dict of data."""
        treeModel = qtg.QStandardItemModel(0, 2)
        rootNode = treeModel.invisibleRootItem()
        self.populate_tree_model(rootNode, _data)

        return treeModel

    def set_tree_view(self, _data: Dict):
        print("/n", _data)
        self.ui.tree_view_project.setHeaderHidden(True)
        self.ui.tree_view_project.setModel(self.build_tree_model(_data))
        self.ui.tree_view_project.expandAll()
        self.ui.tree_view_project.resizeColumnToContents(0)
        self.ui.tree_view_project.setColumnWidth(
            0, int(round(self.ui.tree_view_project.columnWidth(0) * 1.1, 0))
        )
        self.ui.tree_view_project.collapseAll()
