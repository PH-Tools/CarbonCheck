# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Annual Heating / Cooling Demand"""

from typing import Any, List, Optional

from ph_units.converter import (
    UnitTypeNameNotFound,
    _standardize_unit_name,
    unit_type_alias_dict,
)
from ph_units.parser import parse_input
from ph_units.unit_type import Unit


class AnnualDemand:
    def __init__(self, _name: str) -> None:
        self.name = _name
        self._lines = []
        self.transmission_losses = Unit(0.0, "KBTU")
        self.ventilation_losses = Unit(0.0, "KBTU")
        self.total_heat_losses = Unit(0.0, "KBTU")
        self.solar_heat_gains = Unit(0.0, "KBTU")
        self.internal_heat_gains = Unit(0.0, "KBTU")
        self.total_heat_gains = Unit(0.0, "KBTU")
        self.useful_heat_gains = Unit(0.0, "KBTU")
        self.utilization_factor = Unit(0.0, "%")
        self.annual_heat_demand = Unit(0.0, "KBTU")
        self.specific_annual_heat_demand = Unit(0.0, "KBTU/FTU")
        self.annual_cooling_demand = Unit(0.0, "KBTU")
        self.cooling_demand_sensible = Unit(0.0, "KBTU")
        self.cooling_demand_latent = Unit(0.0, "KBTU")

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def __setattr__(self, __name: Optional[str], __value: Any) -> None:
        if __name == None:
            return

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

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({vars(self).items()})"


class WufiPDF_AnnualHeatingAndCoolingDemand:
    __pdf_heading_string__ = "ANNUAL HEAT DEMAND ANNUAL COOLING DEMAND"
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self.heating_demand = AnnualDemand("heating_demand")
        self.cooling_demand = AnnualDemand("cooling_demand")

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        """
        Transmission losses : 169,662 kBtu/yr Solar heat gains: 111,236 kBtu/yr
        Ventilation losses: 1,948,921 kBtu/yr Internal heat gains: 116,982 kBtu/yr
        Total heat losses: 2,118,583 kBtu/yr Total heat gains: 228,218 kBtu/yr
        Solar heat gains: 75,879 kBtu/yr Transmission losses : 282,365 kBtu/yr
        Internal heat gains: 87,496 kBtu/yr Ventilation losses: 2,870,785 kBtu/yr
        Total heat gains: 163,375 kBtu/yr Total heat losses: 3,153,150 kBtu/yr
        Utilization factor: 88.1 % Utilization factor: 6 %
        Useful heat gains: 143,865 kBtu/yr Useful heat losses: 189,427 kBtu/yr
        Annual heat demand: 1,974,718 kBtu/yr Cooling demand - sensible: 38,791 kBtu/yr
        Specific annual heat demand: 382,240.3 Btu/ft²yr Cooling demand - latent: 168,414 kBtu/yr
        Annual cooling demand: 207,205 kBtu/yr
        Specific annual cooling demand: 40.1 kBtu/ft²yr
        ....
        """
        for line in self._lines:
            line = line.split(":")
            if len(line) < 2:
                continue

            htg_attr_name = line[0].lower().strip().replace(" ", "_")
            # -- Handle all the weird lines...
            if htg_attr_name == "annual_heat_demand":
                # line = ["Annual heat demand", "1,974,718 kBtu/yr Cooling demand - sensible", "38,791 kBtu/yr"]
                middle_string, clg_attr_value = line[1:]
                clg_attr_value = clg_attr_value.replace("/yr", "").strip()
                htg_attr_value, clg_attr_name = middle_string.split("/yr ")
                clg_attr_name = (
                    clg_attr_name.replace(" - ", "_").replace(" ", "_").strip().lower()
                )
            elif htg_attr_name == "specific_annual_heat_demand":
                # line = ["Specific annual heat demand", "382,240.3 Btu/ft²yr Cooling demand - latent", ""168,414 kBtu/yr"]
                middle_string, clg_attr_value = line[1:]
                clg_attr_value = clg_attr_value.replace("/yr", "").strip()
                htg_attr_value, clg_attr_name = middle_string.split("yr ")
                clg_attr_name = (
                    clg_attr_name.replace(" - ", "_").replace(" ", "_").strip().lower()
                )
                htg_attr_name = None
                htg_attr_value = None
            elif htg_attr_name == "annual_cooling_demand":
                # line = ["Annual cooling demand", "207,205 kBtu/yr"]
                clg_attr_name, clg_attr_value = line
                clg_attr_name = (
                    clg_attr_name.replace(" - ", "_").replace(" ", "_").strip().lower()
                )
                clg_attr_value = clg_attr_value.replace("/yr", "").strip()
                htg_attr_name = None
                htg_attr_value = None
            elif htg_attr_name == "utilization_factor":
                htg_attr_value, clg_attr_name = line[1].strip().split(" % ")
                htg_attr_value = float(htg_attr_value) / 100
                clg_attr_value = line[-1].strip()
            elif htg_attr_name not in self.heating_demand.__dict__:
                # -- Ignore anything that isn't one of the object's attributes.
                continue
            else:
                # -- Handle all the 'normal' lines
                htg_attr_value, clg_attr_name = line[1].strip().split("/yr ")
                clg_attr_name = clg_attr_name.lower().strip().replace(" ", "_")
                clg_attr_value = line[-1].strip()
                clg_attr_value = clg_attr_value.replace("/yr", "").strip()

            self.heating_demand.__setattr__(htg_attr_name, htg_attr_value)
            self.cooling_demand.__setattr__(clg_attr_name, clg_attr_value)
