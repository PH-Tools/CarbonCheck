# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Function to write out an NBDM model to a .JSON file."""

import json
import pathlib

from NBDM.model import serialization
from NBDM.model.project import NBDM_Project


def NBDM_Project_to_json_file(_project: NBDM_Project, _output_file: pathlib.Path) -> None:
    """Write out an NBDM model to a .JSON file."""
    d = serialization.to_dict(_project)
    json_object = json.dumps(d, indent=4)
    _output_file.write_text(json_object)
