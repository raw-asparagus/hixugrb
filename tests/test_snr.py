"""Tests for SNR forecasts (slow — marked accordingly)."""

import pytest
from hi_gamma_xcorr import statistics as stats


@pytest.mark.slow
def test_snr_meerkat_uhf():
    snr = stats.compute_SNR('MeerKAT', 'UHF', ell_min=10, ell_max=500,
                            n_ell=20, n_z=8, n_M=12)
    assert 0.1 < snr < 10, f"MeerKAT UHF SNR = {snr}"


@pytest.mark.slow
def test_snr_ska1_band2():
    snr = stats.compute_SNR('SKA1', 'Band2', ell_min=10, ell_max=500,
                            n_ell=20, n_z=8, n_M=12)
    # Coarse grid (n_z=8, n_M=12) — order-of-magnitude check only.
    # Pinetti target: 5.7 (with different model choices).
    assert 0.1 < snr < 20, f"SKA1 Band2 SNR = {snr}"


@pytest.mark.slow
def test_snr_ska2_band2():
    snr = stats.compute_SNR('SKA2', 'Band2', ell_min=10, ell_max=500,
                            n_ell=20, n_z=8, n_M=12)
    # Coarse grid — order-of-magnitude check only.
    assert 0.1 < snr < 25, f"SKA2 Band2 SNR = {snr}"


@pytest.mark.slow
def test_snr_increases_with_sensitivity():
    """SKA2 should have higher SNR than SKA1."""
    snr1 = stats.compute_SNR('SKA1', 'Band2', ell_min=10, ell_max=300,
                             n_ell=15, n_z=6, n_M=10)
    snr2 = stats.compute_SNR('SKA2', 'Band2', ell_min=10, ell_max=300,
                             n_ell=15, n_z=6, n_M=10)
    assert snr2 > snr1, f"SKA2 ({snr2}) should beat SKA1 ({snr1})"
