# -*- Python Version: 3.10 -*-

"""Main Application."""

import pathlib
from types import ModuleType

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
        self.view.ui.actionOpen.triggered.connect(self.menu_file_open)
        self.view.ui.actionSave.triggered.connect(self.menu_file_save)
        self.view.ui.actionSave_As.triggered.connect(self.menu_file_save_as)

        self.view.ui.btn_add_team_info.clicked.connect(self.add_project_info_from_file)
        self.view.ui.btn_add_baseline_seg.clicked.connect(self.add_baseline_seg_from_file)
        self.view.ui.btn_add_proposed_seg.clicked.connect(self.add_proposed_seg_from_file)
        self.view.ui.btn_create_report.clicked.connect(self.write_report_to_file)

        self.model.load_team_data.connect(self.view.set_treeView_data_team)
        self.model.load_baseline_segments_data.connect(self.view.set_treeView_data_baseline)
        self.model.load_proposed_segments_data.connect(self.view.set_treeView_data_proposed)

        self.model.read_treeView_team.connect(self.view.get_treeView_data_team)
        self.model.read_treeView_site.connect(self.view.get_treeView_data_site)
        self.model.read_treeView_baseline_segments.connect(self.view.get_treeView_data_baseline_building)
        self.model.read_treeView_proposed_segments.connect(self.view.get_treeView_data_proposed_building)
        
        self.view.got_team_data.connect(self.model.set_project_team_from_treeView_data)
        self.view.got_site_data.connect(self.model.set_project_site_from_treeView_data)
        self.view.got_baseline_building_data.connect(self.model.set_project_baseline_segments_from_treeView_data)
        self.view.got_proposed_building_data.connect(self.model.set_project_proposed_segments_from_treeView_data)

        return None

    def menu_file_open(self) -> None:
        """Get a CC Project file path and open it. Execute on Menu / File / Open..."""
        filepath = self.view.get_file_path(filter=view_main_window.file_type.JSON)
        if not filepath:
            return None
        self.model.load_cc_project_from_file(filepath)

    def menu_file_save(self) -> None:
        filepath = self.view.get_save_file_path()
        if not filepath:
            return
        filepath = pathlib.Path(filepath).resolve()
        self.model.write_json_file(filepath)

    def menu_file_save_as(self) -> None:
        filepath = self.view.get_save_file_path()
        if not filepath:
            return
        filepath = pathlib.Path(filepath).resolve()
        self.model.write_json_file(filepath)

    def add_project_info_from_file(self) -> None:
        """Load 'Project' information from a single PHPP file (Team, Climate, Site...)"""
        filepath = self.view.get_file_path(filter=view_main_window.file_type.XL)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.read_project_data_from_file.emit(self.model.NBDM_project, filepath)

    def add_baseline_seg_from_file(self) -> None:
        """Load a new Baseline Segment's data from a single PHPP file."""
        filepath = self.view.get_file_path(filter=view_main_window.file_type.XL)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.read_baseline_seg_data_from_file.emit(
            self.model.NBDM_project, filepath
        )

    def add_proposed_seg_from_file(self) -> None:
        """Load a new Proposed Segment's data from a single PHPP file."""
        filepath = self.view.get_file_path(filter=view_main_window.file_type.XL)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.read_proposed_seg_data_from_file.emit(
            self.model.NBDM_project, filepath
        )

    def write_report_to_file(self) -> None:
        """Write out the data to a new Excel report"""
        print(">> 1) CCApp.write_report_to_file()")
        self.model.set_project_from_gui()
        # self.model.write_excel_report.emit(self.model.NBDM_project)
