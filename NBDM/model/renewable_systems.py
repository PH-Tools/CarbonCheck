# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Renewable Systems Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Generator

from ph_units.unit_type import Unit

from NBDM.model import operations
from NBDM.model.enums import renewable_device_type
from NBDM.model.collections import Collection


@dataclass
class NBDM_RenewableDevice:
    device_type: renewable_device_type = field(default=renewable_device_type.NONE)

    @property
    def display_name(self) -> str:
        return str(self.device_type.name).title().replace("_", " ")

    @property
    def key(self) -> str:
        return self.device_type.name

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_RenewableDevice:
        """Custom from_dict method to handle the Unit type."""
        return cls(renewable_device_type(_d["device_type"]))


@dataclass
class NBDM_BuildingSegmentRenewableSystems:
    _devices: Collection[NBDM_RenewableDevice] = field(default_factory=Collection)

    @property
    def devices(self) -> Generator[NBDM_RenewableDevice, None, None]:
        return (
            self._devices[a.key]
            for a in sorted(self._devices.values(), key=lambda d: d.display_name)
        )

    @devices.setter
    def devices(self, value: Dict[str, NBDM_RenewableDevice]) -> None:
        self._devices = Collection()
        for v in value.values():
            self.add_device(v)

    def clear_devices(self) -> None:
        self._devices = Collection()

    def add_device(self, device: NBDM_RenewableDevice) -> None:
        self._devices.add_item(device)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentRenewableSystems:
        """Custom from_dict method to walk over all the devices in the system."""
        obj = cls()

        # -- Build all the Renewable System Devices and add them to the object.
        for device_dict in _d.get("_devices", {}).values():
            new_assembly_type = NBDM_RenewableDevice.from_dict(device_dict)
            obj.add_device(new_assembly_type)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentRenewableSystems
    ) -> NBDM_BuildingSegmentRenewableSystems:
        raise NotImplementedError()

    def __add__(
        self, other: NBDM_BuildingSegmentRenewableSystems
    ) -> NBDM_BuildingSegmentRenewableSystems:
        raise NotImplementedError()
