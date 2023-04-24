# -*- Python Version: 3.11 -*-

"""Dropdown options for the Baseline Codes."""

from enum import Enum
from typing import List

class ClimateZones(Enum):
    """The climate zones that are available for the PH Baseliner."""

    CZ4 = "CZ4 (Except Marine 4)"
    CZ5 = "CZ5 (and Marine 4)"
    CZ6 = "CZ6"

    @classmethod
    def as_list(cls) -> List[str]:
        """Return a list of the Enum values as strings."""
        return [_.value for _ in cls]


class BaselineCodes(Enum):
    """The baseline codes that are available for the PH Baseliner."""

    ECCCNYS_2020 = "ECC of NYS 2020"

    @classmethod
    def as_list(cls) -> List[str]:
        """Return a list of the Enum values as strings."""
        return [_.value for _ in cls]