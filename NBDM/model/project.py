# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Project Classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from NBDM.model import serialization
from NBDM.model.appliances import NBDM_BuildingSegmentAppliances
from NBDM.model.building import NBDM_Building, NBDM_BuildingSegment
from NBDM.model.cooling_systems import NBDM_BuildingSegmentCoolingSystems
from NBDM.model.dhw_systems import NBDM_BuildingSegmentDHWSystems
from NBDM.model.envelope import NBDM_BuildingSegmentEnvelope
from NBDM.model.heating_systems import NBDM_BuildingSegmentHeatingSystems
from NBDM.model.renewable_systems import NBDM_BuildingSegmentRenewableSystems
from NBDM.model.site import NBDM_Site
from NBDM.model.team import NBDM_Team
from NBDM.model.ventilation_systems import NBDM_BuildingSegmentVentilationSystems


@dataclass
class NBDM_Variant:
    """A single 'Variant' with building data"""

    variant_name: str = "-"
    building: NBDM_Building = field(default_factory=NBDM_Building)

    def get_building_segment(self, _name: str) -> NBDM_BuildingSegment:
        """Retrieve a specific Building-Segment by name."""
        return self.building.get_building_segment(_name)

    def add_building_segment(self, _bldg_segment: NBDM_BuildingSegment) -> None:
        self.building.add_building_segment(_bldg_segment)

    def clear_variant_building_segments(self) -> None:
        """Clear all the Building-Segments"""
        self.building.clear_building_segments()

    def remove_segment_by_name(self, _name: str) -> Optional[NBDM_BuildingSegment]:
        """Remove a Building-Segment from the self.building by name."""
        return self.building.remove_segment_by_name(_name)

    @property
    def building_segments(self) -> List[NBDM_BuildingSegment]:
        """Return a list with all the Building-Segments in alphabetical order."""
        return self.building.building_segments

    @property
    def building_segment_names(self) -> List[str]:
        """Return a list of all the Building-Segment names in alphabetical order."""
        return self.building.building_segment_names

    @property
    def has_building_segments(self) -> bool:
        return False if not self.building._building_segments else True

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Variant:
        return serialization.build_NBDM_obj_from_dict(cls, _d)

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

    proposed: NBDM_Variant = field(default_factory=NBDM_Variant)
    baseline: NBDM_Variant = field(default_factory=NBDM_Variant)

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
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    def __iter__(self):
        for _ in (self.proposed, self.baseline):
            yield _


@dataclass
class NBDM_Project:
    """A single Project with site, client and building data."""

    project_name: str = "-"
    client: str = "-"
    report_date: str = "-"
    team: NBDM_Team = field(default_factory=NBDM_Team)
    site: NBDM_Site = field(default_factory=NBDM_Site)
    variants: NBDM_Variants = field(default_factory=NBDM_Variants)

    # --
    envelope: NBDM_BuildingSegmentEnvelope = field(
        default_factory=NBDM_BuildingSegmentEnvelope
    )
    appliances: NBDM_BuildingSegmentAppliances = field(
        default_factory=NBDM_BuildingSegmentAppliances
    )
    heating_systems: NBDM_BuildingSegmentHeatingSystems = field(
        default_factory=NBDM_BuildingSegmentHeatingSystems
    )
    cooling_systems: NBDM_BuildingSegmentCoolingSystems = field(
        default_factory=NBDM_BuildingSegmentCoolingSystems
    )
    dhw_systems: NBDM_BuildingSegmentDHWSystems = field(
        default_factory=NBDM_BuildingSegmentDHWSystems
    )
    ventilation_systems: NBDM_BuildingSegmentVentilationSystems = field(
        default_factory=NBDM_BuildingSegmentVentilationSystems
    )
    renewable_systems: NBDM_BuildingSegmentRenewableSystems = field(
        default_factory=NBDM_BuildingSegmentRenewableSystems
    )

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
        return serialization.build_NBDM_obj_from_dict(cls, _d)

    @classmethod
    def default_with_one_segment(cls) -> NBDM_Project:
        """Default Project with a single BuildingSegment on each variant."""
        project = cls()
        project.variants.baseline.add_building_segment(NBDM_BuildingSegment())
        project.variants.proposed.add_building_segment(NBDM_BuildingSegment())
        return project

    def add_new_baseline_segment(self, _segment: NBDM_BuildingSegment):
        """Adds a new BuildingSegment to the Project's "Baseline" variant

        Arguments:
        ----------
            * _segment: (NBDM_BuildingSegment) The NBDM_BuildingSegment to add.
        """
        self.variants.baseline.add_building_segment(_segment)

    def add_new_proposed_segment(self, _segment: NBDM_BuildingSegment):
        """Adds a new BuildingSegment to the Project's "Proposed" variant

        Arguments:
        ----------
            * _segment: (NBDM_BuildingSegment) The NBDM_BuildingSegment to add.
        """
        self.variants.proposed.add_building_segment(_segment)

    def clear_project_building_segments(self):
        """Clears all BuildingSegments from the Project."""
        self.variants.baseline.clear_variant_building_segments()
        self.variants.proposed.clear_variant_building_segments()
