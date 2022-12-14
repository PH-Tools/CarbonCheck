# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Geometry Classes."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization
from NBDM.model import operations


@dataclass
class NBDM_BuildingSegmentGeometry:
    area_envelope: float
    area_floor_area_net_interior_weighted: float
    volume_net_interior: float

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentGeometry:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(
        self, other: NBDM_BuildingSegmentGeometry
    ) -> NBDM_BuildingSegmentGeometry:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentGeometry
    ) -> NBDM_BuildingSegmentGeometry:
        return operations.add_NBDM_Objects(self, other)
