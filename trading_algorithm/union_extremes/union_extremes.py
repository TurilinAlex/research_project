import numpy as np

from .._base_combination_extremes import BaseCombinationExtremes
from ..utils import merge_sorted_arrays


class UnionExtremes(BaseCombinationExtremes):

    # noinspection PyProtectedMember
    def extract_extremes(
        self,
        coincident: int,
        start_eps: int,
        is_save: bool = True,
    ):
        indexes = self._get_input_indexes_for_extremes()

        eps_min, extremes_min = self._min_extremes._extract_extremes(
            coincident=coincident,
            start_eps=start_eps,
            indexes=indexes,
        )
        eps_max, extremes_max = self._max_extremes._extract_extremes(
            coincident=coincident,
            start_eps=start_eps,
            indexes=indexes,
        )

        extremes = self._combination_extremes(
            min_extremes=extremes_min,
            max_extremes=extremes_max,
        )

        if is_save:
            self._save_extremes(eps=0, extremes=extremes)
            self._min_extremes._save_extremes(
                eps=eps_min,
                extremes=extremes_min,
                prepare=self._prepare_extremes,
            )
            self._max_extremes._save_extremes(
                eps=eps_max,
                extremes=extremes_max,
                prepare=self._prepare_extremes,
            )

        return extremes

    # noinspection PyProtectedMember
    def extract_trends(
        self,
        eps: int,
        after_iter: int | None = None,
        is_save: bool = True,
    ):
        indexes_min = self._min_extremes.get_extr_indexes(after_iter=after_iter)
        trends_min = self._min_extremes._extract_trends(indexes=indexes_min, eps=eps)

        indexes_max = self._max_extremes.get_extr_indexes(after_iter=after_iter)
        trends_max = self._max_extremes._extract_trends(indexes=indexes_max, eps=eps)

        trends = self._combination_trends(trends_min=trends_min, trends_max=trends_max)
        if is_save:
            self._save_trends(trends=trends, after_iter=after_iter)
            self._min_extremes._save_trends(
                trends=trends_min,
                after_iter=after_iter,
            )
            self._max_extremes._save_trends(
                trends=trends_max,
                after_iter=after_iter,
            )

        return trends

    def _combination_extremes(
        self,
        min_extremes: np.ndarray,
        max_extremes: np.ndarray,
    ):
        return merge_sorted_arrays(min_indexes=min_extremes, max_indexes=max_extremes)

    def _combination_trends(
        self,
        trends_min: np.ndarray,
        trends_max: np.ndarray,
    ):
        return merge_sorted_arrays(min_indexes=trends_min, max_indexes=trends_max)
