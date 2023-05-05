# -*- Python Version: 3.11 -*-

"""Main Application."""

from datetime import datetime
import logging
import logging.config
import os
import pathlib
from queue import Queue
import sys
from types import ModuleType
from typing import Dict, Tuple
import yaml

try:
    from PyQt6 import QtGui as qtg
    from PyQt6 import QtWidgets as qtw
    from PyQt6 import QtCore as qtc
except Exception as e:
    raise Exception("Error importing PyQt6 library?", e)

try:
    from App.views.view_main_window import CCMainWindow, file_type
    from App.cc_model import CCModel
    from App.cc_workers import WorkerReceiveText, WriteStream
except Exception as e:
    raise Exception("Error importing App library?", e)

try:
    from ph_baseliner.codes.options import (
        BaselineCodes,
        ClimateZones,
        Use_Groups,
        PF_Groups,
    )
except Exception as e:
    raise Exception("Error importing App library?", e)


def find_application_path() -> pathlib.Path:
    """Returns the path to the application root location.

    The 'application' will be located and run from different places, depending on the OS and
    whether it is run as an 'app' or run as a 'script'.
    If the application is run as a frozen bundle, the PyInstaller boot-loader
    extends the sys module by a flag 'frozen=True' and sets the __file__ path into variable '_MEIPASS'.

    For instance:

    App (sys.frozen==True):
    ----
        MacOS:
        - sys.executable            = '/Users/em/Dropbox/bldgtyp/2209_Nash_Home/12_Scripts/dist/app'
        - os.path.abspath(__file__) = '/var/folders/vm/rkn0g153d2tph6hz8r00000gn/T/_MEIh08vPN/app.py'
        - sys._MEIPASS              = '/var/folders/vm/rkn0g153d2tph6hz8r00000gn/T/_MEI1fU4xe'

        Windows:
        - sys.executable            = '\\\\Mac\\Dropbox\\bldgtyp\\2209_Nash_Home\\12_Scripts\\dist\\app.exe'
        - os.path.abspath(__file__) = 'C:\\Users\\em\\AppData\\Local\\Temp\\_MEI34162\\app.py'
        - sys._MEIPASS              = 'C:\\Users\\em\\AppData\\Local\\Temp\\_MEI34162'

    Script (ie: from inside VSCode)
    ------
        MacOS:
        - sys.executable            = '/Users/em/Dropbox/bldgtyp/2209_Nash_Home/12_Scripts/venv/bin/python'
        - os.path.abspath(__file__) = '/Users/em/Dropbox/bldgtyp/2209_Nash_Home/12_Scripts/app.py'
        - sys._MEIPASS              = None (does not exist)

        Windows:
        - sys.executable            = '\\\\mac\\Dropbox\\bldgtyp\\2209_Nash_Home\\12_Scripts\\venv\\Scripts\\python.exe'
        - os.path.abspath(__file__) = '\\\\mac\\Dropbox\\bldgtyp\\2209_Nash_Home\\12_Scripts\\app.py'
        - sys._MEIPASS              = None (does not exist)

    So, if its a script, use __file__, but if its an 'app', use sys.executable for the app location.
    """

    def _app_is_run_as_frozen_app() -> bool:
        """Return True if the app is run as a frozen app, False if not."""
        return getattr(sys, "frozen", False)

    # -- return the PARENT of the app's location as the application root
    if _app_is_run_as_frozen_app():
        return pathlib.Path(sys.executable).parent
    else:
        return pathlib.Path(os.path.abspath(__file__)).parent


def addLoggingLevel(levelName, levelNum, methodName=None):
    # Adopted from https://stackoverflow.com/a/35804945/1691778
    # Adds a new logging method to the logging module
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError("{} already defined in logging module".format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError("{} already defined in logging module".format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError("{} already defined in logger class".format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


class CCTabReport:
    """The 'Report' tab of the CarbonCheck application."""

    def __init__(self, _model: CCModel, _view: CCMainWindow):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating CCTabReport")

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

    def write_report_to_file(self, _log_path: pathlib.Path) -> None:
        """Write out the data to a new Excel report"""
        self.logger.debug("Writing report to file")

        self.model.set_project_from_gui()
        self.model.write_excel_report.emit(self.model.NBDM_project, _log_path)

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
        self.setText(
            "This will overwrite values in the PHPP file with the Baseline values."
        )
        self.setInformativeText(
            "Note: please make sure that you have create a "
            "backup copy of your PHPP before proceeding.\n"
            "Are you sure you want to continue?"
        )
        self.btn_yes = qtw.QMessageBox.StandardButton.Yes
        self.btn_no = qtw.QMessageBox.StandardButton.No
        self.setStandardButtons(self.btn_yes | self.btn_no)
        self.setDefaultButton(self.btn_no)


class CCTabPHPPBaseline:
    """The PHPP Baseline Configuration tab."""

    def __init__(self, _model: CCModel, _view: CCMainWindow):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating CCTabPHPPBaseline")

        self.model = _model
        self.view = _view
        self.populate_dropdown_codes()
        self.populate_dropdown_climate_zones()
        self.populate_dropdown_use_types()
        self.populate_dropdown_pf_groups()

    def populate_dropdown_codes(self):
        """Populate the dropdown menu with the available Baseline Segments."""
        self.logger.debug(
            "Populating dropdown menu with available Baseline Building Codes"
        )
        self.view.ui.comboBox_projBaselineCode.clear()
        self.view.ui.comboBox_projBaselineCode.addItems(
            self.model.get_allowable_code_names()
        )

    def populate_dropdown_climate_zones(self):
        """Populate the dropdown menu with the available Baseline Segments."""
        self.logger.debug("Populating dropdown menu with available Climate Zones")
        self.view.ui.comboBox_projASHRAEClimateZone.clear()
        self.view.ui.comboBox_projASHRAEClimateZone.addItems(
            self.model.get_allowable_climate_zone_names()
        )

    def populate_dropdown_use_types(self):
        """Populate the dropdown menu with the available Baseline Segments."""
        self.logger.debug("Populating dropdown menu with available Use-Types")
        self.view.ui.comboBox_projUseGroup.clear()
        self.view.ui.comboBox_projUseGroup.addItems(
            self.model.get_allowable_use_type_names()
        )

    def populate_dropdown_pf_groups(self):
        """Populate the dropdown menu with the available Baseline Segments."""
        self.logger.debug("Populating dropdown menu with available PF Groups")
        self.view.ui.comboBox_projPFGroup.clear()
        self.view.ui.comboBox_projPFGroup.addItems(
            self.model.get_allowable_pf_group_names()
        )

    def set_source_phpp_file_path(self) -> None:
        """Set the path to the PHPP file to be used as the Baseline."""
        filepath = self.view.get_file_path(filter=file_type.XL)
        self.logger.debug(f"Setting source PHPP file path to {filepath}")

        if not filepath or not filepath.exists():
            self.logger.error(f"Could not find the file: {filepath}")
            return None

        self.view.ui.lineEdit_selectSourcePHPPforBaseliner.setText(str(filepath))

    def get_source_phpp_file_path(self) -> pathlib.Path:
        """Get the path to the PHPP file to be used as the Baseline."""
        self.logger.debug("Getting source PHPP file path")

        if not self.view.ui.lineEdit_selectSourcePHPPforBaseliner.text():
            self.set_source_phpp_file_path()

        return pathlib.Path(self.view.ui.lineEdit_selectSourcePHPPforBaseliner.text())

    def get_baseline_code_standard_as_enum(self) -> BaselineCodes:
        """Get the Baseline Code as an Enum."""
        return BaselineCodes(self.view.ui.comboBox_projBaselineCode.currentText())

    def get_baseline_climate_zone_as_enum(self) -> ClimateZones:
        """Get the Baseline Code Climate Zone as an Enum."""
        return ClimateZones(self.view.ui.comboBox_projASHRAEClimateZone.currentText())

    def get_baseline_use_group_as_enum(self) -> Use_Groups:
        """Get the Baseline Code Use Group as an Enum."""
        return Use_Groups(self.view.ui.comboBox_projUseGroup.currentText())

    def get_baseline_pf_group_as_enum(self) -> PF_Groups:
        """Get the Baseline Code PF Group as an Enum."""
        return PF_Groups(self.view.ui.comboBox_projPFGroup.currentText())

    def collect_baseline_options(self) -> Dict:
        """Collect the Baseline options from the GUI into a Dict"""
        self.logger.debug("Collecting Baseline options from the GUI into a Dict")

        return {
            "baseline_code_standard": self.get_baseline_code_standard_as_enum(),
            "baseline_code_climate_zone": self.get_baseline_climate_zone_as_enum(),
            "set_envelope_u_values": self.view.ui.checkBox_baseliner_setEnvelopeUValues.isChecked(),
            "set_window_u_values": self.view.ui.checkBox_baseliner_setWindowUValues.isChecked(),
            "set_win_areas": self.view.ui.checkBox_baseliner_setWindowAreas.isChecked(),
            "set_skylight_areas": self.view.ui.checkBox_baseliner_setSkylightAreas.isChecked(),
            "set_lighting": self.view.ui.checkBox_baseliner_setSpaceLightingLPD.isChecked(),
            "baseline_code_pf_group": self.get_baseline_pf_group_as_enum(),
            "baseline_code_use_group": self.get_baseline_use_group_as_enum(),
        }

    def write_baseline_phpp(self) -> None:
        """Load the BaselineCode file, and set the PHPP values."""
        self.logger.debug("Writing Baseline PHPP file")

        # -- Show warning popup first
        confirmation_dialog = PHPPBaselineConfirmationDialog(
            "Are you sure you want to do this?"
        )
        if confirmation_dialog.exec() != qtw.QMessageBox.StandardButton.Yes:
            self.logger.debug("User cancelled Baseline PHPP file write")
            return None

        # -- Load the PHPP file
        phpp_filepath = self.get_source_phpp_file_path()
        if not phpp_filepath:
            self.logger.debug(f"Could not find PHPP file: {phpp_filepath}")
            return None

        # -- Load the Baseline Code file
        baseline_code_option = self.get_baseline_code_standard_as_enum()
        baseline_model = self.model.load_baseline_code_file(baseline_code_option)
        if not baseline_model:
            return None

        baseline_options = self.collect_baseline_options()
        self.model.write_PHPP_baseline.emit(
            phpp_filepath, baseline_model, baseline_options
        )


class CCApp(qtw.QApplication):
    """CarbonCheck Application Controller."""

    # -- Thread worker Signal for redirecting stdout
    received_text = qtc.pyqtSignal(str)

    def __init__(self, _output_format: ModuleType, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.application_path = find_application_path()
        self._startup_preview_panel()  # -- Connect preview panel to stdout
        self.startup_logging()

        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting up the CarbonCheck Application.")
        self.logger.debug(f"application_path: {self.application_path}")
        self.logger.debug(f"log_path: {self.log_path}")

        self.view = CCMainWindow()
        self.model = CCModel(_output_format, self.application_path)
        self.tab_report = CCTabReport(self.model, self.view)
        self.tab_phpp_baseline = CCTabPHPPBaseline(self.model, self.view)

        self._connect_signals()
        self._connect_button_loggers()
        self._connect_action_loggers()

        # Set up to terminate the QThread when we exit
        self.aboutToQuit.connect(self.force_quit)

    def force_quit(self) -> None:
        """Force the QThread to quit."""
        for worker_thread in self.model.worker_threads:
            # For use when the window is closed
            if worker_thread.isRunning():
                self.kill_thread(worker_thread)

    def kill_thread(self, _worker_thread: qtc.QThread) -> None:
        """Kill the QThread."""
        # Just tell the worker to stop, then tell it to quit and wait for that
        # to happen
        _worker_thread.requestInterruption()
        if _worker_thread.isRunning():
            _worker_thread.quit()
            _worker_thread.wait()
        else:
            # -- worker has already exited
            pass

    def startup_logging(self) -> None:
        """Configure logging for the application."""

        # -- Get the Logging file path
        self.log_path = pathlib.Path(self.application_path, "Logs")
        if not self.log_path.exists():
            os.makedirs(self.log_path)
        else:
            # -- Remove old log files
            for file in self.log_path.glob("*.log"):
                file.unlink()

        # -- Be sure to add the excel custom log level
        addLoggingLevel("EXCEL", logging.INFO + 5)

        # -- Find the logging configuration YAML file
        config_file = pathlib.Path(self.application_path, "__logging_config__.yaml")
        if not config_file.exists():
            msg = f"ERROR: Logging configuration file not found: {config_file}"
            qtw.QMessageBox(
                qtw.QMessageBox.Icon.Warning, "Missing Configuration File", msg
            ).exec()

        # -- Load logging configuration from YAML file
        with open(config_file, "rt") as f:
            config = yaml.safe_load(f.read())

        # -- Setup the log file paths
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        cc_log_filename = str(config["handlers"]["to_file_handler"]["filename"]).format(
            __timestamp__=timestamp
        )
        self.cc_log_filepath = pathlib.Path(self.log_path, cc_log_filename)
        config["handlers"]["to_file_handler"]["filename"] = self.cc_log_filepath

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        excel_log_filename = str(config["handlers"]["to_excel"]["filename"]).format(
            __timestamp__=timestamp
        )
        self.excel_log_filepath = pathlib.Path(self.log_path, excel_log_filename)
        config["handlers"]["to_excel"]["filename"] = self.excel_log_filepath

        # -- Configure logging using the loaded configuration from file
        logging.config.dictConfig(config)

    def click_logger(self) -> None:
        """Record the user's button / action clicks to the Log."""
        self.logger.debug(f"User Clicked: {self.sender().objectName()}")

    def _connect_signals(self) -> None:
        """Hook up all the signals and slots."""
        self.logger.debug("Connecting signals and slots.")

        # .connect( SLOT )
        self.view.ui.actionOpen.triggered.connect(self.menu_file_open)
        self.view.ui.actionSave.triggered.connect(self.menu_file_save)
        self.view.ui.actionSave_As.triggered.connect(self.menu_file_save_as)
        self.view.ui.actionClose.triggered.connect(self.menu_close)
        self.view.ui.actionExport_Report_To.triggered.connect(
            self.tab_report.write_report_to_file
        )

        # -- Tab Report Buttons
        self.view.ui.btn_add_team_info.clicked.connect(
            self.tab_report.add_project_info_from_file
        )
        self.view.ui.btn_add_baseline_seg.clicked.connect(
            self.tab_report.add_baseline_seg_from_file
        )
        self.view.ui.btn_add_proposed_seg.clicked.connect(
            self.tab_report.add_proposed_seg_from_file
        )
        self.view.ui.btn_create_report.clicked.connect(self.write_report)
        self.view.ui.btn_del_baseline_seg.clicked.connect(
            self.tab_report.delete_baseline_seg
        )
        self.view.ui.btn_del_proposed_seg.clicked.connect(
            self.tab_report.delete_proposed_seg
        )

        # -- Tab PHPP Baseline Buttons
        self.view.ui.btn_selectSourcePHPPforBaseliner.clicked.connect(
            self.tab_phpp_baseline.set_source_phpp_file_path
        )
        self.view.ui.btn_writeBaselinePHPP.clicked.connect(
            self.tab_phpp_baseline.write_baseline_phpp
        )

        self.model.load_team_data.connect(self.view.set_treeView_data_team)
        self.model.load_baseline_segments_data.connect(
            self.view.set_treeView_data_baseline
        )
        self.model.load_proposed_segments_data.connect(
            self.view.set_treeView_data_proposed
        )

        self.model.read_treeView_team.connect(self.view.get_treeView_data_team)
        self.model.read_treeView_site.connect(self.view.get_treeView_data_site)
        self.model.read_treeView_baseline_segments.connect(
            self.view.get_treeView_data_baseline_building
        )
        self.model.read_treeView_proposed_segments.connect(
            self.view.get_treeView_data_proposed_building
        )

        self.view.got_team_data.connect(self.model.set_project_team_from_treeView_data)
        self.view.got_site_data.connect(self.model.set_project_site_from_treeView_data)
        self.view.got_baseline_building_data.connect(
            self.model.set_project_baseline_segments_from_treeView_data
        )
        self.view.got_proposed_building_data.connect(
            self.model.set_project_proposed_segments_from_treeView_data
        )

        return None

    def _connect_button_loggers(self):
        """Connect all the QButtons to the click_logger method for debugging."""
        for button in self.view.buttons:
            button.clicked.connect(self.click_logger)

    def _connect_action_loggers(self):
        """Connect all the QActions to the click_logger method for debugging."""
        for action in self.view.actions:
            action.triggered.connect(self.click_logger)

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
        self.mutex = qtc.QMutex()
        self.worker_txt_receiver = WorkerReceiveText(self.queue, self.mutex)
        self.worker_txt_receiver_thread = qtc.QThread()

    def _start_worker_threads(self):
        self.worker_txt_receiver.moveToThread(self.worker_txt_receiver_thread)
        self.worker_txt_receiver_thread.start()

    @qtc.pyqtSlot(str)
    def _append_text(self, text):
        self.view.ui.textEdit_output.moveCursor(qtg.QTextCursor.MoveOperation.End)
        self.view.ui.textEdit_output.insertPlainText(text)

    def _connect_worker_signals(self):
        self.worker_txt_receiver.received_text.connect(self._append_text)
        self.worker_txt_receiver_thread.started.connect(self.worker_txt_receiver.run)

    def write_report(self):
        """Write the report to the log file."""
        self.tab_report.write_report_to_file(self.excel_log_filepath)

    # -------------------------------------------------------------------------
    # -- Menu methods

    def menu_file_open(self) -> None:
        """Get a CC Project file path and open it. Execute on Menu / File / Open..."""
        self.logger.debug("Opening a new project file.")
        filepath = self.view.get_file_path(filter=file_type.JSON)
        if not filepath:
            self.logger.debug("No file path provided by user.")
            return None
        self.model.load_cc_project_from_file(filepath)

    def menu_file_save(self) -> None:
        """Execute on Menu / File / Save."""
        self.logger.debug("Saving the project to the current file.")
        filepath = self.view.get_save_file_path()
        if not filepath:
            self.logger.debug("No file path provided by user.")
            return
        filepath = pathlib.Path(filepath).resolve()
        self.model.write_json_file(filepath)

    def menu_file_save_as(self) -> None:
        self.logger.debug("Saving the project to a new file.")
        filepath = self.view.get_save_file_path()
        if not filepath:
            self.logger.debug("No file path provided by user.")
            return
        filepath = pathlib.Path(filepath).resolve()
        self.model.write_json_file(filepath)

    def menu_close(self) -> None:
        """Execute on Menu / File / Close."""
        self.logger.debug("Closing the application.")
        self.view.close()
