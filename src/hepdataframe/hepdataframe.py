"""HEP Dataframe"""
from __future__ import annotations

from typing import Any, List, Union

import awkward as ak
import numpy as np
import numpy.typing as nptype

MetaTypes = Union[float, int, str, List[Union[float, int, str]]]


class HEPDataframe:
    """HEP Dataframe"""

    def __init__(self, data: ak.Record, **kwargs: MetaTypes) -> None:
        """Define a HEPDataframe."""
        if (not isinstance(data, ak.Array)) and (not isinstance(data, ak.Record)):
            raise TypeError("Data should be an 'awkward.Record' or 'awkward.Array'.")
        if not data.fields:
            raise AttributeError(
                "Data should have fields. Usually, 'awkward.Array' with fields are build from dicts or using 'awkward.zip' (https://awkward-array.readthedocs.io/en/latest/_auto/ak.zip.html)."
            )

        self.meta = kwargs
        self.data = data
        self.weights = ak.Array({"weight": np.ones(self.length)})

    @classmethod
    def from_dataframe(cls, dataframe: HEPDataframe) -> HEPDataframe:
        """Define a new HEPDataframe from another HEPDataframe."""
        new_df = cls(data=dataframe.data, **dataframe.meta)
        for weight_name in dataframe.weights.fields:
            new_df.add_weight(weight_name, dataframe.weights[weight_name])
        return new_df

    @classmethod
    def _from_data_weights_meta(
        cls, data: ak.Record, weights: ak.Array | ak.Record, **kwargs: MetaTypes
    ) -> HEPDataframe:
        """Define a new HEPDataframe from another HEPDataframe.
        Users are not expected to use it."""
        # TODO: Check if weights have a proper naming.
        # TODO check types for all arguments.
        # TODO: check if arguments have fields
        new_df = cls(data=data, **kwargs)
        for weight_name in weights.fields:
            new_df.add_weight(weight_name, weights[weight_name])
        return new_df

    def add_weight(
        self, weight_name: str, weight: nptype.ArrayLike | ak.Array | ak.Record
    ) -> HEPDataframe:
        """Add a weight."""
        # TODO: Include systematics.
        # TODO: Check if is 1D
        # TODO: check if has no fields.
        self.weights[weight_name] = weight
        return self

    def add_column(
        self, column_name: str, column: nptype.ArrayLike | ak.Array | ak.Record
    ) -> HEPDataframe:
        """Add a column."""
        # TODO: check if has no fields.
        self.data[column_name] = column
        return self

    def __getitem__(
        self, index: int | slice | list[bool] | list[int] | nptype.ArrayLike | ak.Array
    ) -> HEPDataframe:
        """Get events by index."""
        if isinstance(index, int):
            index = [index]
        data = self.data[index]
        weights = self.weights[index]
        return HEPDataframe._from_data_weights_meta(data, weights, **self.meta)

    def __setitem__(self, key: Any, value: Any) -> None:
        raise TypeError(
            "HEPDataframe does not support mutable operations at event level."
        )

    def head(self, n_events: int = 5) -> HEPDataframe:
        """Return the first `n_events` events. Default: first 5 events."""
        if n_events <= 0:
            raise ValueError("`n_events` should be greater than 0.")
        return self[0:n_events]

    def tail(self, n_events: int = 5) -> HEPDataframe:
        """Return the last `n_events` events. Default: last 5 events."""
        if n_events <= 0:
            raise ValueError("`n_events` should be greater than 0.")

        if n_events >= self.length:
            n_events = self.length
        return self[self.length - n_events :]

    def __len__(self) -> int:
        """Return the length of the dataframe."""
        return self.length

    @property
    def length(self) -> int:
        """Return the number of events in the dataframe."""
        return len(self.data)

    def __str__(self) -> str:
        """HEPDataframe string representation."""
        meta_str = "\n"
        for met, val in self.meta.items():
            meta_str += f"{met}: {val} - "
        return f"HEPDataframe: {meta_str[:-2]} \nLength: {self.length} \nData: {self.data} \nWeights (nominal): {self.weights['weight']}"

    def __repr__(self) -> str:
        """HEPDataframe representation."""
        return self.__str__()


def main() -> None:
    """HEP Dataframe - Main"""
    my_array = ak.Array({"x": [1, 2, 3], "y": [[1, 2, 3, 4, 5], [1], []]})
    my_df = HEPDataframe(data=my_array, foo="bar")
    print("#####")
    print(my_df)
    print("#####")
    print(my_df[0])
    print("#####")
    print(my_df)
    print("#####")
    print(my_df.head(99))
    print("#####")
    print(my_df.tail())


if __name__ == "__main__":
    main()
    # print(type(ak.Array({"x": [1, 2, 3]})))
