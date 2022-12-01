# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Occupancy Classes."""

from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization


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
    def from_dict(cls, _d: Dict) -> "NBDM_BuildingSegmentOccupancy":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)
