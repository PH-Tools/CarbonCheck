# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create NBDM Envelope from WUFI-PDF."""


from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.assemblies_win_types import (
    WufiPDF_AssemblyAndWindowTypes,
    WufiPDF_AssemblyType,
    WufiPDF_WindowType,
)
from NBDM.model.envelope import (
    NBDM_AssemblyType,
    NBDM_BuildingSegmentEnvelope,
    NBDM_GlazingType,
)


def create_NBDM_AssemblyType_from_WufiPDF(
    _assembly_type: WufiPDF_AssemblyType,
) -> NBDM_AssemblyType:
    """Create NBDM AssemblyType from WUFI-PDF."""

    return NBDM_AssemblyType(
        name=_assembly_type.name,
        u_value=_assembly_type.u_value,
        r_value=_assembly_type.r_value,
        ext_exposure="NA",
        int_exposure="NA",
    )


def create_NBDM_GlazingType_from_WufiPDF(
    _window_type: WufiPDF_WindowType,
) -> NBDM_GlazingType:
    """Create NBDM GlazingType from WUFI-PDF."""

    return NBDM_GlazingType(
        display_name=_window_type.name,
        u_value=_window_type.u_value,
        g_value=_window_type.g_value,
    )


def create_NBDM_Envelope_from_WufiPDF(
    _pdf_data: PDFSectionsCollection,
) -> NBDM_BuildingSegmentEnvelope:
    """Create NBDM Envelope from WUFI-PDF."""

    new_obj = NBDM_BuildingSegmentEnvelope()

    if envelope_data := _pdf_data.get_section(WufiPDF_AssemblyAndWindowTypes):
        for assembly_type in envelope_data._assembly_types:
            new_obj.add_assembly_type(
                create_NBDM_AssemblyType_from_WufiPDF(assembly_type)
            )
        for window_type in envelope_data._window_types:
            new_obj.add_glazing_type(create_NBDM_GlazingType_from_WufiPDF(window_type))

    return new_obj
