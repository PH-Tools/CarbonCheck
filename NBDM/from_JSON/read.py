# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to create an NBDM model from a .JSON file."""

import json
import pathlib

from NBDM.model.project import NBDM_Project


def NBDM_Project_from_json_file(_json_file: pathlib.Path) -> NBDM_Project:
    # -- Load the file contents as a python dict
    with _json_file.open() as f:
        d = json.load(f)

    return NBDM_Project.from_dict(d)
