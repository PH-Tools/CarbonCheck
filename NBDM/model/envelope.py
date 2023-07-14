# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Envelope Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

from ph_units.unit_type import Unit

from NBDM.model import operations
from NBDM.model.collections import Collection


@dataclass
class NBDM_EnvelopeAssembly:
    name: str
    u_value: Unit
    r_value: Unit
    ext_exposure: str
    int_exposure: str

    @property
    def key(self) -> str:
        return self.name

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_EnvelopeAssembly:
        """Custom from_dict method to handle the Unit type."""
        d = {}
        for k, v in _d.items():
            if isinstance(v, dict):
                d[k] = Unit.from_dict(v)
            else:
                d[k] = v
        return cls(**d)


@dataclass
class NBDM_BuildingSegmentEnvelope:
    _assemblies: Collection = field(default_factory=Collection)

    @property
    def assemblies(self) -> Dict[str, NBDM_EnvelopeAssembly]:
        return {k: self._assemblies[k] for k in sorted(self._assemblies.keys())}

    @assemblies.setter
    def assemblies(self, value: Dict[str, NBDM_EnvelopeAssembly]) -> None:
        self._assemblies = Collection()
        for v in value.values():
            self._assemblies.add_item(v)

    def clear_envelope_assemblies(self) -> None:
        """Clear all envelope assemblies from the building segment."""
        self._assemblies = Collection()

    def add_envelope_assembly(self, assembly: NBDM_EnvelopeAssembly) -> None:
        """Add an envelope assembly to the building segment."""
        self._assemblies.add_item(assembly)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentEnvelope:
        """Custom from_dict method to walk over all the assemblies."""
        obj = cls()

        # -- Build all the Assemblies and add them to the object.
        for assembly_dict in _d.get("_assemblies", {}).values():
            new_assembly = NBDM_EnvelopeAssembly.from_dict(assembly_dict)
            obj.add_envelope_assembly(new_assembly)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentEnvelope
    ) -> NBDM_BuildingSegmentEnvelope:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentEnvelope
    ) -> NBDM_BuildingSegmentEnvelope:
        return operations.add_NBDM_Objects(self, other)
