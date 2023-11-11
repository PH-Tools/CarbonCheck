# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create NBDM_Site object from WUFI-PDF data."""


from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.climate_summary import WufiPDF_ClimateSummary
from NBDM.from_WUFI_PDF.pdf_sections.project_data import WufiPDF_ProjectData
from NBDM.from_WUFI_PDF.pdf_sections.site import WufiPDF_PropertySite
from NBDM.model.site import NBDM_Climate, NBDM_Location, NBDM_ProjectAddress, NBDM_Site


def create_NBDM_Climate_from_WufiPDF(_pdf_data: PDFSectionsCollection) -> NBDM_Climate:
    """Create NBDM_Climate object from WUFI-PDF data."""

    new_climate = NBDM_Climate()

    # -- Pull out the data from the PDF dict, if it exists
    if pdf_climate_section := _pdf_data.get_section(WufiPDF_PropertySite):
        new_climate.zone_passive_house = pdf_climate_section.zone_passive_house
        new_climate.data_set = pdf_climate_section.data_set

    if pdf_proj_data_section := _pdf_data.get_section(WufiPDF_ProjectData):
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


def create_NBDM_Location_from_WufiPDF(_pdf_data: PDFSectionsCollection) -> NBDM_Location:
    """Create NBDM_Location object from WUFI-PDF data."""

    new_location = NBDM_Location()

    if pdf_section_project_data := _pdf_data.get_section(WufiPDF_ProjectData):
        new_location.address = create_NBDM_BuildingAddress_from_WufiPDF(
            pdf_section_project_data
        )

    if pdf_section_climate := _pdf_data.get_section(WufiPDF_ClimateSummary):
        new_location.longitude = pdf_section_climate.longitude
        new_location.latitude = pdf_section_climate.latitude

    return new_location


def create_NBDM_Site_from_WufiPDF(_pdf_data: PDFSectionsCollection) -> NBDM_Site:
    """Create NBDM_Site object from WUFI-PDF data."""

    new_site = NBDM_Site()
    new_site.climate = create_NBDM_Climate_from_WufiPDF(_pdf_data)
    new_site.location = create_NBDM_Location_from_WufiPDF(_pdf_data)

    return new_site
