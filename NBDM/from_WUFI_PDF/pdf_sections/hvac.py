# -*- Python Version: 3.11 -*-

"""WUFI-PDF Section: HVAC"""

from enum import Enum
from typing import List, Union
import re

from ph_units.unit_type import Unit

from NBDM.model.enums import (
    heating_device_type,
    cooling_device_type,
    dhw_tank_device_type,
)


class WufiPDF_HvacDeviceType(Enum):
    """HVAC Device Types mapped to the string descriptions in the WUFI-PDF."""

    NONE = "-"
    HEAT_PUMP = "Heat pump"
    WATER_STORAGE = "Water storage"
    BOILER = "Boiler"
    MECH_VENT = "Mechanical ventilation"
    RENEWABLE = "Photovoltaic / renewable energy"


class WufiPDF_HvacDevice:
    def __init__(
        self, _device_type: WufiPDF_HvacDeviceType, _device_name: str = ""
    ) -> None:
        self.device_type = _device_type
        self.device_name = _device_name
        self._lines: List[str] = []
        self._tables: List[List[str]] = []

        # -- various attributes for the various devices
        self.cop: Unit = Unit(0.0, "BTU/HR-W")
        self.sensible_recovery: Unit = Unit(0.0, "%")
        self.moisture_recovery: Unit = Unit(0.0, "%")
        self.quantity: int = 0
        self.annual_energy_production = Unit(0.0, "KWH")
        self.storage_capacity = Unit(0.0, "GAL")
        self.tank_heat_loss = Unit(0.0, "BTU/HR-F")

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def process_heat_pump_text(self) -> None:
        for line in self._lines:
            if "Annual heating coefficient of performance (COP) [-]" in line:
                value = line.split("[-]")[-1].strip()
                self.cop = Unit(value, "BTU/HR-W")

    def process_boiler_text(self) -> None:
        pass

    def process_water_storage_text(self) -> None:
        """self._lines = [
        Water storage
        Storage capacity [gal]79.2519
        Specific total thermal storage losses [Btu/hr F]7.5818
        Specific storage losses standby part only [Btu/hr F]7.5818
        Typical storage water temperature [°F]140
        Within thermal envelope Yes
        Quantity 1
        Coverage DHW
        ]
        """
        for line in self._lines:
            if "Storage capacity [gal]" in line:
                value = line.split("[gal]")[-1].strip()
                self.storage_capacity = Unit(value, "GAL")
            elif "Specific total thermal storage losses [Btu/hr F]" in line:
                value = line.split("[Btu/hr F]")[-1].strip()
                self.tank_heat_loss = Unit(value, "BTU/HR-F")

    def process_mech_vent_text(self) -> None:
        """self._lines = [
        Mechanical ventilation
        Sensible recovery efficiency [-]0.73
        Humidity recovery efficiency [-]0
        Electric efficiency [W/cfm]0.7646
        Equipped with frost protection Yes
        Subsoil heat exchanger efficiency [-]0
        Quantity 1
        HRV/ERV in conditioned space Yes
        No summer bypass feature (summer ventilation with HRV/ERV) No
        Defrost active Yes
        Temperature below which defrost must be used [°F]23
        Z.1, R.1, User defined: -
        Apartment_1_default_space; Z.1, R.2, User
        Rooms ventilated by this unit defined: -Apartment_2_default_space; Z.1,
        R.3, User defined: -
        Apartment_3_default_space; Z.1, R.4, User
        ]
        """

        for line in self._lines:
            if "Sensible recovery efficiency [-]" in line:
                value = float(line.split("[-]")[-1])
                if value < 1.0:
                    value = value * 100
                self.sensible_recovery = Unit(value, "%")
            elif "Humidity recovery efficiency [-]" in line:
                value = float(line.split("[-]")[-1])
                if value < 1.0:
                    value = value * 100
                self.moisture_recovery = Unit(value, "%")
            elif "Quantity" in line:
                value = line.split(" ")[-1]
                self.quantity = int(value)

    def process_renewable_text(self) -> None:
        """self._lines = [
        Photovoltaic / renewable energy
        Photovoltaic / renewable energy [kWh/yr]1000
        Utilization factor [-]1
        ]
        """
        for line in self._lines:
            if "Photovoltaic / renewable energy [kWh/yr]" in line:
                value = line.split("[kWh/yr]")[-1].strip().replace(",", "")
                self.annual_energy_production = Unit(value, "KWH")

    def process_section_text(self) -> None:
        """self._lines = [
        Heat pump
        Annual heating coefficient of performance (COP) [-]2.5
        Total system performance ratio of heat generator [-]0.4
        Coverage Heating 1
        ]
        """
        if self.device_type is WufiPDF_HvacDeviceType.HEAT_PUMP:
            self.process_heat_pump_text()
        elif self.device_type is WufiPDF_HvacDeviceType.BOILER:
            self.process_boiler_text()
        elif self.device_type is WufiPDF_HvacDeviceType.WATER_STORAGE:
            self.process_water_storage_text()
        elif self.device_type is WufiPDF_HvacDeviceType.MECH_VENT:
            self.process_mech_vent_text()
        elif self.device_type is WufiPDF_HvacDeviceType.RENEWABLE:
            self.process_renewable_text()
        else:
            pass

    def __str__(self) -> str:
        attr_list = [f"{k}={v}" for k, v in self.__dict__.items() if v and k != "_lines"]
        return f"{self.__class__.__name__}({attr_list})"


# -----------------------------------------------------------------------------
class WufiPDF_HvacDevices:
    def __init__(self) -> None:
        self._lines: List[str] = []
        self._tables: List[List[str]] = []
        self._devices: List[WufiPDF_HvacDevice] = []

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def process_section_text(self) -> None:
        device = WufiPDF_HvacDevice(WufiPDF_HvacDeviceType.NONE)

        for line in self._lines:
            parts = line.split(":")  # -- ':' means it might be a device heading...
            possible_device_name = parts[0].strip().split(",")[0].strip()

            try:
                # -- See if this line is the start of a device-type
                # -- if not a valid type, will raise a ValueError
                device_type = WufiPDF_HvacDeviceType(possible_device_name)

                # -- Start a new Device
                device_name = parts[1].strip()
                device = WufiPDF_HvacDevice(device_type, device_name)
                self._devices.append(device)
            except ValueError:
                device.add_line(line)

        for device in self._devices:
            device.process_section_text()

    @property
    def ventilation_devices(self) -> List[WufiPDF_HvacDevice]:
        return [
            d for d in self._devices if d.device_type == WufiPDF_HvacDeviceType.MECH_VENT
        ]

    @property
    def dhw_tank_devices(self) -> List[WufiPDF_HvacDevice]:
        return [
            d
            for d in self._devices
            if d.device_type == WufiPDF_HvacDeviceType.WATER_STORAGE
        ]

    @property
    def renewable_devices(self) -> List[WufiPDF_HvacDevice]:
        return [
            d for d in self._devices if d.device_type == WufiPDF_HvacDeviceType.RENEWABLE
        ]


class WufiPDF_HvacDistribution:
    def __init__(self) -> None:
        self._lines = []
        self._tables = []
        self._distribution: List[WufiPDF_HvacDistribution] = []

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def process_section_text(self) -> None:
        pass


# -----------------------------------------------------------------------------
class WufiPDF_HVAC:
    __pdf_heading_string__ = "HVAC"
    get_tables = False

    def __init__(self) -> None:
        self._lines: List[str] = []
        self._tables = []
        self._device_groups: List[WufiPDF_HvacDevices] = []
        self._distribution_groups: List[WufiPDF_HvacDistribution] = []

    @property
    def heating_devices(self) -> List[WufiPDF_HvacDevice]:
        return []

    @property
    def ventilation_devices(self) -> List[WufiPDF_HvacDevice]:
        return [d for gr in self._device_groups for d in gr.ventilation_devices]

    @property
    def dhw_tank_devices(self) -> List[WufiPDF_HvacDevice]:
        return [d for gr in self._device_groups for d in gr.dhw_tank_devices]

    @property
    def renewable_devices(self) -> List[WufiPDF_HvacDevice]:
        return [d for gr in self._device_groups for d in gr.renewable_devices]

    def add_line(self, _line: str) -> None:
        self._lines.append(_line)

    def add_table(self, _table: List) -> None:
        self._tables.append(_table)

    def process_section_text(self) -> None:
        section = WufiPDF_HvacDevices()

        # -- Separate out each System's text
        for line in self._lines:
            match = re.search(r"System \d", line)  # -- might be a 'Group' heading
            if match and "Device" in line:
                # -- Start a new 'Group''
                section = WufiPDF_HvacDevices()
                self._device_groups.append(section)
            elif match and "Distribution" in line:
                section = WufiPDF_HvacDistribution()
                self._distribution_groups.append(section)
            else:
                section.add_line(line)

        for section in self._device_groups:
            section.process_section_text()
