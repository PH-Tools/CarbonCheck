# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for setting the PHPP envelope constructions to the baseline values. """

from PHX.PHPP import phpp_app
from PHX.PHPP.phpp_model.areas_surface import ExistingSurfaceRow
from PHX.model.enums.building import ComponentFaceType, ComponentExposureExterior

from ph_baseliner.codes.model import BaselineCode
from ph_baseliner.codes.options import ClimateZones
from ph_baseliner.phpp.u_values import (create_baseline_constructions, 
            add_baseline_constructions_to_phpp, BaselineConstructionPHPPids)

def set_baseline_envelope_constructions(
        phpp_conn: phpp_app.PHPPConnection,
        baseline_code: BaselineCode,
        climate_zone: ClimateZones,
) -> None:
    """Set the PHPP Areas worksheet envelope constructions to the baseline values.
    
    Will create and add new Constructions to the PHPP U-Values worksheet, and the 
    PHPP Areas worksheet surfaces will each be updated to use the new constructions.

    Arguments:
    ----------
        * phpp_conn: phpp_app.PHPPConnection:
            The PHPP Connection
        * baseline_code: BaselineCode:
            The baseline code
        * climate_zone: ClimateZones:
            The climate zone
    """
    baseline_constructions = create_baseline_constructions(baseline_code, climate_zone)
    construction_phpp_ids = add_baseline_constructions_to_phpp(phpp_conn, baseline_constructions)
    reset_phpp_areas_constructions(phpp_conn, construction_phpp_ids)

def reset_phpp_areas_constructions(
        phpp_conn: phpp_app.PHPPConnection, 
        construction_ids: BaselineConstructionPHPPids
) -> None:
    """Reset the PHPP Areas worksheet to the baseline constructions."""
    
    def row_is_exposed_wall(row_data: ExistingSurfaceRow) -> bool:
        """Exposed wall is a wall that is not a ground floor."""
        return row_data.face_type == ComponentFaceType.WALL and row_data.face_exposure == ComponentExposureExterior.EXTERIOR

    def row_is_ground_wall(row_data: ExistingSurfaceRow) -> bool:
        """Ground wall is a wall that is a ground floor."""
        return row_data.face_type == ComponentFaceType.WALL and row_data.face_exposure == ComponentExposureExterior.GROUND

    def row_is_roof(row_data: ExistingSurfaceRow) -> bool:
        """Roof is a roof that is not a ground floor."""
        return row_data.face_type == ComponentFaceType.ROOF_CEILING and row_data.face_exposure == ComponentExposureExterior.EXTERIOR

    def row_is_ground_floor(row_data: ExistingSurfaceRow) -> bool:
        """Ground floor is a floor that is a ground floor."""
        return row_data.face_type == ComponentFaceType.FLOOR and row_data.face_exposure == ComponentExposureExterior.GROUND

    def row_is_exposed_floor(row_data: ExistingSurfaceRow) -> bool:
        """Exposed floor is a floor that is not a ground floor."""
        return row_data.face_type == ComponentFaceType.FLOOR and row_data.face_exposure == ComponentExposureExterior.EXTERIOR
        
    for i, surface_row_data in phpp_conn.areas.surfaces.all_surface_rows:
        
        if surface_row_data.no_name:
            continue
        
        if row_is_roof(surface_row_data):
            phpp_conn.areas.set_surface_row_construction(i, construction_ids.roof)
            phpp_conn.areas.set_surface_row_solar_absorptivity(i, 0.75)
            phpp_conn.areas.set_surface_row_emissivity(i, 0.90)
        elif row_is_exposed_wall(surface_row_data):
            phpp_conn.areas.set_surface_row_construction(i, construction_ids.exposed_wall)
            phpp_conn.areas.set_surface_row_solar_absorptivity(i, 0.75)
            phpp_conn.areas.set_surface_row_emissivity(i, 0.90)
        elif row_is_ground_wall(surface_row_data):
            phpp_conn.areas.set_surface_row_construction(i, construction_ids.ground_wall)
        elif row_is_exposed_floor(surface_row_data):
            phpp_conn.areas.set_surface_row_construction(i, construction_ids.exposed_floor)
            phpp_conn.areas.set_surface_row_solar_absorptivity(i, 0.75)
            phpp_conn.areas.set_surface_row_emissivity(i, 0.90)
        elif row_is_ground_floor(surface_row_data):
            phpp_conn.areas.set_surface_row_construction(i, construction_ids.ground_floor)