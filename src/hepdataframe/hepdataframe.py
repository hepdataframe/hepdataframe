"""HEP Dataframe"""
from __future__ import annotations

# import awkward as ak
import numpy as np
from numpy.typing import ArrayLike


class HEPDataframe:
    """HEP Dataframe"""

    def __init__(self, data: ArrayLike) -> None:
        """Define a HEPDataframe."""
        # if not isinstance(data, ArrayLike):
        #     raise TypeError("Events should be an 'awkward.Array'.")
        self.data = data

    @property
    def my_property(self) -> ArrayLike:
        """My property."""
        return np.array([1, 2, 3])


def main(fooo: str) -> None:
    """HEP Dataframe - Main"""
    print(fooo)
    print(np.array([1, 2, 3]))


if __name__ == "__main__":
    main("bar")
