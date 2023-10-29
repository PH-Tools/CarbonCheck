# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create NBDM_Team object from WUFI-PDF data."""


from NBDM.model.team import NBDM_Team


def create_NBDM_Team_from_WufiPDF(_pdf_data) -> NBDM_Team:
    new_team = NBDM_Team()

    return new_team
