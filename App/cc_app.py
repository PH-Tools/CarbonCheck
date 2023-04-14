# -*- Python Version: 3.10 -*-

"""Main Application."""

from typing import Optional
from types import ModuleType
import pathlib

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from App.views import view_main_window
from App.cc_model import CCModel


class CCApp(qtw.QApplication):
    """CarbonCheck Application Controller."""

    def __init__(self, _output_format: ModuleType, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- Create the View
        self.view = view_main_window.CCMainWindow()

        # -- Create the Model
        self.model = CCModel(_output_format)

        # -- Connect View and Model
        self.connect_signals()

    def connect_signals(self) -> None:
        """Hook up all the signals and slots."""
        # .connect( SLOT )
        self.view.ui.actionOpen.triggered.connect(self.on_click_menu_file_open)
        self.model.team_data_loaded.connect(self.view.set_team_tree_view)
        self.model.proposed_segments_data_loaded.connect(self.view.set_proposed_tree_view)
        self.model.baseline_segments_data_loaded.connect(self.view.set_baseline_tree_view)
        return None

    def load_cc_project_from_file(self, file_path: Optional[pathlib.Path]) -> None:
        """Load an existing CC Project from a JSON file."""
        if file_path:
            self.model.load_cc_project_from_file(file_path)
        return None

    def on_click_menu_file_open(self) -> None:
        """Get a CC Project file path and open it. Execute on Menu / File / Open..."""
        file_path = self.view.get_file_path(filter="json")
        self.load_cc_project_from_file(file_path)
        return None
