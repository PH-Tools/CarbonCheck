# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Property / Site"""

from typing import List


class WufiPDF_PropertySite:
    __pdf_heading_string__ = "Property/Site"
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self.zone_passive_house = ""
        self.data_set = ""

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        """lines = [
        Building name: An Example Building
        Property information
        Owner's name: An Example Owner
        Property address: Building Street
        City: Building City
        Zip: 10001
        Site information
        Climate Location: User defined
        ]
        """

        self.zone_passive_house = "N/A"  # Phius doesn't use this

        for line in self._lines:
            line_parts = line.split(":")
            if "Climate Location" in line_parts[0]:
                attribute_name = "data_set"
                value = line_parts[1].strip()
                setattr(self, attribute_name, value)
