# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Geometry Classes."""

from dataclasses import dataclass
from typing import Dict

@dataclass
class NBDM_BuildingSegmentGeometry:
    area_envelope: float
    area_floor_area_gross: float
    area_floor_area_net_interior_weighted: float
    area_floor_area_interior_parking: float
    volume_gross: float
    volume_net_interior: float
    total_stories: int
    num_stories_above_grade: int
    num_stories_below_grade: int

    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_BuildingSegmentGeometry':
        obj = cls(
            area_envelope = _d['area_envelope'],
            area_floor_area_gross = _d['area_floor_area_gross'],
            area_floor_area_net_interior_weighted = _d['area_floor_area_net_interior_weighted'],
            area_floor_area_interior_parking = _d['area_floor_area_interior_parking'],
            volume_gross = _d['volume_gross'],
            volume_net_interior = _d['volume_net_interior'],
            total_stories = _d['total_stories'],
            num_stories_above_grade = _d['num_stories_above_grade'],
            num_stories_below_grade = _d['num_stories_below_grade'],
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj