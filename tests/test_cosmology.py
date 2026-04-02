"""Tests for the cosmological backbone (Phase 1)."""

import pytest
from hi_gamma_xcorr import cosmology as cosmo, config as cfg


def test_sigma8_accuracy():
    sig8 = cosmo.sigma_R(8.0, 0.0)
    assert abs(sig8 - cfg.SIGMA_8) / cfg.SIGMA_8 < 0.001, \
        f"sigma_8 = {sig8}, expected {cfg.SIGMA_8} within 0.1%"


def test_hubble_z0():
    assert cosmo.H(0.0) == pytest.approx(cfg.H0, rel=1e-6)


def test_comoving_distance_z1():
    chi = cosmo.chi(1.0)
    # chi(z=1) ~ 2290 Mpc/h for Planck 2018
    assert 2200 < chi < 2400


def test_growth_factor_normalized():
    assert cosmo.growth_factor(0.0) == pytest.approx(1.0, abs=1e-6)


def test_growth_factor_monotonic():
    D0 = cosmo.growth_factor(0.0)
    D1 = cosmo.growth_factor(1.0)
    D2 = cosmo.growth_factor(2.0)
    assert D0 > D1 > D2, "Growth factor should decrease with z"


def test_plin_positive():
    import numpy as np
    k = np.logspace(-2, 1, 20)
    P = cosmo.P_lin(k, 0.0)
    assert np.all(P > 0), "P_lin must be positive"


def test_plin_shape():
    """P_lin should peak around k ~ 0.01-0.02 h/Mpc."""
    import numpy as np
    P_low = cosmo.P_lin(0.001, 0.0)
    P_peak = cosmo.P_lin(0.02, 0.0)
    P_high = cosmo.P_lin(1.0, 0.0)
    assert P_peak > P_low
    assert P_peak > P_high
