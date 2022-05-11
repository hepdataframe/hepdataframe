from __future__ import annotations

import hepdataframe as hepdf


def test_version() -> None:
    """Test version."""
    assert hepdf.__version__
