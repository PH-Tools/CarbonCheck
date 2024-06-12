import os
import pathlib

from NBDM.from_JSON.read import NBDM_Project_from_json_file
from NBDM.model.project import NBDM_Project
from NBDM.to_JSON.write import NBDM_Project_to_json_file

JSON_FILE = pathlib.Path("tests/_source_json/la_mora.json")


def test_read_json_file_succeeds() -> None:
    new_nbdm_project = NBDM_Project_from_json_file(JSON_FILE)
    assert isinstance(new_nbdm_project, NBDM_Project)


def test_read_json_file_then_write_out() -> None:
    nbdm_project_from_file = NBDM_Project_from_json_file(JSON_FILE)

    # -- Write out the project to a file
    WRITE_FILE = pathlib.Path("__test_json_output_file__.json")
    try:
        NBDM_Project_to_json_file(nbdm_project_from_file, WRITE_FILE)
        assert pathlib.Path.exists(WRITE_FILE)
    finally:
        if pathlib.Path.exists(WRITE_FILE):
            os.remove(WRITE_FILE)
