# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create NBDM_Team object from PHPP data."""


from PHX.PHPP import phpp_app
from NBDM.model.team import NBDM_Team


def create_NBDM_Team(_phpp_conn: phpp_app.PHPPConnection) -> NBDM_Team:
    """Return a new NBDM_Team object with attributes set to a source PHPP.

    Arguments:
    ----------
        * _phpp_conn: (phpp_app.PHPPConnection) THe PHPP Connection object.

    Returns:
    --------
        * (NBDM_Team): A new NBDM_Team object with the values set from the source
            PHPP Excel document.
    """

    new_team = NBDM_Team()

    # -- Go read in all the PHPP info from the Variants worksheet
    # -- and set the attributes of the new team members
    data_arch = _phpp_conn.verification.read_architect()
    new_team.designer.name = data_arch.name
    for attr, val in vars(data_arch).items():
        setattr(new_team.designer.contact_info, attr, val)

    data_energy_consultant = _phpp_conn.verification.read_energy_consultant()
    new_team.primary_energy_consultant.name = data_energy_consultant.name
    for attr, val in vars(data_energy_consultant).items():
        setattr(new_team.primary_energy_consultant.contact_info, attr, val)

    data_site_owner = _phpp_conn.verification.read_site_owner()
    new_team.site_owner.name = data_site_owner.name
    for attr, val in vars(data_site_owner).items():
        setattr(new_team.site_owner.contact_info, attr, val)

    return new_team
