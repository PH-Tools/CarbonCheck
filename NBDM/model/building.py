# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from functools import reduce

from NBDM.model.geometry import NBDM_BuildingSegmentGeometry
from NBDM.model.occupancy import NBDM_BuildingSegmentOccupancy
from NBDM.model.performance import NBDM_BuildingSegmentPerformance
from NBDM.model import serialization
from NBDM.model import enums


@dataclass
class NBDM_BuildingSegment:
    segment_name: str = "-"
    construction_type: enums.construction_type = field(
        default=enums.construction_type.NEW_CONSTRUCTION
    )
    construction_method: enums.construction_method = field(
        default=enums.construction_method.METHOD_A
    )
    geometry: NBDM_BuildingSegmentGeometry = field(
        default_factory=NBDM_BuildingSegmentGeometry
    )
    occupancy: NBDM_BuildingSegmentOccupancy = field(
        default_factory=NBDM_BuildingSegmentOccupancy
    )
    performance: NBDM_BuildingSegmentPerformance = field(
        default_factory=NBDM_BuildingSegmentPerformance
    )

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegment:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    def __sub__(self, other: NBDM_BuildingSegment) -> NBDM_BuildingSegment:
        return self.__class__(
            self.segment_name,
            self.construction_type,
            self.construction_method,
            self.geometry - other.geometry,
            self.occupancy - other.occupancy,
            self.performance - other.performance,
        )

    def __add__(self, other: NBDM_BuildingSegment) -> NBDM_BuildingSegment:
        return self.__class__(
            self.segment_name,
            self.construction_type,
            self.construction_method,
            self.geometry + other.geometry,
            self.occupancy + other.occupancy,
            self.performance + other.performance,
        )


@dataclass
class NBDM_Building:
    building_name: str = "-"
    building_type: enums.building_type = field(default=enums.building_type.MULTIFAMILY)
    _building_segments: Dict[str, NBDM_BuildingSegment] = field(default_factory=dict)

    def add_building_segment(self, _segment: NBDM_BuildingSegment) -> None:
        """Add a new Building Segment to the Building."""
        self._building_segments[_segment.segment_name] = _segment

    def get_building_segment(self, _name: str) -> NBDM_BuildingSegment:
        """Retrieve a specific Building Segment by name."""
        return self._building_segments[_name]

    def clear_building_segments(self) -> None:
        """Clear all Building Segments from the Building."""
        self._building_segments.clear()

    def remove_segment_by_name(self, _name: str) -> Optional[NBDM_BuildingSegment]:
        """Remove a specific Building Segment from the NBDM_Building by name."""
        return self._building_segments.pop(_name, None)

    @property
    def building_segment_names(self) -> List[str]:
        """Return a list of the Building Segment Names in alphabetical order."""
        return sorted(self._building_segments.keys())

    @property
    def building_segments(self) -> List[NBDM_BuildingSegment]:
        """Return a list of the Building Segments in alphabetical order."""
        return [self.get_building_segment(nm) for nm in self.building_segment_names]

    @property
    def geometry(self) -> NBDM_BuildingSegmentGeometry:
        """Return the geometry of the entire building as a single segment."""
        return reduce(
            lambda x, y: x + y, (seg.geometry for seg in self.building_segments)
        )

    @property
    def occupancy(self) -> NBDM_BuildingSegmentOccupancy:
        """Return the occupancy of the entire building as a single segment."""
        return reduce(
            lambda x, y: x + y, (seg.occupancy for seg in self.building_segments)
        )

    @property
    def performance(self) -> NBDM_BuildingSegmentPerformance:
        """Return the energy performance of the entire building as a single segment."""
        return reduce(
            lambda x, y: x + y, (seg.performance for seg in self.building_segments)
        )

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Building:
        """Implements a custom 'from_dict' in order to iterate over the segments."""
        obj = cls(
            building_name=_d["building_name"],
            building_type=enums.building_type(_d["building_type"]),
        )
        for seg in (
            NBDM_BuildingSegment.from_dict(_) for _ in _d["_building_segments"].values()
        ):
            obj.add_building_segment(seg)

        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(
            vars(obj).keys(), _d.keys()
        )

        return obj

    def __sub__(self, other: NBDM_Building) -> NBDM_Building:
        new_building = self.__class__(
            self.building_name,
            self.building_type,
        )

        for self_seg, other_seg in zip(self.building_segments, other.building_segments):
            new_building.add_building_segment(self_seg - other_seg)

        return new_building

    def __add__(self, other: NBDM_Building) -> NBDM_Building:
        new_building = self.__class__(
            self.building_name,
            self.building_type,
        )

        for self_seg, other_seg in zip(self.building_segments, other.building_segments):
            new_building.add_building_segment(self_seg + other_seg)

        return new_building
