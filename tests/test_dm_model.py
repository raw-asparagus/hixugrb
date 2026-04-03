"""Tests for the dark matter model."""

import pytest
import numpy as np
from hi_gamma_xcorr import dm_model as dm, config as cfg


def test_clumping_factor_range():
    Delta2 = dm.clumping_factor(0.0, n_M=50, boost_scenario='none')
    assert 1e4 < Delta2 < 1e7, f"Delta^2 = {Delta2}"


def test_clumping_factor_positive():
    for z in [0.0, 0.5, 1.0]:
        Delta2 = dm.clumping_factor(z, n_M=30, boost_scenario='none')
        assert Delta2 > 0


def test_dm_window_positive():
    W = dm.W_gamma_DM(5.0, 0.5, 100.0, sigma_v=cfg.SIGMA_V_THERMAL)
    assert W > 0, "DM window should be positive for valid parameters"


def test_dm_window_scales_with_sigma_v():
    W1 = dm.W_gamma_DM(5.0, 0.5, 100.0, sigma_v=3e-26)
    W2 = dm.W_gamma_DM(5.0, 0.5, 100.0, sigma_v=3e-25)
    ratio = W2 / W1
    assert ratio == pytest.approx(10.0, rel=0.01)


def test_dm_window_zero_above_mass():
    """Photon energy above m_chi should give ~zero window."""
    W = dm.W_gamma_DM(200.0, 0.5, 100.0)  # E > m_chi
    assert W == 0.0 or W < 1e-50


# ---------------------------------------------------------------------------
# Boost factor tests
# ---------------------------------------------------------------------------

def test_boost_z0_milky_way():
    """B(10^12 M_sun, z=0) should be ~10-20 (Moliné Fig. 6)."""
    M_mw = 1e12 / cfg.h  # 10^12 M_sun in M_sun/h
    B = dm.boost_moline(np.array([M_mw]), 0.0)
    assert 5 < B[0] < 50, f"B(10^12, z=0) = {B[0]:.1f}"


def test_boost_z_scaling():
    """B(M, z=1) should be ~half of B(M, z=0) from 1/(1+z) scaling."""
    M_test = np.array([1e12 / cfg.h])
    B0 = dm.boost_moline(M_test, 0.0)[0]
    B1 = dm.boost_moline(M_test, 1.0)[0]
    ratio = B1 / B0
    assert ratio == pytest.approx(0.5, rel=0.01), f"B(z=1)/B(z=0) = {ratio:.3f}"


def test_boost_increases_with_mass():
    """Boost should increase with halo mass."""
    M_arr = np.array([1e8, 1e10, 1e12, 1e14]) / cfg.h
    B_arr = dm.boost_moline(M_arr, 0.0)
    assert all(B_arr[i+1] > B_arr[i] for i in range(len(B_arr)-1))


def test_boost_positive():
    """Boost should be non-negative at all masses and redshifts."""
    for z in [0.0, 1.0, 3.0]:
        M_arr = np.logspace(6, 15, 20) / cfg.h
        B_arr = dm.boost_moline(M_arr, z)
        assert np.all(B_arr >= 0)
