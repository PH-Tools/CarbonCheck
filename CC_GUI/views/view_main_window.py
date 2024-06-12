# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Main Application View Class."""

import logging
import pathlib
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

from CC_GUI.views.tree_view_tools import build_treeView, get_treeView_model_as_dict

# -- Layout from QtDesigner
from CC_GUI.views.ui_files.layout_app import Ui_MainWindow


class file_type(Enum):
    NONE = ""
    JSON = "JSON (*.json)"
    PH_MODEL = "PHPP or WUFI-XML (*.xlsx *.xml)"
    PH_SOURCE_FILE = "PHPP or WUFI-PDF (*.xlsx *.xls *.xlsm *.pdf)"
    XML = "XML (*.xml)"
    XL = "Excel (*.xlsx *.xls *.xlsm)"
    PDF = "PDF (*.pdf)"


class CCMainWindow(qtw.QMainWindow):
    """Main Application View."""

    sig_got_proposed_building_data = qtc.pyqtSignal(dict)
    sig_got_baseline_building_data = qtc.pyqtSignal(dict)

    def __init__(self, _icon_path: pathlib.Path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

        # -- UI Layout from QtDesigner
        self.logger.debug("Loading UI Layout from QtDesigner.")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # -- Setup the Application Icon
        try:
            self.setWindowIcon(qtg.QIcon(str(_icon_path.resolve())))
        except Exception as e:
            self.logger.error(f"Error setting window icon: {e}")

    @property
    def buttons(self) -> List[qtw.QPushButton]:
        """Return a list of all buttons in the UI."""
        return self.findChildren(qtw.QPushButton)  # type: ignore

    @property
    def actions(self) -> List[qtg.QAction]:
        """Return a list of all Actions in the UI."""
        return self.findChildren(qtg.QAction)  # type: ignore

    def get_file_path(
        self, filter: file_type = file_type.PH_MODEL
    ) -> Optional[pathlib.Path]:
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
    def sig_get_treeView_data_proposed_building(self) -> None:
        """Return the Proposed Building treeView data as a dict."""
        self.logger.info("Getting Proposed Building Segment data from the GUI.")
        _treeview_model = getattr(self.ui, "tree_view_model_proposed", None)
        data = get_treeView_model_as_dict(_treeview_model) if _treeview_model else {}
        self.sig_got_proposed_building_data.emit(data)

    @qtc.pyqtSlot()
    def get_treeView_data_baseline_building(self) -> None:
        """Return the Baseline Building treeView data as a dict."""
        self.logger.info("Getting Baseline Building Segment data from the GUI.")
        _treeview_model = getattr(self.ui, "tree_view_model_baseline", None)
        data = get_treeView_model_as_dict(_treeview_model) if _treeview_model else {}
        self.sig_got_baseline_building_data.emit(data)

    # -------------------------------------------------------------------------
    # treView Setters

    @qtc.pyqtSlot(dict)
    def set_treeView_data_proposed(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Proposed Segment Data."""
        model, tree_view = build_treeView(_data, self.ui.tree_view_proposed)

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
