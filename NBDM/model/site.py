# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Project Site Classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from NBDM.model import serialization


@dataclass
class NBDM_ProjectAddress:
    building_number: str = "-"
    street_name: str = "-"
    city: str = "-"
    state: str = "-"
    post_code: str = "-"

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_ProjectAddress:
        return serialization.build_NBDM_obj_from_dict(cls, _d)


@dataclass
class NBDM_Climate:
    zone_passive_house: str = "-"
    country: str = "-"
    region: str = "-"
    data_set: str = "-"

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Climate:
        return serialization.build_NBDM_obj_from_dict(cls, _d)


@dataclass
class NBDM_Location:
    address: NBDM_ProjectAddress = field(default_factory=NBDM_ProjectAddress)
    longitude: float = 0.0
    latitude: float = 0.0

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Location:
        return serialization.build_NBDM_obj_from_dict(cls, _d)


@dataclass
class NBDM_Site:
    climate: NBDM_Climate = field(default_factory=NBDM_Climate)
    location: NBDM_Location = field(default_factory=NBDM_Location)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Site:
        return serialization.build_NBDM_obj_from_dict(cls, _d)
