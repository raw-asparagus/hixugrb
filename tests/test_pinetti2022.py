"""Tests for the Pinetti (2022) thesis-faithful parallel module."""

import pytest
import numpy as np
from hi_gamma_xcorr import pinetti2022 as p22
from hi_gamma_xcorr import config as cfg, halo_model as hm, hi_model as hi


def test_pinetti_q_differs_from_pipeline():
    assert p22.PINETTI_Q == 0.75
    assert p22.PINETTI_Q != cfg.SMT_Q


def test_pinetti_omega_hi_fixed():
    assert p22.PINETTI_OMEGA_HI == 2.45e-4


def test_concentration_thesis_differs():
    """Thesis Correa coefficients should give different c(M,z) than pipeline."""
    M = np.array([1e12])
    c_pipe = hm.concentration_correa(M, 0.0)
    c_thesis = p22.concentration_correa_thesis(M, 0.0)
    # Both should be positive and reasonable
    assert float(c_pipe[0]) > 1
    assert float(c_thesis[0]) > 1
    # They should differ
    assert not np.isclose(c_pipe[0], c_thesis[0], rtol=0.01)


def test_T_bar_b_thesis_z0():
    """T_b(z=0) should be approximately 44 muK = 0.044 mK."""
    T = p22.T_bar_b_thesis(0.0)
    assert T == pytest.approx(0.044, abs=0.001)


def test_bias_pinetti_differs():
    """q=0.75 bias should differ from pipeline q=0.707 bias."""
    b_pipe = hm.bias(1e12, 0.5)
    b_pin = p22.bias_pinetti(1e12, 0.5)
    assert b_pipe > 0
    assert b_pin > 0
    # q=0.75 gives slightly different bias
    assert not np.isclose(b_pipe, b_pin, rtol=0.005)


def test_W_HI_pinetti_in_band():
    """W_HI_pinetti should be positive inside the band."""
    W = p22.W_HI_pinetti(0.8, 0.4, 1.45)
    assert W > 0


def test_W_HI_pinetti_outside_band():
    """W_HI_pinetti should be zero outside the band."""
    assert p22.W_HI_pinetti(0.1, 0.4, 1.45) == 0.0
    assert p22.W_HI_pinetti(2.0, 0.4, 1.45) == 0.0


def test_W_HI_pinetti_differs_from_pipeline():
    """Pipeline and thesis W_HI differ by convention choices (post bug-fixes).

    Pipeline:
      - Computed Omega_HI(z) from halo integral (z-dependent, ~1.3e-3 at z=0.8)
      - NO b_HI in W_HI (Pinetti 2020 Eq. 3.15: W_HI = T_b * phi)
    Thesis (pinetti2022):
      - Fixed Omega_HI = 2.45e-4 (T_b = 44 microK * (1+z)^2/E(z))
      - Includes b_HI_pinetti in W_HI (q=0.75 bias)

    At z=0.8, pipeline's computed Omega_HI >> 2.45e-4, so pipeline T_b dominates
    even though thesis multiplies by b_HI.
    """
    W_pipe = hi.W_HI(0.8, 0.4, 1.45)
    W_pin = p22.W_HI_pinetti(0.8, 0.4, 1.45)
    assert W_pipe > 0 and W_pin > 0
    assert W_pipe > W_pin, f"W_pipe={W_pipe}, W_pin={W_pin}"


def test_limber_k_no_half_integer():
    """Thesis uses k = ell/chi, no +0.5 correction."""
    assert p22.limber_k(100, 1000.0) == pytest.approx(0.1)
    # Pipeline would give 100.5/1000 = 0.1005
    assert p22.limber_k(100, 1000.0) != pytest.approx(100.5 / 1000.0)


def test_deviations_registry():
    """DEVIATIONS dict should contain all known deviations."""
    expected_keys = {'smt_q', 'omega_hi', 'correa_coeffs', 'limber_k',
                     'T_b_form', 'pppc4dmid', 'sfg_kr2_sign'}
    assert set(p22.DEVIATIONS.keys()) == expected_keys
    for key, val in p22.DEVIATIONS.items():
        assert 'pipeline' in val
        assert 'pinetti' in val
        assert 'description' in val
