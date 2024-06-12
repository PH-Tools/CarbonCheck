from pathlib import Path

from rich import print

from NBDM.from_WUFI_PDF import (
    create_NBDM_Appliances_from_WufiPDF,
    create_NBDM_BuildingSegmentFromWufiPDF,
    create_NBDM_Cooling_Systems_from_WufiPDF,
    create_NBDM_DHW_Systems_from_WufiPDF,
    create_NBDM_Envelope_from_WufiPDF,
    create_NBDM_Heating_Systems_from_WufiPDF,
    create_NBDM_Renewable_Systems_from_WufiPDF,
    create_NBDM_Site_from_WufiPDF,
    create_NBDM_Team_from_WufiPDF,
    create_NBDM_Vent_Systems_from_WufiPDF,
)
from NBDM.from_WUFI_PDF.pdf_reader import PDFReader
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC
from NBDM.from_WUFI_PDF.pdf_sections.site_energy_monthly import (
    WufiPDF_SiteEnergyMonthly,
)
from NBDM.model.project import NBDM_Project

reader = PDFReader()
file_path = Path("tests/_source_pdf/la_mora_proposed.pdf")
reader.extract_pdf_text_from_file(file_path)

new_project = NBDM_Project()
# new_project.appliances = create_NBDM_Appliances_from_WufiPDF(reader.pdf_sections)
new_project.renewable_systems = create_NBDM_Renewable_Systems_from_WufiPDF(
    reader.pdf_sections
)
# new_project.cooling_systems = create_NBDM_Cooling_Systems_from_WufiPDF(
#     reader.pdf_sections
# )
# new_project.dhw_systems = create_NBDM_DHW_Systems_from_WufiPDF(reader.pdf_sections)
print(new_project.renewable_systems)
