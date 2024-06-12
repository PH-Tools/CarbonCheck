from ph_units.unit_type import Unit

from NBDM.from_WUFI_PDF.pdf_reader_sections import PDFSectionsCollection
from NBDM.from_WUFI_PDF.performance import build_NBDM_performanceFromWufiPDF


def test_ridgeway_create_nbdm_performance_site_energy_from_wufi_pdf(
    sample_pdf_data_ridgeway_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_ridgeway_proposed)

    # -- Site Energy
    assert obj.site_energy.consumption_gas == Unit(0, "KBTU")
    assert obj.site_energy.consumption_electricity == Unit(1_821_080.4438749999, "KBTU")
    assert obj.site_energy.consumption_district_heat == Unit(0, "KBTU")
    assert obj.site_energy.consumption_other == Unit(0, "KBTU")
    assert obj.site_energy.production_solar_photovoltaic == Unit(351_641.49984, "KBTU")
    assert obj.site_energy.production_solar_thermal == Unit(0, "KBTU")
    assert obj.site_energy.production_other == Unit(0, "KBTU")


def test_la_mora_create_nbdm_performance_site_energy_from_wufi_pdf(
    sample_pdf_data_la_mora_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_la_mora_proposed)

    # -- Site Energy
    assert obj.site_energy.consumption_gas == Unit(0, "KBTU")
    assert obj.site_energy.consumption_electricity == Unit(1_288_488.1781106002, "KBTU")
    assert obj.site_energy.consumption_district_heat == Unit(0, "KBTU")
    assert obj.site_energy.consumption_other == Unit(0, "KBTU")
    assert obj.site_energy.production_solar_photovoltaic == Unit(
        78_257.43089999999, "KBTU"
    )
    assert obj.site_energy.production_solar_thermal == Unit(0, "KBTU")
    assert obj.site_energy.production_other == Unit(0, "KBTU")


def test_create_nbdm_performance_source_energy_from_wufi_pdf(
    sample_pdf_data_ridgeway_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_ridgeway_proposed)

    # -- Source Energy
    # -- all are zero'd out cus' WUFI doesn't report this data
    assert obj.source_energy.consumption_gas == Unit(0.0, "-")
    assert obj.source_energy.consumption_electricity == Unit(0.0, "-")
    assert obj.source_energy.consumption_district_heat == Unit(0, "-")
    assert obj.source_energy.consumption_other == Unit(0, "-")
    assert obj.source_energy.production_solar_photovoltaic == Unit(0, "-")
    assert obj.source_energy.production_solar_thermal == Unit(0, "-")
    assert obj.source_energy.production_other == Unit(0, "-")


def test_create_nbdm_performance_heat_demand_from_wufi_pdf(
    sample_pdf_data_ridgeway_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_ridgeway_proposed)

    # -- Heating Demand
    assert obj.annual_heating_energy_demand.losses_transmission == Unit(611_713.0, "KBTU")
    assert obj.annual_heating_energy_demand.losses_ventilation == Unit(322_960.0, "KBTU")
    assert obj.annual_heating_energy_demand.gains_solar == Unit(250_855.0, "KBTU")
    assert obj.annual_heating_energy_demand.gains_internal == Unit(495_426.0, "KBTU")
    assert obj.annual_heating_energy_demand.utilization_factor == Unit(0.83, "%")
    assert obj.annual_heating_energy_demand.heating_demand == Unit(315_092.0, "KBTU")


def test_create_nbdm_performance_cooling_demand_from_wufi_pdf(
    sample_pdf_data_ridgeway_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_ridgeway_proposed)

    assert obj.annual_cooling_energy_demand.losses_transmission == Unit(
        1_149_853.0, "KBTU"
    )
    assert obj.annual_cooling_energy_demand.losses_ventilation == Unit(
        1_911_881.0, "KBTU"
    )
    assert obj.annual_cooling_energy_demand.gains_solar == Unit(399_453.0, "KBTU")
    assert obj.annual_cooling_energy_demand.gains_internal == Unit(934_143.0, "KBTU")
    assert obj.annual_cooling_energy_demand.utilization_factor == Unit(0.0, "%")
    assert obj.annual_cooling_energy_demand.sensible_cooling_demand == Unit(
        299393.0, "KBTU"
    )
    assert obj.annual_cooling_energy_demand.latent_cooling_demand == Unit(
        122065.0, "KBTU"
    )


def test_create_nbdm_performance_peak_heat_load_from_wufi_pdf(
    sample_pdf_data_ridgeway_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_ridgeway_proposed)

    assert obj.peak_heating_load.losses_transmission == Unit(206_663.4, "BTUH")
    assert obj.peak_heating_load.losses_ventilation == Unit(141_844.1, "BTUH")
    assert obj.peak_heating_load.gains_solar == Unit(42_158.1, "BTUH")
    assert obj.peak_heating_load.gains_internal == Unit(40_428.7, "BTUH")
    assert obj.peak_heating_load.peak_heating_load == Unit(265_920.8, "BTUH")


def test_create_nbdm_performance_peak_cooling_load_from_wufi_pdf(
    sample_pdf_data_ridgeway_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_ridgeway_proposed)

    assert obj.peak_cooling_load.losses_transmission == Unit(-820.7, "BTUH")
    assert obj.peak_cooling_load.losses_ventilation == Unit(-4_581.6, "BTUH")
    assert obj.peak_cooling_load.gains_solar == Unit(58_670.5, "BTUH")
    assert obj.peak_cooling_load.gains_internal == Unit(106_647.8, "BTUH")
    assert obj.peak_cooling_load.peak_sensible_cooling_load == Unit(170_720.6, "BTUH")
    assert obj.peak_cooling_load.peak_latent_cooling_load == Unit(0.0, "BTUH")


def test_la_mora_create_nbdm_performance_solar_from_wufi_pdf(
    sample_pdf_data_la_mora_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_la_mora_proposed)

    assert obj.site_energy.production_solar_photovoltaic == Unit(
        78_257.43089999999, "KBTU"
    )


def test_ridgeway_create_nbdm_performance_solar_from_wufi_pdf(
    sample_pdf_data_ridgeway_proposed: PDFSectionsCollection,
) -> None:
    obj = build_NBDM_performanceFromWufiPDF(sample_pdf_data_ridgeway_proposed)

    assert obj.site_energy.production_solar_photovoltaic == Unit(351_641.49984, "KBTU")
