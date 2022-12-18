# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Project Classes."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

from NBDM.model.building import NBDM_Building
from NBDM.model.site import NBDM_Site
from NBDM.model.building import NBDM_BuildingSegment
from NBDM.model.team import NBDM_Team
from NBDM.model import serialization
from NBDM.model import enums


@dataclass
class NBDM_Variant:
    """A single 'Variant' with building data"""

    variant_name: str = "-"
    building: NBDM_Building = NBDM_Building()

    def get_building_segment(self, _name: str) -> NBDM_BuildingSegment:
        """Retrieve a specific Building-Segment by name."""
        return self.building.get_building_segment(_name)

    def add_building_segment(self, _bldg_segment: NBDM_BuildingSegment) -> None:
        self.building.add_building_segment(_bldg_segment)

    @property
    def building_segments(self) -> List[NBDM_BuildingSegment]:
        """Return a list with all the Building-Segments in alphabetical order."""
        return self.building.building_segments

    @property
    def building_segment_names(self) -> List[str]:
        """Return a list of all the Building-Segment names in alphabetical order."""
        return self.building.building_segment_names

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Variant:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __sub__(self, other: NBDM_Variant) -> NBDM_Variant:
        return self.__class__(
            variant_name=self.variant_name, building=self.building - other.building
        )

    def __add__(self, other: NBDM_Variant) -> NBDM_Variant:
        return self.__class__(
            variant_name=self.variant_name, building=self.building + other.building
        )


@dataclass
class NBDM_Variants:
    """A group of 2 variants: 'Proposed' and 'Baseline'."""

    proposed: NBDM_Variant = NBDM_Variant()
    baseline: NBDM_Variant = NBDM_Variant()

    @property
    def change_from_baseline_variant(self) -> NBDM_Variant:
        """Return a new Variant with values representing the change from Baseline."""
        variant = getattr(self, "_change_from_baseline", None)
        if variant:
            return variant
        else:
            self._change_from_baseline = self.baseline - self.proposed
            return self._change_from_baseline

    @property
    def building_segment_names_baseline(self) -> List[str]:
        """Return a list of the Baseline Building-Segment Names."""
        return self.baseline.building_segment_names

    @property
    def building_segment_names_proposed(self) -> List[str]:
        """Return a list of the Proposed Building-Segment Names."""
        return self.proposed.building_segment_names

    @property
    def building_segments_baseline(self) -> List[NBDM_BuildingSegment]:
        """Return a list of the Baseline Building-Segments."""
        return self.baseline.building_segments

    @property
    def building_segments_proposed(self) -> List[NBDM_BuildingSegment]:
        """Return a list of the Proposed Building-Segments."""
        return self.proposed.building_segments

    def check_building_segments_match(self) -> None:
        """Raise Error if the Baseline/Proposed Building Segment orders do not match."""
        error_msg = (
            f"\n\tError: The Baseline Building Segments:\n\t{self.building_segment_names_baseline}"
            f"\n\tdo not match the Proposed Building Segments:\n\t{self.building_segment_names_proposed}?"
        )

        assert (
            self.building_segment_names_baseline == self.building_segment_names_proposed
        ), error_msg

    @property
    def building_segments(
        self,
    ) -> List[Tuple[NBDM_BuildingSegment, NBDM_BuildingSegment]]:
        """Return all building segments in a list of tuples: (baseline, proposed)"""
        self.check_building_segments_match()

        return list(zip(self.building_segments_baseline, self.building_segments_proposed))

    @property
    def building_segments_with_change(self):
        """Return all building segments in a list of tuples: (baseline, proposed, change)"""
        self.check_building_segments_match()

        return list(
            zip(
                self.building_segments_baseline,
                self.building_segments_proposed,
                self.change_from_baseline_variant.building_segments,
            )
        )

    @property
    def buildings(self) -> Tuple[NBDM_Building, NBDM_Building]:
        """Return both buildings in a tuple: (baseline, proposed)"""
        return (self.baseline.building, self.proposed.building)

    @property
    def buildings_with_change(
        self,
    ) -> Tuple[NBDM_Building, NBDM_Building, NBDM_Building]:
        """Return both buildings in a tuple, along with the 'change': (baseline, proposed, change)"""
        return (
            self.baseline.building,
            self.proposed.building,
            self.change_from_baseline_variant.building,
        )

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Variants:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    def __iter__(self):
        for _ in (self.proposed, self.baseline):
            yield _


@dataclass
class NBDM_Project:
    """A single Project with site, client and building data."""

    project_name: str = "-"
    client: str = "-"
    salesforce_num: str = "-"
    report_date: str = "-"
    nyc_ecc_year: enums.nyc_ecc_year = enums.nyc_ecc_year._2019
    historic_preservation_site: bool = False
    disadvantaged_communities: bool = False
    team: NBDM_Team = NBDM_Team()
    site: NBDM_Site = NBDM_Site()
    variants: NBDM_Variants = NBDM_Variants()

    @property
    def building_segment_names_baseline(self) -> List[str]:
        """Return a list of all the Baseline Building Segment Names"""
        return self.variants.building_segment_names_baseline

    @property
    def building_segments_baseline(self) -> List[NBDM_BuildingSegment]:
        """Return a list of all the Baseline Building Segments"""
        return self.variants.building_segments_baseline

    @property
    def building_segment_names_proposed(self) -> List[str]:
        """Return a list of all the Proposed Building Segment Names"""
        return self.variants.building_segment_names_proposed

    @property
    def building_segments_proposed(self) -> List[NBDM_BuildingSegment]:
        """Return a list of all the Proposed Building Segments"""
        return self.variants.building_segments_proposed

    @property
    def buildings(self) -> Tuple[NBDM_Building, NBDM_Building]:
        """Return all buildings in a list of tuples: (baseline, proposed)"""
        return self.variants.buildings

    @property
    def buildings_with_change(
        self,
    ) -> Tuple[NBDM_Building, NBDM_Building, NBDM_Building]:
        """Return all buildings with change in a list of tuples: (baseline, proposed, change)"""
        return self.variants.buildings_with_change

    @property
    def building_segments(
        self,
    ) -> List[Tuple[NBDM_BuildingSegment, NBDM_BuildingSegment]]:
        """Return all building segments in a list of tuples: (baseline, proposed)"""
        return self.variants.building_segments

    @property
    def building_segments_with_change(
        self,
    ) -> List[Tuple[NBDM_BuildingSegment, NBDM_BuildingSegment, NBDM_BuildingSegment]]:
        """Return all building segments with change in a list of tuples: (baseline, proposed, change)"""
        return self.variants.building_segments_with_change

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Project:
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)

    @classmethod
    def default_with_one_segment(cls) -> NBDM_Project:
        """Default Project with a single BuildingSegment on each variant."""
        project = cls()
        project.variants.baseline.add_building_segment(NBDM_BuildingSegment())
        project.variants.proposed.add_building_segment(NBDM_BuildingSegment())
        return project
