# -----------------------------------------------------------------------------
# -- Import functions for ease of access
from NBDM.from_WUFI_PDF.appliances import create_NBDM_Appliances_from_WufiPDF
from NBDM.from_WUFI_PDF.bldg_segment import create_NBDM_BuildingSegmentFromWufiPDF
from NBDM.from_WUFI_PDF.cooling_systems import create_NBDM_Cooling_Systems_from_WufiPDF
from NBDM.from_WUFI_PDF.dhw_systems import create_NBDM_DHW_Systems_from_WufiPDF
from NBDM.from_WUFI_PDF.envelope import create_NBDM_Envelope_from_WufiPDF
from NBDM.from_WUFI_PDF.heating_systems import create_NBDM_Heating_Systems_from_WufiPDF
from NBDM.from_WUFI_PDF.renewable_systems import (
    create_NBDM_Renewable_Systems_from_WufiPDF,
)
from NBDM.from_WUFI_PDF.site import create_NBDM_Site_from_WufiPDF
from NBDM.from_WUFI_PDF.team import create_NBDM_Team_from_WufiPDF
from NBDM.from_WUFI_PDF.ventilation_systems import create_NBDM_Vent_Systems_from_WufiPDF

# -----------------------------------------------------------------------------
from NBDM.from_WUFI_PDF.pdf_reader import PDFReader

# -- Import all of the section types. NOTE: we can't do this
# -- dynamically (searching through the folder...) cus' if we do that, the
# -- packager (cxFreeze | PyInstaller) won't find all the required modules.
from NBDM.from_WUFI_PDF.pdf_sections._default import _WufiPDF_DefaultSection
from NBDM.from_WUFI_PDF.pdf_sections.annual_demand import (
    WufiPDF_AnnualHeatingAndCoolingDemand,
)
from NBDM.from_WUFI_PDF.pdf_sections.areas import WufiPDF_Areas
from NBDM.from_WUFI_PDF.pdf_sections.assemblies_win_types import (
    WufiPDF_AssemblyAndWindowTypes,
)
from NBDM.from_WUFI_PDF.pdf_sections.aux_electric import WufiPDF_AuxElectricity
from NBDM.from_WUFI_PDF.pdf_sections.bldg_info import WufiPDF_BuildingInformation
from NBDM.from_WUFI_PDF.pdf_sections.building_elements import WufiPDF_BuildingElements
from NBDM.from_WUFI_PDF.pdf_sections.calc_parameters import WufiPDF_CalculationParameters
from NBDM.from_WUFI_PDF.pdf_sections.climate_detailed import WufiPDF_ClimateDetailed
from NBDM.from_WUFI_PDF.pdf_sections.climate_summary import WufiPDF_ClimateSummary
from NBDM.from_WUFI_PDF.pdf_sections.dhw_and_distribution import (
    WufiPDF_DHWandDistribution,
)
from NBDM.from_WUFI_PDF.pdf_sections.envelope_summary import WufiPDF_EnvelopeSummary
from NBDM.from_WUFI_PDF.pdf_sections.heat_flow_heating import (
    WufiPDF_HeatingSeasonHeatFlows,
)
from NBDM.from_WUFI_PDF.pdf_sections.hvac import WufiPDF_HVAC
from NBDM.from_WUFI_PDF.pdf_sections.internal_gains import WufiPdf_InternalGains
from NBDM.from_WUFI_PDF.pdf_sections.peak_load import WufiPDF_PeakHeatingAndCoolingLoad
from NBDM.from_WUFI_PDF.pdf_sections.ph_data import WufiPDF_PassiveHouseData
from NBDM.from_WUFI_PDF.pdf_sections.ph_recommendations import WufiPDF_PHRecommendations
from NBDM.from_WUFI_PDF.pdf_sections.ph_requirements import WufiPDF_PHRequirements
from NBDM.from_WUFI_PDF.pdf_sections.project_data import WufiPDF_ProjectData
from NBDM.from_WUFI_PDF.pdf_sections.res_electric import WufiPDF_ResidentialElectric
from NBDM.from_WUFI_PDF.pdf_sections.results import WufiPDF_Results
from NBDM.from_WUFI_PDF.pdf_sections.site import WufiPDF_PropertySite
from NBDM.from_WUFI_PDF.pdf_sections.site_energy_monthly import WufiPDF_SiteEnergyMonthly
from NBDM.from_WUFI_PDF.pdf_sections.specific_monthly_demand import (
    WufiPDF_SpecificMonthlyDemand,
)
from NBDM.from_WUFI_PDF.pdf_sections.thermal_bridges import WufiPDF_ThermalBridges
from NBDM.from_WUFI_PDF.pdf_sections.ventilation import WufiPDF_Ventilation
from NBDM.from_WUFI_PDF.pdf_sections.windows import WufiPDF_Windows
from NBDM.from_WUFI_PDF.pdf_sections.zones_and_components import (
    WufiPDF_ZonesAndComponents,
)

# -- Register each of the PDF sections with the PDF Reader class
PDFReader.register_pdf_section(_WufiPDF_DefaultSection)
PDFReader.register_pdf_section(WufiPDF_AnnualHeatingAndCoolingDemand)
PDFReader.register_pdf_section(WufiPDF_Areas)
PDFReader.register_pdf_section(WufiPDF_AssemblyAndWindowTypes)
PDFReader.register_pdf_section(WufiPDF_AuxElectricity)
PDFReader.register_pdf_section(WufiPDF_BuildingInformation)
PDFReader.register_pdf_section(WufiPDF_BuildingElements)
PDFReader.register_pdf_section(WufiPDF_CalculationParameters)
PDFReader.register_pdf_section(WufiPDF_ClimateSummary)
PDFReader.register_pdf_section(WufiPDF_ClimateDetailed)
PDFReader.register_pdf_section(WufiPDF_DHWandDistribution)
PDFReader.register_pdf_section(WufiPDF_EnvelopeSummary)
PDFReader.register_pdf_section(WufiPDF_HeatingSeasonHeatFlows)
PDFReader.register_pdf_section(WufiPDF_HVAC)
PDFReader.register_pdf_section(WufiPdf_InternalGains)
PDFReader.register_pdf_section(WufiPDF_PeakHeatingAndCoolingLoad)
PDFReader.register_pdf_section(WufiPDF_PassiveHouseData)
PDFReader.register_pdf_section(WufiPDF_PHRecommendations)
PDFReader.register_pdf_section(WufiPDF_PHRequirements)
PDFReader.register_pdf_section(WufiPDF_ProjectData)
PDFReader.register_pdf_section(WufiPDF_ResidentialElectric)
PDFReader.register_pdf_section(WufiPDF_Results)
PDFReader.register_pdf_section(WufiPDF_SiteEnergyMonthly)
PDFReader.register_pdf_section(WufiPDF_PropertySite)
PDFReader.register_pdf_section(WufiPDF_SpecificMonthlyDemand)
PDFReader.register_pdf_section(WufiPDF_ThermalBridges)
PDFReader.register_pdf_section(WufiPDF_Ventilation)
PDFReader.register_pdf_section(WufiPDF_Windows)
PDFReader.register_pdf_section(WufiPDF_ZonesAndComponents)
