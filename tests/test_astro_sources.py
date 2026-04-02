"""Tests for astrophysical gamma-ray source models."""

import pytest
import numpy as np
from scipy.integrate import quad
from hi_gamma_xcorr import astro_sources as astro, config as cfg


@pytest.mark.parametrize("src,n_lo,n_hi", [
    ('FSRQ', 1e-10, 1e-7),
    ('BL_Lac', 1e-8, 1e-4),
    ('mAGN', 1e-9, 1e-5),
    ('SFG', 1e-10, 1e-6),
])
def test_source_density_z0(src, n_lo, n_hi):
    params = cfg.ASTRO_SOURCES[src]
    n, _ = quad(lambda lnL: astro.glf(np.exp(lnL), 0.0, src) * np.exp(lnL),
                np.log(params['L_min']), np.log(params['L_max']), limit=100)
    assert n_lo <= n <= n_hi, f"n({src}, z=0) = {n:.2e}"


def test_glf_positive():
    for src in ['BL_Lac', 'FSRQ', 'mAGN', 'SFG']:
        L = cfg.ASTRO_SOURCES[src]['L_min'] * 10
        phi = astro.glf(L, 0.5, src)
        assert phi >= 0, f"GLF({src}) = {phi}, must be non-negative"


def test_window_astro_positive():
    W = astro.W_gamma_astro(5.0, 0.5, 'BL_Lac')
    assert W > 0


def test_mean_intensity_positive():
    I = astro.mean_intensity(1.0, 'FSRQ', z_max=3.0, n_z=15)
    assert I > 0
