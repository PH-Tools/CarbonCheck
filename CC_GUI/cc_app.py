# -*- Python Version: 3.11 -*-

"""Main Application."""

from datetime import datetime
from dataclasses import dataclass
import logging
import logging.config
from pathlib import Path
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
    from CC_GUI.views.view_main_window import CCMainWindow, file_type
    from CC_GUI.views.view_baseline_options_window import Window_BaselineOptions
    from CC_GUI.views.view_team_site_window import Window_TeamAndSiteData
    from CC_GUI.views.view_building_components import Window_BuildingComponents
    from CC_GUI.views.tree_view_tools import find_parent_treeView_index
    from CC_GUI.cc_model import CCModel
    from CC_GUI.cc_workers import WorkerReceiveText, WriteStream
    from CC_GUI.cc_app_config import (
        find_application_path,
        log_exception,
        add_logging_level,
    )
except Exception as e:
    raise Exception("Error importing CC_GUI library?", e)
try:
    from ph_baseliner.codes.options import (
        BaselineCodes,
        ClimateZones,
        Use_Groups,
        PF_Groups,
    )
    from ph_baseliner.codes.model import BaselineCode
except Exception as e:
    raise Exception("Error importing App library?", e)


class Tab_Report:
    """The 'Report' tab of the CarbonCheck application."""

    def __init__(
        self, _model: CCModel, _view: CCMainWindow, _excel_log_path: Path
    ) -> None:
        self.excel_log_path = _excel_log_path
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating Tab_Report...")

        self.model = _model
        self.view = _view

        # -- Connect the Baseline Options Button and Data
        self.window_team_and_site = Window_TeamAndSiteData()
        self.window_bldg_components = Window_BuildingComponents()
        self.logger.debug("Tab_Report successfully setup.")

    def _connect_buttons_and_signals(self) -> None:
        """Connect the buttons and signals for the 'Report' tab."""
        # -- Hook up the [ View ]--Signals->  - - - >-Slots--[ Model ]
        self.window_team_and_site.got_team_data.connect(
            self.model.set_project_team_from_treeView_data
        )
        self.window_team_and_site.got_site_data.connect(
            self.model.set_project_site_from_treeView_data
        )

        # -- Hook up the [ View ]--Signals->  - - - >-Methods--[ Self ]
        # -- Tab Buttons
        self.view.ui.btn_add_baseline_seg.clicked.connect(self.add_baseline_seg_from_file)
        self.view.ui.btn_add_proposed_seg.clicked.connect(self.add_proposed_seg_from_file)
        self.view.ui.btn_create_report.clicked.connect(self.write_report)
        self.view.ui.btn_del_baseline_seg.clicked.connect(self.delete_baseline_seg)
        self.view.ui.btn_del_proposed_seg.clicked.connect(self.delete_proposed_seg)
        self.view.ui.btn_show_team_info.clicked.connect(self.team_and_site_show)
        self.view.ui.btn_show_bldg_components.clicked.connect(self.bldg_component_show)

        # -- Team and Site Info Window and Buttons
        self.window_team_and_site.got_team_data.connect(self.model.update_treeview_team)
        self.window_team_and_site.got_site_data.connect(self.model.update_treeview_team)
        self.window_team_and_site.ui.btn_add_team_info.clicked.connect(
            self.add_project_info_from_file
        )
        self.window_team_and_site.ui.btn_OK.clicked.connect(self.team_and_site_ok)
        self.window_team_and_site.ui.btn_Cancel.clicked.connect(self.team_and_site_cancel)

        # -- Building Component Window and Buttons
        self.window_bldg_components.got_building_component_data.connect(
            self.model.set_project_bldg_components_from_treeView_data
        )
        self.window_bldg_components.got_building_component_data.connect(
            self.model.update_treeview_bldg_components
        )
        self.window_bldg_components.ui.btn_add_bldg_component_info.clicked.connect(
            self.add_bldg_component_info_from_file
        )
        self.window_bldg_components.ui.btn_OK.clicked.connect(self.bldg_component_ok)
        self.window_bldg_components.ui.btn_Cancel.clicked.connect(
            self.bldg_component_cancel
        )

    # -------------------------------------------------------------------------
    # -- Building Segments Window and Buttons

    def add_baseline_seg_from_file(self) -> None:
        """Load a new Baseline Segment's data from a single PHPP file."""
        filepath = self.view.get_file_path(filter=file_type.PH_SOURCE_FILE)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.sig_read_baseline_seg_data_from_file.emit(
            self.model.NBDM_project, filepath
        )

    def add_proposed_seg_from_file(self) -> None:
        """Load a new Proposed Segment's data from a single PHPP file."""
        filepath = self.view.get_file_path(filter=file_type.PH_SOURCE_FILE)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.sig_read_proposed_seg_data_from_file.emit(
            self.model.NBDM_project, filepath
        )

    def delete_baseline_seg(self) -> None:
        """Remove a baseline segment from the treeView."""

        selected_indexes = self.view.ui.tree_view_baseline.selectedIndexes()
        if not selected_indexes:
            return None

        # -- Find the Building Segment Name selected in the treeView
        starting_idx = selected_indexes[0]
        parent_idx = find_parent_treeView_index(starting_idx)
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
        parent_idx = find_parent_treeView_index(starting_idx)
        bldg_segment_name = parent_idx.data().split(":")[-1].strip()

        # -- Remove it
        print(f"Removing Proposed Segment '{bldg_segment_name}' from the Project.")
        self.model.remove_proposed_segment_by_name(bldg_segment_name)

    # -------------------------------------------------------------------------
    # -- Team and Site Window and Buttons

    def add_project_info_from_file(self) -> None:
        """Load 'Project' information from a single PHPP/WUFI-PDF file (Team, Climate, Site...)"""
        filepath = self.view.get_file_path(filter=file_type.PH_SOURCE_FILE)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.sig_read_project_data_from_file.emit(self.model.NBDM_project, filepath)

    def team_and_site_show(self) -> None:
        """Show the Team/Site Data input Window."""
        self.window_team_and_site.show()
        self.model.update_treeview_team()

    def team_and_site_ok(self) -> None:
        """Run on 'OK' click from the Team and Site Info Window."""
        self.model.set_project_from_gui()
        self.window_team_and_site.close_window()

    def team_and_site_cancel(self) -> None:
        """Run on 'Cancel' click from the Team and Site Info Window."""
        self.window_team_and_site.close_window()

    # -------------------------------------------------------------------------
    # -- Building Component Window and Buttons

    def add_bldg_component_info_from_file(self) -> None:
        """Load 'Bldg-Component' information from a single PHPP/WUFI-PDF file (Envelope, Appliances, etc..)"""
        filepath = self.view.get_file_path(filter=file_type.PH_SOURCE_FILE)

        if not filepath or not filepath.exists():
            return None

        # -- Send the signal to the Model to run the reader
        self.model.sig_read_bldg_component_data_from_file.emit(
            self.model.NBDM_project, filepath
        )

    def bldg_component_show(self) -> None:
        """Show the Building-Components Data input Window."""
        self.window_bldg_components.show()
        self.model.update_treeview_bldg_components()

    def bldg_component_ok(self) -> None:
        """Run on 'OK' click from the Building-Components Info Window."""
        self.model.set_project_from_gui()
        self.window_bldg_components.close_window()

    def bldg_component_cancel(self) -> None:
        """Run on 'Cancel' click from the Building-Components Info Window."""
        self.window_bldg_components.close_window()

    # -------------------------------------------------------------------------
    # -- Write Report Buttons

    def write_report(self) -> None:
        """Write the report to the log file."""
        self.write_report_to_file(self.excel_log_path)

    def write_report_to_file(self, _log_path: Path) -> None:
        """Write out the data to a new Excel report"""
        self.logger.debug("Writing report to file")
        self.logger.debug("Rebuilding NBDM Project from GUI data")
        self.model.set_project_from_gui()
        self.model.sig_write_excel_report.emit(self.model.NBDM_project, _log_path)


class Dialog_PHPPBaselineConfirmation(qtw.QMessageBox):
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


@dataclass
class BaselinerOptionsData:
    set_envelope_u_values: bool = True
    set_window_u_values: bool = True
    set_win_areas: bool = True
    set_skylight_areas: bool = True
    set_lighting: bool = True

    def set_from_dict(self, _dict) -> None:
        """Set the options from a dictionary."""
        for key, value in _dict.items():
            setattr(self, key, value)


class Tab_Baseline:
    """The PH-Model Baseline Configuration tab."""

    def __init__(self, _model: CCModel, _view: CCMainWindow):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Creating Tab_PHPPBaseline...")

        self.model = _model
        self.view = _view

        # -- Connect the Baseline Options Button and Data
        self.baseline_options = BaselinerOptionsData()
        self.window_baseline_options = Window_BaselineOptions()
        self.view.ui.btn_moreBaselineOptions.clicked.connect(
            self.show_baseline_options_window
        )
        self.window_baseline_options.options_data.connect(self.set_baseline_options)

        # --
        self.populate_dropdown_codes()
        self.populate_dropdown_climate_zones()
        self.populate_dropdown_use_types()
        self.populate_dropdown_pf_groups()
        self.logger.debug("Tab_PHPPBaseline successfully setup.")

    def _connect_buttons_and_signals(self):
        """Connect the buttons and signals for this tab."""
        # -- Tab Buttons: PHPP Baseline
        self.view.ui.btn_selectSourcePHPPforBaseliner.clicked.connect(
            self.set_source_phpp_file_path
        )
        self.view.ui.btn_createBaselinePhModel.clicked.connect(self.create_baseline)

        # -- Tab Buttons: PHPP Baseline Options Window
        self.window_baseline_options.ui.btn_OK.clicked.connect(
            self.window_baseline_options.get_baseline_option_values
        )
        self.window_baseline_options.ui.btn_Cancel.clicked.connect(
            self.window_baseline_options.close_window
        )

    def show_baseline_options_window(self) -> None:
        """Show the Baseline Options Window."""
        self.window_baseline_options.show()

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
        filepath = self.view.get_file_path(filter=file_type.PH_MODEL)
        self.logger.debug(f"Setting source PHPP file path to {filepath}")

        if not filepath or not filepath.exists():
            self.logger.error(f"Could not find the file: {filepath}")
            return None

        self.view.ui.lineEdit_selectSourcePHPPforBaseliner.setText(str(filepath))

    def get_ph_model_source_file_path(self) -> Path:
        """Get the path to the PHPP file to be used as the Baseline."""
        self.logger.debug("Getting source PHPP file path")

        if not self.view.ui.lineEdit_selectSourcePHPPforBaseliner.text():
            self.set_source_phpp_file_path()

        return Path(self.view.ui.lineEdit_selectSourcePHPPforBaseliner.text())

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
            "set_envelope_u_values": self.baseline_options.set_envelope_u_values,
            "set_window_u_values": self.baseline_options.set_window_u_values,
            "set_win_areas": self.baseline_options.set_win_areas,
            "set_skylight_areas": self.baseline_options.set_skylight_areas,
            "set_lighting": self.baseline_options.set_lighting,
            "baseline_code_pf_group": self.get_baseline_pf_group_as_enum(),
            "baseline_code_use_group": self.get_baseline_use_group_as_enum(),
        }

    def create_baseline(self) -> None:
        self.logger.debug("Creating Baseline PH Model")

        # -- Load the Source File specified by the user
        source_file = self.get_ph_model_source_file_path()
        if not source_file:
            self.logger.debug(f"Could not find PH-Model file: {source_file}")
            return None

        # -- Load the Baseline Code file
        baseline_code_option = self.get_baseline_code_standard_as_enum()
        baseline_model = self.model.load_baseline_code_file(baseline_code_option)
        if not baseline_model:
            return None

        # get the extension of the source file
        file_extension = source_file.suffix
        if file_extension in [".xml"]:
            self.create_baseline_wufi(source_file, baseline_model)
        elif file_extension in [".xls", ".xlsx", ".xlsm"]:
            self.create_baseline_phpp(source_file, baseline_model)
        else:
            self.logger.info(
                f"File type '{file_extension}' not supported. Please specify a PHPP or WUFI-XML file."
            )
            return None

    def create_baseline_phpp(
        self, _source_file: Path, _baseline_model: BaselineCode
    ) -> None:
        """Load the BaselineCode file, and set the PHPP values."""
        self.logger.debug("Writing Baseline PHPP file")

        # -- Show warning popup first
        confirmation_dialog = Dialog_PHPPBaselineConfirmation(
            "Are you sure you want to do this?"
        )
        if confirmation_dialog.exec() != qtw.QMessageBox.StandardButton.Yes:
            self.logger.debug("User cancelled Baseline PHPP file write")
            return None

        baseline_options = self.collect_baseline_options()
        self.model.sig_write_PHPP_baseline.emit(
            _source_file, _baseline_model, baseline_options
        )

    def create_baseline_wufi(
        self, _source_file: Path, _baseline_model: BaselineCode
    ) -> None:
        """Load the BaselineCode file, and set the WUFI values."""
        self.logger.debug("Writing Baseline WUFI-XML file")

        baseline_options = self.collect_baseline_options()
        self.model.sig_write_WUFI_baseline.emit(
            _source_file, _baseline_model, baseline_options
        )

    # @qtc.pyqtSlot(dict)
    def set_baseline_options(self, _data: Dict[str, bool]):
        """Set the Baseline Options."""
        self.logger.debug("Setting the Baseline Options")
        self.baseline_options.set_from_dict(_data)


class CCApp(qtw.QApplication):
    """CarbonCheck Application Controller."""

    # -- Thread worker Signal for redirecting stdout
    received_text = qtc.pyqtSignal(str)

    def __init__(
        self,
        _output_format: ModuleType,
        _log_file_path: Path,
        _resources_path: Path,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.styles_sheet_path = _resources_path / "cc_styles.qss"
        self.path_logo_cc = _resources_path / "logo_CarbonCheck.ico"
        self.path_logo_nyserda = _resources_path / "logo_NYSERDA.png"
        self.path_logo_pha = _resources_path / "logo_PHA.png"
        self.path_logging_config = _resources_path / "__logging_config__.yaml"

        self.load_style_sheet(self.styles_sheet_path)
        self.application_path = find_application_path()
        self._startup_preview_panel()  # -- Connect preview panel to stdout
        self.app_log_filepath, self.excel_log_filepath = self.startup_logging(
            _log_file_path
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting up the CarbonCheck Application.")
        self.logger.debug(f"application_path: {self.application_path}")
        self.logger.debug(f"log_path: {self.app_log_filepath}")

        self.view = CCMainWindow(self.path_logo_cc)
        self.model = CCModel(_output_format, self.application_path)
        self.tab_report = Tab_Report(self.model, self.view, self.excel_log_filepath)
        self.tab_baseline = Tab_Baseline(self.model, self.view)

        self.set_logo_paths()
        self._connect_menu_actions()
        self._connect_all_button_signals()
        self._connect_button_loggers()
        self._connect_action_loggers()

        # Set up to terminate the QThread when we exit
        self.aboutToQuit.connect(self.force_quit)
        self.logger.info("Finished starting up Application.")

    def set_logo_paths(self) -> None:
        # -- NYSERDA
        self.view.ui.labelPHALogo.setPixmap(
            qtg.QPixmap(str(self.path_logo_pha.resolve()))
        )
        self.view.ui.labelNYSERDALogo.setPixmap(
            qtg.QPixmap(str(self.path_logo_nyserda.resolve()))
        )

    def load_style_sheet(self, _stylesheet_path: Path) -> None:
        style_file = qtc.QFile(str(_stylesheet_path.resolve()))
        style_file.open(qtc.QFile.OpenModeFlag.ReadOnly | qtc.QFile.OpenModeFlag.Text)
        self.setStyleSheet(str(style_file.readAll(), "utf-8"))  # type: ignore
        style_file.close()

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

    def startup_logging(self, _log_path: Path) -> Tuple[Path, Path]:
        """Configure logging for the application."""

        # -- Error Log for backup
        sys.excepthook = log_exception

        # -- Be sure to add the excel and wufi custom log level
        add_logging_level("EXCEL", logging.INFO + 5)
        add_logging_level("WUFI", logging.INFO + 5)

        # -- Find the logging configuration YAML file
        if not self.path_logging_config.exists():
            msg = (
                f"ERROR: Logging configuration file not found: {self.path_logging_config}"
            )
            qtw.QMessageBox(
                qtw.QMessageBox.Icon.Warning, "Missing Configuration File", msg
            ).exec()
            return (Path(), Path())

        # -- Load logging configuration from YAML file
        with open(self.path_logging_config, "rt") as f:
            config = yaml.safe_load(f.read())

        # -- Setup the log file paths
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        app_log_filename = str(config["handlers"]["to_file_handler"]["filename"]).format(
            __timestamp__=timestamp
        )
        app_log_filepath = Path(_log_path, app_log_filename)
        config["handlers"]["to_file_handler"]["filename"] = app_log_filepath

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        excel_log_filename = str(config["handlers"]["to_excel"]["filename"]).format(
            __timestamp__=timestamp
        )
        excel_log_filepath = Path(_log_path, excel_log_filename)
        config["handlers"]["to_excel"]["filename"] = excel_log_filepath

        # -- Configure logging using the loaded configuration from file
        logging.config.dictConfig(config)

        return app_log_filepath, excel_log_filepath

    def click_logger(self) -> None:
        """Record the user's button / action clicks to the Log."""
        self.logger.debug(f"User Clicked: {self.sender().objectName()}")

    def _connect_menu_actions(self) -> None:
        """Connect the Menu Actions to the appropriate slots."""
        self.view.ui.actionUpdate.triggered.connect(self.menu_update)
        self.view.ui.actionOpen.triggered.connect(self.menu_file_open)
        self.view.ui.actionSave.triggered.connect(self.menu_file_save)
        self.view.ui.actionSave_As.triggered.connect(self.menu_file_save_as)
        self.view.ui.actionClose.triggered.connect(self.menu_close)
        self.view.ui.actionExport_Report_To.triggered.connect(
            self.tab_report.write_report_to_file
        )

    def _connect_all_button_signals(self) -> None:
        """Hook up all the Buttons signals to the appropriate slot."""
        self.logger.debug("Connecting signals and slots...")

        # ---------------------------------------------------------------------
        # -- Hook up the [ Model ]--Signals->  - - - >-Slots--[ View ]

        # -- Set the [View] treeView Data
        self.model.sig_load_team_data.connect(
            self.tab_report.window_team_and_site.set_treeView_data_team
        )
        self.model.sig_load_site_data.connect(
            self.tab_report.window_team_and_site.set_treeView_data_team
        )
        self.model.sig_load_baseline_segments_data.connect(
            self.view.set_treeView_data_baseline
        )
        self.model.sig_load_proposed_segments_data.connect(
            self.view.set_treeView_data_proposed
        )
        self.model.sig_load_bldg_components_data.connect(
            self.tab_report.window_bldg_components.set_treeView_bldg_components
        )

        # -- Read data form [View] treeView
        self.model.sig_read_treeView_team.connect(
            self.tab_report.window_team_and_site.get_treeView_data_team
        )
        self.model.sig_read_treeView_site.connect(
            self.tab_report.window_team_and_site.get_treeView_data_site
        )
        self.model.sig_read_treeView_baseline_segments.connect(
            self.view.get_treeView_data_baseline_building
        )
        self.model.sig_read_treeView_proposed_segments.connect(
            self.view.sig_get_treeView_data_proposed_building
        )
        self.model.sig_read_treeView_bldg_components.connect(
            self.tab_report.window_bldg_components.get_treeView_data_building_components
        )

        # ---------------------------------------------------------------------
        # -- Hook up the [ View ]--Signals->  - - - >-Slots--[ Model ]
        self.view.sig_got_baseline_building_data.connect(
            self.model.set_project_baseline_segments_from_treeView_data
        )
        self.view.sig_got_proposed_building_data.connect(
            self.model.set_project_proposed_segments_from_treeView_data
        )

        # ---------------------------------------------------------------------
        # -- Connect the Tab Buttons and signals
        self.tab_report._connect_buttons_and_signals()
        self.tab_baseline._connect_buttons_and_signals()
        self.logger.debug("Done connecting signals and slots.")

    def _connect_button_loggers(self) -> None:
        """Connect all the QButtons to the click_logger method for debugging."""
        self.logger.debug("Connecting button loggers...")

        for button in self.view.buttons:
            button.clicked.connect(self.click_logger)

        for button in self.tab_baseline.window_baseline_options.buttons:
            button.clicked.connect(self.click_logger)

        for button in self.tab_report.window_team_and_site.buttons:
            button.clicked.connect(self.click_logger)

        for button in self.tab_report.window_bldg_components.buttons:
            button.clicked.connect(self.click_logger)

    def _connect_action_loggers(self) -> None:
        """Connect all the QActions to the click_logger method for debugging."""
        self.logger.debug("Connecting action loggers...")

        for action in self.view.actions:
            action.triggered.connect(self.click_logger)

    # -------------------------------------------------------------------------
    # -- GUI Preview Panel internal methods

    def _startup_preview_panel(self) -> None:
        # -- Setup the Queue for capturing stdout to the GUI's preview panel, as shown in:
        # https://stackoverflow.com/questions/21071448/redirecting-stdout-and-stderr-to-a-pyqt4-qtextedit-from-a-secondary-thread
        # https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file
        self.queue = Queue()
        sys.stdout = WriteStream(self.queue)
        self._configure_worker_threads()

    def _configure_worker_threads(self) -> None:
        """Configure and start up all the worker threads for stdout stream."""
        self._create_workers()
        self._start_worker_threads()
        self._connect_worker_signals()

    def _create_workers(self) -> None:
        self.mutex = qtc.QMutex()
        self.worker_txt_receiver = WorkerReceiveText(self.queue, self.mutex)
        self.worker_txt_receiver_thread = qtc.QThread()

    def _start_worker_threads(self) -> None:
        self.worker_txt_receiver.moveToThread(self.worker_txt_receiver_thread)
        self.worker_txt_receiver_thread.start()

    @qtc.pyqtSlot(str)
    def _append_text(self, text: str) -> None:
        self.view.ui.textEdit_output.moveCursor(qtg.QTextCursor.MoveOperation.End)
        self.view.ui.textEdit_output.insertPlainText(text)

    def _connect_worker_signals(self):
        self.worker_txt_receiver.received_text.connect(self._append_text)
        self.worker_txt_receiver_thread.started.connect(self.worker_txt_receiver.run)

    # -------------------------------------------------------------------------
    # -- Menu methods

    def menu_update(self) -> None:
        """Update the CarbonCheck software. Execute on Menu / Update..."""
        self.logger.debug("Updating the CarbonCheck software.")
        self.model.update_cc_software(self.application_path)

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
        filepath = Path(filepath).resolve()
        self.model.write_json_file(filepath)

    def menu_file_save_as(self) -> None:
        self.logger.debug("Saving the project to a new file.")
        filepath = self.view.get_save_file_path()
        if not filepath:
            self.logger.debug("No file path provided by user.")
            return
        filepath = Path(filepath).resolve()
        self.model.write_json_file(filepath)

    def menu_close(self) -> None:
        """Execute on Menu / File / Close."""
        self.logger.debug("Closing the application.")
        self.view.close()
