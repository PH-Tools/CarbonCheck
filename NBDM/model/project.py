# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Project Classes."""

from dataclasses import dataclass
from typing import Dict

from NBDM.model.building import NBDM_Building
from NBDM.model.site import NBDM_Site


@dataclass
class NBDM_Variant:
    variant_name: str
    building: NBDM_Building

    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_Variant':
        obj = cls(
            variant_name=_d['variant_name'],
            building=NBDM_Building.from_dict(_d['building']),
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj


@dataclass
class NBDM_Variants:
    proposed: NBDM_Variant
    baseline: NBDM_Variant

    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_Variants':
        obj = cls(
            proposed = NBDM_Variant.from_dict(_d['proposed']),
            baseline = NBDM_Variant.from_dict(_d['baseline']),
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
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

    @classmethod
    def from_dict(cls, _d: Dict) -> 'NBDM_Project':
        obj = cls(
            project_name=_d['project_name'],
            client=_d['client'],
            site=NBDM_Site.from_dict(_d['site']),
            variants=NBDM_Variants.from_dict(_d['variants']),
        )
        assert vars(obj).keys() == _d.keys(), "Error: Key mismatch: {} <--> {}".format(vars(obj).keys(), _d.keys())
        return obj