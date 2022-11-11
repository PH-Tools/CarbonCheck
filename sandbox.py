from tests.conftest import sample_Project
from NBDM.to_JSON import write
from NBDM.from_JSON import read
import pathlib

json_file = pathlib.Path("example.json")
write.NBDM_Project_to_json_file(sample_Project, json_file)
project = read.NBDM_Project_from_json_file(json_file)