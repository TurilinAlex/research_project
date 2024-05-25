from abc import ABC, abstractmethod

import numpy as np

from ._base_data import BaseData
from .max_extremes.max_extremes import MaxExtremes
from .min_extremes.min_extremes import MinExtremes


class BaseCombinationExtremes(BaseData, ABC):
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
        return self._min_extremes.get_extr_eps(after_iter=after_iter)

    def get_extr_eps_max(self, after_iter: int | None = None):
        return self._max_extremes.get_extr_eps(after_iter=after_iter)

    def get_extr_indexes(self, after_iter: int | None = None):
        return self._get_extr_indexes(after_iter=after_iter)

    def get_extr_values(self, after_iter: int | None = None):
        return self._get_extr_values(after_iter=after_iter)

    def get_extr_indexes_min(self, after_iter: int | None = None):
        return self._min_extremes.get_extr_indexes(after_iter=after_iter)

    def get_extr_values_min(self, after_iter: int | None = None):
        return self._min_extremes.get_extr_values(after_iter=after_iter)

    def get_extr_indexes_max(self, after_iter: int | None = None):
        return self._max_extremes.get_extr_indexes(after_iter=after_iter)

    def get_extr_values_max(self, after_iter: int | None = None):
        return self._max_extremes.get_extr_values(after_iter=after_iter)

    def get_trends_indexes(self, after_iter: int | None = None):
        return self._get_trend_indexes(after_iter=after_iter)

    def get_trends_values(self, after_iter: int | None = None):
        return self._get_trend_values(after_iter=after_iter)

    def get_trends_indexes_min(self, after_iter: int | None = None):
        return self._min_extremes.get_trends_indexes(after_iter=after_iter)

    def get_trends_values_min(self, after_iter: int | None = None):
        return self._min_extremes.get_trends_values(after_iter=after_iter)

    def get_trends_indexes_max(self, after_iter: int | None = None):
        return self._max_extremes.get_trends_indexes(after_iter=after_iter)

    def get_trends_values_max(self, after_iter: int | None = None):
        return self._max_extremes.get_trends_values(after_iter=after_iter)

    def to_dict(self, **kwargs):
        _dict = {}
        for syb_interval, data in super().to_dict(**kwargs).items():
            del data["eps"]
            _dict[syb_interval] = data

        return _dict

    def to_json(self, **kwargs):
        _dict = super().to_json(**kwargs)
        for syb_interval, data in _dict.items():
            del data["eps"]

        return _dict

    @abstractmethod
    def extract_extremes(
        self,
        coincident: int,
        start_eps: int,
        is_save: bool = True,
    ) -> np.ndarray:
        pass

    @abstractmethod
    def extract_trends(
        self,
        eps: int,
        after_iter: int | None = None,
        is_save: bool = True,
    ) -> np.ndarray:
        pass

    @abstractmethod
    def combination_extremes(
        self,
        min_extremes: np.ndarray,
        max_extremes: np.ndarray,
    ):
        pass

    @abstractmethod
    def combination_trends(
        self,
        min_trends: np.ndarray,
        max_trends: np.ndarray,
    ):
        pass
