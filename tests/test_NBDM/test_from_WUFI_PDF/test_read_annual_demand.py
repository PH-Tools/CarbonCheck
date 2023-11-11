from typing import Dict, Any
from NBDM.from_WUFI_PDF.pdf_sections.__typing import SupportsWufiPDF_Section
from NBDM.from_WUFI_PDF.pdf_sections.annual_demand import (
    WufiPDF_AnnualHeatingAndCoolingDemand,
    AnnualDemand,
)

from ph_units.unit_type import Unit


def test_pdf_read_sections_heating_demand(
    sample_pdf_data_ridgeway: Dict[str, SupportsWufiPDF_Section]
) -> None:
    section_key = WufiPDF_AnnualHeatingAndCoolingDemand.__pdf_heading_string__
    pdf_section: Any = sample_pdf_data_ridgeway[section_key]
    demand: AnnualDemand = pdf_section.heating_demand

    assert demand.transmission_losses == Unit(611713.0, "KBTU")
    assert demand.ventilation_losses == Unit(322960.0, "KBTU")
    assert demand.total_heat_losses == Unit(934673.0, "KBTU")
    assert demand.solar_heat_gains == Unit(250855.0, "KBTU")
    assert demand.internal_heat_gains == Unit(495426.0, "KBTU")
    assert demand.total_heat_gains == Unit(746280.0, "KBTU")
    assert demand.useful_heat_gains == Unit(619581.0, "KBTU")
    assert demand.utilization_factor == Unit(0.83, "%")
    assert demand.annual_heat_demand == Unit(315092.0, "KBTU")
    assert demand.specific_annual_heat_demand == Unit(0.0, "KBTU/FTU")
    assert demand.annual_cooling_demand == Unit(0.0, "KBTU")
    assert demand.cooling_demand_sensible == Unit(0.0, "KBTU")
    assert demand.cooling_demand_latent == Unit(0.0, "KBTU")


def test_pdf_read_sections_cooling_demand(
    sample_pdf_data_ridgeway: Dict[str, SupportsWufiPDF_Section]
) -> None:
    section_key = WufiPDF_AnnualHeatingAndCoolingDemand.__pdf_heading_string__
    pdf_section: Any = sample_pdf_data_ridgeway[section_key]
    demand: AnnualDemand = pdf_section.cooling_demand

    assert demand.transmission_losses == Unit(1149853.0, "KBTU")
    assert demand.ventilation_losses == Unit(1911881.0, "KBTU")
    assert demand.total_heat_losses == Unit(3061734.0, "KBTU")
    assert demand.solar_heat_gains == Unit(399453.0, "KBTU")
    assert demand.internal_heat_gains == Unit(934143.0, "KBTU")
    assert demand.total_heat_gains == Unit(1333597.0, "KBTU")
    assert demand.useful_heat_gains == Unit(0.0, "KBTU")
    assert demand.utilization_factor == Unit(0.0, "%")
    assert demand.annual_heat_demand == Unit(0.0, "KBTU")
    assert demand.specific_annual_heat_demand == Unit(0.0, "KBTU/FTU")
    assert demand.annual_cooling_demand == Unit(421458.0, "KBTU")
    assert demand.cooling_demand_sensible == Unit(299393.0, "KBTU")
    assert demand.cooling_demand_latent == Unit(122065.0, "KBTU")
