# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: Residential Electric"""

from typing import List
import re

from ph_units.unit_type import Unit

from PHX.model.enums.elec_equip import ElectricEquipmentType


class WufiPDF_ElectricAppliance:
    """Class to hold data for a single electric appliance."""

    def __init__(
        self,
        nbdm_appliance_type: ElectricEquipmentType,
        quantity: int,
        annual_demand_kWh: Unit,
    ) -> None:
        self.nbdm_appliance_type = nbdm_appliance_type
        self.quantity = quantity
        self.annual_demand_kWh = annual_demand_kWh


class WufiPDF_ResidentialElectric:
    __pdf_heading_string__ = "ELECTRICITY DEMAND RESIDENTIAL BUILDING"
    get_tables = False

    # -- Map WUFI_PDF Names to PHX Appliance Types
    device_map = {
        "Kitchen dishwasher": ElectricEquipmentType.DISHWASHER,
        "Laundry - washer": ElectricEquipmentType.CLOTHES_WASHER,
        "Laundry - dryer": ElectricEquipmentType.CLOTHES_DRYER,
        "Kitchen refrigerator": ElectricEquipmentType.REFRIGERATOR,
        "Kitchen freezer": ElectricEquipmentType.FREEZER,
        "Kitchen fridge/freeze combo": ElectricEquipmentType.FRIDGE_FREEZER,
        "Kitchen cooking": ElectricEquipmentType.COOKING,
        "User defined": ElectricEquipmentType.CUSTOM,
        "PHIUS+ Misc Electric Loads": ElectricEquipmentType.MEL,
        "PHIUS+ Interior Lighting": ElectricEquipmentType.LIGHTING_INTERIOR,
        "PHIUS+ Exterior Lighting": ElectricEquipmentType.LIGHTING_EXTERIOR,
        "PHIUS+ Garage Lighting": ElectricEquipmentType.LIGHTING_GARAGE,
        "User defined lighting": ElectricEquipmentType.CUSTOM_LIGHTING,
        "User defined MELs": ElectricEquipmentType.CUSTOM_MEL,
    }

    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self._appliances: List[WufiPDF_ElectricAppliance] = []

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        """
        Norm Electric Non-electric Source
        Type Quantity Indoor demand demand demand energy
        [kWh/yr] [kWh/yr] [kBtu/yr] Electric demand
        Kitchen cooking 4 yes 0.2 1500 0 9211.9
        Kitchen dishwasher 4 yes 1.3 500.9 0 3076
        Kitchen fridge/freeze combo 4 yes 1.2 1781.2 0 10938.8
        Laundry - dryer 4 yes 3.9 1467.5 0 9012.4
        Energy consumed by evaporation 1 yes 3.1 0 176.2 741.7
        Laundry - washer 4 yes 0.3 153.9 0 944.9
        PHIUS+ Exterior Lighting 4 no 71.7 71.7 0 440.1
        PHIUS+ Interior Lighting 4 yes 1,527.8 1527.8 0 9382.6
        PHIUS+ Misc Electric Loads 4 yes 4,698.9 4698.9 0 28857.4
        User defined MELs 1 yes 0 0 0 0
        User defined MELs 1 yes 5,063.2 5063.2 0 31094.7
        User defined 1 yes 1,910 1910 0 11729.8
        User defined lighting 1 no 80 80 0 491.3
        User defined lighting 1 yes 123.1 123.1 0 755.7
        User defined lighting 1 yes 3,481.6 3481.6 0 21381.4
        ...
        """

        for line in self._lines:
            parts = re.split(
                r"(\d+)\s+(.+)", line, 1
            )  # -- Split on first space character after the first number

            if len(parts) != 3:
                continue

            # -- Parse the line
            appliance_type_name = parts[0].strip()
            if nbdm_appliance_type := self.device_map.get(appliance_type_name, None):
                # -- line = ["Laundry - dryer ", "4 ",  "yes 3.9 1467.5 0 9012.4"]

                quantity = int(parts[1].strip())
                _, _, annual_demand, _, _ = parts[2].strip().split(" ")
                annual_demand = Unit(annual_demand, "KWH")

                # -- Create the new appliance and add to the collection
                new_appliance = WufiPDF_ElectricAppliance(
                    nbdm_appliance_type, quantity, annual_demand
                )

                self._appliances.append(new_appliance)
