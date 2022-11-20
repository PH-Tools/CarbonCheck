# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Project Classes."""

from dataclasses import dataclass
from typing import Dict, List

from NBDM.model.building import NBDM_Building
from NBDM.model.site import NBDM_Site
from NBDM.model.building import NBDM_BuildingSegment


@dataclass
class NBDM_Variant:
    variant_name: str
    building: NBDM_Building

    def get_building_segment(self, _name: str) -> NBDM_BuildingSegment:
        return self.building.get_building_segment(_name)

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_Variant":
        obj = cls(
            variant_name=_d["variant_name"],
            building=NBDM_Building.from_dict(_d["building"]),
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(
            vars(obj).keys(), _d.keys()
        )
        return obj


@dataclass
class NBDM_Variants:
    proposed: NBDM_Variant
    baseline: NBDM_Variant

    @property
    def building_segment_names(self) -> List[str]:
        baseline_bldg_seg_names = self.baseline.building.building_segment_names
        proposed_bldg_seg_names = self.proposed.building.building_segment_names
        assert baseline_bldg_seg_names == proposed_bldg_seg_names
        return baseline_bldg_seg_names

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_Variants":
        obj = cls(
            proposed=NBDM_Variant.from_dict(_d["proposed"]),
            baseline=NBDM_Variant.from_dict(_d["baseline"]),
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(
            vars(obj).keys(), _d.keys()
        )
        return obj

    def __iter__(self):
        for _ in (self.proposed, self.baseline):
            yield _


@dataclass
class NBDM_Project:
    project_name: str
    client: str
    site: NBDM_Site
    variants: NBDM_Variants

    @property
    def building_segment_names(self) -> List[str]:
        return self.variants.building_segment_names

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_Project":
        obj = cls(
            project_name=_d["project_name"],
            client=_d["client"],
            site=NBDM_Site.from_dict(_d["site"]),
            variants=NBDM_Variants.from_dict(_d["variants"]),
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(
            vars(obj).keys(), _d.keys()
        )
        return obj
