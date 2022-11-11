# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Project Site Classes."""


from dataclasses import dataclass
from typing import Dict


@dataclass
class NBDM_ProjectAddress:
    number: str
    street: str
    city: str
    state: str
    zip_code: str
    
    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_ProjectAddress':
        obj = cls(
            number = _d['number'],
            street = _d['street'],
            city = _d['city'],
            state = _d['state'],
            zip_code = _d['zip_code'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


@dataclass
class NBDM_Climate:
    zone_ashrae: int
    zone_passive_house: int
    source: str
    
    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_Climate':
        obj = cls(
            zone_ashrae = _d['zone_ashrae'],
            zone_passive_house = _d['zone_passive_house'],
            source = _d['source'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj



@dataclass
class NBDM_Location:
    address: NBDM_ProjectAddress
    longitude: float
    latitude: float
    
    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_Location':
        obj = cls(
            address = _d['address'],
            longitude = _d['longitude'],
            latitude = _d['latitude'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


@dataclass
class NBDM_Site:
    climate: NBDM_Climate
    location: NBDM_Location

    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_Site':
        obj = cls(
            climate = _d['climate'],
            location = _d['location'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj