# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Passive House Requirements"""

from typing import Any, List, Dict
from ph_units.unit_type import Unit
from ph_units.parser import parse_input
from ph_units.converter import _standardize_unit_name, unit_type_alias_dict
from ph_units.converter import UnitTypeNameNotFound


# -----------------------------------------------------------------------------
# -- Subsections --


class _subsection_base:
    __pdf_section_string__ = None

    def __init__(self) -> None:
        self._lines = []

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

    def add_line(self, line: str) -> None:
        self._lines.append(line)

    def process_subsection_text(self) -> None:
        raise NotImplementedError()


class heating_demand(_subsection_base):
    __pdf_section_string__ = "Heating demand"

    def __init__(self) -> None:
        super().__init__()
        self.specific = Unit(0, "KBT/FT2")
        self.target = Unit(0, "KBT/FT2")
        self.total = Unit(0, "KBTU")

    def process_subsection_text(self) -> None:
        """
        ['specific: 382.24 kBtu/ft²yr']
        ['target: 4.75 kBtu/ft²yr 0 1 2 3 4 5 6 7 8 9']
        ['total: 1,974,717.73 kBtu/yr']
        """
        for line in self._lines:
            attr_name, attr_value = line.strip().split(":")
            attr_value = attr_value.split("yr")[0].strip()
            if str(attr_value).endswith("/"):
                attr_value = attr_value[:-1]
            setattr(self, attr_name, attr_value)


class cooling_demand(_subsection_base):
    __pdf_section_string__ = "Cooling demand"

    def __init__(self) -> None:
        super().__init__()
        self.sensible = Unit(0.0, "KBTU/FT2")
        self.latent = Unit(0.0, "KBTU/FT2")
        self.specific = Unit(0.0, "KBTU/FT2")
        self.target = Unit(0.0, "KBTU/FT2")
        self.total = Unit(0.0, "KBTU")

    def process_subsection_text(self) -> None:
        """
        ['sensible: 7.51 kBtu/ft²yr']
        ['latent: 32.6 kBtu/ft²yr']
        ['specific: 40.11 kBtu/ft²yr']
        ['target: 4.75 kBtu/ft²yr 0 1 2 3 4 5 6 7 8 9']
        ['total: 207,205.43 kBtu/yr']
        """
        for line in self._lines:
            attr_name, attr_value = line.strip().split(":")
            attr_value = attr_value.split("yr")[0].strip()
            if str(attr_value).endswith("/"):
                attr_value = attr_value[:-1]
            setattr(self, attr_name, attr_value)


class heating_load(_subsection_base):
    __pdf_section_string__ = "Heating load"

    def __init__(self) -> None:
        super().__init__()
        self.specific = Unit(0.0, "BTU/HR-FT2")
        self.target = Unit(0.0, "BTU/HR-FT2")
        self.total = Unit(0.0, "BTU/HR")

    def process_subsection_text(self) -> None:
        """
        specific: 144.71 Btu/hr ft²
        target: 3.17 Btu/hr ft² 0 1 2 3 4 5 6
        total: 747,678.98 Btu/hr
        """
        for line in self._lines:
            attr_name, attr_value = line.strip().split(":")
            if attr_name == "target":
                attr_value = attr_value.split(" 0")[0]
            setattr(self, attr_name, attr_value)


class cooling_load(_subsection_base):
    __pdf_section_string__ = "Cooling load"

    def __init__(self) -> None:
        super().__init__()
        self.specific = Unit(0.0, "BTU/HR-FT2")
        self.target = Unit(0.0, "BTU/HR-FT2")
        self.total = Unit(0.0, "BTU/HR")

    def process_subsection_text(self) -> None:
        """
        specific: 11.04 Btu/hr ft²
        target: 3.17 Btu/hr ft² 0 1 2 3 4 5 6
        total: 57,023.27 Btu/hr
        WUFI®Passive V.3.3.0.2: Edwin P May/BLDGTYP, LLC Page 1
        WUFI®Passive V.3.3.0.2: Edwin P May/BLDGTYP, LLC Page 1
        Phius 2021 VERIFICATION 2
        """
        for line in self._lines:
            try:
                attr_name, attr_value = line.strip().split(":")
            except ValueError:
                continue

            if attr_name == "target":
                attr_value = attr_value.split(" 0")[0]
            setattr(self, attr_name, attr_value)


class source_energy(_subsection_base):
    __pdf_section_string__ = "Source energy"

    def __init__(self) -> None:
        super().__init__()
        self.total_kwh = Unit(0.0, "KWH")
        self.specific_kwh_per_person = Unit(0.0, "KWH/PERSON")
        self.target_kwh_per_person = Unit(0.0, "BTU/HR-FT2")
        self.total_kbtu = Unit(0.0, "KBTU")
        self.specific_kbtu_per_ft2 = Unit(0.0, "KBTU/FT2")

    def clean_unit_typename(self, unit_type_name: str) -> str:
        """Return the Unit-Type as a normalized, clean string."""
        unit_type_name = unit_type_name.split(" ")[-1]  # Break off the unit part
        unit_type_name = unit_type_name.lower()
        unit_type_name = unit_type_name.replace("/", "_per_")
        unit_type_name = unit_type_name.replace("-", "_")
        unit_type_name = unit_type_name.replace("²", "2")
        return unit_type_name

    def _set_attribute(self, attr_name: str, attr_value: str) -> None:
        """Facade for __setattr__ to convert unit-type-names first."""
        attr_name = f"{attr_name}_{self.clean_unit_typename(attr_value)}"
        setattr(self, attr_name, attr_value)

    def process_subsection_text(self) -> None:
        """
        total: 53,386.69 kWh/yr
        specific: 3,559 kWh/Person yr
        target: 3,875 kWh/Person yr 0 2000 4000 6000 8000 10000
        total: 182,144.98 kBtu/yr
        specific: 35.26 kBtu/ft²yr
        """
        for line in self._lines:
            attr_name, attr_value = line.strip().split(":")

            # -- weird line....
            if attr_name == "target":
                attr_value = attr_value.split(" 0")[0].strip()

            # -- Remove the 'yr' part from any units
            attr_value = attr_value.replace("yr", "").strip()

            # -- Remove trailing slash
            if attr_value.endswith("/"):
                attr_value = attr_value[:-1]

            self._set_attribute(attr_name, attr_value)


class site_energy(_subsection_base):
    __pdf_section_string__ = "Site energy"

    def __init__(self) -> None:
        super().__init__()
        self.total_kwh = Unit(0.0, "KWH")
        self.specific_kwh_per_ft2 = Unit(0.0, "KWH/FT2")
        self.total_kbtu = Unit(0.0, "KBTU")
        self.specific_kbtu_per_ft2 = Unit(0.0, "KBTU/FT2")

    def clean_unit_typename(self, unit_type_name: str) -> str:
        """Return the Unit-Type as a normalized, clean string."""
        unit_type_name = unit_type_name.split(" ")[-1]  # Break off the unit part
        unit_type_name = unit_type_name.lower()
        unit_type_name = unit_type_name.replace("/", "_per_")
        unit_type_name = unit_type_name.replace("-", "_")
        unit_type_name = unit_type_name.replace("²", "2")
        return unit_type_name

    def _set_attribute(self, attr_name: str, attr_value: str) -> None:
        """Facade for __setattr__ to convert unit-type-names first."""
        attr_name = f"{attr_name}_{self.clean_unit_typename(attr_value)}"
        setattr(self, attr_name, attr_value)

    def process_subsection_text(self) -> None:
        """
        total: 101,191.65 kBtu/yr
        specific: 19.59 kBtu/ft²yr
        total: 29,659.27 kWh/yr 0 3.33 6.67 10 13.33 16.67 20
        specific: 5.74 kWh/ft²
        """
        for line in self._lines:
            attr_name, attr_value = line.strip().split(":")

            # -- Weird line...
            if attr_name == "total":
                attr_value = attr_value.split(" 0")[0].strip()

            # -- Remove the 'yr' part from any units
            attr_value = attr_value.replace("yr", "").strip()

            # -- Remove trailing slash
            if attr_value.endswith("/"):
                attr_value = attr_value[:-1]

            self._set_attribute(attr_name, attr_value)


class airtightness(_subsection_base):
    __pdf_section_string__ = "Air tightness"

    def __init__(self) -> None:
        super().__init__()
        self.ach50 = 0.0
        self.cfm50_per_envelope_area = Unit(0.0, "CFM/FT2")
        self.target_ach50 = 0.0
        self.target_cfm50 = Unit(0.0, "CFM/FT2")

    def process_subsection_text(self) -> None:
        """
        ACH50: 0.74 1/hr
        CFM50 per envelope area: 0.06 cfm/ft² 0 0.2 0.4 0.6 0.8 1 1.2
        target: 0.7 1/hr
        target CFM50: 0.06 cfm/ft²
        """
        for line in self._lines:
            attr_name, attr_value = line.strip().split(":")

            # -- Weird line...
            if attr_name == "CFM50 per envelope area":
                attr_value = attr_value.strip().split(" 0")[0].strip()

            # -- Fix
            if attr_name == "target":
                attr_name = "target_ach50"
                attr_value = attr_value.strip().split(" ")[0].strip()

            # -- Fix
            if attr_name == "ACH50":
                attr_value = attr_value.strip().split(" ")[0].strip()

            attr_name = attr_name.replace(" ", "_").lower().strip()

            setattr(self, attr_name, attr_value)


# -----------------------------------------------------------------------------


class WufiPDF_PHRequirements:
    __pdf_heading_string__ = "PASSIVEHOUSE REQUIREMENTS"
    get_tables = False
    result_type_sections: Dict[str, type] = {
        heating_demand.__pdf_section_string__: heating_demand,
        cooling_demand.__pdf_section_string__: cooling_demand,
        heating_load.__pdf_section_string__: heating_load,
        cooling_load.__pdf_section_string__: cooling_load,
        source_energy.__pdf_section_string__: source_energy,
        site_energy.__pdf_section_string__: site_energy,
        airtightness.__pdf_section_string__: airtightness,
    }

    def __init__(self) -> None:
        self._lines: List[str] = []
        self._tables = []

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        subsection = _subsection_base()
        for line in self._lines:
            if subsection_marker := self.result_type_sections.get(line, None):
                subsection = subsection_marker()
                setattr(self, subsection_marker.__name__, subsection)
            else:
                subsection.add_line(line)

        for attr in vars(self):
            if isinstance(getattr(self, attr), _subsection_base):
                getattr(self, attr).process_subsection_text()
