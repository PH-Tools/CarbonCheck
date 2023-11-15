import pathlib

from rich import print
from PHX.from_WUFI_XML.read_WUFI_XML_file import get_WUFI_XML_file_as_dict
from PHX.from_WUFI_XML.phx_converter import convert_WUFI_XML_to_PHX_project

from PHX.from_WUFI_XML.wufi_file_schema import WUFIplusProject


file_paths = [
    pathlib.Path(
        "/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/tests/_source_wufi_xml/la_mora_proposed.xml"
    ),
    pathlib.Path(
        "/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/CarbonCheck/tests/_source_wufi_xml/la_mora_baseline.xml"
    ),
]

for file_path in file_paths:
    # ----------------------------------------------------------------
    # -- 1) Read in the WUFI-XML File as a new Pydantic Model
    print(f"[green bold]> Reading in data from XML-File: {file_path}[/green bold]")
    wufi_xml_data = get_WUFI_XML_file_as_dict(file_path)
    wufi_xml_model = WUFIplusProject.parse_obj(wufi_xml_data)

    # ----------------------------------------------------------------
    # -- 2) Convert the Pydantic WUFI model over to a PHX model
    print(f"[green bold]> Converting XML-data to a PHX-Model[/green bold]")
    phx_project = convert_WUFI_XML_to_PHX_project(wufi_xml_model)
    print(phx_project.name)
