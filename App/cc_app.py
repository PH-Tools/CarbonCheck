# -*- Python Version: 3.11 -*-

"""Main Application."""

import pathlib
from queue import Queue
import sys
from types import ModuleType
from typing import Dict

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from App.views.view_main_window import CCMainWindow, file_type
from App.cc_model import CCModel
from App.cc_workers import WorkerReceiveText, WriteStream

from ph_baseliner.codes.options import BaselineCodes, ClimateZones

class CCTabReport:
    """The 'Report' tab of the CarbonCheck application."""

    def __init__(self, _model: CCModel, _view: CCMainWindow):
        self.model = _model
        self.view = _view

    def add_project_info_from_file(self) -> None:
        """Load 'Project' information from a single PHPP file (Team, Climate, Site...)"""
        filepath = self.view.get_file_path(filter=file_type.XL)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.read_project_data_from_file.emit(self.model.NBDM_project, filepath)

    def add_baseline_seg_from_file(self) -> None:
        """Load a new Baseline Segment's data from a single PHPP file."""
        filepath = self.view.get_file_path(filter=file_type.XL)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.read_baseline_seg_data_from_file.emit(
            self.model.NBDM_project, filepath
        )

    def add_proposed_seg_from_file(self) -> None:
        """Load a new Proposed Segment's data from a single PHPP file."""
        filepath = self.view.get_file_path(filter=file_type.XL)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.read_proposed_seg_data_from_file.emit(
            self.model.NBDM_project, filepath
        )

    def write_report_to_file(self) -> None:
        """Write out the data to a new Excel report"""
        self.model.set_project_from_gui()
        self.model.write_excel_report.emit(self.model.NBDM_project)

    def find_parent_treeView_index(self, _index: qtc.QModelIndex) -> qtc.QModelIndex:
        """Given a starting treeView index, walk up the tree to find the parent index."""
        if not _index.parent().data():
            # -- If the .parent().data() of the index is 'None', this index is the top node
            return _index
        else:
            # -- If not, climb up one level and try again
            return self.find_parent_treeView_index(_index.parent())

    def delete_baseline_seg(self) -> None:
        """Remove a baseline segment from the treeView."""
        
        selected_indexes = self.view.ui.tree_view_baseline.selectedIndexes()
        if not selected_indexes:
            return None
        
        # -- Find the Building Segment Name selected in the treeView
        starting_idx = selected_indexes[0]
        parent_idx = self.find_parent_treeView_index(starting_idx)
        bldg_segment_name = parent_idx.data().split(":")[-1].strip()
        
        # -- Remove it
        print(f"Removing Baseline Segment '{bldg_segment_name}' from the Project.")
        self.model.remove_baseline_segment_by_name(bldg_segment_name)
    
    def delete_proposed_seg(self) -> None:
        """Remove a proposed segment from the treeView."""
        
        selected_indexes = self.view.ui.tree_view_proposed.selectedIndexes()
        if not selected_indexes:
            return None
        
        # -- Find the Building Segment Name selected in the treeView
        starting_idx = selected_indexes[0]
        parent_idx = self.find_parent_treeView_index(starting_idx)
        bldg_segment_name = parent_idx.data().split(":")[-1].strip()
        
        # -- Remove it
        print(f"Removing Proposed Segment '{bldg_segment_name}' from the Project.")
        self.model.remove_proposed_segment_by_name(bldg_segment_name)

class PHPPBaselineConfirmationDialog(qtw.QMessageBox):
    """Warning Message Box before Executing the PHPP Baseline Overwrite."""
   
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        self.message_label = qtw.QLabel(message)
        self.setIcon(qtw.QMessageBox.Icon.Warning)
        self.setText("This will overwrite values in the PHPP file with the Baseline values.")
        self.setInformativeText("Note: please make sure that you have create a "\
                                "backup copy of your PHPP before proceeding.\n"\
                                "Are you sure you want to continue?")
        self.btn_yes = qtw.QMessageBox.StandardButton.Yes
        self.btn_no = qtw.QMessageBox.StandardButton.No
        self.setStandardButtons( self.btn_yes | self.btn_no)
        self.setDefaultButton(self.btn_no)

class CCTabPHPPBaseline:
    """The PHPP Baseline Configuration tab."""
    
    def __init__(self, _model: CCModel, _view: CCMainWindow):
        self.model = _model
        self.view = _view
        self.populate_dropdown_codes()
        self.populate_dropdown_climate_zones()

    def populate_dropdown_codes(self):
        """Populate the dropdown menu with the available Baseline Segments."""
        self.view.ui.comboBox_projBaselineCode.clear()
        self.view.ui.comboBox_projBaselineCode.addItems(
            self.model.get_allowable_code_names()
        )

    def populate_dropdown_climate_zones(self):
        """Populate the dropdown menu with the available Baseline Segments."""
        self.view.ui.comboBox_projASHRAEClimateZone.clear()
        self.view.ui.comboBox_projASHRAEClimateZone.addItems(
            self.model.get_allowable_climate_zone_names()
        )

    def set_source_phpp_file_path(self) -> None:
        """Set the path to the PHPP file to be used as the Baseline."""
        filepath = self.view.get_file_path(filter=file_type.XL)
        if not filepath or not filepath.exists():
            return None

        self.view.ui.lineEdit_selectSourcePHPPforBaseliner.setText(str(filepath))

    def get_source_phpp_file_path(self) -> pathlib.Path:
        """Get the path to the PHPP file to be used as the Baseline."""
        if not self.view.ui.lineEdit_selectSourcePHPPforBaseliner.text():
            self.set_source_phpp_file_path()
        
        return pathlib.Path(self.view.ui.lineEdit_selectSourcePHPPforBaseliner.text())

    def get_baseline_code_standard_as_enum(self) -> BaselineCodes:
        """Get the Baseline Code as an Enum."""
        return BaselineCodes(self.view.ui.comboBox_projBaselineCode.currentText())

    def get_baseline_climate_zone_as_enum(self) -> ClimateZones:
        """Get the Baseline Code Climate Zone as an Enum."""
        return ClimateZones(self.view.ui.comboBox_projASHRAEClimateZone.currentText())

    def collect_baseline_options(self) -> Dict:
        """Collect the Baseline options from the GUI into a Dict"""
        return {
            "baseline_code_standard": self.get_baseline_code_standard_as_enum(),
            "baseline_code_climate_zone": self.get_baseline_climate_zone_as_enum(),
            "set_envelope_u_values": self.view.ui.checkBox_baseliner_setEnvelopeUValues.isChecked(),
            "set_window_u_values": self.view.ui.checkBox_baseliner_setWindowUValues.isChecked(),
            "set_win_areas": self.view.ui.checkBox_baseliner_setWindowAreas.isChecked(),
            "set_skylight_areas": self.view.ui.checkBox_baseliner_setSkylightAreas.isChecked(),
            "set_lighting": self.view.ui.checkBox_baseliner_setSpaceLightingLPD.isChecked(),
         }

    def write_baseline_phpp(self) -> None:
        """Load the BaselineCode file, and set the PHPP values."""
        # -- Show warning popup first
        confirmation_dialog = PHPPBaselineConfirmationDialog("Are you sure you want to do this?")
        if confirmation_dialog.exec() != qtw.QMessageBox.StandardButton.Yes:
            return None

        # -- Load the PHPP file
        phpp_filepath = self.get_source_phpp_file_path()
        if not phpp_filepath:
            return None
        
        # -- Load the Baseline Code file
        baseline_code_option = self.get_baseline_code_standard_as_enum()
        baseline_model = self.model.load_baseline_code_file(baseline_code_option)
        if not baseline_model:
            return None

        baseline_options = self.collect_baseline_options()
        self.model.write_PHPP_baseline.emit(phpp_filepath, baseline_model, baseline_options)


class CCApp(qtw.QApplication):
    """CarbonCheck Application Controller."""

    # -- Thread worker Signal for redirecting stdout
    received_text = qtc.pyqtSignal(str)

    def __init__(self, _output_format: ModuleType, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.view = CCMainWindow()
        self.model = CCModel(_output_format)
        self.tab_report = CCTabReport(self.model, self.view) 
        self.tab_phpp_baseline = CCTabPHPPBaseline(self.model, self.view)
        self._startup_preview_panel() # -- Connect preview panel to stdout
        self._connect_signals()

    def _connect_signals(self) -> None:
        """Hook up all the signals and slots."""
        # .connect( SLOT )
        self.view.ui.actionOpen.triggered.connect(self.menu_file_open)
        self.view.ui.actionSave.triggered.connect(self.menu_file_save)
        self.view.ui.actionSave_As.triggered.connect(self.menu_file_save_as)
        self.view.ui.actionClose.triggered.connect(self.menu_close)
        self.view.ui.actionExport_Report_To.triggered.connect(self.tab_report.write_report_to_file)

        # -- Tab Report Buttons
        self.view.ui.btn_add_team_info.clicked.connect(self.tab_report.add_project_info_from_file)
        self.view.ui.btn_add_baseline_seg.clicked.connect(self.tab_report.add_baseline_seg_from_file)
        self.view.ui.btn_add_proposed_seg.clicked.connect(self.tab_report.add_proposed_seg_from_file)
        self.view.ui.btn_create_report.clicked.connect(self.tab_report.write_report_to_file)
        self.view.ui.btn_del_baseline_seg.clicked.connect(self.tab_report.delete_baseline_seg)
        self.view.ui.btn_del_proposed_seg.clicked.connect(self.tab_report.delete_proposed_seg)

        # -- Tab PHPP Baseline Buttons
        self.view.ui.btn_selectSourcePHPPforBaseliner.clicked.connect(self.tab_phpp_baseline.set_source_phpp_file_path)
        self.view.ui.btn_writeBaselinePHPP.clicked.connect(self.tab_phpp_baseline.write_baseline_phpp)

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

    # -------------------------------------------------------------------------
    # -- GUI Preview Panel internal methods

    def _startup_preview_panel(self):
        # -- Setup the Queue for capturing stdout to the GUI's preview panel, as shown in:
        # https://stackoverflow.com/questions/21071448/redirecting-stdout-and-stderr-to-a-pyqt4-qtextedit-from-a-secondary-thread
        # https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file
        self.queue = Queue()
        sys.stdout = WriteStream(self.queue)
        self._configure_worker_threads()

    def _configure_worker_threads(self):
        """Configure and start up all the worker threads for stdout stream."""
        self._create_workers()
        self._start_worker_threads()
        self._connect_worker_signals()
    
    def _create_workers(self):
        self.worker_txt_receiver = WorkerReceiveText(self.queue)
        self.worker_txt_receiver_thread = qtc.QThread()
    
    def _start_worker_threads(self):
        self.worker_txt_receiver.moveToThread(self.worker_txt_receiver_thread)
        self.worker_txt_receiver_thread.start()
    
    @qtc.pyqtSlot(str)
    def _append_text(self,text):
        self.view.ui.textEdit_output.moveCursor(qtg.QTextCursor.MoveOperation.End)
        self.view.ui.textEdit_output.insertPlainText( text )

    def _connect_worker_signals(self):
        self.worker_txt_receiver.received_text.connect(self._append_text)
        self.worker_txt_receiver_thread.started.connect(self.worker_txt_receiver.run)

    # -------------------------------------------------------------------------
    # -- Menu methods

    def menu_file_open(self) -> None:
        """Get a CC Project file path and open it. Execute on Menu / File / Open..."""
        filepath = self.view.get_file_path(filter=file_type.JSON)
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

    def menu_close(self) -> None:
        """Execute on Menu / File / Close."""
        self.view.close()
    