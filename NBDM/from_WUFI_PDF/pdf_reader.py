# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""PDFReader class for loading and reading WUFI-PDF files."""

import importlib.util
from importlib.machinery import SourceFileLoader
import inspect
import pathlib
from typing import Optional, Dict

import pdfplumber

from NBDM.from_WUFI_PDF.pdf_sections._default import _DefaultSection
from NBDM.from_WUFI_PDF.pdf_sections.typing import PDFSectionType


class PDFReader:
    base_path = pathlib.Path(
        "/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/NBDM/from_WUFI_PDF/pdf_sections"
    )

    def __init__(self) -> None:
        self.pdf_sections: Dict[str, PDFSectionType] = self.import_pdf_section_classes()

    def import_pdf_section_classes(self) -> Dict[str, PDFSectionType]:
        """Import all the PDF Section classes and return them as a single Dict.

        The dict key will be the '__pdf_heading_string__' attribute of the class.
        """

        classes: Dict[str, PDFSectionType] = {}
        for py_file in self.base_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue

            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            if not spec:
                continue

            module = importlib.util.module_from_spec(spec)
            loader: Optional[SourceFileLoader]
            if loader := getattr(spec, "loader", None):
                loader.exec_module(module)
            else:
                continue

            for name, obj in inspect.getmembers(module):
                if hasattr(obj, "__pdf_heading_string__"):
                    PDFSectionType.register(type(obj))
                    classes[obj.__pdf_heading_string__] = obj()

        return classes

    def load_pdf_file_data(self, _filepath: pathlib.Path) -> None:
        """Populate the .sections with data from a PDF file."""

        with pdfplumber.open(_filepath) as pdf:
            # -- Start with the default section
            section = self.pdf_sections[_DefaultSection.__pdf_heading_string__]

            for page in pdf.pages[0:]:
                lines = page.extract_text(
                    x_tolerance=3,
                    y_tolerance=3,
                    layout=False,
                    x_density=7.25,
                    y_density=13,
                )

                for line in lines.split("\n"):
                    # -- See if the line is one of the 'Section-Markers'
                    # -- like "BUILDING INFORMATION", etc...
                    if section_marker := self.pdf_sections.get(line, None):
                        # -- If it is, make that section the 'active' one
                        section = section_marker
                    else:
                        # -- otherwise, just add the line to the 'active' section
                        section.add_line(line)

    def extract_pdf_text(self, _filepath: pathlib.Path) -> Dict[str, PDFSectionType]:
        """Extract the text from a WUFI-PDF file and return it as a dict of PDFSection objects."""
        self.load_pdf_file_data(_filepath)
        for pdf_section in self.pdf_sections.values():
            pdf_section.process_section_text()

        return self.pdf_sections
