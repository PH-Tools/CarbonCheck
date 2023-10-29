# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Building Information"""

from typing import Any, List
from ph_units.unit_type import Unit
from ph_units.parser import parse_input
from ph_units.converter import _standardize_unit_name, unit_type_alias_dict
from ph_units.converter import UnitTypeNameNotFound


class WufiPDF_BuildingInformation:
    __pdf_heading_string__ = "BUILDING INFORMATION"
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self.category = ""
        self.units = 0
        self.number_of_occupants = 0.0
        self.total_area_envelope = Unit(0.0, "FT2")
        self.floor_area = Unit(0.0, "FT2")
        self.enclosed_volume = Unit(0.0, "FT3")

    def add_line(self, _line: str) -> None:
        """Add a line of text to the section."""
        line = _line.split(":")
        self._lines.append(line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if not isinstance(__value, str):
            return super().__setattr__(__name, __value)

        # -- Try and pull out any unit part of the string
        val, unit = parse_input(__value)
        if not unit:
            return super().__setattr__(__name, __value)

        try:
            unit = _standardize_unit_name(unit, unit_type_alias_dict)
            return super().__setattr__(__name, Unit(val, unit))
        except UnitTypeNameNotFound:
            return super().__setattr__(__name, __value)

    def process_section_text(self) -> None:
        """Sort through the input text and pull out the relevant values."""

        for line in self._lines:
            line_category_name = line[0].strip().replace(" ", "_").lower()

            if len(line) == 1:
                continue

            if line_category_name == "climate":
                # -- odd line = ['Climate', ' User defined Enclosed volume', ' 50,853.1 ft³']
                setattr(self, "enclosed_volume", line[-1].strip())
            elif line_category_name == "overheat_temperature":
                # -- odd line = ['Overheat temperature', ' 77 °F Envelope area/iCFA', ' 1.6']
                val = line[1].strip().split("Envelope area")[0]
                setattr(self, "overheat_temperature", val)
            elif line_category_name == "number_of_occupants":
                # -- weird note = ['Number of occupants', ' 15 (Design)'],
                val = line[-1].strip().split(" ")[0]
                setattr(self, "number_of_occupants", val)
            else:
                setattr(self, line_category_name, line[1].strip())
