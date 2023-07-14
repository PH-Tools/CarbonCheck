# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM Envelope from PHPP."""

from PHX.PHPP.phpp_app import PHPPConnection

from NBDM.model.envelope import NBDM_BuildingSegmentEnvelope, NBDM_EnvelopeAssembly


def create_NBDM_Envelope(_phpp_conn: PHPPConnection) -> NBDM_BuildingSegmentEnvelope:
    """Read in data from a PHPP document and create a new NBDM_BuildingSegmentEnvelope Object."""
    new_obj = NBDM_BuildingSegmentEnvelope()

    for assembly in _phpp_conn.u_values.get_all_envelope_assemblies():
        new_assembly = NBDM_EnvelopeAssembly(
            name=assembly.name,
            u_value=assembly.u_value,
            r_value=assembly.r_value,
            ext_exposure=assembly.ext_exposure,
            int_exposure=assembly.int_exposure,
        )
        new_obj.add_envelope_assembly(new_assembly)

    return new_obj
