"""Tests for the angular power spectrum computation."""

import pytest
import numpy as np
from hi_gamma_xcorr import angular_power as ap, config as cfg


def test_dm_sigma_v_linearity():
    """C_l^DM should scale linearly with sigma_v."""
    ell = np.array([100.])
    kwargs = dict(z_min=0.4, z_max=1.45, telescope='MeerKAT', band_name='UHF',
                  m_chi_GeV=100.0, source_classes=[], include_DM=True, n_z=5, n_k_M=10)
    C1 = ap.C_ell_HI_gamma(ell, 5.0, sigma_v=3e-26, **kwargs)['DM'][0]
    C2 = ap.C_ell_HI_gamma(ell, 5.0, sigma_v=3e-25, **kwargs)['DM'][0]
    assert C1 > 0 and C2 > 0, f"C1={C1}, C2={C2}"
    ratio = C2 / C1
    assert ratio == pytest.approx(10.0, rel=0.02), f"ratio = {ratio}"


def test_cl_finite():
    """C_l should be finite (no NaN or Inf)."""
    ell = np.array([50., 200.])
    result = ap.C_ell_HI_gamma(
        ell, 5.0, 0.4, 1.45, 'MeerKAT', 'UHF',
        source_classes=['BL_Lac'], include_DM=False, n_z=5, n_k_M=10
    )
    assert np.all(np.isfinite(result['BL_Lac']))
    assert np.all(np.isfinite(result['total']))


def test_cl_decreases_with_ell():
    """C_l should generally decrease with ell (2-halo dominated)."""
    ell = np.array([30., 100., 300.])
    result = ap.C_ell_HI_gamma(
        ell, 5.0, 0.4, 1.45, 'MeerKAT', 'UHF',
        source_classes=['BL_Lac'], include_DM=False, n_z=5, n_k_M=10
    )
    C = result['BL_Lac']
    assert C[0] > C[-1], "C_l should decrease with ell"


def test_hi_auto_positive():
    ell = np.array([100.])
    C_HI = ap.C_ell_HI_auto(ell, 0.4, 1.45, n_z=5, n_M=10)
    assert C_HI[0] > 0
