# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Heating Systems Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Generator

from ph_units.unit_type import Unit

from NBDM.model.enums import heating_device_type
from NBDM.model.collections import Collection


@dataclass
class NBDM_HeatingDevice:
    device_type: heating_device_type = field(default=heating_device_type.NONE)
    coverage_segment_heating: Unit = field(default_factory=Unit)
    coverage_segment_cooling: Unit = field(default_factory=Unit)
    _display_name: str = ""

    @property
    def display_name(self) -> str:
        if not self._display_name:
            return str(self.device_type.name).title().replace("_", " ")
        else:
            return self._display_name

    @display_name.setter
    def display_name(self, value: str) -> None:
        self._display_name = value

    @property
    def key(self) -> str:
        return f"{self.device_type.name}-{self.display_name}-{self.coverage_segment_heating}-{self.coverage_segment_cooling}"

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_HeatingDevice:
        """Custom from_dict method to handle the Unit type."""
        return cls(
            heating_device_type(_d["device_type"]),
            Unit.from_dict(_d["coverage_segment_heating"]),
            Unit.from_dict(_d["coverage_segment_cooling"]),
            _d.get("_display_name", ""),
        )


@dataclass
class NBDM_BuildingSegmentHeatingSystems:
    _devices: Collection[NBDM_HeatingDevice] = field(default_factory=Collection)

    @property
    def devices(self) -> Generator[NBDM_HeatingDevice, None, None]:
        return (
            self._devices[a.key]
            for a in sorted(self._devices.values(), key=lambda d: d.display_name)
        )

    @devices.setter
    def devices(self, value: Dict[str, NBDM_HeatingDevice]) -> None:
        self._devices = Collection()
        for v in value.values():
            self.add_device(v)

    def clear_devices(self) -> None:
        self._devices = Collection()

    def add_device(self, device: NBDM_HeatingDevice) -> None:
        self._devices.add_item(device)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentHeatingSystems:
        """Custom from_dict method to walk over all the devices in the system."""
        obj = cls()

        # -- Build all the Heating System Devices and add them to the object.
        for device_dict in _d.get("_devices", {}).values():
            new_assembly_type = NBDM_HeatingDevice.from_dict(device_dict)
            obj.add_device(new_assembly_type)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentHeatingSystems
    ) -> NBDM_BuildingSegmentHeatingSystems:
        raise NotImplementedError()

    def __add__(
        self, other: NBDM_BuildingSegmentHeatingSystems
    ) -> NBDM_BuildingSegmentHeatingSystems:
        raise NotImplementedError()
