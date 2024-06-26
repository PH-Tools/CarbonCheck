# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Team Member and Contact Information Classes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from NBDM.model import serialization


@dataclass
class NBDM_TeamContactInfo:
    """Contact Information for an individual team member."""

    building_number: str = "-"
    street_name: str = "-"
    city: str = "-"
    state: str = "-"
    country: str = "-"
    post_code: str = "-"
    phone: str = "-"
    email: str = "-"

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_TeamContactInfo:
        return serialization.build_NBDM_obj_from_dict(cls, _d)


@dataclass
class NBDM_TeamMember:
    """An individual team member."""

    name: str = "-"
    contact_info: NBDM_TeamContactInfo = field(default_factory=NBDM_TeamContactInfo)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_TeamMember:
        return serialization.build_NBDM_obj_from_dict(cls, _d)


@dataclass
class NBDM_Team:
    """A collection of Team member information."""

    site_owner: NBDM_TeamMember = field(default_factory=NBDM_TeamMember)
    designer: NBDM_TeamMember = field(default_factory=NBDM_TeamMember)
    contractor: NBDM_TeamMember = field(default_factory=NBDM_TeamMember)
    primary_energy_consultant: NBDM_TeamMember = field(default_factory=NBDM_TeamMember)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Team:
        return serialization.build_NBDM_obj_from_dict(cls, _d)
