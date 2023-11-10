# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Peak Heating and Cooling Load"""


from typing import Any, Optional, List
from ph_units.unit_type import Unit
from ph_units.parser import parse_input
from ph_units.converter import _standardize_unit_name, unit_type_alias_dict
from ph_units.converter import UnitTypeNameNotFound


class PeakLoad:
    def __init__(self, _name: str) -> None:
        self.name = _name
        self._lines = []
        self.transmission_heat_losses = Unit(0.0, "BTUH")
        self.ventilation_heat_losses = Unit(0.0, "BTUH")
        self.total_heat_loss = Unit(0.0, "BTUH")
        self.solar_heat_gain = Unit(0.0, "BTUH")
        self.internal_heat_gain = Unit(0.0, "BTUH")
        self.total_heat_gains_heating = Unit(0.0, "BTUH")
        self.total_heat_gains_cooling = Unit(0.0, "BTUH")
        self.heating_load = Unit(0.0, "BTUH")
        self.cooling_load_sensible = Unit(0.0, "BTUH")
        self.cooling_load_latent = Unit(0.0, "BTUH")
        self.cooling_load = Unit(0.0, "BTUH")

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

    @property
    def total_cooling_load(self) -> Unit:
        return self.cooling_load_sensible + self.cooling_load_latent

    def __eq__(self, other: "PeakLoad") -> bool:
        for attr in self.__dict__:
            if attr.startswith("_"):
                continue

            if getattr(self, attr) != getattr(other, attr):
                return False

        return True

    def __lt__(self, other: "PeakLoad") -> bool:
        if self.heating_load < other.heating_load:
            return True

        if self.total_cooling_load < other.total_cooling_load:
            return True

        return False


class WufiPDF_PeakHeatingAndCoolingLoad:
    __pdf_heading_string__ = "HEATING LOAD COOLING LOAD"
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self.heating_load_1 = PeakLoad("heating_load_1")
        self.heating_load_2 = PeakLoad("heating_load_2")
        self.cooling_load = PeakLoad("cooling_load")

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        """
        Transmission heat losses: 58,327.2 Btu/hr 37,455 Btu/hr Solar heat gain: 15,409.9 Btu/hr
        Ventilation heat losses: 705,303.5 Btu/hr 417,370.6 Btu/hr Internal heat gain: 13,355.4 Btu/hr
        Total heat loss: 763,630.7 Btu/hr 454,825.6 Btu/hr Total heat gains cooling: 28,765.3 Btu/hr
        Solar heat gain: 13,331.2 Btu/hr 3,342.7 Btu/hr Transmission heat losses: 684.7 Btu/hr
        Internal heat gain: 2,620.5 Btu/hr 2,620.5 Btu/hr Ventilation heat losses: -28,942.6 Btu/hr
        Total heat gains heating: 15,951.7 Btu/hr 5,963.2 Btu/hr Total heat loss: -28,258 Btu/hr
        Heating load: 747,679 Btu/hr 448,862.4 Btu/hr Cooling load - sensible: 57,023.3 Btu/hr
        Cooling load - latent: 0 Btu/hr
        Relevant heating load: 747,679 Btu/hr Relevant cooling load: 57,023.3 Btu/hr
        Specific heating load: 144.7 Btu/hr ft² Specific maximum cooling load: 11 Btu/hr ft²
        """

        for line in self._lines:
            line = line.split(":")
            if len(line) < 2:
                continue

            htg_attr_name = line[0].replace(" - ", "_").lower().strip().replace(" ", "_")

            # -- Handle the weird lines...
            if htg_attr_name == "heating_load":
                # line = ["Heating load",  "747,679 Btu/hr 448,862.4 Btu/hr Cooling load - sensible", "57,023.3 Btu/hr"]
                _, middle, clg_attr_value = line
                htg_attr_value_1, htg_attr_value_2, clg_attr_name = middle.split(
                    " Btu/hr "
                )
                clg_attr_name = (
                    clg_attr_name.replace(" - ", "_").lower().strip().replace(" ", "_")
                )
                htg_attr_value_1 = str(htg_attr_value_1) + " BTU/HR"
                htg_attr_value_2 = str(htg_attr_value_2) + " BTU/HR"
            elif htg_attr_name == "cooling_load_latent":
                # line = ["Cooling load - latent", "0 Btu/hr"]
                clg_attr_name, clg_attr_value = line
                clg_attr_name = (
                    clg_attr_name.replace(" - ", "_").lower().strip().replace(" ", "_")
                )
                htg_attr_name = None
                htg_attr_value_1 = None
                htg_attr_value_2 = None
            elif htg_attr_name == "relevant_heating_load":
                # line = ["Relevant heating load", "747,679 Btu/hr Relevant cooling load", "57,023.3 Btu/hr"]
                _, middle, clg_attr_value = line
                _, clg_attr_name = middle.split(" Btu/hr ")
                clg_attr_name = "cooling_load"
                htg_attr_name = None
                htg_attr_value_1 = None
                htg_attr_value_2 = None
            elif htg_attr_name == "Specific_heating_load":
                # line = ["Specific heating load", "144.7 Btu/hr ft² Specific maximum cooling load", "11 Btu/hr ft²"]
                # - Ignore
                continue
            elif htg_attr_name not in self.heating_load_1.__dict__:
                # -- Ignore anything that isn't one of the object's attributes.
                continue
            else:
                # -- Handle the 'normal' lines
                try:
                    _, middle, clg_attr_value = line
                except Exception as e:
                    print("ERROR:", line)
                    raise Exception(e)

                htg_attr_value_1, htg_attr_value_2, clg_attr_name = middle.split(
                    " Btu/hr "
                )
                clg_attr_name = clg_attr_name.lower().strip().replace(" ", "_")
                htg_attr_value_1 = str(htg_attr_value_1) + " BTU/HR"
                htg_attr_value_2 = str(htg_attr_value_2) + " BTU/HR"

            self.heating_load_1.__setattr__(htg_attr_name, htg_attr_value_1)
            self.heating_load_2.__setattr__(htg_attr_name, htg_attr_value_2)
            self.cooling_load.__setattr__(clg_attr_name, clg_attr_value)
