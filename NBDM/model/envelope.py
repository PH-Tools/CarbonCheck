# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""NBDM Building Envelope Classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import (
    Dict,
    Optional,
    List,
    Iterator,
    Any,
    TypeVar,
    ItemsView,
    ValuesView,
    KeysView,
)

from ph_units.unit_type import Unit

from NBDM.model import serialization
from NBDM.model import operations


class Collection:
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}

    def __getitem__(self, key: str):
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def items(self) -> ItemsView[str, Any]:
        return self._data.items()

    def keys(self) -> KeysView[str]:
        return self._data.keys()

    def values(self) -> ValuesView[Any]:
        return self._data.values()

    def __iter__(self) -> Iterator[Any]:
        return iter(self._data.values())

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        return repr(self._data)

    def __str__(self) -> str:
        return str(self._data)


@dataclass
class NBDM_EnvelopeAssembly:
    name: str
    u_value: Unit
    r_value: Unit
    ext_exposure: str
    int_exposure: str


@dataclass
class NBDM_BuildingSegmentEnvelope:
    _assemblies: Collection = field(default_factory=Collection)

    @property
    def assemblies(self) -> Dict[str, NBDM_EnvelopeAssembly]:
        return {k: self._assemblies[k] for k in sorted(self._assemblies.keys())}

    @assemblies.setter
    def assemblies(self, value: Dict[str, NBDM_EnvelopeAssembly]) -> None:
        self._assemblies = Collection()
        for k, v in value.items():
            self._assemblies[k] = v

    def clear_envelope_assemblies(self) -> None:
        """Clear all envelope assemblies from the building segment."""
        self._assemblies = Collection()

    def add_envelope_assembly(self, assembly: NBDM_EnvelopeAssembly) -> None:
        """Add an envelope assembly to the building segment."""
        self._assemblies[assembly.name] = assembly

    @classmethod
    def from_dict(cls, _d: Dict) -> NBDM_BuildingSegmentEnvelope:
        """Custom from_dict method to walk over all the assemblies."""
        obj = cls()
        return obj

    def __sub__(
        self, other: NBDM_BuildingSegmentEnvelope
    ) -> NBDM_BuildingSegmentEnvelope:
        return operations.subtract_NBDM_Objects(self, other)

    def __add__(
        self, other: NBDM_BuildingSegmentEnvelope
    ) -> NBDM_BuildingSegmentEnvelope:
        return operations.add_NBDM_Objects(self, other)
