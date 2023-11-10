from .__typing import WufiPDF_SectionType
from ..pdf_reader import PDFReader

# -- Import all of the section types. NOTE: we can't do this
# -- dynamically (searching through the folder...) cus' if we do that, the
# -- packager (cxFreeze | PyInstaller) won't find all the required modules.
from ._default import _WufiPDF_DefaultSection
from .annual_demand import WufiPDF_AnnualHeatingAndCoolingDemand
from .areas import WufiPDF_Areas
from .assemblies_win_types import WufiPDF_AssemblyAndWindowTypes
from .aux_electric import WufiPDF_AuxElectricity
from .bldg_info import WufiPDF_BuildingInformation
from .building_elements import WufiPDF_BuildingElements
from .calc_parameters import WufiPDF_CalculationParameters
from .climate_detailed import WufiPDF_ClimateDetailed
from .climate_summary import WufiPDF_ClimateSummary
from .dhw_and_distribution import WufiPDF_DHWandDistribution
from .envelope_summary import WufiPDF_EnvelopeSummary
from .heat_flow_heating import WufiPDF_HeatingSeasonHeatFlows
from .hvac import WufiPDF_HVAC
from .internal_gains import WufiPdf_InternalGains
from .peak_load import WufiPDF_PeakHeatingAndCoolingLoad
from .ph_data import WufiPDF_PassiveHouseData
from .ph_recommendations import WufiPDF_PHRecommendations
from .ph_requirements import WufiPDF_PHRequirements
from .project_data import WufiPDF_ProjectData
from .res_electric import WufiPDF_ResidentialElectric
from .results import WufiPDF_Results
from .site_energy_monthly import WufiPDF_SiteEnergyMonthly
from .site import WufiPDF_PropertySite
from .specific_monthly_demand import WufiPDF_SpecificMonthlyDemand
from .thermal_bridges import WufiPDF_ThermalBridges
from .ventilation import WufiPDF_Ventilation
from .windows import WufiPDF_Windows
from .zones_and_components import WufiPDF_ZonesAndComponents

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
