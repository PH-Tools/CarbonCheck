# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Collection Class for managing groups of NBDM Objects."""

from __future__ import annotations

from typing import (
    Any,
    Dict,
    Generic,
    ItemsView,
    Iterator,
    KeysView,
    Protocol,
    TypeVar,
    ValuesView,
)


class CollectionItem(Protocol):
    """Minimum Protocol for Collection Items."""

    key: Any

    def from_dict(self, _d: Dict) -> CollectionItem:
        ...


T = TypeVar("T", bound=CollectionItem)


class Collection(Generic[T]):
    def __init__(self) -> None:
        self._data: Dict[str, T] = {}

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: T) -> None:
        msg = "Please use the 'add_item' method to add items to the Collection."
        raise NotImplementedError(msg)

    def add_item(self, _item: T) -> None:
        """Add an item to the collection."""
        self._data[_item.key] = _item

    def items(self) -> ItemsView[str, T]:
        return self._data.items()

    def keys(self) -> KeysView[str]:
        return self._data.keys()

    def values(self) -> ValuesView[T]:
        return self._data.values()

    def __iter__(self) -> Iterator[T]:
        return iter(self._data.values())

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __repr__(self) -> str:
        return repr(self._data)

    def __str__(self) -> str:
        return str(self._data)
