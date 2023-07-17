# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building DHW Systems Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Generator

from ph_units.unit_type import Unit

from NBDM.model import operations
from NBDM.model.enums import dhw_tank_device_type
from NBDM.model.enums import heating_device_type
from NBDM.model.collections import Collection


@dataclass
class NBDM_DHWHeatingDevice:
    device_type: heating_device_type = field(default=heating_device_type.NONE)
    coverage_segment_hot_water: Unit = field(default_factory=Unit)

    @property
    def display_name(self) -> str:
        return str(self.device_type.name).title().replace("_", " ")

    @property
    def key(self) -> str:
        return self.device_type.name

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_DHWHeatingDevice:
        """Custom from_dict method to handle the Unit type."""
        return cls(
            heating_device_type(_d["device_type"]),
            Unit.from_dict(_d["coverage_segment_hot_water"]),
        )


@dataclass
class NBDM_DHWTankDevice:
    device_type: dhw_tank_device_type = field(default=dhw_tank_device_type.NONE)
    coverage_segment_hot_water: Unit = field(default_factory=Unit)

    @property
    def display_name(self) -> str:
        return str(self.device_type.name).title().replace("_", " ")

    @property
    def key(self) -> str:
        return self.device_type.name

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_DHWTankDevice:
        """Custom from_dict method to handle the Unit type."""
        return cls(dhw_tank_device_type(_d["type_name"]))


@dataclass
class NBDM_BuildingSegmentDHWSystems:
    _heating_devices: Collection[NBDM_DHWHeatingDevice] = field(
        default_factory=Collection
    )
    _tank_devices: Collection[NBDM_DHWTankDevice] = field(default_factory=Collection)

    @property
    def heating_devices(self) -> Generator[NBDM_DHWHeatingDevice, None, None]:
        return (
            self._heating_devices[a.key]
            for a in sorted(self._heating_devices.values(), key=lambda d: d.display_name)
        )

    @heating_devices.setter
    def heating_devices(self, value: Dict[str, NBDM_DHWHeatingDevice]) -> None:
        self._heating_devices = Collection()
        for v in value.values():
            self.add_heating_device(v)

    @property
    def tank_devices(self) -> Generator[NBDM_DHWHeatingDevice, None, None]:
        return (
            self._tank_devices[a.key]
            for a in sorted(self._tank_devices.values(), key=lambda d: d.display_name)
        )

    @tank_devices.setter
    def tank_devices(self, value: Dict[str, NBDM_DHWHeatingDevice]) -> None:
        self._tank_devices = Collection()
        for v in value.values():
            self.add_heating_device(v)

    def clear_heating_devices(self) -> None:
        self._heating_devices = Collection()

    def add_heating_device(self, device: NBDM_DHWHeatingDevice) -> None:
        self._heating_devices.add_item(device)

    def clear_tank_devices(self) -> None:
        self._tank_devices = Collection()

    def add_tank_device(self, device: NBDM_DHWTankDevice) -> None:
        self._tank_devices.add_item(device)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentDHWSystems:
        """Custom from_dict method to walk over all the devices in the system."""
        obj = cls()

        # -- Build all the DHW System Devices and add them to the object.
        for heating_device_dict in _d.get("_heating_devices", {}).values():
            new_assembly_type = NBDM_DHWHeatingDevice.from_dict(heating_device_dict)
            obj.add_heating_device(new_assembly_type)

        for tank_device_dict in _d.get("_tank_devices", {}).values():
            new_assembly_type = NBDM_DHWTankDevice.from_dict(tank_device_dict)
            obj.add_tank_device(new_assembly_type)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentDHWSystems
    ) -> NBDM_BuildingSegmentDHWSystems:
        raise NotImplementedError()

    def __add__(
        self, other: NBDM_BuildingSegmentDHWSystems
    ) -> NBDM_BuildingSegmentDHWSystems:
        raise NotImplementedError()
