# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Zones / Components"""

from typing import List


class WufiPDF_ZonesAndComponents:
    __pdf_heading_string__ = "Zones / Components"
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        pass
