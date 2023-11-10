# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Heat Flow - Heating Period"""

from typing import List


class WufiPDF_HeatingSeasonHeatFlows:
    __pdf_heading_string__ = "HEAT FLOW - HEATING PERIOD"
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
