"""Grouped HEP Dataframe"""
from __future__ import annotations

from typing import List

from hepdataframe import HEPDataframe


class GroupedDataframes:
    """Grouped HEP Dataframe"""

    def __init__(self, dataframes: List[HEPDataframe]) -> None:
        """Define a Grouped HEPDataframe."""
        # TODO: check if inputs are a List of HEPDataframes
        self.dataframes = dataframes


def main() -> None:
    """Grouped HEP Dataframe - Main"""


if __name__ == "__main__":
    main()
