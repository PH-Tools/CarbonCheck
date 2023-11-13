from NBDM.from_WUFI_PDF.pdf_reader import PDFReader
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC
from NBDM.from_WUFI_PDF.pdf_sections.site_energy_monthly import WufiPDF_SiteEnergyMonthly
from pathlib import Path
from NBDM.from_WUFI_PDF import create_NBDM_BuildingSegmentFromWufiPDF

reader = PDFReader()
file_path = Path("tests/_source_pdf/la_mora_baseline.pdf")
reader.extract_pdf_text_from_file(file_path)
if site_energy := reader.pdf_sections.get_section(WufiPDF_SiteEnergyMonthly):
    print(site_energy.table_electricity_kwh.total_consumption_kbtu)
    print(site_energy.table_electricity_kwh.total_consumption_kwh)

new_project = create_NBDM_BuildingSegmentFromWufiPDF(reader.pdf_sections)
print(new_project.segment_name)
