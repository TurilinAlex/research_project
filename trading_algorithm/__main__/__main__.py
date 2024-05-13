import numpy as np
from trading_math import argsort


def main():
    values = np.array([1, 2, 3, 4, 5], dtype=np.int32)
    indexes = np.zeros(len(values), dtype=np.int32)
    argsort(values, indexes, len(values))
    print(indexes)


if __name__ == '__main__':
    main()
