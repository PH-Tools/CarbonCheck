# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Report Team and Site Data Window View Class."""

import logging
from typing import List, Dict, Any

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from CC_GUI.views.tree_view_tools import (
    get_treeView_model_as_dict,
    build_treeView,
)

# -- Layout from QtDesigner
from CC_GUI.views.ui_files.layout_bldg_components import Ui_Form


class Window_BuildingComponents(qtw.QWidget):
    """Building Components Window View."""

    got_building_component_data = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

        # -- UI Layout from QtDesigner
        self.logger.debug("Loading Bldg-Component UI Layout from QtDesigner.")
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    @property
    def buttons(self) -> List[qtw.QPushButton]:
        """Return a list of all buttons in the UI."""
        return self.findChildren(qtw.QPushButton)  # type: ignore

    @property
    def actions(self) -> List[qtg.QAction]:
        """Return a list of all Actions in the UI."""
        return self.findChildren(qtg.QAction)  # type: ignore

    def close_window(self) -> None:
        """Close the Window."""
        self.logger.debug("Closing Bldg-Component Window.")
        self.close()

    # -------------------------------------------------------------------------
    # treeView Getters

    @qtc.pyqtSlot()
    def get_treeView_data_building_components(self) -> None:
        """Return the 'Envelope' treeView data as a dict."""
        self.logger.info("Getting Project Building Component data from the GUI.")
        _treeview_model = getattr(self.ui, "tree_view_model_compo_info", None)
        data = get_treeView_model_as_dict(_treeview_model) if _treeview_model else {}
        self.got_building_component_data.emit(data)

    # -------------------------------------------------------------------------
    # treView Setters

    @qtc.pyqtSlot(dict)
    def set_treeView_bldg_components(self, _data: Dict[str, Any]) -> qtw.QTreeView:
        """Create the TreeView objects for the Project's Building-Component Information."""
        model, tree_view = build_treeView(_data, self.ui.tree_view_bldg_component_info)

        # -- I don't know why the normal .model() always returns 'None'? So
        # -- for now I guess lets just store this someplace we can be sure that
        # -- we can access it easily enough.
        setattr(self.ui, "tree_view_model_compo_info", model)
        return tree_view
