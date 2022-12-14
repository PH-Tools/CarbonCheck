# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Project Site Classes."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization


@dataclass
class NBDM_ProjectAddress:
    building_number: str
    street_name: str
    city: str
    state: str
    zip_code: str

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_ProjectAddress:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    @classmethod
    def default(cls) -> NBDM_ProjectAddress:
        return cls("-", "-", "-", "-", "-")


@dataclass
class NBDM_Climate:
    zone_ashrae: str
    zone_passive_house: str
    source: str

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Climate:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    @classmethod
    def default(cls) -> NBDM_Climate:
        return cls("-", "-", "-")


@dataclass
class NBDM_Location:
    address: NBDM_ProjectAddress
    longitude: float
    latitude: float

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Location:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    @classmethod
    def default(cls) -> NBDM_Location:
        return cls(NBDM_ProjectAddress.default(), 0, 0)


@dataclass
class NBDM_Site:
    climate: NBDM_Climate
    location: NBDM_Location

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Site:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    @classmethod
    def default(cls) -> NBDM_Site:
        return cls(NBDM_Climate.default(), NBDM_Location.default())
