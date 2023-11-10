# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create NBDM_Site object from WUFI-PDF data."""

from typing import Dict
from NBDM.model.site import NBDM_Site, NBDM_Climate, NBDM_Location, NBDM_ProjectAddress
from NBDM.from_WUFI_PDF.pdf_reader import WufiPDF_SectionType
from NBDM.from_WUFI_PDF.pdf_sections.climate_summary import WufiPDF_ClimateSummary
from NBDM.from_WUFI_PDF.pdf_sections.site import WufiPDF_PropertySite
from NBDM.from_WUFI_PDF.pdf_sections.project_data import WufiPDF_ProjectData
from rich import print


def create_NBDM_Climate_from_WufiPDF(
    _pdf_data: Dict[str, WufiPDF_SectionType]
) -> NBDM_Climate:
    """Create NBDM_Climate object from WUFI-PDF data."""

    new_climate = NBDM_Climate()

    # -- Pull out the data from the PDF dict, if it exists
    pdf_climate_section: WufiPDF_PropertySite
    if pdf_climate_section := _pdf_data.get(WufiPDF_PropertySite.__pdf_heading_string__, None):  # type: ignore
        new_climate.zone_passive_house = pdf_climate_section.zone_passive_house
        new_climate.data_set = pdf_climate_section.data_set

    pdf_proj_data_section: WufiPDF_ProjectData
    if pdf_proj_data_section := _pdf_data.get(WufiPDF_ProjectData.__pdf_heading_string__, None):  # type: ignore
        new_climate.country = pdf_proj_data_section.building.country
        new_climate.region = pdf_proj_data_section.building.state

    return new_climate


def create_NBDM_BuildingAddress_from_WufiPDF(
    _pdf_data: WufiPDF_ProjectData,
) -> NBDM_ProjectAddress:
    """Create NBDM_ProjectAddress object from WUFI-PDF data."""

    new_address = NBDM_ProjectAddress()

    new_address.building_number = _pdf_data.building.building_number
    new_address.street_name = _pdf_data.building.street
    new_address.city = _pdf_data.building.locality
    new_address.state = _pdf_data.building.state
    new_address.post_code = _pdf_data.building.postal_code

    return new_address


def create_NBDM_Location_from_WufiPDF(
    _pdf_data: Dict[str, WufiPDF_SectionType]
) -> NBDM_Location:
    """Create NBDM_Location object from WUFI-PDF data."""

    new_location = NBDM_Location()

    # -- Pull out the data from the PDF dict, if it exists
    pdf_section_project_data: WufiPDF_ProjectData
    if pdf_section_project_data := _pdf_data.get(WufiPDF_ProjectData.__pdf_heading_string__, None):  # type: ignore
        new_location.address = create_NBDM_BuildingAddress_from_WufiPDF(
            pdf_section_project_data
        )

    pdf_section_climate: WufiPDF_ClimateSummary
    if pdf_section_climate := _pdf_data.get(WufiPDF_ClimateSummary.__pdf_heading_string__, None):  # type: ignore
        new_location.longitude = pdf_section_climate.longitude
        new_location.latitude = pdf_section_climate.latitude

    return new_location


def create_NBDM_Site_from_WufiPDF(_pdf_data: Dict[str, WufiPDF_SectionType]) -> NBDM_Site:
    """Create NBDM_Site object from WUFI-PDF data."""

    new_site = NBDM_Site()
    new_site.climate = create_NBDM_Climate_from_WufiPDF(_pdf_data)
    new_site.location = create_NBDM_Location_from_WufiPDF(_pdf_data)

    return new_site
