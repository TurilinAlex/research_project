import numpy as np

from ._min_extremes import BaseMinExtremes


class MinExtremes(BaseMinExtremes):

    def extract_extremes(
        self,
        coincident: int,
        start_eps: int,
        is_save: bool = True,
    ) -> tuple[int, np.ndarray]:
        indexes = self._get_input_indexes_for_extremes()

        eps, extremes = self._extract_extremes(
            indexes=indexes,
            coincident=coincident,
            start_eps=start_eps,
        )

        if is_save:
            self._save_extremes(
                eps=eps,
                extremes=extremes,
            )

        return eps, extremes

    def extract_trends(
        self,
        eps: int,
        after_iter: int | None = None,
        is_save: bool = True,
    ) -> np.ndarray:
        indexes = self.get_extr_indexes(after_iter=after_iter)
        trends = self._extract_trends(indexes=indexes, eps=eps)

        if is_save:
            self._save_trends(trends=trends, after_iter=after_iter)

        return trends
