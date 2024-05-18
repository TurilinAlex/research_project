import numpy as np


def min_extremum(index: np.ndarray, eps: int) -> np.ndarray:
    n, extreme_min = len(index), []
    for i in range(n):
        for j in range(1, i + 1):
            if abs(index[i] - index[i - j]) <= eps:
                break
        else:
            extreme_min.append(index[i])
    return np.array(extreme_min)


def max_extremum(index: np.ndarray[np.uint32], eps: int) -> np.ndarray[np.uint32]:
    n, extreme_max = len(index), []
    for i in range(n):
        for j in range(1, (n - i)):
            if abs(index[i] - index[i + j]) <= eps:
                break
        else:
            extreme_max.append(index[i])
    return np.array(extreme_max)


def merge_sorted_arrays(min_indexes: np.ndarray, max_indexes: np.ndarray) -> np.ndarray:
    i, j, k = 0, 0, 0
    merged_array = np.empty(
        len(min_indexes) + len(max_indexes), dtype=min_indexes.dtype
    )

    while i < len(min_indexes) and j < len(max_indexes):
        if min_indexes[i] <= max_indexes[j]:
            merged_array[k] = min_indexes[i]
            i += 1
        else:
            merged_array[k] = max_indexes[j]
            j += 1
        k += 1

    while i < len(min_indexes):
        merged_array[k] = min_indexes[i]
        i += 1
        k += 1

    while j < len(max_indexes):
        merged_array[k] = max_indexes[j]
        j += 1
        k += 1

    return merged_array


def merge_sorted_arrays_custom(
    extr_min_index: np.ndarray[np.uint32],
    extr_max_index: np.ndarray[np.uint32],
    values: np.ndarray[np.float32],
):
    def get_status():
        if i < len(extr_min_index) and j < len(extr_max_index):
            if extr_max_index[j] < extr_min_index[i]:
                return -1
            if extr_max_index[j] > extr_min_index[i]:
                return 1
            if extr_max_index[j] == extr_min_index[i]:
                return 0

        if i >= len(extr_min_index):
            return -1
        if j >= len(extr_max_index):
            return 1

        return 0

    extr, extr_min_new, extr_max_new = [], [], []
    i = j = 0
    status = 0
    i_min = j_max = None
    min_over, max_over = max(values) + 1, min(values) - 1

    value_min, value_max = min_over, max_over

    while i + j < len(extr_min_index) + len(extr_max_index):
        status = get_status()

        if status >= 0:
            if values[extr_min_index[i]] < value_min:
                value_min = values[extr_min_index[i]]
                i_min = extr_min_index[i]
            if j_max is not None:
                extr_max_new.append(j_max)
                extr.append(j_max)
                j_max = None
            value_max = max_over
            i += 1
        else:
            if values[extr_max_index[j]] >= value_max:
                value_max = values[extr_max_index[j]]
                j_max = extr_max_index[j]
            if i_min is not None:
                extr_min_new.append(i_min)
                extr.append(i_min)
                i_min = None
            value_min = min_over
            j += 1

    if status < 0:
        extr.append(j_max)
        extr_max_new.append(j_max)
    else:
        extr.append(i_min)
        extr_min_new.append(i_min)

    return np.array(extr), np.array(extr_min_new), np.array(extr_max_new)
