# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Heating Systems Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, get_type_hints
from uuid import uuid4, UUID

from ph_units.unit_type import Unit

from NBDM.model import operations
from NBDM.model.collections import Collection
from NBDM.model.enums import appliance_type


@dataclass
class NBDM_Appliance:
    id_num: UUID = field(default_factory=uuid4)
    appliance_type: appliance_type = field(default=appliance_type.CUSTOM)
    quantity: int = 1
    annual_energy_use: Unit = field(default_factory=Unit)
    display_name: str = str(appliance_type.name)

    @property
    def key(self) -> str:
        return str(self.id_num)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_Appliance:
        """Custom from_dict method to handle the Unit type."""
        d = {}

        for field_name, field_type in get_type_hints(cls).items():
            if field_name not in _d.keys():
                msg = f"Error: Missing Key  {field_name} in {cls.__name__} from_dict method."
                raise KeyError(msg)

            if field_type == appliance_type:
                d[field_name] = appliance_type(_d[field_name])
            elif field_type == Unit:
                d[field_name] = Unit.from_dict(_d[field_name])
            else:
                d[field_name] = field_type(_d[field_name])

        return cls(**d)


@dataclass
class NBDM_BuildingSegmentAppliances:
    _appliances: Collection = field(default_factory=Collection)

    @property
    def appliances(self) -> Dict[str, NBDM_Appliance]:
        return {k: self._appliances[k] for k in sorted(self._appliances.keys())}

    @appliances.setter
    def appliances(self, value: Dict[str, NBDM_Appliance]) -> None:
        self._appliances = Collection()
        for v in value.values():
            self._appliances.add_item(v)

    def clear_appliances(self) -> None:
        """Clear all appliances assemblies from the building segment."""
        self._appliances = Collection()

    def add_appliance(self, _appliance: NBDM_Appliance) -> None:
        self._appliances.add_item(_appliance)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentAppliances:
        """Custom from_dict method to walk over all the appliances."""
        obj = cls()

        # -- Build all the Appliances and add them to the object.
        for appliance_dict in _d.get("_appliances", {}).values():
            new_appliance = NBDM_Appliance.from_dict(appliance_dict)
            obj.add_appliance(new_appliance)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentAppliances
    ) -> NBDM_BuildingSegmentAppliances:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentAppliances
    ) -> NBDM_BuildingSegmentAppliances:
        return operations.add_NBDM_Objects(self, other)
