"""HEP Dataframe"""
from __future__ import annotations

from typing import Any, Callable

import awkward as ak
import numpy as np
import numpy.typing as nptype

from .hepdf_typing import MetaTypes


class HEPDataframe:
    """HEP Dataframe"""

    # TODO: Concatenate
    # TODO: Dump to ROOT file
    # TODO: Dump to JSON file
    # TODO: Load to ROOT file
    # TODO: Load to JSON file
    # TODO: Count
    # TODO: Histogram 1D
    # TODO: Histogram ND
    # TODO: Rewrite `main` as tests

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
        self.filters = ak.Array({"no_filter": np.full(self.length, True)})

    @classmethod
    def from_dataframe(cls, dataframe: HEPDataframe) -> HEPDataframe:
        """Define a new HEPDataframe from another HEPDataframe."""
        new_df = cls(data=dataframe.data, **dataframe.meta)
        for weight_name in dataframe.weights.fields:
            new_df.add_weight(weight_name, dataframe.weights[weight_name])
        for filter_name in dataframe.filters.fields:
            new_df.add_weight(filter_name, dataframe.filters[filter_name])
        return new_df

    @classmethod
    def _from_data_weights_filters_meta(
        cls, data: ak.Record, weights: ak.Array, filters: ak.Array, **kwargs: MetaTypes
    ) -> HEPDataframe:
        """Define a new HEPDataframe from another HEPDataframe.
        Users are not expected to use it."""
        # TODO: Check if weights have a proper naming.
        # TODO check types for all arguments.
        # TODO: check if arguments have fields
        new_df = cls(data=data, **kwargs)
        for weight_name in weights.fields:
            new_df.add_weight(weight_name, weights[weight_name])
        for filter_name in filters.fields:
            new_df.add_weight(filter_name, filters[filter_name])
        return new_df

    def add_meta(self, meta_info_name: str, meta_info: MetaTypes) -> HEPDataframe:
        """Add a meta information."""
        # TODO:"check if key is string."
        # TODO: could be a callable.
        self.meta[meta_info_name] = meta_info
        return self

    def add_weight(
        self, weight_name: str, weight: nptype.ArrayLike | ak.Array | ak.Record
    ) -> HEPDataframe:
        """Add a weight."""
        # TODO: Include systematics.
        # TODO: Check if is 1D
        # TODO: check if has no fields.
        # TODO: could be a callable.
        self.weights[weight_name] = weight
        # TODO: recompute nominal weights.
        return self

    def add_column(
        self, column_name: str, column: nptype.ArrayLike | ak.Array | ak.Record
    ) -> HEPDataframe:
        """Add a column."""
        # TODO: check if has no fields.
        # TODO: could be a callable.
        self.data[column_name] = column
        return self

    def add_filter(
        self, filter_name: str, filter_: nptype.ArrayLike | ak.Array | ak.Record
    ) -> HEPDataframe:
        """Add a filter."""
        # TODO: check if has no fields.
        # TODO: could be a callable.
        if not filter_name.startswith("filter"):
            filter_name = f"filter_{filter_name}"
        self.filters[filter_name] = filter_
        return self

    def pipe(
        self,
        function_to_pipe: Callable,
    ) -> HEPDataframe:
        """Pip a function. The function should receive a HEPDataframe and return also a HEPDataframe."""
        # TODO: check if function_to_pipe returns a HEPDataframe
        return function_to_pipe(self)

    def __getitem__(
        self, index: int | slice | list[bool] | list[int] | nptype.ArrayLike | ak.Array
    ) -> HEPDataframe:
        """Get events by index."""
        if isinstance(index, int):
            index = [index]
        data = self.data[index]
        weights = self.weights[index]
        filters = self.filters[index]
        return HEPDataframe._from_data_weights_filters_meta(
            data, weights, filters, **self.meta
        )

    def __setitem__(self, key: Any, value: Any) -> None:
        raise TypeError(
            "HEPDataframe does not support mutable operations at event level."
        )

    def __len__(self) -> int:
        """Return the length of the dataframe."""
        return self.length

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

    def groupby(
        self, **filters: nptype.ArrayLike | ak.Array | ak.Record
    ) -> GroupedDataframes:
        """Groups events according to `filters`.
        ATTENTION: There is no guarantees that the produced groups are non-overlapping. The user should define appropriate filters to achieve this.
        """
        # TODO: Check if no fields.
        # TODO: Check if 1D
        # TODO: Check if callable

        groups = {}
        for group_name, filter_ in filters.items():
            groups[group_name] = self[filter_]

        return GroupedDataframes(groups)

    @property
    def length(self) -> int:
        """Return the number of events in the dataframe."""
        return len(self.data)

    def __str__(self) -> str:
        """HEPDataframe string representation."""
        meta_str = "--> Meta:\n"
        for met, val in self.meta.items():
            meta_str += f"    {met}: {val}\n"
        filters_str = "--> Filters\n"
        for filter_name in self.filters.fields:
            filters_str += f"    {filter_name}: {self.filters[filter_name]}\n"
        return f"--> HEPDataframe: \n{meta_str[:-2]} \n--> Length: {self.length} \n--> Data (fields): {self.data.fields} \n--> Data: {self.data} \n--> Weights (fields): {self.weights.fields} \n--> Weights (nominal): {self.weights['weight']} \n{filters_str}"

    def __repr__(self) -> str:
        """HEPDataframe representation."""
        return self.__str__()


class GroupedDataframes:
    """Grouped HEP Dataframe"""

    def __init__(self, dataframes: dict[str, HEPDataframe]) -> None:
        # def __init__(self) -> None:
        """Define a Grouped HEPDataframe."""
        # TODO: check if inputs are a List of HEPDataframes
        self.dataframes = dataframes

    @property
    def length(self) -> int:
        """Return the number of groups in the GroupedDataframes."""
        return len(self.dataframes)

    def __str__(self) -> str:
        """GroupedDataframes string representation."""
        return f"--> GroupedDataframes: \n--> Length: {self.length} \n--> Groups labels: {self.dataframes.keys()}"

    def __repr__(self) -> str:
        """GroupedDataframes representation."""
        return self.__str__()

    def __getitem__(self, key: str) -> HEPDataframe:
        """Get HEPDataframe, from GroupedDataframes, by key."""
        # TODO: Check if key is str
        # TODO: Implement a get by key.
        return self.dataframes[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        raise TypeError(
            "GroupedDataframes does not support mutable operations at event level."
        )


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
    print("#####")
    print(my_df.add_weight("my_weight", np.ones(my_df.length) * 3))
    print(my_df.weights.fields)
    print("#####")
    print(my_df.add_column("my_column", np.ones(my_df.length) * 9))
    print("#####")
    print(my_df.add_column("my_awk_column", ak.Array([[], [55], [66, 77]])))
    print(my_df.data.fields)
    print("#####")
    print(my_df.add_meta("my_meta", 34))
    print("#####")
    print(my_df.pipe(lambda x: x))
    print("#####")
    print(my_df.add_filter("dummy_filter", np.full(my_df.length, False)))
    print("#####")
    my_groups = my_df.groupby(
        group_1=np.array([True, False, True]),
        group_2=np.array([False, True, False]),
    )
    print(my_groups)
    print(my_groups["group_1"].data.x)
    print(my_groups["group_2"].data.x)


if __name__ == "__main__":
    main()
