# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

"""Functions to create NBDM_BuildingSegmentPerformance objects from WUFI-PDF data."""

from typing import Optional

from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.pdf_sections.annual_demand import (
    AnnualDemand,
    WufiPDF_AnnualHeatingAndCoolingDemand,
)
from NBDM.from_WUFI_PDF.pdf_sections.peak_load import (
    PeakLoad,
    WufiPDF_PeakHeatingAndCoolingLoad,
)
from NBDM.from_WUFI_PDF.pdf_sections.site_energy_monthly import (
    WufiPDF_SiteEnergyMonthly,
)
from NBDM.model.performance import (
    NBDM_AnnualCoolingDemandEnergy,
    NBDM_AnnualHeatingDemandEnergy,
    NBDM_BuildingSegmentPerformance,
    NBDM_PeakCoolingLoad,
    NBDM_PeakHeatingLoad,
    NBDM_SiteEnergy,
    NBDM_SourceEnergy,
)


def build_NBDM_siteEnergyFromWufiPDF(
    _pdf_data: WufiPDF_SiteEnergyMonthly,
) -> NBDM_SiteEnergy:
    return NBDM_SiteEnergy(
        consumption_gas=_pdf_data.consumption_gas,
        consumption_electricity=_pdf_data.consumption_electricity,
        consumption_district_heat=_pdf_data.consumption_district_heat,
        consumption_other=_pdf_data.consumption_other,
        production_solar_photovoltaic=_pdf_data.production_solar_photovoltaic,
        production_solar_thermal=_pdf_data.production_solar_thermal,
        production_other=_pdf_data.production_other,
    )


def build_NBDM_sourceEnergyFromWufiPDF() -> NBDM_SourceEnergy:
    return NBDM_SourceEnergy()


def build_annualHeatingDemandFromWufiPDF(
    _pdf_data: AnnualDemand,
) -> NBDM_AnnualHeatingDemandEnergy:
    return NBDM_AnnualHeatingDemandEnergy(
        heating_demand=_pdf_data.annual_heat_demand,
        losses_transmission=_pdf_data.transmission_losses,
        losses_ventilation=_pdf_data.ventilation_losses,
        gains_solar=_pdf_data.solar_heat_gains,
        gains_internal=_pdf_data.internal_heat_gains,
        utilization_factor=_pdf_data.utilization_factor,
    )


def build_annualCoolingDemandFromWufiPDF(
    _pdf_data: AnnualDemand,
) -> NBDM_AnnualCoolingDemandEnergy:
    return NBDM_AnnualCoolingDemandEnergy(
        sensible_cooling_demand=_pdf_data.cooling_demand_sensible,
        latent_cooling_demand=_pdf_data.cooling_demand_latent,
        losses_transmission=_pdf_data.transmission_losses,
        losses_ventilation=_pdf_data.ventilation_losses,
        utilization_factor=_pdf_data.utilization_factor,
        gains_solar=_pdf_data.solar_heat_gains,
        gains_internal=_pdf_data.internal_heat_gains,
    )


def build_NBDM_peakHeatingLoadFromWufiPDF(_pdf_data: PeakLoad) -> NBDM_PeakHeatingLoad:
    return NBDM_PeakHeatingLoad(
        peak_heating_load=_pdf_data.heating_load,
        losses_transmission=_pdf_data.transmission_heat_losses,
        losses_ventilation=_pdf_data.ventilation_heat_losses,
        gains_solar=_pdf_data.solar_heat_gain,
        gains_internal=_pdf_data.internal_heat_gain,
    )


def build_NBDM_peakCoolingLoadFromWufiPDF(_pdf_data: PeakLoad) -> NBDM_PeakCoolingLoad:
    return NBDM_PeakCoolingLoad(
        peak_sensible_cooling_load=_pdf_data.cooling_load_sensible,
        peak_latent_cooling_load=_pdf_data.cooling_load_latent,
        losses_transmission=_pdf_data.transmission_heat_losses,
        losses_ventilation=_pdf_data.ventilation_heat_losses,
        gains_solar=_pdf_data.solar_heat_gain,
        gains_internal=_pdf_data.internal_heat_gain,
    )


def build_NBDM_performanceFromWufiPDF(
    _pdf_data: PDFSectionsCollection,
) -> NBDM_BuildingSegmentPerformance:
    new_nbdm_obj = NBDM_BuildingSegmentPerformance()

    # -- Pull out the relevant sections
    # -------------------------------------------------------------------------
    site_energy_section: Optional[WufiPDF_SiteEnergyMonthly]
    if site_energy_section := _pdf_data.get_section(WufiPDF_SiteEnergyMonthly):
        new_nbdm_obj.site_energy = build_NBDM_siteEnergyFromWufiPDF(site_energy_section)
        new_nbdm_obj.source_energy = build_NBDM_sourceEnergyFromWufiPDF()

    # -------------------------------------------------------------------------
    load_section: Optional[WufiPDF_PeakHeatingAndCoolingLoad]
    if load_section := _pdf_data.get_section(WufiPDF_PeakHeatingAndCoolingLoad):
        new_nbdm_obj.peak_heating_load = build_NBDM_peakHeatingLoadFromWufiPDF(
            max(load_section.heating_load_1, load_section.heating_load_2)
        )
        new_nbdm_obj.peak_cooling_load = build_NBDM_peakCoolingLoadFromWufiPDF(
            load_section.cooling_load
        )

    # -------------------------------------------------------------------------
    demand_section: Optional[WufiPDF_AnnualHeatingAndCoolingDemand]
    if demand_section := _pdf_data.get_section(WufiPDF_AnnualHeatingAndCoolingDemand):
        new_nbdm_obj.annual_heating_energy_demand = build_annualHeatingDemandFromWufiPDF(
            demand_section.heating_demand
        )
        new_nbdm_obj.annual_cooling_energy_demand = build_annualCoolingDemandFromWufiPDF(
            demand_section.cooling_demand
        )

    return new_nbdm_obj
