# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Geometry Classes."""

from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization


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
    def from_dict(cls, _d: Dict) -> "NBDM_BuildingSegmentGeometry":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __add__(self, other) -> "NBDM_BuildingSegmentGeometry":
        obj = self.__class__(
            self.area_envelope + other.area_envelope,
            self.area_floor_area_gross + other.area_floor_area_gross,
            self.area_floor_area_net_interior_weighted
            + other.area_floor_area_net_interior_weighted,
            self.area_floor_area_interior_parking
            + other.area_floor_area_interior_parking,
            self.volume_gross + other.volume_gross,
            self.volume_net_interior + other.volume_net_interior,
            self.total_stories + other.total_stories,
            self.num_stories_above_grade + other.num_stories_above_grade,
            self.num_stories_below_grade + other.num_stories_below_grade,
        )
        return obj
