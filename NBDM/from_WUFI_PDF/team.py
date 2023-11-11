# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create NBDM_Team object from WUFI-PDF data."""


from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.project_data import (
    WufiPDF_BuildingAddress,
    WufiPDF_ProjectData,
)
from NBDM.model.team import NBDM_Team, NBDM_TeamContactInfo, NBDM_TeamMember


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


def create_NBDM_Team_from_WufiPDF(_pdf_data: PDFSectionsCollection) -> NBDM_Team:
    new_team = NBDM_Team()

    if owner_data := _pdf_data.get_section(WufiPDF_ProjectData):
        new_team.site_owner = team_member_from_WufiPDF_data(owner_data.owner)
        new_team.primary_energy_consultant = team_member_from_WufiPDF_data(
            owner_data.responsible
        )
        new_team.designer = team_member_from_WufiPDF_data(owner_data.responsible)

    return new_team
