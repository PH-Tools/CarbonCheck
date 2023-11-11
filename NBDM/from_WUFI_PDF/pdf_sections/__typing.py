# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Base"""

# from abc import ABC, abstractmethod
from typing import List, Protocol


class SupportsWufiPDF_Section(Protocol):
    """Protocol for all PDF Section classes."""

    __pdf_heading_string__: str = ""
    get_tables: bool = False
    _lines: List
    _tables: List

    def add_line(self, _line: str) -> None:
        ...

    def add_table(self, _table: List) -> None:
        ...

    def process_section_text(self) -> None:
        ...
