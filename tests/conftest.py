"""Shared fixtures for the HI x gamma-ray pipeline test suite."""

import pytest
from hi_gamma_xcorr import cosmology as cosmo


@pytest.fixture(scope="session", autouse=True)
def init_cosmology():
    """Initialize cosmology (CAMB + hmf) once for the entire test session."""
    cosmo.init()
