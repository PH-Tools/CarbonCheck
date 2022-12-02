# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Geometry Classes."""

from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization
from NBDM.model import operations


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

    def __sub__(
        self, other: "NBDM_BuildingSegmentGeometry"
    ) -> "NBDM_BuildingSegmentGeometry":
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: "NBDM_BuildingSegmentGeometry"
    ) -> "NBDM_BuildingSegmentGeometry":
        return operations.add_NBDM_Objects(self, other)
