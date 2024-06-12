from NBDM.model import serialization
from NBDM.model.site import NBDM_Climate, NBDM_Location, NBDM_ProjectAddress, NBDM_Site


def test_project_site(sample_NBDM_Site: NBDM_Site):
    assert sample_NBDM_Site


def test_site_to_dict(sample_NBDM_Site: NBDM_Site):
    d1 = serialization.to_dict(sample_NBDM_Site)
    obj = NBDM_Site.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_location_to_dict(sample_NBDM_Site: NBDM_Site):
    d1 = serialization.to_dict(sample_NBDM_Site.location)
    obj = NBDM_Location.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_project_address_to_dict(sample_NBDM_Site: NBDM_Site):
    d1 = serialization.to_dict(sample_NBDM_Site.location.address)
    obj = NBDM_ProjectAddress.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2


def test_climate_to_dict(sample_NBDM_Site: NBDM_Site):
    d1 = serialization.to_dict(sample_NBDM_Site.climate)
    obj = NBDM_Climate.from_dict(d1)
    d2 = serialization.to_dict(obj)

    assert d1 == d2
