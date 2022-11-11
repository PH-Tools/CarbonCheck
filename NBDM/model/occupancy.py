# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Occupancy Classes."""

from dataclasses import dataclass
from typing import Dict

@dataclass
class NBDM_BuildingSegmentOccupancy:
    total_dwelling_units: int
    num_apartments_studio: int
    num_apartments_1_br: int
    num_apartments_2_br: int
    num_apartments_3_br: int
    num_apartments_4_br: int
    total_occupants: int

    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_BuildingSegmentOccupancy':
        obj = cls(
            total_dwelling_units = _d['total_dwelling_units'],
            num_apartments_studio = _d['num_apartments_studio'],
            num_apartments_1_br = _d['num_apartments_1_br'],
            num_apartments_2_br = _d['num_apartments_2_br'],
            num_apartments_3_br = _d['num_apartments_3_br'],
            num_apartments_4_br = _d['num_apartments_4_br'],
            total_occupants = _d['total_occupants'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj