# -*- Python Version: 3.11 -*-

"""Thread Workers called by Model and App processes."""

import logging
import pathlib
from queue import Queue
import sys
from typing import Dict, Optional

try:
    import xlwings as xw
except Exception as e:
    raise Exception("Error importing xlwings library?", e)

try:
    from PyQt6 import QtGui as qtg
    from PyQt6 import QtWidgets as qtw
    from PyQt6 import QtCore as qtc
except Exception as e:
    raise Exception("Error importing PyQt6 library?", e)

try:
    from PHX.xl import xl_app
    from PHX.PHPP import phpp_app
    from PHX.PHPP.sheet_io.io_exceptions import PHPPDataMissingException
except Exception as e:
    raise Exception("Error importing PHX library?", e)

try:
    from NBDM.model.project import NBDM_Project
    from NBDM.to_Excel import report
    from NBDM.from_PHPP import (
        create_NBDM_BuildingSegment,
        create_NBDM_Team,
        create_NBDM_Site,
    )
except Exception as e:
    raise Exception("Error importing NBDM library?", e)

try:
    from ph_baseliner.codes.model import BaselineCode
    from ph_baseliner.codes.options import ClimateZones, PF_Groups, Use_Groups
    from ph_baseliner.phpp.areas import set_baseline_envelope_constructions
    from ph_baseliner.phpp.windows import (
        set_baseline_window_construction,
        set_baseline_window_area,
        set_baseline_skylight_area,
    )
    from ph_baseliner.phpp.lighting import set_baseline_lighting_installed_power_density
except Exception as e:
    raise Exception("Error importing ph_baseliner library?", e)


SEPARATOR = "- " * 50


def print_error(_msg: str, _e: Optional[Exception] = None):
    """Print an error message to the console."""
    print("\n")
    print(SEPARATOR)
    print(SEPARATOR)
    print("\n")
    print(_msg)
    if _e:
        print(_e)
    print("\n")
    print(SEPARATOR)
    print(SEPARATOR)
    print("\n")


class WriteStream(object):
    """Storage and redirect for receiving text from a queue."""

    def __init__(self, queue: Queue):
        self.queue = queue
        self.stdout = sys.stdout

    def write(self, text: str):
        self.queue.put(text)
        self.stdout.write(text)

    def flush(self, *args, **kwargs):
        pass


class WorkerReceiveText(qtc.QObject):
    """Thread worker for receiving text from a queue.

    A QObject (to be run in a QThread) which sits waiting for data to come through
    a Queue.Queue(). It blocks until data is available, and once it has got something
    from the queue, it sends it back to the "MainThread" by emitting a QtSignal
    """

    received_text = qtc.pyqtSignal(str)

    def __init__(self, queue: Queue, mutex: qtc.QMutex, *args, **kwargs):
        qtc.QObject.__init__(self, *args, **kwargs)
        self.queue = queue
        self.mutex = mutex

    @qtc.pyqtSlot()
    def run(self):
        """ChatGPT told me to do it this way."""

        while True:
            # Lock the thread before accessing the queue
            with qtc.QMutexLocker(self.mutex):
                if not self.queue.empty():
                    text = self.queue.get()
                    self.received_text.emit(text)

            # ChatGPT says I should do this
            # But I don't think I should...
            # # Check if the thread should exit
            # if self.thread().isInterruptionRequested():
            #     break


class WorkerReadProjectData(qtc.QObject):
    """Thread Worker for loading Project Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)
    logger = logging.getLogger()

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)
        self.logger.excel("Reading Project Team and Site data from Excel.")

        try:
            self.logger.excel(f"Connecting to excel document: {_filepath}")
            xl = xl_app.XLConnection(
                xl_framework=xw, output=self.logger.excel, xl_file_path=_filepath
            )
            phpp_conn = phpp_app.PHPPConnection(xl)
        except Exception as e:
            msg = f"Error connecting to the PHPP: '{_filepath}'"
            print_error(msg, e)
            self.logger.error(msg, e, exc_info=True)
            return None

        with phpp_conn.xl.in_silent_mode():
            _project.team = create_NBDM_Team(phpp_conn)
            _project.site = create_NBDM_Site(phpp_conn)

        self.loaded.emit(_project)


class WorkerReadBaselineSegmentData(qtc.QObject):
    """Thread Worker for loading Baseline Segment Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)
    logger = logging.getLogger()

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)
        self.logger.excel("Reading Baseline Building Segment data from Excel.")
        try:
            self.logger.excel("Connecting to excel...")
            xl = xl_app.XLConnection(
                xl_framework=xw, output=self.logger.excel, xl_file_path=_filepath
            )
            phpp_conn = phpp_app.PHPPConnection(xl)
        except Exception as e:
            msg = f"Error connecting to the PHPP: '{_filepath}'."
            print_error(msg, e)
            self.logger.error(msg, e, exc_info=True)
            return None

        with phpp_conn.xl.in_silent_mode():
            try:
                new_seg = create_NBDM_BuildingSegment(phpp_conn)
            except PHPPDataMissingException as e:
                msg = "Error creating the Baseline Building Segment."
                print_error(msg, e)
                self.logger.error(msg, e, exc_info=True)
                return None

            _project.add_new_baseline_segment(new_seg)

        self.loaded.emit(_project)


class WorkerReadProposedSegmentData(qtc.QObject):
    """Thread Worker for loading Proposed Segment Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)
    logger = logging.getLogger()

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)
        self.logger.excel("Reading Proposed Building Segment data from Excel.")
        try:
            self.logger.excel("Connecting to excel...")
            xl = xl_app.XLConnection(
                xl_framework=xw, output=self.logger.excel, xl_file_path=_filepath
            )
            phpp_conn = phpp_app.PHPPConnection(xl)
        except Exception as e:
            msg = f"Error connecting to the PHPP: '{_filepath}'."
            print_error(msg, e)
            self.logger.error(msg, e, exc_info=True)
            return None

        with phpp_conn.xl.in_silent_mode():
            new_seg = create_NBDM_BuildingSegment(phpp_conn)
            _project.add_new_proposed_segment(new_seg)

        self.loaded.emit(_project)


class WorkerWriteExcelReport(qtc.QObject):
    """Thread Worker for writing out the report to Excel."""

    written = qtc.pyqtSignal(NBDM_Project)
    logger = logging.getLogger()

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _log_path: pathlib.Path) -> None:
        print(SEPARATOR)

        if not self.valid_project(_project):
            self.logger.excel("Project is not valid. Cannot write report.")
            return

        self.logger.info("Writing report data to Excel.")

        try:
            self.logger.info("Connecting to excel...")
            xl = xl_app.XLConnection(xl_framework=xw, output=self.logger.info)
            output_report = report.OutputReport(_xl=xl, _autofit=True, _hide_groups=False)
        except Exception as e:
            msg = f"Error connecting to Excel?"
            print_error(msg, e)
            self.logger.error(msg, e, exc_info=True)
            return None

        with xl.in_silent_mode():
            xl.activate_new_workbook()
            row_num = output_report.write_NBDM_Project(_nbdm_object=_project)
            row_num = output_report.write_NBDM_WholeBuilding(_nbdm_object=_project)
            row_num = output_report.write_NBDM_BuildingSegments(_nbdm_object=_project)
            row_num = output_report.write_log(_log_path)
            output_report.remove_sheet_1()

        self.written.emit(_project)

    def valid_project(self, _project: NBDM_Project) -> bool:
        """Return True if it a valid Project with data that can be written to the report."""
        if not _project.variants.baseline.has_building_segments:
            msg = "Error: 'Baseline' Building Segment data missing. Cannot generate report yet."
            print_error(msg)
            self.logger.error(msg)
            return False

        if not _project.variants.proposed.has_building_segments:
            msg = "Error: 'Proposed' Building Segment data missing. Cannot generate report yet."
            print_error(msg)
            self.logger.error(msg)
            return False

        return True


class WorkerSetPHPPBaseline(qtc.QObject):
    """Thread Worker for setting the Baseline values in PHPP."""

    written = qtc.pyqtSignal()
    logger = logging.getLogger()

    @qtc.pyqtSlot(pathlib.Path, BaselineCode, dict)
    def run(
        self, _filepath: pathlib.Path, _baseline_code: BaselineCode, _options: Dict
    ) -> None:
        """Set the Baseline values in the PHPP.

        Args:
            * _filepath (pathlib.Path): Path to the PHPP file.
            * _baseline_code (BaselineCode): The Baseline Code to use.
            * _options (Dict[str, Any]): Options to use when setting the Baseline values.
        """

        print(SEPARATOR)
        self.logger.info(f"Setting Baseline values on the PHPP: '{_filepath}'.")

        try:
            self.logger.excel("Connecting to excel...")
            xl = xl_app.XLConnection(
                xl_framework=xw, output=self.logger.excel, xl_file_path=_filepath
            )
            phpp_conn = phpp_app.PHPPConnection(xl)
        except Exception as e:
            msg = f"Error connecting to the PHPP: '{_filepath}'."
            print_error(msg, e)
            self.logger.error(msg, e, exc_info=True)
            return None

        # -- Pull out the user-provided options.
        climate_zone = ClimateZones(_options.get("baseline_code_climate_zone", False))
        pf_group = PF_Groups(_options.get("baseline_code_pf_group", False))
        use_group = Use_Groups(_options.get("baseline_code_use_group", False))

        self.logger.excel(f"Using climate-zone: '{climate_zone.value}' for baseline.")
        self.logger.excel(f"Using PF-Group: '{pf_group.value}' for baseline.")
        self.logger.excel(f"Using Use-Group: '{use_group.value}' for baseline.")

        # -- Set the Baseline values in the PHPP
        with phpp_conn.xl.in_silent_mode():
            self.logger.excel("Setting Baseline values...")

            if _options.get("set_envelope_u_values", False):
                self.logger.excel("Setting Baseline opaque envelope U-values.")
                set_baseline_envelope_constructions(
                    phpp_conn, _baseline_code, climate_zone, use_group
                )

            if _options.get("set_window_u_values", False):
                self.logger.excel("Setting Baseline window U-values.")
                set_baseline_window_construction(
                    phpp_conn, _baseline_code, climate_zone, pf_group, use_group
                )

            if _options.get("set_win_areas", False):
                self.logger.excel("Setting Baseline window areas.")
                set_baseline_window_area(phpp_conn, _baseline_code)

            if _options.get("set_skylight_areas", False):
                self.logger.excel("Setting Baseline skylight areas.")
                set_baseline_skylight_area(phpp_conn, _baseline_code)

            if _options.get("set_lighting", False):
                self.logger.excel("Setting Baseline Lighting installed power density.")
                set_baseline_lighting_installed_power_density(phpp_conn, _baseline_code)
