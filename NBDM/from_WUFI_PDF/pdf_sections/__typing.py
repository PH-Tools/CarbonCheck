# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Base"""

# from abc import ABC, abstractmethod
from typing import List, Protocol


class WufiPDF_SectionType(Protocol):
    """Abstract base class for all PDF Section classes."""

    __pdf_heading_string__: str = ""
    get_tables: bool = False
    _lines: List
    _tables: List

    # def __init__(self) -> None:
    #     self._lines = []
    #     self._tables = []

    # @abstractmethod
    def add_line(self, _line: str) -> None:
        ...

    # @abstractmethod
    def add_table(self, _table: List) -> None:
        ...

    # @abstractmethod
    def process_section_text(self) -> None:
        ...
