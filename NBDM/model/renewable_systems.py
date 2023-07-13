# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Renewable Systems Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

from ph_units.unit_type import Unit

from NBDM.model import serialization
from NBDM.model import operations


@dataclass
class NBDM_BuildingSegmentRenewableSystems:
    a: Optional[int] = None

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentRenewableSystems:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    def __sub__(
        self, other: NBDM_BuildingSegmentRenewableSystems
    ) -> NBDM_BuildingSegmentRenewableSystems:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentRenewableSystems
    ) -> NBDM_BuildingSegmentRenewableSystems:
        return operations.add_NBDM_Objects(self, other)
