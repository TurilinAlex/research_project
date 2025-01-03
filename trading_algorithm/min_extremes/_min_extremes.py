from abc import ABC, abstractmethod

import numpy as np
from trading_math import diff_between_indexes_min, extract_min_extremes

from .._base_extremes import BaseExtremes


class BaseMinExtremes(BaseExtremes, ABC):
    def _diff_between_indexes(self, indexes: np.ndarray, eps: int):
        n = len(indexes)

        self._diff = np.zeros(n, dtype=np.int32)
        self._marker_for_diff = np.zeros(n + 1, dtype=np.int32)

        diff_between_indexes_min(indexes, self._diff, self._marker_for_diff, n, eps)

        if self.get_current_iter() == 0:
            self._diff_start = self._diff.copy()

    def _localize_trends(self, indexes: np.ndarray, eps: int):
        return extract_min_extremes(indexes, len(indexes), eps)

    @abstractmethod
    def extract_extremes(
        self,
        coincident: int,
        start_eps: int,
        is_save: bool = True,
    ) -> tuple[int, np.ndarray]:
        pass

    @abstractmethod
    def extract_trends(
        self,
        eps: int,
        after_iter: int | None = None,
        is_save: bool = True,
    ) -> np.ndarray:
        pass
