# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to create NBDM BuildingSegment objects from WUFI-PDF data."""

from typing import Dict

from NBDM.model import geometry
from NBDM.from_WUFI_PDF.pdf_sections.typing import PDFSectionType
from NBDM.from_WUFI_PDF.pdf_sections.bldg_info import BuildingInformation


def build_NBDM_geometryFromWufiPDF(
    _pdf_data: Dict[str, PDFSectionType]
) -> geometry.NBDM_BuildingSegmentGeometry:
    bldg_info: BuildingInformation = _pdf_data[BuildingInformation.__pdf_heading_string__]  # type: ignore
    return geometry.NBDM_BuildingSegmentGeometry(
        area_envelope=bldg_info.total_area_envelope,
        area_floor_area_net_interior_weighted=bldg_info.floor_area,
        volume_net_interior=bldg_info.enclosed_volume,
    )
