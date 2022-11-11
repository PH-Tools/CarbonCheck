from dataclasses import asdict
from NBDM.model.project import NBDM_Project, NBDM_Variants, NBDM_Variant

def test_project(sample_NBDM_Project: NBDM_Project):
    assert sample_NBDM_Project

def test_proposed_variant_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = asdict(sample_NBDM_Project.variants.proposed)
    obj = NBDM_Variant.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

def test_baseline_variant_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = asdict(sample_NBDM_Project.variants.baseline)
    obj = NBDM_Variant.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

def test_variants_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = asdict(sample_NBDM_Project.variants)
    obj = NBDM_Variants.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2

    for variant in sample_NBDM_Project.variants:
        d1 = asdict(variant)
        obj = NBDM_Variant.from_dict(d1)
        d2 = asdict(obj)

    assert d1 == d2
def test_project_to_dict(sample_NBDM_Project: NBDM_Project):
    d1 = asdict(sample_NBDM_Project)
    obj = NBDM_Project.from_dict(d1)
    d2 = asdict(obj)

    assert d1 == d2