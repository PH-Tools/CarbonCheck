# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create NBDM_Team object from WUFI-PDF data."""

from typing import Dict, Optional
from NBDM.model.team import NBDM_Team, NBDM_TeamMember, NBDM_TeamContactInfo
from NBDM.from_WUFI_PDF.pdf_reader import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections.project_data import (
    WufiPDF_ProjectData,
    WufiPDF_BuildingAddress,
)


def team_member_contact_info_from_WufiPDF_data(
    _pdf_data: WufiPDF_BuildingAddress,
) -> NBDM_TeamContactInfo:
    new_contact_info = NBDM_TeamContactInfo()

    new_contact_info.building_number = _pdf_data.building_number
    new_contact_info.street_name = _pdf_data.street
    new_contact_info.city = _pdf_data.locality
    new_contact_info.country = _pdf_data.country
    new_contact_info.post_code = _pdf_data.postal_code

    return new_contact_info


def team_member_from_WufiPDF_data(_pdf_data: WufiPDF_BuildingAddress) -> NBDM_TeamMember:
    new_team_member = NBDM_TeamMember()

    new_team_member.name = _pdf_data.name
    new_team_member.contact_info = team_member_contact_info_from_WufiPDF_data(_pdf_data)

    return new_team_member


def create_NBDM_Team_from_WufiPDF(_pdf_data: Dict[str, WufiPDF_SectionType]) -> NBDM_Team:
    new_team = NBDM_Team()

    owner_data: Optional[WufiPDF_ProjectData] = None
    if owner_data := _pdf_data.get(WufiPDF_ProjectData.__pdf_heading_string__, None):  # type: ignore
        new_team.site_owner = team_member_from_WufiPDF_data(owner_data.owner)
        new_team.primary_energy_consultant = team_member_from_WufiPDF_data(
            owner_data.responsible
        )
        new_team.designer = team_member_from_WufiPDF_data(owner_data.responsible)

    return new_team
