"""main UT."""

import importlib
import os

os.environ["TEST_ENV"] = "1"

MAIN_MODULE = importlib.import_module("main")


def test_dummy():
    """Dummy test to ensure at least one UT."""
    assert MAIN_MODULE is not None
