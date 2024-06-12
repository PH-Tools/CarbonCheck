# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""PDFReader class for loading and reading WUFI-PDF files."""

import pathlib
from logging import Logger
from typing import Dict, Optional, Type, TypeVar

import pdfplumber

from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.__typing import SupportsWufiPDF_Section
from NBDM.from_WUFI_PDF.pdf_sections._default import _WufiPDF_DefaultSection

T = TypeVar("T", bound=SupportsWufiPDF_Section)


class PDFReader:
    """PDFReader class for loading and reading data from WUFI-PDF files."""

    # -- Store a reference to each of the PDF-Section classes registered with the PDF-Reader
    pdf_section_classes: Dict[str, Type[SupportsWufiPDF_Section]] = {}

    def __init__(self, _logger: Optional[Logger] = None) -> None:
        self.logger = _logger or Logger("PDF_Reader")
        self.logger.info("Initializing PDFReader")

        # -------
        self.pdf_sections = PDFSectionsCollection(self.logger)
        self.setup_pdf_sections()

    def setup_pdf_sections(self) -> PDFSectionsCollection:
        """Create a new PDF-Section-Object for each type that is registered with the PDF-Reader."""
        for section_class in self.pdf_section_classes.values():
            self.pdf_sections.set_section(section_class, section_class())
        return self.pdf_sections

    @classmethod
    def register_pdf_section_class(
        cls, pdf_section_class: Type[SupportsWufiPDF_Section]
    ) -> None:
        """Register a new PDF-Section class as part of the PDF-Reader."""
        cls.pdf_section_classes[pdf_section_class.__pdf_heading_string__] = (
            pdf_section_class
        )

    def load_pdf_file_data(self, _filepath: pathlib.Path) -> None:
        """Populate the .sections with data from a PDF file."""

        self.logger.info(f"Reading in the PDF file: {_filepath}")
        self.logger.info(
            f"Looking for sections: '{[section_name for section_name in list(self.pdf_sections.keys())]}'"
        )

        with pdfplumber.open(_filepath) as pdf:
            # -- Start with the default section
            section = self.pdf_sections[_WufiPDF_DefaultSection.__pdf_heading_string__]

            for page in pdf.pages[0:]:
                self.logger.info(f"Extracting Text from page: {page.page_number}")

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
                        self.logger.info(f"Found PDF Section-Marker: in line '{line}'.")
                        self.logger.info(
                            f"Changing section to {section_marker.__pdf_heading_string__}."
                        )
                        section = section_marker

                    else:
                        # -- otherwise, just add the line to the 'active' section
                        section.add_line(line)

                # -- Try and pull out the tables, if relevant
                if not getattr(section, "get_tables", False):
                    continue

                self.logger.info(f"Extracting Table from page: {page.page_number}")
                for table in page.extract_tables():
                    try:
                        section.add_table(table)
                    except AttributeError:
                        pass

    def extract_pdf_text_from_file(
        self, _filepath: pathlib.Path
    ) -> PDFSectionsCollection:
        """Extract the text from a WUFI-PDF file and return it as a dict of PDFSection objects."""
        self.pdf_sections.__file_name__ = pathlib.Path(_filepath.name).stem
        self.setup_pdf_sections()
        self.load_pdf_file_data(_filepath)
        self.pdf_sections.process_all_sections()
        return self.pdf_sections
