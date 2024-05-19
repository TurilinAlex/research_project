from dataclasses import dataclass, field
from typing import Callable

import numpy as np


@dataclass
class HistoryData:
    eps: int
    extremes: np.ndarray
    trends: np.ndarray = field(default_factory=lambda: np.array([], dtype=np.int32))


class BaseData:

    def __init__(self, values: np.ndarray):
        self._values: np.ndarray = values
        self.__history: dict[int, HistoryData] = {}
        self.__iteration: int = 0

    def __repr__(self, interval=None):
        _str = f"<<<<<<<<<<<{self.__class__.__name__:^19}>>>>>>>>>>>\n"
        if interval is not None:
            for key, value in self.__history.items():
                _eps = f"{'eps:':>13} {value.eps:<6d}\n" if value.eps != 0 else ""
                _str += (
                    f"{'Iter':=<19}{key:^3d}{'':=<19}\n"
                    f"{'interval:':>13} begin={f'{interval[key].begin:_}':<8} end={f'{interval[key].end:_}':<8}\n"
                    + _eps
                    + f"{'extremes:':>13} {value.extremes}\n"
                    f"{'trends:':>13} {value.trends}\n"
                )
            return _str

        for key, value in self.__history.items():
            _eps = f"{'eps:':>13} {value.eps:<6d}\n" if value.eps != 0 else ""
            _str += (
                f"{'Iter':=<19}{key:^3d}{'':=<19}\n"
                + _eps
                + f"{'extremes:':>13} {value.extremes}\n"
                f"{'trends:':>13} {value.trends}\n"
            )
        return _str

    def get_current_iter(self):
        return self.__iteration

    def _save_extremes(
        self,
        eps: int,
        extremes: np.ndarray,
        prepare: Callable[[np.ndarray], np.ndarray] = None,
    ):

        self.__iteration += 1

        if self.__iteration > 1:

            if prepare is None:
                prepare = self._prepare_extremes

            self.__history[self.__iteration] = HistoryData(
                eps=eps,
                extremes=prepare(extremes=extremes),
            )
        else:
            self.__history[self.__iteration] = HistoryData(
                eps=eps,
                extremes=extremes,
            )

    def _save_trends(self, trends: np.ndarray, after_iter: int | None):
        if after_iter is None:
            after_iter = self.__iteration

        self.__history[after_iter].trends = trends

    def _prepare_extremes(self, extremes: np.ndarray):
        return self.__history[self.__iteration - 1].extremes[extremes]

    def _prepare_trends(self, extremes: np.ndarray, after_iter):
        return self.__history[after_iter].extremes[extremes]

    def _get_input_indexes_for_extremes(self) -> np.ndarray:
        if self.__iteration == 0:
            return np.argsort(self._values, kind="mergesort").astype(np.int32)

        return np.argsort(
            self._values[self.__history[self.__iteration].extremes], kind="mergesort"
        ).astype(np.int32)

    def _get_extr_eps(self, after_iter: int | None):
        return self.__extract(after_iter=after_iter, attr="eps")

    def _get_extr_indexes(self, after_iter: int | None):
        return self.__extract(after_iter=after_iter, attr="extremes")

    def _get_trend_indexes(self, after_iter: int | None):
        return self.__extract(after_iter=after_iter, attr="trends")

    def _get_extr_values(self, after_iter: int | None):
        return self._values[self._get_extr_indexes(after_iter=after_iter)]

    def _get_trend_values(self, after_iter: int | None):
        return self._values[self._get_trend_indexes(after_iter=after_iter)]

    def __validate(self, after_iter: int):
        if 0 <= after_iter <= self.__iteration:
            return after_iter

        raise ValueError(
            f"Invalid iteration value: {after_iter=}. "
            f"Current iter 0 <= {after_iter} <= {self.__iteration}"
        )

    def __extract(self, after_iter, attr: str) -> int | np.ndarray:
        if after_iter is None:
            return getattr(self.__history[self.__iteration], attr)

        after_iter = self.__validate(after_iter=after_iter)
        return getattr(self.__history[after_iter], attr)
