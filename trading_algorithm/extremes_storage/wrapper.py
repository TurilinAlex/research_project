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


class _Node:
    def __init__(
        self,
        _previous: "_Node" = None,
        _next: "_Node" = None,
    ):
        self._next = None
        self._previous = None
        self._history_interval: dict[int, _Interval] = {}

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, values):
        self._next = values

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, values):
        self._previous = values

    def get_begin_index(self, after_iter: int):
        return self._history_interval[after_iter].begin

    def get_end_index(self, after_iter: int):
        return self._history_interval[after_iter].end


class NodeMinExtremes(_Node, MinExtremes):

    def __init__(
        self,
        values: np.ndarray,
        _previous: "NodeMinExtremes" = None,
        _next: "NodeMinExtremes" = None,
    ):
        _Node.__init__(self=self, _previous=_previous, _next=_next)
        MinExtremes.__init__(self=self, values=values)

        self._next = _next
        self._previous = _previous

        _start = (
            0
            if self.previous is None
            else self.previous.get_end_index(self.get_current_iter())
        )
        self._history_interval: dict[int, _Interval] = {
            self.get_current_iter(): _Interval(_start, _start + len(values)),
        }

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
        self._history_interval[self.get_current_iter()] = _Interval(
            begin=_start, end=_start + len(self.get_extr_indexes_min())
        )

    def __repr__(self, **kwargs):
        return super().__repr__(self._history_interval)


class NodeMaxExtremes(_Node, MaxExtremes):

    def __init__(
        self,
        values: np.ndarray,
        _previous: "NodeMaxExtremes" = None,
        _next: "NodeMaxExtremes" = None,
    ):
        _Node.__init__(self=self, _previous=_previous, _next=_next)
        MaxExtremes.__init__(self=self, values=values)

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


class NodeUnionExtremes(_Node, UnionExtremes):

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

        _Node.__init__(self=self, _previous=_previous, _next=_next)
        UnionExtremes.__init__(
            self=self,
            values=values,
            min_extremes=_min_extremes,
            max_extremes=_max_extremes,
        )

        _start = (
            0
            if self.previous is None
            else self.previous.get_end_index(self.get_current_iter())
        )
        self.__history: dict[int, _Interval] = {
            self.get_current_iter(): _Interval(_start, _start + len(values)),
        }

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
            begin=_start, end=_start + len(self.get_extr_indexes_union())
        )

    def __repr__(self, **kwargs):
        return (
            f"{super().__repr__(self.__history)}"
            f"{self._min_extremes!r}"
            f"{self._max_extremes!r}"
        )
