# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Assembly / Window Types"""

from typing import List
from ph_units.unit_type import Unit


class WufiPDF_AssemblyType:
    """A WUFI-PDF Assembly Type."""

    def __init__(self) -> None:
        self.name = ""
        self.u_value = Unit(0.0, "BTU/HR-FT2-F")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name} u-value={self.u_value})"

    @property
    def r_value(self) -> Unit:
        return self.u_value.inverse()


class WufiPDF_WindowType:
    """A WUFI-PDF Window Type."""

    def __init__(self) -> None:
        self.name = ""
        self.u_value = Unit(0.0, "BTU/HR-FT2-F")
        self.g_value = Unit(0.0, "-")

    def __str__(self) -> str:
        return f"{self.__class__.__name__} (name={self.name}, u-value={self.u_value} g-value={self.g_value})"


class WufiPDF_AssemblyAndWindowTypes:
    __pdf_heading_string__ = "Assemblies/window types"
    get_tables = False

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self._assembly_types: List[WufiPDF_AssemblyType] = []
        self._window_types: List[WufiPDF_WindowType] = []

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        """_lines=[
        Assembly (Id.3): Generic Ground Slab
        Homogenous layers
        Thermal resistance: 10.046 hr ft² °F/Btu (without Rsi, Rse)
        Heat transfer coefficient (U-value): 0.091 Btu/hr ft² °F
        Thickness: 9.843 in
        Material/Layer c Thickness
        Nr. (from outside to inside) [lb/ft³] [Btu/lb°F] [Btu/hr ft °F] [in] Color
        1 Generic 50mm Insulation 2.68 0.29 0.0173 1.969
        2 Generic HW Concrete 139.84 0.21 1.1267 7.874
        ...
        Window type (Id 2): Design-Skylights
        Basic data
        Uw -mounted [Btu/hr ft² °F] 0.2889
        Frame factor 0.7242
        Glass U-value [Btu/hr ft² °F] 0.25
        SHGC/Solar energy transmittance (perpendicular) 0.4
        Frame data
        Setting Left Right Top Bottom
        Frame width [in] 3.937 3.937 3.937 3.937
        Frame U-value [Btu/hr ft² °F] 0.25 0.25 0.25 0.25
        Glazing-to-frame psi-value [Btu/hr ft °F] 0.0231 0.0231 0.0231 0.0231
        Frame-to-Wall psi-value [Btu/hr ft °F] 0.0231 0.0231 0.0231 0.0231
        Solar radiation angle dependent data
        Total
        Angle
        solar
        [°]
        trans.
        0
        ...
        ]
        """

        # -- Create default types.
        assembly_type = WufiPDF_AssemblyType()
        window_type = WufiPDF_WindowType()

        for line in self._lines:
            # -- Populate the Assembly Types
            if "Assembly (Id." in line:
                assembly_type = WufiPDF_AssemblyType()
                self._assembly_types.append(assembly_type)
                assembly_type.name = line.split(":")[1].strip()
            elif "Heat transfer coefficient (U-value):" in line:
                assembly_type.u_value = Unit(
                    float(line.split(":")[1].strip().split(" ")[0]), "BTU/HR-FT2-F"
                )

            # -- Populate the Window Types
            if "Window type (Id" in line:
                window_type = WufiPDF_WindowType()
                self._window_types.append(window_type)
                window_type.name = line.split(":")[1].strip()
            elif "Glass U-value" in line:
                window_type.u_value = Unit(
                    float(line.split(" ")[-1].strip()), "BTU/HR-FT2-F"
                )
            elif "SHGC/Solar energy transmittance (perpendicular)" in line:
                window_type.g_value = Unit(float(line.split(" ")[-1].strip()), "-")
