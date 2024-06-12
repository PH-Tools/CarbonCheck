# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Ventilation Systems Classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generator

from ph_units.unit_type import Unit

from NBDM.model import operations
from NBDM.model.collections import Collection


@dataclass
class NBDM_VentilationDevice:
    display_name: str = "-"
    vent_unit_type_name: str = "-"
    quantity: int = 0
    hr_efficiency: Unit = field(default_factory=Unit)
    mr_efficiency: Unit = field(default_factory=Unit)

    @property
    def key(self) -> str:
        return self.display_name

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_VentilationDevice:
        """Custom from_dict method to handle the Unit type."""
        return cls(
            _d["display_name"],
            _d["vent_unit_type_name"],
            _d["quantity"],
            Unit.from_dict(_d["hr_efficiency"]),
            Unit.from_dict(_d["mr_efficiency"]),
        )


@dataclass
class NBDM_BuildingSegmentVentilationSystems:
    _devices: Collection[NBDM_VentilationDevice] = field(default_factory=Collection)

    @property
    def devices(self) -> Generator[NBDM_VentilationDevice, None, None]:
        return (
            self._devices[a.key]
            for a in sorted(self._devices.values(), key=lambda d: d.display_name)
        )

    @devices.setter
    def devices(self, value: Dict[str, NBDM_VentilationDevice]) -> None:
        self._devices = Collection()
        for v in value.values():
            self.add_device(v)

    def clear_devices(self) -> None:
        self._devices = Collection()

    def add_device(self, device: NBDM_VentilationDevice) -> None:
        self._devices.add_item(device)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentVentilationSystems:
        """Custom from_dict method to walk over all the devices in the system."""
        obj = cls()

        # -- Build all the Ventilation System Devices and add them to the object.
        for device_dict in _d.get("_devices", {}).values():
            mew_device = NBDM_VentilationDevice.from_dict(device_dict)
            obj.add_device(mew_device)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentVentilationSystems
    ) -> NBDM_BuildingSegmentVentilationSystems:
        raise NotImplementedError()

    def __add__(
        self, other: NBDM_BuildingSegmentVentilationSystems
    ) -> NBDM_BuildingSegmentVentilationSystems:
        raise NotImplementedError()
