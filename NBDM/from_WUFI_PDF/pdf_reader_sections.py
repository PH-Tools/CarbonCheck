# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Wrapper Class to organize the PDF Sections."""

from logging import Logger
from typing import (
    Any,
    Dict,
    ItemsView,
    Iterator,
    KeysView,
    Optional,
    Type,
    TypeVar,
    ValuesView,
)

from NBDM.from_WUFI_PDF.pdf_sections.__typing import SupportsWufiPDF_Section

T = TypeVar("T", bound=SupportsWufiPDF_Section)


class PDFSectionsCollection:
    """A Wrapper Class to organize the PDF Sections."""

    __file_name__: str = "_unnamed_pdf_document_"

    def __init__(self, _logger: Optional[Logger] = None) -> None:
        self._d: Dict[str, SupportsWufiPDF_Section] = {}
        self.logger = _logger or Logger("PDF_Sections_Collection")

    def get_section(self, _section_class_type: Type[T]) -> Optional[T]:
        """Return the PDF-Section of the given type, or None if not found."""
        try:
            return self._d[_section_class_type.__pdf_heading_string__]
        except KeyError:
            return None

    def set_section(self, _section_class_type: Type[T], _section_object: T) -> None:
        """Add a new PDF-Section to the collection."""
        self._d[_section_class_type.__pdf_heading_string__] = _section_object

    def __getitem__(self, _section_class_type_name: str) -> SupportsWufiPDF_Section:
        return self._d[_section_class_type_name]

    def __setitem__(
        self, _section_class_type_name: str, _section: SupportsWufiPDF_Section
    ) -> None:
        self._d[_section_class_type_name] = _section

    def __contains__(self, _section_class_type: SupportsWufiPDF_Section) -> bool:
        return _section_class_type.__pdf_heading_string__ in self._d

    def __iter__(self) -> Iterator[str]:
        return iter(self._d)

    def __len__(self) -> int:
        return len(self._d)

    def keys(self) -> KeysView[str]:
        return self._d.keys()

    def values(self) -> ValuesView[SupportsWufiPDF_Section]:
        return self._d.values()

    def items(self) -> ItemsView[str, SupportsWufiPDF_Section]:
        return self._d.items()

    def get(self, _key: str, _default: Any = None) -> Optional[SupportsWufiPDF_Section]:
        return self._d.get(_key, _default)

    def __repr__(self) -> str:
        return f"PDFSectionsCollection({self._d})"

    def process_all_sections(self) -> None:
        """Walk through all the PDF-Sections and process the raw data which was read from the PDF-file"""
        for pdf_section in self.values():
            self.logger.info(
                f"Processing Text from the PDF Section: {pdf_section.__pdf_heading_string__}"
            )
            pdf_section.process_section_text()
