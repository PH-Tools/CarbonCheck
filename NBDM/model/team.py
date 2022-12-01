# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Team Member and Contact Information Classes."""

from dataclasses import dataclass
from typing import Dict
from NBDM.model import serialization


@dataclass
class NBDM_TeamContactInfo:
    """Contact Information for an individual team member."""

    building_number: str
    street_name: str
    city: str
    state: str
    zip_code: str
    phone: str
    email: str

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_TeamContactInfo":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)


@dataclass
class NBDM_TeamMember:
    """An individual team member."""

    name: str
    contact_info: NBDM_TeamContactInfo

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_TeamMember":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)


@dataclass
class NBDM_Team:
    """A collection of Team member information."""

    site_owner: NBDM_TeamMember
    designer: NBDM_TeamMember
    contractor: NBDM_TeamMember
    primary_energy_consultant: NBDM_TeamMember

    @classmethod
    def from_dict(cls, _d: Dict) -> "NBDM_Team":
        attr_dict = serialization.build_attr_dict(cls, _d)
        return cls(**attr_dict)
