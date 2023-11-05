# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Thread Workers called by Model and App processes."""

from enum import Enum
import io
import traceback
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
    # -- PHX-PHPP Modules
    from PHX.xl import xl_app
    from PHX.PHPP import phpp_app
    from PHX.PHPP.sheet_io.io_exceptions import PHPPDataMissingException

    # -- PHX-WUFI Modules
    from PHX.from_WUFI_XML.read_WUFI_XML_file import get_WUFI_XML_file_as_dict
    from PHX.from_WUFI_XML.phx_converter import convert_WUFI_XML_to_PHX_project
    from PHX.to_WUFI_XML import xml_builder, xml_txt_to_file
    from PHX.from_WUFI_XML.wufi_file_schema import WUFIplusProject
except Exception as e:
    raise Exception("Error importing PHX library?", e)

try:
    from NBDM.model.project import NBDM_Project
    from NBDM.to_Excel import report
    from NBDM.from_PHPP import (
        create_NBDM_BuildingSegment,
        create_NBDM_Team,
        create_NBDM_Site,
        create_NBDM_Envelope,
        create_NBDM_Appliances,
        create_NBDM_Cooling_Systems,
        create_NBDM_Heating_Systems,
        create_NBDM_Ventilation_Systems,
        create_NBDM_Renewable_Systems,
        create_NBDM_DHW_Systems,
    )
    from NBDM.from_WUFI_PDF import pdf_reader
    from NBDM.from_WUFI_PDF import (
        create_NBDM_BuildingSegmentFromWufiPDF,
        create_NBDM_Team_from_WufiPDF,
        create_NBDM_Site_from_WufiPDF,
        create_NBDM_Envelope_from_WufiPDF,
        create_NBDM_Appliances_from_WufiPDF,
        create_NBDM_Heating_Systems_from_WufiPDF,
        create_NBDM_Cooling_Systems_from_WufiPDF,
        create_NBDM_Vent_Systems_from_WufiPDF,
        create_NBDM_DHW_Systems_from_WufiPDF,
        create_NBDM_Renewable_Systems_from_WufiPDF,
    )
except Exception as e:
    raise Exception("Error importing NBDM library?", e)

try:
    from ph_baseliner.codes.model import BaselineCode
    from ph_baseliner.codes.options import ClimateZones, PF_Groups, Use_Groups
    from ph_baseliner.phpp import areas as phpp_areas
    from ph_baseliner.phpp import windows as phpp_windows
    from ph_baseliner.phpp import lighting as phpp_lighting
    from ph_baseliner.phx import areas as phx_areas
    from ph_baseliner.phx import windows as phx_windows
    from ph_baseliner.phx import lighting as phx_lighting
except Exception as e:
    raise Exception("Error importing ph_baseliner library?", e)


SEPARATOR = "- " * 50


class SegmentTypename(Enum):
    """Enum for the different types of Building Segments."""

    BASELINE = "Baseline"
    PROPOSED = "Proposed"


def print_error(_msg: str, _e: Optional[Exception] = None):
    """Print an error message to the console."""
    print("\n")
    print(SEPARATOR)
    print(SEPARATOR)
    print("\n")
    print("\t", _msg)
    if _e:
        print("\t", _e)
    print("\n")
    print(SEPARATOR)
    print(SEPARATOR)
    print("\n")


class WriteStream(object):
    """Storage and redirect for receiving text from a queue."""

    def __init__(self, queue: Queue):
        self.queue = queue
        self._stdout = sys.stdout

    def write(self, text: str):
        self.queue.put(text)
        self._stdout.write(text)

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

    def _read_data_from_phpp(
        self, _project: NBDM_Project, _filepath: pathlib.Path
    ) -> Optional[NBDM_Project]:
        self.output = self.logger.excel  # type: ignore
        self.output("Reading Project Team and Site data from Excel.")

        # -- Connect to the PHPP XL Document
        try:
            self.logger.info(f"Connecting to excel document: {_filepath}")
            xl = xl_app.XLConnection(
                xl_framework=xw, output=self.output, xl_file_path=_filepath
            )
            phpp_conn = phpp_app.PHPPConnection(xl)
        except Exception as e:
            msg = f"Error connecting to the PHPP: '{_filepath}'"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        # -- Create new Team and Site objects from the PHPP
        try:
            with phpp_conn.xl.in_silent_mode():
                _project.team = create_NBDM_Team(phpp_conn)
                _project.site = create_NBDM_Site(phpp_conn)
        except Exception as e:
            msg = f"Error creating the Team and Site from file: {_filepath.name}."
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        self.output("Done reading from PHPP.")
        self.loaded.emit(_project)

        return _project

    def _read_data_from_wufi_pdf(
        self, _project: NBDM_Project, _filepath: pathlib.Path
    ) -> Optional[NBDM_Project]:
        self.output = self.logger.wufi  # type: ignore
        self.output(f"Reading Project Team and Site data from file: {_filepath.name}.")

        # -- Read in the WUFI-PDF file
        try:
            self.logger.info(f"Opening WUFI-PDF document: {_filepath}")
            pdf_reader_obj = pdf_reader.PDFReader()
            pdf_data = pdf_reader_obj.extract_pdf_text(_filepath)
        except Exception as e:
            msg = f"Error reading WUFI-PDF file:\n{e}"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        # -- Create the new NBDM team and site objects
        try:
            _project.team = create_NBDM_Team_from_WufiPDF(pdf_data)
            _project.site = create_NBDM_Site_from_WufiPDF(pdf_data)
        except Exception as e:
            msg = f"Error reading the Team and Site from WUFI-PDF file: {_filepath.name}."
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        self.output("Done reading from WUFI-PDF.")
        self.loaded.emit(_project)

        return _project

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)

        if _filepath.suffix.upper() in [".XLSX", ".XLS", ".XLSM"]:
            if project := self._read_data_from_phpp(_project, _filepath):
                self.loaded.emit(project)
        elif _filepath.suffix.upper() == ".PDF":
            if project := self._read_data_from_wufi_pdf(_project, _filepath):
                self.loaded.emit(project)
        else:
            msg = (
                f"Error: The file format '{_filepath.suffix}' is not supported?  "
                "Please select a valid Excel (*.xlsx | *.xls) or WUFI-PDF (*.pdf) file."
            )
            raise Exception(msg)


class _WorkerReadSegmentData(qtc.QObject):
    """Base Thread Worker for loading Segment Data from PHPP or WUFI-Passive."""

    loaded: qtc.pyqtSignal
    logger: logging.Logger
    segment_typename: SegmentTypename

    def _read_data_from_phpp(
        self, _project: NBDM_Project, _filepath: pathlib.Path
    ) -> Optional[NBDM_Project]:
        self.output = self.logger.excel  # type: ignore
        self.output(
            f"Reading Baseline {self.segment_typename.value} Segment data from File: {_filepath}"
        )

        # -- Connect to the PHPP XL Document
        try:
            self.logger.info(f"Connecting to excel document: {_filepath}")
            xl = xl_app.XLConnection(
                xl_framework=xw, output=self.output, xl_file_path=_filepath
            )
            phpp_conn = phpp_app.PHPPConnection(xl)
        except Exception as e:
            msg = f"Error connecting to the PHPP: '{_filepath}'."
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        # -- Create a new NBDM Segment from the PHPP
        with phpp_conn.xl.in_silent_mode():
            try:
                new_seg = create_NBDM_BuildingSegment(phpp_conn)
            except PHPPDataMissingException as e:
                msg = f"Error creating the {self.segment_typename.value} Building Segment from file: {_filepath.name}."
                print_error(msg, e)
                self.logger.error(e, exc_info=True)
                return None

        if self.segment_typename == SegmentTypename.BASELINE:
            _project.add_new_baseline_segment(new_seg)
        elif self.segment_typename == SegmentTypename.PROPOSED:
            _project.add_new_proposed_segment(new_seg)

        self.output(
            f"Done reading from {self.segment_typename.value} Segment File: {_filepath.name}"
        )
        return _project

    def _read_data_from_wufi_pdf(
        self, _project: NBDM_Project, _filepath: pathlib.Path
    ) -> Optional[NBDM_Project]:
        self.output = self.logger.wufi  # type: ignore
        self.output(
            f"Reading {self.segment_typename.value} Building Segment data from File: {_filepath}"
        )

        # -- Read in the WUFI-PDF file
        try:
            self.logger.info(f"Reading WUFI-PDF file: {_filepath}")
            pdf_reader_obj = pdf_reader.PDFReader()
            pdf_data = pdf_reader_obj.extract_pdf_text(_filepath)
        except Exception as e:
            msg = f"Error reading WUFI-PDF file:\n{e}"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        # -- Build a new NBDM Segment from the WUFI-PDF data
        try:
            new_seg = create_NBDM_BuildingSegmentFromWufiPDF(pdf_data)
        except Exception as e:
            msg = f"Error creating the {self.segment_typename.value} Building Segment from WUFI-PDF file: {_filepath.name}."
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        if self.segment_typename == SegmentTypename.BASELINE:
            _project.add_new_baseline_segment(new_seg)
        elif self.segment_typename == SegmentTypename.PROPOSED:
            _project.add_new_proposed_segment(new_seg)

        self.output(f"Done reading Building Segment from file: {_filepath.name}")
        return _project

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)

        if _filepath.suffix.upper() in [".XLSX", ".XLS", ".XLSM"]:
            if project := self._read_data_from_phpp(_project, _filepath):
                self.loaded.emit(project)
        elif _filepath.suffix.upper() == ".PDF":
            if project := self._read_data_from_wufi_pdf(_project, _filepath):
                self.loaded.emit(project)
        else:
            msg = (
                f"Error: The file format '{_filepath.suffix}' is not supported?  "
                "Please select a valid Excel (*.xlsx | *.xls) or WUFI-PDF (*.pdf) file."
            )
            raise Exception(msg)


class WorkerReadBaselineSegmentData(_WorkerReadSegmentData):
    """Thread Worker for loading Baseline Segment Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)
    logger = logging.getLogger()
    segment_typename = SegmentTypename.BASELINE


class WorkerReadProposedSegmentData(_WorkerReadSegmentData):
    """Thread Worker for loading Proposed Segment Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)
    logger = logging.getLogger()
    segment_typename = SegmentTypename.PROPOSED


class WorkerWriteExcelReport(qtc.QObject):
    """Thread Worker for writing out the report to Excel."""

    written = qtc.pyqtSignal(NBDM_Project)
    logger = logging.getLogger()

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

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _log_path: pathlib.Path) -> None:
        print(SEPARATOR)
        self.output = self.logger.excel  # type: ignore

        if not self.valid_project(_project):
            self.output("Project is not valid. Cannot write report.")
            return

        self.output = self.logger.excel  # type: ignore
        self.output("Writing report data to Excel.")

        try:
            self.logger.info("Connecting to excel...")
            xl = xl_app.XLConnection(xl_framework=xw, output=self.logger.info)
            output_report = report.OutputReport(_xl=xl, _autofit=True, _hide_groups=False)
        except Exception as e:
            msg = f"Error connecting to Excel?"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        try:
            with xl.in_silent_mode():
                xl.activate_new_workbook()
                row_num = output_report.write_NBDM_Project(_nbdm_object=_project)
                row_num = output_report.write_NBDM_Building_Components(
                    _nbdm_object=_project
                )
                row_num = output_report.write_NBDM_WholeBuilding(_nbdm_object=_project)
                row_num = output_report.write_NBDM_BuildingSegments(_nbdm_object=_project)
                row_num = output_report.write_log(_log_path)
                output_report.remove_sheet_1()
        except Exception as e:
            msg = f"Error writing to Excel document: {xl.xl_file_path}"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)

        self.output("Done writing to Excel.")
        self.written.emit(_project)


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
        self.output = self.logger.excel  # type: ignore
        self.output(f"Setting Baseline values on the PHPP: '{_filepath}'.")

        # -- Connect to Excel and the Specified PHPP file.
        try:
            self.logger.info(f"Connecting to excel document: {_filepath}")
            xl = xl_app.XLConnection(
                xl_framework=xw, output=self.output, xl_file_path=_filepath
            )
            phpp_conn = phpp_app.PHPPConnection(xl)
        except Exception as e:
            msg = f"Error connecting to the PHPP: '{_filepath}'."
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        # -- Pull out the user-provided options.
        climate_zone = ClimateZones(_options.get("baseline_code_climate_zone", False))
        pf_group = PF_Groups(_options.get("baseline_code_pf_group", False))
        use_group = Use_Groups(_options.get("baseline_code_use_group", False))

        self.output(f"Using climate-zone: '{climate_zone.value}' for baseline.")
        self.output(f"Using PF-Group: '{pf_group.value}' for baseline.")
        self.output(f"Using Use-Group: '{use_group.value}' for baseline.")

        # -- Set the Baseline values in the PHPP
        with phpp_conn.xl.in_silent_mode():
            self.output("Setting Baseline values...")

            if _options.get("set_envelope_u_values", False):
                self.output("Setting Baseline opaque envelope U-values.")
                phpp_areas.set_baseline_envelope_constructions(
                    phpp_conn, _baseline_code, climate_zone, use_group
                )

            if _options.get("set_window_u_values", False):
                self.output("Setting Baseline window U-values.")
                phpp_windows.set_baseline_window_construction(
                    phpp_conn, _baseline_code, climate_zone, pf_group, use_group
                )

            if _options.get("set_win_areas", False):
                self.output("Setting Baseline window areas.")
                phpp_windows.set_baseline_window_area(phpp_conn, _baseline_code)

            if _options.get("set_skylight_areas", False):
                self.output("Setting Baseline skylight areas.")
                phpp_windows.set_baseline_skylight_area(phpp_conn, _baseline_code)

            if _options.get("set_lighting", False):
                self.output("Setting Baseline Lighting installed power density.")
                phpp_lighting.set_baseline_lighting_installed_power_density(
                    phpp_conn, _baseline_code
                )

        self.output("Done setting baseline values in the PHPP.")


class WorkerSetWUFIBaseline(qtc.QObject):
    """Thread Worker for setting the Baseline values in PHPP."""

    written = qtc.pyqtSignal()
    logger = logging.getLogger()

    @qtc.pyqtSlot(pathlib.Path, BaselineCode, dict)
    def run(
        self, _filepath: pathlib.Path, _baseline_code: BaselineCode, _options: Dict
    ) -> None:
        """Set the Baseline values in a WUFI XML file.

        Args:
            * _filepath (pathlib.Path): Path to the WUFI-XML file.
            * _baseline_code (BaselineCode): The Baseline Code to use.
            * _options (Dict[str, Any]): Options to use when setting the Baseline values.
        """
        print(SEPARATOR)
        self.output = self.logger.wufi  # type: ignore
        self.output(f"Setting Baseline values on the WUFI File: '{_filepath}'.")

        # ---------------------------------------------------------------------
        # -- Load the specified WUFI-XML file
        self.output(f"Reading in the WUFI-XML document: {_filepath}")
        wufi_xml_data = get_WUFI_XML_file_as_dict(_filepath)

        self.output(f"Converting WUFI-XML file to a new PHX Model")
        try:
            wufi_xml_model = WUFIplusProject.parse_obj(wufi_xml_data)
            phx_project = convert_WUFI_XML_to_PHX_project(wufi_xml_model)
        except Exception as e:
            msg = (
                "Error: Something went wrong converting the WUFI-XML file to a PHX-Model?"
            )
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        # ---------------------------------------------------------------------
        # -- Pull out the user-provided options.
        climate_zone = ClimateZones(_options.get("baseline_code_climate_zone", False))
        pf_group = PF_Groups(_options.get("baseline_code_pf_group", False))
        use_group = Use_Groups(_options.get("baseline_code_use_group", False))

        self.output(f"Using climate-zone: '{climate_zone.value}' for baseline.")
        self.output(f"Using PF-Group: '{pf_group.value}' for baseline.")
        self.output(f"Using Use-Group: '{use_group.value}' for baseline.")

        # ---------------------------------------------------------------------
        # -- Baseline the PHX Model
        self.output("Setting Baseline values...")

        if _options.get("set_envelope_u_values", False):
            self.output("Setting Baseline opaque envelope U-values.")
            phx_project = phx_areas.set_baseline_envelope_constructions(
                phx_project, _baseline_code, climate_zone, use_group, self.output
            )

        if _options.get("set_window_u_values", False):
            self.output("Setting Baseline window U-values.")
            phx_project = phx_windows.set_baseline_window_construction(
                phx_project,
                _baseline_code,
                climate_zone,
                pf_group,
                use_group,
                self.output,
            )

        if _options.get("set_win_areas", False):
            self.output("Setting Baseline window areas.")
            phx_project = phx_windows.set_baseline_window_area(
                phx_project, _baseline_code, self.output
            )

        if _options.get("set_skylight_areas", False):
            self.output("Setting Baseline skylight areas.")
            phx_project = phx_windows.set_baseline_skylight_area(
                phx_project, _baseline_code, self.output
            )

        if _options.get("set_lighting", False):
            self.output("Setting Baseline Lighting installed power density.")
            phx_project = phx_lighting.set_baseline_lighting_installed_power_density(
                phx_project, _baseline_code, self.output
            )

        self.output("Done setting baseline values in the WUFI Model.")

        # ---------------------------------------------------------------------
        # -- Output the XMl model back to the original file location
        try:
            xml_txt = xml_builder.generate_WUFI_XML_from_object(phx_project)
        except Exception as e:
            msg = "Error: Something went wrong trying to generate the XML file from PHX-Project?"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        output_filepath = pathlib.Path(_filepath.parent, f"{_filepath.stem}_baseline.xml")
        self.output(f"Saving the XML file to: '{output_filepath}'")
        try:
            xml_txt_to_file.write_XML_text_file(output_filepath, xml_txt, False)
        except Exception as e:
            msg = f"Error writing the XML file to: '{output_filepath}'"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        self.output("Done writing the new WUFI Baseline file.")


class WorkerReadBldgComponentData(qtc.QObject):
    """Thread Worker for loading Building Component Data from PHPP."""

    loaded = qtc.pyqtSignal(NBDM_Project)
    logger = logging.getLogger()

    def _read_data_from_phpp(
        self, _project: NBDM_Project, _filepath: pathlib.Path
    ) -> Optional[NBDM_Project]:
        self.output = self.logger.excel  # type: ignore
        self.output("Reading Building Component data from Excel.")

        try:
            self.logger.info(f"Connecting to excel document: {_filepath}")
            xl = xl_app.XLConnection(
                xl_framework=xw, output=self.output, xl_file_path=_filepath
            )
            phpp_conn = phpp_app.PHPPConnection(xl)
        except Exception as e:
            msg = f"Error connecting to the PHPP: '{_filepath}'"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        # -- Read in the data from PHPP
        try:
            with phpp_conn.xl.in_silent_mode():
                _project.envelope = create_NBDM_Envelope(phpp_conn)
                _project.appliances = create_NBDM_Appliances(phpp_conn)
                _project.heating_systems = create_NBDM_Heating_Systems(phpp_conn)
                _project.cooling_systems = create_NBDM_Cooling_Systems(phpp_conn)
                _project.ventilation_systems = create_NBDM_Ventilation_Systems(phpp_conn)
                _project.dhw_systems = create_NBDM_DHW_Systems(phpp_conn)
                _project.renewable_systems = create_NBDM_Renewable_Systems(phpp_conn)
        except Exception as e:
            msg = (
                f"Error creating the Building Component data from file: {_filepath.name}."
            )
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        self.output("Done reading from PHPP.")
        self.loaded.emit(_project)

        return _project

    def _read_data_from_wufi_pdf(
        self, _project: NBDM_Project, _filepath: pathlib.Path
    ) -> Optional[NBDM_Project]:
        self.output = self.logger.excel  # type: ignore
        self.output("Reading Building Component data from WUFI-PDF.")

        # -- Read in the WUFI-PDF file
        try:
            self.logger.info(f"Opening WUFI-PDF document: {_filepath}")
            pdf_reader_obj = pdf_reader.PDFReader()
            pdf_data = pdf_reader_obj.extract_pdf_text(_filepath)
        except Exception as e:
            msg = f"Error reading WUFI-PDF file:\n{e}"
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        # -- Create the new NBDM team and site objects from the WUFI-File
        try:
            _project.envelope = create_NBDM_Envelope_from_WufiPDF(pdf_data)
            _project.appliances = create_NBDM_Appliances_from_WufiPDF(pdf_data)
            _project.heating_systems = create_NBDM_Heating_Systems_from_WufiPDF(pdf_data)
            _project.cooling_systems = create_NBDM_Cooling_Systems_from_WufiPDF(pdf_data)
            _project.ventilation_systems = create_NBDM_Vent_Systems_from_WufiPDF(pdf_data)
            _project.dhw_systems = create_NBDM_DHW_Systems_from_WufiPDF(pdf_data)
            _project.renewable_systems = create_NBDM_Renewable_Systems_from_WufiPDF(
                pdf_data
            )
        except Exception as e:
            msg = (
                f"Error creating the Building Component data from file: {_filepath.name}."
            )
            print_error(msg, e)
            self.logger.error(e, exc_info=True)
            return None

        self.output("Done reading from WUFI-PDF.")
        self.loaded.emit(_project)

        return _project

    @qtc.pyqtSlot(NBDM_Project, pathlib.Path)
    def run(self, _project: NBDM_Project, _filepath: pathlib.Path) -> None:
        print(SEPARATOR)
        if _filepath.suffix.upper() in [".XLSX", ".XLS", ".XLSM"]:
            if project := self._read_data_from_phpp(_project, _filepath):
                self.loaded.emit(project)
        elif _filepath.suffix.upper() == ".PDF":
            if project := self._read_data_from_wufi_pdf(_project, _filepath):
                self.loaded.emit(project)
        else:
            msg = (
                f"Error: The file format '{_filepath.suffix}' is not supported?  "
                "Please select a valid Excel (*.xlsx | *.xls) or WUFI-PDF (*.pdf) file."
            )
            raise Exception(msg)
