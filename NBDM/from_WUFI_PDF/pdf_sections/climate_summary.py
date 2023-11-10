# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Climate-Summary"""

from typing import List
from ph_units.unit_type import Unit
from rich import print


class WufiPDF_ClimateSummary:
    __pdf_heading_string__ = "CLIMATE"  # Note: upper case, not lower
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self.longitude = 0.0
        self.latitude = 0.0

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        """lines =[
        Latitude: 40.7 ° Ground
        Longitude: -73.8 ° Average ground surface temperature: 56.2 °F
        Elevation of weather station: 16.4 ft Amplitude ground surface temperature: 54.7 °F
        Elevation of building site: 16.4 ft Ground thermal conductivity: 1.2 Btu/hr ft °F
        Heat capacity air: 0.018 Btu/ft³F Ground heat capacity: 29.8 Btu/ft³F
        Daily temperature swing summer: 14.4 °F Depth below grade of groundwater: 9.8 ft
        Average wind speed: 13.1 ft/s Flow rate groundwater: 0.2 ft/d
        ...
        ]
        """

        for line in self._lines:
            line_parts = line.split(":")

            # -- Pull out the data
            if "Latitude" in line:
                attribute_name = "latitude"
                value = line_parts[1].strip().split(" ", 1)[0]
            elif "Longitude" in line:
                attribute_name = "longitude"
                value = line_parts[1].strip().split(" ", 1)[0]
            else:
                attribute_name, value = None, None

            # -- Set the attribute
            if attribute_name and value:
                try:
                    setattr(self, attribute_name, float(value))
                except ValueError:
                    msg = f"Could not convert '{attribute_name}' value of: {value} to a number?"
                    raise ValueError(msg)
