# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Baseline Options Window View Class."""

import logging
from typing import List

from PyQt6 import QtCore as qtc
from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw

# -- Layout from QtDesigner
from CC_GUI.views.ui_files.layout_baseline_options import Ui_Form


class Window_BaselineOptions(qtw.QWidget):
    """Baseline Options Window View."""

    options_data = qtc.pyqtSignal(dict)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

        # -- UI Layout from QtDesigner
        self.logger.debug("Loading UI Layout from QtDesigner.")
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
        self.close()

    def get_baseline_option_values(self) -> None:
        d = {
            "set_envelope_u_values": self.ui.checkBox_baseliner_setEnvelopeUValues.isChecked(),
            "set_window_u_values": self.ui.checkBox_baseliner_setWindowUValues.isChecked(),
            "set_win_areas": self.ui.checkBox_baseliner_setWindowAreas.isChecked(),
            "set_skylight_areas": self.ui.checkBox_baseliner_setSkylightAreas.isChecked(),
            "set_lighting": self.ui.checkBox_baseliner_setSpaceLightingLPD.isChecked(),
        }
        self.logger.debug(f"Baseline Options: {d}")
        self.options_data.emit(d)
        self.close_window()
