# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Envelope Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Generator

from ph_units.unit_type import Unit

from NBDM.model import operations
from NBDM.model.collections import Collection


@dataclass
class NBDM_GlazingType:
    display_name: str
    u_value: Unit
    g_value: Unit

    @property
    def key(self) -> str:
        return self.display_name

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_GlazingType:
        """Custom from_dict method to handle the Unit type."""
        d = {}
        for k, v in _d.items():
            if isinstance(v, dict):
                d[k] = Unit.from_dict(v)
            else:
                d[k] = v
        return cls(**d)


@dataclass
class NBDM_AssemblyType:
    name: str
    u_value: Unit
    r_value: Unit
    ext_exposure: str
    int_exposure: str

    @property
    def key(self) -> str:
        return self.name

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_AssemblyType:
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
    _assembly_types: Collection[NBDM_AssemblyType] = field(default_factory=Collection)
    _glazing_types: Collection[NBDM_GlazingType] = field(default_factory=Collection)

    @property
    def assembly_types(self) -> Generator[NBDM_GlazingType, None, None]:
        return (
            self._assembly_types[a.key]
            for a in sorted(self._assembly_types.values(), key=lambda a: a.name)
        )

    @assembly_types.setter
    def assembly_types(self, value: Dict[str, NBDM_AssemblyType]) -> None:
        self._assembly_types = Collection()
        for v in value.values():
            self.add_assembly_type(v)

    @property
    def glazing_types(self) -> Generator[NBDM_GlazingType, None, None]:
        return (
            self._glazing_types[g.key]
            for g in sorted(self._glazing_types.values(), key=lambda g: g.display_name)
        )

    @glazing_types.setter
    def glazing_types(self, value: Dict[str, NBDM_GlazingType]) -> None:
        self._glazing_types = Collection()
        for v in value.values():
            self.add_glazing_type(v)

    def clear_assembly_types(self) -> None:
        """Clear all envelope assemblies from the building segment."""
        self._assembly_types = Collection()

    def clear_glazing_types(self) -> None:
        """Clear all glazing types from the building segment."""
        self._glazing_types = Collection()

    def add_assembly_type(self, assembly_type: NBDM_AssemblyType) -> None:
        """Add an envelope assembly to the building segment."""
        self._assembly_types.add_item(assembly_type)

    def add_glazing_type(self, glazing_type: NBDM_GlazingType) -> None:
        """Add a new glazing type to the building segment."""
        self._glazing_types.add_item(glazing_type)

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentEnvelope:
        """Custom from_dict method to walk over all the assemblies."""
        obj = cls()

        # -- Build all the Assemblies and add them to the object.
        for assembly_dict in _d.get("_assembly_types", {}).values():
            new_assembly_type = NBDM_AssemblyType.from_dict(assembly_dict)
            obj.add_assembly_type(new_assembly_type)

        # -- Build all the Glazing Types and add them to the object.
        for glazing_dict in _d.get("_glazing_types", {}).values():
            new_glazing_type = NBDM_GlazingType.from_dict(glazing_dict)
            obj.add_glazing_type(new_glazing_type)

        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentEnvelope
    ) -> NBDM_BuildingSegmentEnvelope:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentEnvelope
    ) -> NBDM_BuildingSegmentEnvelope:
        return operations.add_NBDM_Objects(self, other)
