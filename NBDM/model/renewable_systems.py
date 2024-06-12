# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Renewable Systems (PV, Solar Hot-Water, ...) Classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generator

from ph_units.unit_type import Unit

from NBDM.model.collections import Collection


@dataclass
class NBDM_SolarDHWDevice:
    footprint: Unit = field(default_factory=Unit)
    annual_dhw_energy: Unit = field(default_factory=Unit)
    annual_dhw_contribution: Unit = field(default_factory=Unit)
    annual_heating_energy: Unit = field(default_factory=Unit)
    annual_heating_contribution: Unit = field(default_factory=Unit)

    @property
    def key(self) -> str:
        return f"Solar Hot-Water: {self.footprint}"

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_SolarDHWDevice:
        """Custom from_dict method to handle the Unit type."""
        return cls(
            Unit.from_dict(_d["footprint"]),
            Unit.from_dict(_d["annual_dhw_energy"]),
            Unit.from_dict(_d["annual_dhw_contribution"]),
            Unit.from_dict(_d["annual_heating_energy"]),
            Unit.from_dict(_d["annual_heating_contribution"]),
        )


@dataclass
class NBDM_SolarPVDevice:
    display_name: str = ""
    footprint: Unit = field(default_factory=Unit)
    size: Unit = field(default_factory=Unit)
    annual_pv_energy: Unit = field(default_factory=Unit)

    @property
    def key(self) -> str:
        return f"Solar PV: {self.display_name}"

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_SolarPVDevice:
        """Custom from_dict method to handle the Unit type."""
        return cls(
            _d["display_name"],
            Unit.from_dict(_d["footprint"]),
            Unit.from_dict(_d["size"]),
            Unit.from_dict(_d["annual_pv_energy"]),
        )


@dataclass
class NBDM_BuildingSegmentRenewableSystems:
    _solar_dhw_devices: Collection[NBDM_SolarDHWDevice] = field(
        default_factory=Collection
    )
    _solar_pv_devices: Collection[NBDM_SolarPVDevice] = field(default_factory=Collection)

    @property
    def solar_dhw_devices(self) -> Generator[NBDM_SolarDHWDevice, None, None]:
        return (
            self._solar_dhw_devices[a.key]
            for a in sorted(self._solar_dhw_devices.values(), key=lambda d: d.key)
        )

    @solar_dhw_devices.setter
    def solar_dhw_devices(self, value: Dict[str, NBDM_SolarDHWDevice]) -> None:
        self._solar_dhw_devices = Collection()
        for v in value.values():
            self.add_solar_dhw_device(v)

    @property
    def solar_pv_devices(self) -> Generator[NBDM_SolarPVDevice, None, None]:
        return (
            self._solar_pv_devices[a.key]
            for a in sorted(self._solar_pv_devices.values(), key=lambda d: d.key)
        )

    @solar_pv_devices.setter
    def solar_pv_devices(self, value: Dict[str, NBDM_SolarPVDevice]) -> None:
        self._solar_pv_devices = Collection()
        for v in value.values():
            self.add_solar_pv_device(v)

    def clear_dhw_devices(self) -> None:
        self._solar_dhw_devices = Collection()

    def clear_pv_devices(self) -> None:
        self._solar_pv_devices = Collection()

    def add_solar_dhw_device(self, device: NBDM_SolarDHWDevice) -> None:
        self._solar_dhw_devices.add_item(device)

    def add_solar_pv_device(self, device: NBDM_SolarPVDevice) -> None:
        self._solar_pv_devices.add_item(device)

    @property
    def total_solar_ph_energy(self) -> Unit:
        return sum([d.annual_pv_energy for d in self.solar_pv_devices], Unit(0.0, "KWH"))

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentRenewableSystems:
        """Custom from_dict method to walk over all the devices in the system."""
        obj = cls()

        # -- Build all the Renewable System Devices and add them to the object.
        for device_dict in _d.get("_solar_dhw_devices", {}).values():
            new_device = NBDM_SolarDHWDevice.from_dict(device_dict)
            obj.add_solar_dhw_device(new_device)

        # -- Build all the Renewable System Devices and add them to the object.
        for device_dict in _d.get("_solar_pv_devices", {}).values():
            new_device = NBDM_SolarPVDevice.from_dict(device_dict)
            obj.add_solar_pv_device(new_device)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentRenewableSystems
    ) -> NBDM_BuildingSegmentRenewableSystems:
        raise NotImplementedError()

    def __add__(
        self, other: NBDM_BuildingSegmentRenewableSystems
    ) -> NBDM_BuildingSegmentRenewableSystems:
        raise NotImplementedError()
