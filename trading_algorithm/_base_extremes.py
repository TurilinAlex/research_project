from abc import ABC, abstractmethod

import numpy as np
from trading_math import localize_extremes, select_eps

from ._base_data import BaseData


class BaseExtremes(BaseData, ABC):
    def __init__(self, values: np.ndarray):
        super().__init__(values)
        self._diff: list[int] | None = None
        self._marker_for_diff: list[int] | None = None

        self._diff_start: list[int] | None = None

    def get_eps_relatively_input(self, after_iter: int) -> int:
        if after_iter == 1:
            return self.get_extr_eps(after_iter=after_iter)

        indexes = self.get_extr_indexes(after_iter=after_iter)
        return min(self._diff_start[i] for i in indexes) - 1

    def _extract_extremes(
        self,
        indexes: np.ndarray,
        coincident: int,
        start_eps: int,
    ) -> tuple[int, np.ndarray]:
        self._diff_between_indexes(indexes=indexes, eps=start_eps)
        eps = self._select_eps(coincident=coincident, eps=start_eps)
        extremes = self._localize_extremes(eps=eps)

        return eps, extremes

    def _extract_trends(self, indexes: np.ndarray, eps: int):
        values = self._values[indexes]
        sort_indexes = np.argsort(values, kind="mergesort").astype(np.int32)
        temp_trends = self._localize_trends(indexes=sort_indexes, eps=eps)
        return indexes[temp_trends]

    def _select_eps(self, coincident: int, eps: int):
        return select_eps(self._marker_for_diff, len(self._marker_for_diff), coincident, eps)

    def _localize_extremes(self, eps: int) -> np.ndarray:
        return localize_extremes(self._diff, len(self._diff), eps)

    @abstractmethod
    def _diff_between_indexes(self, indexes: np.ndarray, eps: int):
        pass

    @abstractmethod
    def _localize_trends(self, indexes: np.ndarray, eps: int):
        pass
