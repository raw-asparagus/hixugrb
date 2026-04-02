"""Tests for the instrument noise model (Phase 6)."""

import pytest
import numpy as np
from hi_gamma_xcorr import noise_model as nm, config as cfg


def test_tsys_1ghz():
    T = nm.T_sys(1000)
    assert 20 < T < 40, f"T_sys(1 GHz) = {T} K"


def test_tsys_increases_at_low_freq():
    T_high = nm.T_sys(1000)
    T_low = nm.T_sys(500)
    assert T_low > T_high


def test_fermi_noise_matches_table2():
    """Fermi noise values must match Pinetti Table 2 exactly."""
    for ie in range(cfg.FERMI_N_BINS):
        N = nm.noise_fermi(ie)
        expected = cfg.FERMI_N_GAMMA[ie]
        assert N == pytest.approx(expected, rel=1e-10), \
            f"Bin {ie}: N={N} vs expected {expected}"


def test_beam_fermi_decreases_with_ell():
    ell = np.array([10., 100., 500., 1000.])
    B = nm.beam_fermi(ell, 5.0)
    assert all(B[i] >= B[i+1] for i in range(len(B)-1))


def test_beam_fermi_bounded():
    B = nm.beam_fermi(np.array([100.]), 5.0)
    assert 0 < B[0] <= 1.0


def test_beam_radio_bounded():
    B = nm.beam_radio(np.array([100.]), 0.5, 13.5)
    assert 0 < B[0] <= 1.0


def test_noise_dish_positive():
    N = nm.noise_dish(0.5, 'MeerKAT', 'UHF')
    assert N > 0


def test_fsky_effective():
    f = nm.f_sky_effective('MeerKAT', 'UHF', 5)
    assert 0 < f < 1
