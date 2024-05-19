from abc import ABC, abstractmethod

import numpy as np

from .._base_data import BaseData
from ..max_extremes.max_extremes import MaxExtremes
from ..min_extremes.min_extremes import MinExtremes


class BaseUnionExtremes(BaseData, ABC):
    def __init__(self, values: np.ndarray, min_extremes=None, max_extremes=None):
        super().__init__(values)

        self._min_extremes: MinExtremes = (
            MinExtremes(values=values) if min_extremes is None else min_extremes
        )
        self._max_extremes: MaxExtremes = (
            MaxExtremes(values=values) if max_extremes is None else max_extremes
        )

    @property
    def min_extremes(self):
        return self._min_extremes

    @property
    def max_extremes(self):
        return self._max_extremes

    def get_extr_eps_min(self, after_iter: int | None = None):
        return self._min_extremes.get_extr_eps_min(after_iter=after_iter)

    def get_extr_eps_max(self, after_iter: int | None = None):
        return self._max_extremes.get_extr_eps_max(after_iter=after_iter)

    def get_extr_indexes_union(self, after_iter: int | None = None):
        return self._get_extr_indexes(after_iter=after_iter)

    def get_extr_values_union(self, after_iter: int | None = None):
        return self._get_extr_values(after_iter=after_iter)

    def get_extr_indexes_min(self, after_iter: int | None = None):
        return self._min_extremes.get_extr_indexes_min(after_iter=after_iter)

    def get_extr_values_min(self, after_iter: int | None = None):
        return self._min_extremes.get_extr_values_min(after_iter=after_iter)

    def get_extr_indexes_max(self, after_iter: int | None = None):
        return self._max_extremes.get_extr_indexes_max(after_iter=after_iter)

    def get_extr_values_max(self, after_iter: int | None = None):
        return self._max_extremes.get_extr_values_max(after_iter=after_iter)

    def get_trends_indexes_union(self, after_iter: int | None = None):
        return self._get_trend_indexes(after_iter=after_iter)

    def get_trends_values_union(self, after_iter: int | None = None):
        return self._get_trend_values(after_iter=after_iter)

    def get_trends_indexes_min(self, after_iter: int | None = None):
        return self._min_extremes.get_trends_indexes_min(after_iter=after_iter)

    def get_trends_values_min(self, after_iter: int | None = None):
        return self._min_extremes.get_trends_values_min(after_iter=after_iter)

    def get_trends_indexes_max(self, after_iter: int | None = None):
        return self._max_extremes.get_trends_indexes_max(after_iter=after_iter)

    def get_trends_values_max(self, after_iter: int | None = None):
        return self._max_extremes.get_trends_values_max(after_iter=after_iter)

    @abstractmethod
    def _union_extremes(
        self,
        min_extremes: np.ndarray,
        max_extremes: np.ndarray,
    ):
        pass

    @abstractmethod
    def _union_trends(
        self,
        min_trends: np.ndarray,
        max_trends: np.ndarray,
    ):
        pass
