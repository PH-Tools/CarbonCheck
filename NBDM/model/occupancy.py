# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Occupancy Classes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from NBDM.model import operations, serialization


@dataclass
class NBDM_BuildingSegmentOccupancy:
    total_dwelling_units: int = 0
    total_occupants: float = 0.0

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentOccupancy:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    def __sub__(
        self, other: NBDM_BuildingSegmentOccupancy
    ) -> NBDM_BuildingSegmentOccupancy:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentOccupancy
    ) -> NBDM_BuildingSegmentOccupancy:
        return operations.add_NBDM_Objects(self, other)
