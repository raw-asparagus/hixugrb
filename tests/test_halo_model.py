"""Tests for the halo model machinery (Phase 2)."""

import pytest
import numpy as np
from hi_gamma_xcorr import halo_model as hm, config as cfg


def test_mass_function_normalization():
    norm = hm.check_mass_normalization(z=0.0)
    assert 0.5 < norm < 0.8, f"Mass norm = {norm}, expected ~0.6"


def test_bias_normalization():
    bias_norm = hm.check_bias_normalization(z=0.0)
    assert 0.5 < bias_norm < 1.0


def test_concentration_z0():
    c = float(hm.concentration(np.array([1e12]), 0.0)[0])
    assert 6 < c < 12, f"c(1e12, z=0) = {c}, expected ~8"


def test_nfw_fourier_normalization():
    """u_NFW(k -> 0) should equal 1."""
    u = hm.u_nfw(np.array([1e-6]), 1e12, z=0.0)[0]
    assert u == pytest.approx(1.0, abs=1e-5)


def test_nfw_fourier_decays():
    """u_NFW should decrease from 1 at low k to < 1 at high k."""
    k = np.array([1e-4, 0.1, 1.0, 10.0])
    u = hm.u_nfw(k, 1e12, z=0.0)
    assert u[0] > u[-1]
    assert u[-1] < 1.0


def test_virial_radius_increases_with_mass():
    R1 = hm.R_vir(1e10, 0.0)
    R2 = hm.R_vir(1e12, 0.0)
    R3 = hm.R_vir(1e14, 0.0)
    assert R1 < R2 < R3


def test_circular_velocity_reasonable():
    vc = hm.v_circ(1e12, 0.0)
    assert 100 < vc < 250, f"v_c(1e12) = {vc} km/s, expected 100-250"


def test_dndm_positive():
    for M in [1e10, 1e12, 1e14]:
        dn = hm.dndM(M, 0.0)
        assert dn > 0, f"dndM({M}) = {dn}, must be positive"


def test_dndm_decreases_at_high_mass():
    dn12 = hm.dndM(1e12, 0.0)
    dn14 = hm.dndM(1e14, 0.0)
    assert dn14 < dn12
