# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Project Data"""

from typing import List


class PDF_BuildingAddress:
    def __init__(self):
        self.building_number: str = "-"
        self.street_name: str = "-"
        self.city: str = "-"
        self.state: str = "-"
        self.post_code: str = "-"


class WufiPDF_ProjectData:
    __pdf_heading_string__ = "Project data"
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self.address = PDF_BuildingAddress()

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        pass
