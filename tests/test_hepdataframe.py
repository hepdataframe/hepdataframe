from __future__ import annotations

import awkward as ak

import hepdataframe as hepdf


def test_length() -> None:
    """Test length property."""
    test_array = ak.Array({"x": [1, 2, 3], "y": [[1, 2, 3, 4, 5], [1], []]})
    test_df = hepdf.HEPDataframe(test_array)
    assert test_df.length == 3
