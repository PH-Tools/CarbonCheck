# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Geometry Classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from ph_units.unit_type import Unit

from NBDM.model import operations, serialization


@dataclass
class NBDM_BuildingSegmentGeometry:
    area_envelope: Unit = field(default_factory=Unit)
    area_floor_area_net_interior_weighted: Unit = field(default_factory=Unit)
    volume_net_interior: Unit = field(default_factory=Unit)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentGeometry:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    def __sub__(
        self, other: NBDM_BuildingSegmentGeometry
    ) -> NBDM_BuildingSegmentGeometry:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentGeometry
    ) -> NBDM_BuildingSegmentGeometry:
        return operations.add_NBDM_Objects(self, other)
