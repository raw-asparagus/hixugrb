"""Tests for the HI model.

Parameters from Padmanabhan+ (2017) Table A1 (modified NFW profile).
"""

import pytest
import numpy as np
from hi_gamma_xcorr import hi_model as hi


def test_omega_hi_z0_range():
    """Omega_HI(z=0) should be ~4e-4 to 2e-3 (ALFALFA/HIPASS observations)."""
    omega = hi.Omega_HI(0.0)
    assert 2e-4 < omega < 2e-3, f"Omega_HI(z=0) = {omega}"


def test_hi_bias_z0_range():
    b = hi.b_HI(0.0)
    assert 0.5 < b < 1.5, f"b_HI(z=0) = {b}"


def test_hi_bias_increases_with_z():
    b0 = hi.b_HI(0.0)
    b05 = hi.b_HI(0.5)
    b1 = hi.b_HI(1.0)
    assert b1 > b05 > b0, "HI bias should increase with z"


def test_brightness_temperature_positive():
    Tb = hi.T_bar_b(0.0)
    assert Tb > 0, "T_bar_b must be positive"
    assert Tb < 0.2, f"T_bar_b(z=0) = {Tb} mK, should be < 0.2 mK"


def test_mhi_cutoff():
    """M_HI should be negligible below the v_c0 cutoff mass."""
    mhi_low = hi.M_HI(1e9, 0.0)
    mhi_high = hi.M_HI(1e12, 0.0)
    assert mhi_low < 1e-5 * mhi_high, "HI should be negligible at low mass"


def test_u_hi_normalization():
    """u_HI(k -> 0) should be ~1."""
    u = hi.u_HI(np.array([1e-5]), 1e12, 0.0)
    assert u[0] == pytest.approx(1.0, abs=0.01)


def test_parameters_self_consistent():
    """Verify parameters are from Table A1 (modified NFW), not mixed."""
    from hi_gamma_xcorr import config as cfg
    # Table A1 values
    assert cfg.HI_ALPHA == pytest.approx(0.176, abs=0.001)
    assert cfg.HI_BETA == pytest.approx(-0.69, abs=0.01)
    assert cfg.HI_VC0 == pytest.approx(10**1.61, rel=0.01)
    assert cfg.HI_C0 == pytest.approx(139.0, abs=1.0)
    assert cfg.HI_GAMMA_CONC == pytest.approx(0.13, abs=0.01)
