# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Main Application View Class."""

import logging
from enum import Enum
import pathlib
from typing import List, Dict, Any, Optional, Tuple, Callable

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

# -- Layout from QtDesigner
from CC_GUI.views.ui_files.layout_app import Ui_MainWindow


def get_treeView_model_as_dict(
        _model: qtg.QStandardItemModel, 
        _index_item: Optional[qtc.QModelIndex]=None, 
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


class file_type(Enum):
    NONE = ""
    JSON = "JSON (*.json)"
    XL = "Excel (*.xlsx *.xls *.xlsm)"


class CCMainWindow(qtw.QMainWindow):
    """Main Application View."""

    got_team_data = qtc.pyqtSignal(dict)
    got_site_data = qtc.pyqtSignal(dict)
    got_proposed_building_data = qtc.pyqtSignal(dict) 
    got_baseline_building_data = qtc.pyqtSignal(dict) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

        # -- UI Layout from QtDesigner
        self.logger.debug("Loading UI Layout from QtDesigner.")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    @property
    def buttons(self) -> List[qtw.QPushButton]:
        """Return a list of all buttons in the UI."""
        return self.findChildren(qtw.QPushButton) # type: ignore

    @property
    def actions(self) -> List[qtg.QAction]:
        """Return a list of all Actions in the UI."""
        return self.findChildren(qtg.QAction) # type: ignore

    def get_file_path(self, filter: file_type = file_type.XL) -> Optional[pathlib.Path]:
        """Return a user-selected file path from a Dialog window."""

        file_name, selected_filter = qtw.QFileDialog.getOpenFileName(
            self, "Select a file...", filter=filter.value
        )

        if file_name != "":  # "" returned on 'Cancel'
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

    # -------------------------------------------------------------------------
    # treeView Getters

    @qtc.pyqtSlot()
    def get_treeView_data_team(self):
        """Return the 'Team' treeView data as a dict."""
        self.logger.info("Getting Project Team data from the GUI.")
        _treeview_model = getattr(self.ui, "tree_view_model_team_info", None)
        data = get_treeView_model_as_dict(_treeview_model) if _treeview_model else {}
        self.got_team_data.emit(data)

    @qtc.pyqtSlot()
    def get_treeView_data_site(self):
        """Return the 'Site' treeView data as a dict."""
        self.logger.info("Getting Project Site data from the GUI.")
        _treeview_model = getattr(self.ui, "tree_view_model_team_info", None)
        data = get_treeView_model_as_dict(_treeview_model) if _treeview_model else {}
        self.got_site_data.emit(data)

    @qtc.pyqtSlot()
    def get_treeView_data_proposed_building(self):
        """Return the Proposed Building treeView data as a dict."""
        self.logger.info("Getting Proposed Building Segment data from the GUI.")
        _treeview_model = getattr(self.ui, "tree_view_model_proposed", None)
        data = get_treeView_model_as_dict(_treeview_model) if _treeview_model else {}
        self.got_proposed_building_data.emit(data)

    @qtc.pyqtSlot()
    def get_treeView_data_baseline_building(self):
        """Return the Baseline Building treeView data as a dict."""
        self.logger.info("Getting Baseline Building Segment data from the GUI.")
        _treeview_model = getattr(self.ui, "tree_view_model_baseline", None)
        data = get_treeView_model_as_dict(_treeview_model) if _treeview_model else {}
        self.got_baseline_building_data.emit(data)

    # -------------------------------------------------------------------------
    # treView Setters
    
    @qtc.pyqtSlot(dict)
    def set_treeView_data_team(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Team Information."""
        model, tree_view =  build_treeView(_data, self.ui.tree_view_team_info)
        
        # -- I don't know why the normal .model() always returns 'None'? So 
        # -- for now I guess lets just store this someplace we can be sure that
        # -- we can access it easily enough.
        setattr(self.ui, "tree_view_model_team_info", model)
        return tree_view

    @qtc.pyqtSlot(dict)
    def set_treeView_data_proposed(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Proposed Segment Data."""
        model, tree_view =  build_treeView(_data, self.ui.tree_view_proposed)
        
        # -- I don't know why the normal .model() always returns 'None'? So 
        # -- for now I guess lets just store this someplace we can be sure that
        # -- we can access it easily enough.
        setattr(self.ui, "tree_view_model_proposed", model)
        return tree_view

    @qtc.pyqtSlot(dict)
    def set_treeView_data_baseline(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Baseline Segment Data"""
        model, tree_view = build_treeView(_data, self.ui.tree_view_baseline)
        
        # -- I don't know why the normal .model() always returns 'None'? So 
        # -- for now I guess lets just store this someplace we can be sure that
        # -- we can access it easily enough.
        setattr(self.ui, "tree_view_model_baseline", model)
        return tree_view
    