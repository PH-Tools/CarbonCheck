# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Cooling Systems Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Generator

from ph_units.unit_type import Unit

from NBDM.model.enums import cooling_device_type
from NBDM.model.collections import Collection


@dataclass
class NBDM_CoolingDevice:
    device_type: cooling_device_type = field(default=cooling_device_type.NONE)
    cooling_device_name: str = ""
    SEER: Unit = field(default_factory=Unit)
    num_units: int = 0

    @property
    def display_name(self) -> str:
        return str(self.device_type.name).title().replace("_", " ")

    @property
    def key(self) -> str:
        return self.device_type.name

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_CoolingDevice:
        """Custom from_dict method to handle the Unit type."""
        return cls(
            device_type=cooling_device_type(_d["device_type"]),
            cooling_device_name=_d["cooling_device_name"],
            SEER=Unit.from_dict(_d["SEER"]),
            num_units=int(float(_d["num_units"])),
        )


@dataclass
class NBDM_BuildingSegmentCoolingSystems:
    _devices: Collection[NBDM_CoolingDevice] = field(default_factory=Collection)

    @property
    def devices(self) -> Generator[NBDM_CoolingDevice, None, None]:
        return (
            self._devices[a.key]
            for a in sorted(self._devices.values(), key=lambda d: d.display_name)
        )

    @devices.setter
    def devices(self, value: Dict[str, NBDM_CoolingDevice]) -> None:
        self._devices = Collection()
        for v in value.values():
            self.add_device(v)

    def clear_devices(self) -> None:
        self._devices = Collection()

    def add_device(self, device: NBDM_CoolingDevice) -> None:
        self._devices.add_item(device)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentCoolingSystems:
        """Custom from_dict method to walk over all the devices in the system."""
        obj = cls()

        # -- Build all the Cooling System Devices and add them to the object.
        for device_dict in _d.get("_devices", {}).values():
            new_assembly_type = NBDM_CoolingDevice.from_dict(device_dict)
            obj.add_device(new_assembly_type)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentCoolingSystems
    ) -> NBDM_BuildingSegmentCoolingSystems:
        raise NotImplementedError()

    def __add__(
        self, other: NBDM_BuildingSegmentCoolingSystems
    ) -> NBDM_BuildingSegmentCoolingSystems:
        raise NotImplementedError()
