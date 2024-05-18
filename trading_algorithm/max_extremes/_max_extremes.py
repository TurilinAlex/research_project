from abc import ABC, abstractmethod

import numpy as np

from trading_math import diff_between_indexes_max, extract_max_extremes

from .._base_extremes import BaseExtremes


class BaseMaxExtremes(BaseExtremes, ABC):
    def _diff_between_indexes(self, indexes: np.ndarray, eps: int):
        # sourcery skip: use-assigned-variable

        n = len(indexes)

        self._diff = np.zeros(n, dtype=np.int32)
        self._marker_for_diff = np.zeros(n + 1, dtype=np.int32)

        diff_between_indexes_max(indexes, self._diff, self._marker_for_diff, n, eps)

    def _localize_trends(self, indexes: np.ndarray, eps: int):
        return extract_max_extremes(indexes, len(indexes), eps)

    def get_extr_eps_max(self, after_iter: int | None = None):
        return self._get_extr_eps(after_iter=after_iter)

    def get_extr_indexes_max(self, after_iter: int | None = None):
        return self._get_extr_indexes(after_iter=after_iter)

    def get_extr_values_max(self, after_iter: int | None = None):
        return self._get_extr_values(after_iter=after_iter)

    def get_trends_indexes_max(self, after_iter: int | None = None):
        return self._get_trend_indexes(after_iter=after_iter)

    def get_trends_values_max(self, after_iter: int | None = None):
        return self._get_trend_values(after_iter=after_iter)

    @abstractmethod
    def extract_max_extremes(
        self,
        coincident: int,
        start_eps: int,
        is_save: bool = True,
    ) -> tuple[int, np.ndarray]:
        pass

    @abstractmethod
    def extract_max_trends(
        self,
        eps: int,
        after_iter: int | None = None,
        is_save: bool = True,
    ) -> np.ndarray:
        pass
