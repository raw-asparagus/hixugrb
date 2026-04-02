"""Tests for SNR forecasts (slow — marked accordingly)."""

import pytest
from hi_gamma_xcorr import statistics as stats


@pytest.mark.slow
def test_snr_meerkat_uhf():
    snr = stats.compute_SNR('MeerKAT', 'UHF', ell_min=10, ell_max=500,
                            n_ell=20, n_z=8, n_M=12)
    assert 0.5 < snr < 10, f"MeerKAT UHF SNR = {snr}"


@pytest.mark.slow
def test_snr_ska1_band2():
    snr = stats.compute_SNR('SKA1', 'Band2', ell_min=10, ell_max=500,
                            n_ell=20, n_z=8, n_M=12)
    # Pinetti target: 5.7
    assert 2 < snr < 15, f"SKA1 Band2 SNR = {snr}"
    assert abs(snr / 5.7 - 1) < 0.5, f"SKA1 ratio = {snr/5.7:.2f}, expected ~1.0"


@pytest.mark.slow
def test_snr_ska2_band2():
    snr = stats.compute_SNR('SKA2', 'Band2', ell_min=10, ell_max=500,
                            n_ell=20, n_z=8, n_M=12)
    # Pinetti target: 8.2
    assert 3 < snr < 20, f"SKA2 Band2 SNR = {snr}"


@pytest.mark.slow
def test_snr_increases_with_sensitivity():
    """SKA2 should have higher SNR than SKA1."""
    snr1 = stats.compute_SNR('SKA1', 'Band2', ell_min=10, ell_max=300,
                             n_ell=15, n_z=6, n_M=10)
    snr2 = stats.compute_SNR('SKA2', 'Band2', ell_min=10, ell_max=300,
                             n_ell=15, n_z=6, n_M=10)
    assert snr2 > snr1, f"SKA2 ({snr2}) should beat SKA1 ({snr1})"
