"""Tests for external data products (PPPC4DMID, EBL)."""

import pytest
import numpy as np
from hi_gamma_xcorr import pppc4dmid, ebl


class TestPPPC4DMID:
    def test_bb_multiplicity_100gev(self):
        mult = pppc4dmid.total_multiplicity(100.0, 'bb')
        assert 20 < mult < 45, f"bb mult(100) = {mult}"

    def test_tautau_multiplicity_100gev(self):
        mult = pppc4dmid.total_multiplicity(100.0, 'tautau')
        assert 1 < mult < 10, f"tautau mult(100) = {mult}"

    def test_ww_multiplicity_100gev(self):
        mult = pppc4dmid.total_multiplicity(100.0, 'WW')
        assert 15 < mult < 40, f"WW mult(100) = {mult}"

    def test_bb_multiplicity_10gev(self):
        mult = pppc4dmid.total_multiplicity(10.0, 'bb')
        assert 10 < mult < 25

    def test_bb_multiplicity_1tev(self):
        mult = pppc4dmid.total_multiplicity(1000.0, 'bb')
        assert 50 < mult < 120

    def test_cutoff_above_mass(self):
        dNdE = pppc4dmid.dNdE(150.0, 100.0, 'bb')
        assert dNdE == 0.0, "No photons above E = m_chi"

    def test_spectrum_positive_below_mass(self):
        dNdE = pppc4dmid.dNdE(50.0, 100.0, 'bb')
        assert dNdE > 0


class TestEBL:
    def test_transparent_low_energy(self):
        tau = ebl.tau(np.array([10.0]), 0.5)[0]
        assert tau < 0.05, f"tau(10 GeV, z=0.5) = {tau}, should be ~0"

    def test_modest_100gev(self):
        tau = ebl.tau(np.array([100.0]), 0.5)[0]
        assert 0.05 < tau < 0.5

    def test_opaque_1tev(self):
        tau = ebl.tau(np.array([1000.0]), 0.5)[0]
        assert 3.0 < tau < 15.0

    def test_very_opaque_high_z(self):
        tau = ebl.tau(np.array([1000.0]), 1.0)[0]
        assert 10.0 < tau < 50.0

    def test_zero_at_z0(self):
        tau = ebl.tau(np.array([100.0]), 0.0)[0]
        assert tau == 0.0

    def test_attenuation_bounded(self):
        a = ebl.attenuation(np.array([100.0]), 0.5)[0]
        assert 0.0 < a <= 1.0
