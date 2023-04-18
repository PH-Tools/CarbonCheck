# -*- Python Version: 3.10 -*-

"""Thread Workers called by Model and App processes."""

import pathlib
from queue import Queue
import xlwings as xw

from PyQt6 import QtGui as qtg
from PyQt6 import QtWidgets as qtw
from PyQt6 import QtCore as qtc

from PHX.xl import xl_app
from PHX.PHPP import phpp_app

from NBDM.model.project import NBDM_Project
from NBDM.to_Excel import report
from NBDM.from_PHPP import create_NBDM_BuildingSegment, create_NBDM_Team, create_NBDM_Site

SEPARATOR = "- " * 50

class WriteStream(object):
    """Storage and redirect for receiving text from a queue."""

    def __init__(self, queue: Queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

    def flush(self, *args, **kwargs):
        pass

class WorkerReceiveText(qtc.QObject):
    """Thread worker for receiving text from a queue.
    
    A QObject (to be run in a QThread) which sits waiting for data to come through 
    a Queue.Queue().nIt blocks until data is available, and one it has got something
    from the queue, it sends it to the "MainThread" by emitting a Qt Signal 
    """
    
    received_text = qtc.pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        qtc.QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @qtc.pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.received_text.emit(text)


class WorkerReadProjectData(qtc.QObject):
    """Thread Worker for loading Project Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)
        print("Reading Project Team and Site data from Excel.")
        print("Connecting to excel...")
        xl = xl_app.XLConnection(xl_framework=xw, output=print, xl_file_path=_filepath)
        phpp_conn = phpp_app.PHPPConnection(xl)

        with phpp_conn.xl.in_silent_mode():
            _project.team = create_NBDM_Team(phpp_conn)
            _project.site = create_NBDM_Site(phpp_conn)

        self.loaded.emit(_project)


class WorkerReadBaselineSegmentData(qtc.QObject):
    """Thread Worker for loading Baseline Segment Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)
        print("Reading Baseline Building Segment data from Excel.")
        print("Connecting to excel...")
        xl = xl_app.XLConnection(xl_framework=xw, output=print, xl_file_path=_filepath)
        phpp_conn = phpp_app.PHPPConnection(xl)

        with phpp_conn.xl.in_silent_mode():
            new_seg = create_NBDM_BuildingSegment(phpp_conn)
            _project.add_new_baseline_segment(new_seg)

        self.loaded.emit(_project)


class WorkerReadProposedSegmentData(qtc.QObject):
    """Thread Worker for loading Proposed Segment Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)
        print("Reading Proposed Building Segment data from Excel.")
        print("Connecting to excel...")
        xl = xl_app.XLConnection(xl_framework=xw, output=print, xl_file_path=_filepath)
        phpp_conn = phpp_app.PHPPConnection(xl)

        with phpp_conn.xl.in_silent_mode():
            new_seg = create_NBDM_BuildingSegment(phpp_conn)
            _project.add_new_proposed_segment(new_seg)

        self.loaded.emit(_project)


class WorkerWriteExcelReport(qtc.QObject):
    """Thread Worker for writing out the report to Excel."""

    written = qtc.pyqtSignal(NBDM_Project)

    @qtc.pyqtSlot(NBDM_Project)
    def run(self, _project: NBDM_Project) -> None:
        if not self.valid_project(_project):
            return 
        
        print(SEPARATOR)
        print("Writing report data to Excel.")
        print("Connecting to excel...")
        xl = xl_app.XLConnection(xl_framework=xw, output=print)
        output_report = report.OutputReport(_xl=xl, _autofit=True, _hide_groups=False)

        with xl.in_silent_mode():
            xl.activate_new_workbook()
            row_num = output_report.write_NBDM_Project(_nbdm_object=_project)
            row_num = output_report.write_NBDM_WholeBuilding(_nbdm_object=_project)
            row_num = output_report.write_NBDM_BuildingSegments(_nbdm_object=_project)
            output_report.remove_sheet_1()

        self.written.emit(_project)
    
    def valid_project(self, _project: NBDM_Project) -> bool:
        """Return True if it a valid Project with data that can be written to the report."""
        if not _project.variants.baseline.has_building_segments:
            print("\n")
            print(SEPARATOR)
            print("Error: 'Baseline' Building Segment data missing. Cannot generate report yet.")
            print(SEPARATOR)
            print("\n")
            return False

        if not _project.variants.proposed.has_building_segments:
            print("\n")
            print(SEPARATOR)
            print("Error: 'Proposed' Building Segment data missing. Cannot generate report yet.")
            print(SEPARATOR)
            print("\n")
            return False
        
        return True