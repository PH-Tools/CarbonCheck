# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM_Site object from PHPP data."""


from PHX.PHPP import phpp_app

from NBDM.model.site import NBDM_Site


def create_NBDM_Site(_phpp_conn: phpp_app.PHPPConnection) -> NBDM_Site:
    """Return a new NBDM_Site object with attributes set to a source PHPP.

    Arguments:
    ----------
        * _phpp_conn: (phpp_app.PHPPConnection) THe PHPP Connection object.

    Returns:
    --------
        * (NBDM_Site): A new NBDM_Site object with the values set from the source
            PHPP Excel document.
    """

    new_site = NBDM_Site()

    # -- Get the Site Address data
    data_arch = _phpp_conn.verification.read_building()
    for attr, val in vars(data_arch).items():
        setattr(new_site.location.address, attr, val)

    # -- Pull in the climate-related data for the location
    new_site.location.latitude = _phpp_conn.climate.read_latitude()
    new_site.location.longitude = _phpp_conn.climate.read_longitude()

    # -- Get Climate Data
    new_site.climate.country = _phpp_conn.climate.read_active_country()
    new_site.climate.region = _phpp_conn.climate.read_active_region()
    new_site.climate.data_set = _phpp_conn.climate.read_active_data_set()

    return new_site
