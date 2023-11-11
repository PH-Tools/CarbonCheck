from NBDM.from_WUFI_PDF.pdf_reader import PDFReader
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC
from pathlib import Path

reader = PDFReader()
reader.extract_pdf_text(Path("tests/_source_pdf/ridgeway_proposed.pdf"))


# site_energy = reader.pdf_sections.get_section(WufiPDF_SiteEnergyMonthly)
# site_energy.process_section_text()
# print(site_energy.table_electricity_kwh.total_consumption_kbtu)
# print(site_energy.table_electricity_kwh.total_consumption_kwh)
