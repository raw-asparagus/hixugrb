"""Tests for the dark matter model (Phase 4)."""

import pytest
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
