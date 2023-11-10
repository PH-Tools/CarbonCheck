# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Windows"""

from typing import List


class WufiPDF_Windows:
    __pdf_heading_string__ = "WINDOWS"
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self):
        pass
