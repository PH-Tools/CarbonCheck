# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Site Energy [Monthly]"""


import math
from typing import List, Union

from ph_units.unit_type import Unit


class SiteEnergyMonthlyTableRow:
    """A single row of data from the Site-Energy-Monthly table"""

    month_codes = [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
    ]

    def __init__(self):
        for month_code in self.month_codes:
            setattr(self, month_code, 0.0)

    @property
    def data(self) -> List[float]:
        """Return a list of the data in month-order."""
        return [getattr(self, n) for n in self.month_codes]

    @property
    def total(self) -> float:
        """Return the total of all the row's data."""
        if all(isinstance(d, (int, float)) for d in self.data):
            return sum(self.data)
        else:
            return 0.0

    def get_month_name(self, i: int) -> str:
        """Return the month-name (code) by its number (0-based)."""
        try:
            return self.month_codes[i]
        except IndexError as e:
            msg = f"Error: I do not know how to find month number: '{i}' ?"
            raise IndexError(msg, e)

    def clean_input_data(self, _data: str) -> Union[str, float]:
        """Process the PDF data items, remove commas and new-lines."""
        try:
            val = float(_data.strip().replace("\n", "").replace(",", ""))
            # -- WUFI will sometimes report "NaN" if there are errors. This gets
            # -- interpreted by 'float()' as a 'nan' value?! What in the absolute fuck
            # -- python.... thats some javascript style bullshit right there.
            if math.isnan(val):
                return 0.0
            else:
                return val
        except ValueError:
            return _data

    def process_pdf_table_row_data(self, _pdf_row_data: List[str]) -> None:
        """Clean and organize all PDF input data."""
        row_data = _pdf_row_data[1:]
        for i, data_item in enumerate(row_data):
            month_name = self.get_month_name(i)
            setattr(self, month_name, self.clean_input_data(data_item))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(data={self.data})"


class SiteEnergyMonthlyTable:
    """A Table of Data"""

    def __init__(self) -> None:
        self.space_heating = SiteEnergyMonthlyTableRow()
        self.space_cooling = SiteEnergyMonthlyTableRow()
        self.hot_water = SiteEnergyMonthlyTableRow()
        self.auxiliary_energy_fans = SiteEnergyMonthlyTableRow()
        self.large_appliances = SiteEnergyMonthlyTableRow()
        self.lighting = SiteEnergyMonthlyTableRow()
        self.miscellaneous_loads = SiteEnergyMonthlyTableRow()
        self.renewable_electricity_production = SiteEnergyMonthlyTableRow()

    def get_row_data_type_name(self, _row_data: List[str]) -> str:
        """Return the name of the row-type based on the first item in the row-data input."""
        return str(_row_data[0]).strip().replace(" ", "_").replace("/", "_").lower()

    def process_pdf_table_data(self, _pdf_data: List[List[str]]) -> None:
        """Clean and organize all of the PDF table data found"""

        for row_data in _pdf_data:
            # -- Find the right row to add the data to
            row_type = self.get_row_data_type_name(row_data)
            if not (row := getattr(self, row_type, None)):
                continue
            row.process_pdf_table_row_data(row_data)

    @property
    def consumption_rows(self) -> List[SiteEnergyMonthlyTableRow]:
        """Return a list of the rows with energy consumption data"""
        return [
            v
            for k, v in self.__dict__.items()
            if (k != "renewable_electricity_production" and not k.startswith("_"))
        ]

    @property
    def production_rows(self) -> List[SiteEnergyMonthlyTableRow]:
        """Return a list of the rows with energy production data"""
        return [
            v for k, v in self.__dict__.items() if k == "renewable_electricity_production"
        ]

    @property
    def total_consumption_kwh(self) -> Unit:
        """Return the total energy consumption (KWH)"""
        return Unit(sum(row.total for row in self.consumption_rows), "KWH")

    @property
    def total_consumption_kbtu(self) -> Unit:
        """Return the total energy consumption (KBTU)"""
        return self.total_consumption_kwh.as_a("KBTU")

    @property
    def total_production_kwh(self) -> Unit:
        """Return the total energy production (KWH)"""
        return Unit(sum(row.total for row in self.production_rows), "KWH")

    @property
    def total_production_kbtu(self) -> Unit:
        """Return the total energy production (KBTU)"""
        return self.total_production_kwh.as_a("KBTU")


class WufiPDF_SiteEnergyMonthly:
    __pdf_heading_string__ = "SITE ENERGY MONTHLY REPORT"
    get_tables = True

    def __init__(self) -> None:
        self._lines = []
        self._tables: List[List[List[str]]] = []
        self.table_electricity_kwh = SiteEnergyMonthlyTable()
        self.table_gas_kwh = SiteEnergyMonthlyTable()

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List[List[str]]) -> None:
        """Add a new table-data list to the list of tables."""
        self._tables.append(_table)

    def process_section_text(self) -> None:
        """Clean and organize all of the PDF data found."""
        try:
            self.table_electricity_kwh.process_pdf_table_data(self._tables[0])
            self.table_gas_kwh.process_pdf_table_data(self._tables[1])
        except IndexError as e:
            msg = "Error: Missing Site-Energy-Monthly Table?"
            raise IndexError(msg, e)

    @property
    def consumption_gas(self) -> Unit:
        """Return the total energy consumption (KBTU)"""
        return self.table_gas_kwh.total_consumption_kbtu

    @property
    def consumption_electricity(self) -> Unit:
        """Return the total energy consumption (KBTU)"""
        return self.table_electricity_kwh.total_consumption_kbtu

    @property
    def consumption_district_heat(self) -> Unit:
        """Return 0.0"""
        return Unit(0.0, "KBTU")

    @property
    def consumption_other(self) -> Unit:
        """Return 0.0"""
        return Unit(0.0, "KBTU")

    @property
    def production_solar_photovoltaic(self) -> Unit:
        """Return the total energy production (KBTU)"""
        return self.table_electricity_kwh.total_production_kbtu

    @property
    def production_solar_thermal(self) -> Unit:
        """Return 0.0"""
        return Unit(0.0, "KBTU")

    @property
    def production_other(self) -> Unit:
        """Return 0.0"""
        return Unit(0.0, "KBTU")
