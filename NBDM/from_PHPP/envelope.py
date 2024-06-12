# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Envelope from PHPP."""

from typing import List

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.envelope import (
    NBDM_AssemblyType,
    NBDM_BuildingSegmentEnvelope,
    NBDM_GlazingType,
)


def create_NBDM_Constructions(_phpp_conn: PHPPConnection) -> List[NBDM_AssemblyType]:
    """Read in data from a PHPP document and create a list of NBDM_EnvelopeAssembly Objects."""
    used_const_names = _phpp_conn.areas.surfaces.get_all_construction_names()

    nbdm_assembly_types = []
    for assembly_type in _phpp_conn.u_values.get_all_envelope_assemblies():
        if assembly_type.name not in used_const_names:
            continue

        new_nbdm_assembly = NBDM_AssemblyType(
            name=assembly_type.name,
            u_value=assembly_type.u_value,
            r_value=assembly_type.r_value,
            ext_exposure=assembly_type.ext_exposure,
            int_exposure=assembly_type.int_exposure,
        )
        nbdm_assembly_types.append(new_nbdm_assembly)

    return nbdm_assembly_types


def create_NBDM_GlazingTypes(_phpp_conn: PHPPConnection) -> List[NBDM_GlazingType]:
    used_glazing_names = _phpp_conn.windows.get_all_glazing_names()

    nbdm_glazing_types = []
    for glazing_type in _phpp_conn.components.glazings.get_all_glazing_types():
        if glazing_type.name not in used_glazing_names:
            continue

        new_nbdm_glazing_type = NBDM_GlazingType(
            display_name=glazing_type.name,
            u_value=glazing_type.u_value,
            g_value=glazing_type.g_value,
        )
        nbdm_glazing_types.append(new_nbdm_glazing_type)

    return nbdm_glazing_types


def create_NBDM_Envelope(_phpp_conn: PHPPConnection) -> NBDM_BuildingSegmentEnvelope:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentEnvelope Object."""
    new_obj = NBDM_BuildingSegmentEnvelope()
    for nbdm_assembly in create_NBDM_Constructions(_phpp_conn):
        new_obj.add_assembly_type(nbdm_assembly)

    for nbdm_aperture_type in create_NBDM_GlazingTypes(_phpp_conn):
        new_obj.add_glazing_type(nbdm_aperture_type)

    return new_obj
