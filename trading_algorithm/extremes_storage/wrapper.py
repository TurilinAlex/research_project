from dataclasses import dataclass
from typing import Callable

import numpy as np

from ..max_extremes.max_extremes import MaxExtremes
from ..min_extremes.min_extremes import MinExtremes
from ..union_extremes.union_extremes import UnionExtremes


@dataclass
class _Interval:
    begin: int
    end: int


class NodeMinExtremes(MinExtremes):

    def __init__(
        self,
        values: np.ndarray,
        _previous: "NodeMinExtremes" = None,
        _next: "NodeMinExtremes" = None,
    ):
        super().__init__(values=values)

        self.__next = _next
        self.__previous = _previous

        _start = (
            0
            if self.previous is None
            else self.previous.get_end_index(self.get_current_iter())
        )
        self.__history: dict[int, _Interval] = {
            self.get_current_iter(): _Interval(_start, _start + len(values)),
        }

    @property
    def next(self) -> "NodeMinExtremes":
        return self.__next

    @next.setter
    def next(self, values: "NodeMinExtremes"):
        self.__next = values

    @property
    def previous(self) -> "NodeMinExtremes":
        return self.__previous

    @previous.setter
    def previous(self, values: "NodeMinExtremes"):
        self.__previous = values

    def get_begin_index(self, after_iter: int):
        after_iter = self.after_iter_validate(after_iter=after_iter)
        return self.__history[after_iter].begin

    def get_end_index(self, after_iter: int):
        after_iter = self.after_iter_validate(after_iter=after_iter)
        return self.__history[after_iter].end

    def to_dict(self, **kwargs):
        return super().to_dict(interval=self.__history)

    def to_json(self, **kwargs):
        return super().to_json(interval=self.__history)

    def _save_extremes(
        self,
        eps: int,
        extremes: np.ndarray,
        prepare: Callable[[np.ndarray], np.ndarray] = None,
    ):
        super()._save_extremes(eps=eps, extremes=extremes, prepare=prepare)

        _start = (
            0
            if self.previous is None
            else self.previous.get_end_index(self.get_current_iter())
        )
        self.__history[self.get_current_iter()] = _Interval(
            begin=_start, end=_start + len(self.get_extr_indexes())
        )

    def __repr__(self, **kwargs):
        return super().__repr__(self.__history)


class NodeMaxExtremes(MaxExtremes):

    def __init__(
        self,
        values: np.ndarray,
        _previous: "NodeMaxExtremes" = None,
        _next: "NodeMaxExtremes" = None,
    ):
        super().__init__(values=values)

        self.__next = _next
        self.__previous = _previous

        _start = (
            0
            if self.previous is None
            else self.previous.get_end_index(self.get_current_iter())
        )
        self.__history: dict[int, _Interval] = {
            self.get_current_iter(): _Interval(_start, _start + len(values)),
        }

    @property
    def next(self) -> "NodeMaxExtremes":
        return self.__next

    @next.setter
    def next(self, values: "NodeMaxExtremes"):
        self.__next = values

    @property
    def previous(self) -> "NodeMaxExtremes":
        return self.__previous

    @previous.setter
    def previous(self, values: "NodeMaxExtremes"):
        self.__previous = values

    def get_begin_index(self, after_iter: int):
        after_iter = self.after_iter_validate(after_iter=after_iter)
        return self.__history[after_iter].begin

    def get_end_index(self, after_iter: int):
        after_iter = self.after_iter_validate(after_iter=after_iter)
        return self.__history[after_iter].end

    def to_dict(self, **kwargs):
        return super().to_dict(interval=self.__history)

    def to_json(self, **kwargs):
        return super().to_json(interval=self.__history)

    def _save_extremes(
        self,
        eps: int,
        extremes: np.ndarray,
        prepare: Callable[[np.ndarray], np.ndarray] = None,
    ):
        super()._save_extremes(eps=eps, extremes=extremes, prepare=prepare)

        _start = (
            0
            if self.previous is None
            else self.previous.get_end_index(self.get_current_iter())
        )
        self.__history[self.get_current_iter()] = _Interval(
            begin=_start, end=_start + len(self.get_extr_indexes())
        )

    def __repr__(self, **kwargs):
        return super().__repr__(self.__history)


class NodeUnionExtremes(UnionExtremes):

    def __init__(
        self,
        values: np.ndarray,
        _previous: "NodeUnionExtremes" = None,
        _next: "NodeUnionExtremes" = None,
    ):
        self.__next = _next
        self.__previous = _previous

        _previous_min_extremes = (
            None if self.previous is None else self.previous.min_extremes
        )
        _previous_max_extremes = (
            None if self.previous is None else self.previous.max_extremes
        )

        _next_min_extremes = None if self.next is None else self.next.min_extremes
        _next_max_extremes = None if self.next is None else self.next.max_extremes

        _min_extremes = NodeMinExtremes(
            values=values, _previous=_previous_min_extremes, _next=_next_min_extremes
        )
        _max_extremes = NodeMaxExtremes(
            values=values, _previous=_previous_max_extremes, _next=_next_max_extremes
        )

        super().__init__(
            values=values, min_extremes=_min_extremes, max_extremes=_max_extremes
        )

        _start = (
            0
            if self.previous is None
            else self.previous.get_end_index(self.get_current_iter())
        )
        self.__history: dict[int, _Interval] = {
            self.get_current_iter(): _Interval(_start, _start + len(values)),
        }

    @property
    def next(self) -> "NodeUnionExtremes":
        return self.__next

    @next.setter
    def next(self, values: "NodeUnionExtremes"):
        self.__next = values

    @property
    def previous(self) -> "NodeUnionExtremes":
        return self.__previous

    @previous.setter
    def previous(self, values: "NodeUnionExtremes"):
        self.__previous = values

    def get_begin_index(self, after_iter: int):
        after_iter = self.after_iter_validate(after_iter=after_iter)
        return self.__history[after_iter].begin

    def get_end_index(self, after_iter: int):
        after_iter = self.after_iter_validate(after_iter=after_iter)
        return self.__history[after_iter].end

    def to_dict(self, **kwargs):
        return super().to_dict(interval=self.__history)

    def to_json(self, **kwargs):
        return super().to_json(interval=self.__history)

    def _save_extremes(
        self,
        eps: int,
        extremes: np.ndarray,
        prepare: Callable[[np.ndarray], np.ndarray] = None,
    ):
        super()._save_extremes(eps=eps, extremes=extremes, prepare=prepare)

        _start = (
            0
            if self.previous is None
            else self.previous.get_end_index(self.get_current_iter())
        )
        self.__history[self.get_current_iter()] = _Interval(
            begin=_start, end=_start + len(self.get_extr_indexes())
        )

    def __repr__(self, **kwargs):
        return (
            f"{super().__repr__(self.__history)}"
            f"{self._min_extremes!r}"
            f"{self._max_extremes!r}"
        )
