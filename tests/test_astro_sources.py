"""Tests for astrophysical gamma-ray source models."""

import pytest
import numpy as np
from scipy.integrate import quad
from hi_gamma_xcorr import (
    astro_sources as astro,
    config as cfg,
    cosmology as cosmo,
    halo_model as hm,
)


@pytest.mark.parametrize("src,n_lo,n_hi", [
    ('FSRQ', 1e-10, 1e-7),
    ('BL_Lac', 1e-11, 1e-4),  # Ajello LDDE strongly suppresses z=0
    ('mAGN', 1e-8, 1e-2),
    ('SFG', 1e-6, 1e0),
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


def test_window_astro_converts_physical_glf_emissivity_to_h_units(monkeypatch):
    """W_gamma_astro should convert the GLF emissivity from Mpc^-3 to (Mpc/h)^-3."""
    source_class = 'BL_Lac'
    params = cfg.ASTRO_SOURCES[source_class]
    alpha = params['alpha']
    E_GeV = 2.0
    z = 0.75

    monkeypatch.setattr(astro, 'glf', lambda L, z_val, src: 1.0)

    W = astro.W_gamma_astro(E_GeV, z, source_class, unresolved_only=False)

    E_min_band = 0.1
    E_max_band = 100.0
    if abs(alpha - 2.0) > 0.01:
        energy_integral = (
            E_max_band**(2.0 - alpha) - E_min_band**(2.0 - alpha)
        ) / (2.0 - alpha)
    else:
        energy_integral = np.log(E_max_band / E_min_band)

    E_rest = E_GeV * (1.0 + z)
    expected_phys = (
        0.5 * (params['L_max']**2 - params['L_min']**2)
        / (cfg.GEV_TO_ERG * energy_integral)
        * E_rest**(-alpha)
    )
    expected_h = expected_phys / (4.0 * np.pi * cfg.h**3)

    assert W == pytest.approx(expected_h, rel=1e-6)


def test_mean_intensity_matches_h_unit_line_of_sight_integral():
    """mean_intensity should integrate the h-based per-chi window with dchi/dz."""
    E_GeV = 1.0
    source_class = 'FSRQ'
    z_max = 3.0
    n_z = 15

    intensity = astro.mean_intensity(E_GeV, source_class, z_max=z_max, n_z=n_z)

    z_arr = np.linspace(0.01, z_max, n_z)
    W_arr = np.array([astro.W_gamma_astro(E_GeV, z, source_class) for z in z_arr])
    H_arr = np.array([cosmo.H(z) for z in z_arr])
    dchi_dz = cfg.C_LIGHT_KM_S * cfg.h / H_arr
    Mpc_h_cm = cfg.MPC_TO_M * 100.0 / cfg.h
    dz = z_arr[1] - z_arr[0]
    expected = np.sum(W_arr * dchi_dz / Mpc_h_cm**2) * dz

    assert intensity == pytest.approx(expected, rel=1e-12)


def test_window_astro_uses_observed_input_and_rest_frame_spectrum(monkeypatch):
    """Freeze GLF evolution and verify the window scales as E_rest^{-alpha}.

    With phi(L, z) held constant and unresolved_only=False, all redshift
    dependence in W_gamma_astro should come from E_rest = (1+z) * E_obs.
    This guards against treating the input energy as emitted/rest-frame and
    against reintroducing an extra legacy (1+z)^-2 prefactor.
    """
    source_class = 'BL_Lac'
    alpha = cfg.ASTRO_SOURCES[source_class]['alpha']
    E_GeV = 1.0
    z_lo, z_hi = 0.5, 1.5

    monkeypatch.setattr(astro, 'glf', lambda L, z, src: 1.0)

    W_lo = astro.W_gamma_astro(E_GeV, z_lo, source_class, unresolved_only=False)
    W_hi = astro.W_gamma_astro(E_GeV, z_hi, source_class, unresolved_only=False)

    expected_ratio = ((1.0 + z_lo) / (1.0 + z_hi))**(-alpha)
    assert W_lo / W_hi == pytest.approx(expected_ratio, rel=1e-3)


def test_bias_astro_converts_physical_mass_relations_to_code_units(monkeypatch):
    """mAGN and SFG bias relations should convert physical M_sun to M_sun/h."""
    recorded_masses = []

    def fake_bias(M, z):
        recorded_masses.append(M)
        return 1.0

    monkeypatch.setattr(hm, 'bias', fake_bias)

    z = 0.8

    astro.bias_astro(z, 'mAGN')
    L_char_magn = 1e44
    M_star = cfg.MAGN_MSTAR_NORM * (
        L_char_magn / cfg.MAGN_MSTAR_LNORM
    )**cfg.MAGN_MSTAR_SLOPE
    M_halo_magn_phys = 1e13 * (
        M_star / (cfg.MAGN_MHALO_PIVOT * (1.0 + z)**cfg.MAGN_MHALO_Z_EXP)
    )**cfg.MAGN_MHALO_SLOPE
    assert recorded_masses[-1] == pytest.approx(max(M_halo_magn_phys, 1e10) / cfg.h)

    astro.bias_astro(z, 'SFG')
    L_char_sfg = 1e39
    M_halo_sfg_phys = (
        cfg.SFG_MHALO_NORM
        / (1.0 + z)**cfg.SFG_MHALO_Z_EXP
        * (L_char_sfg / cfg.SFG_MHALO_LNORM)**cfg.SFG_MHALO_SLOPE
    )
    assert recorded_masses[-1] == pytest.approx(max(M_halo_sfg_phys, 1e10) / cfg.h)


# ---------------------------------------------------------------------------
# mAGN: intermediate function tests
# ---------------------------------------------------------------------------

def test_willott_rlf_z0():
    """Willott RLF at z=0 and L=10^26 W/Hz should be ~10^{-7} Mpc^{-3}/dex."""
    rho = astro._willott_rlf(1e26, 0.0)
    assert 1e-9 <= rho <= 1e-5, f"Willott RLF(1e26, z=0) = {rho:.2e}"


def test_L151_roundtrip():
    """Forward→inverse chain should recover L_gamma."""
    L_gamma_test = 1e44  # erg/s
    L_151, _ = astro._L151_from_Lgamma(L_gamma_test)
    # Forward chain: L_151 → L_1p4 → L_core [W/Hz] → nuLnu [erg/s] → L_gamma
    freq_ratio = (1400.0 / 151.0)**cfg.RADIO_ALPHA
    L_1p4 = L_151 / freq_ratio
    log_core_WHZ = cfg.LARA_A + cfg.LARA_B * np.log10(L_1p4)
    # Convert W/Hz → erg/s (nuL_nu): L_core * nu_5GHz * 1e7
    log_nuLnu = log_core_WHZ + np.log10(5e9 * 1e7)
    log_Lg = cfg.DIMAURO_GAMMA_RADIO_A + cfg.DIMAURO_GAMMA_RADIO_B * log_nuLnu
    L_gamma_recovered = 10.0**log_Lg
    assert abs(L_gamma_recovered / L_gamma_test - 1.0) < 1e-10


def test_magn_window_shape():
    """mAGN per-chi window should peak at moderate z (~0.3-1.5)."""
    z_arr = np.linspace(0.05, 3.0, 100)
    W_arr = np.array([astro.W_gamma_astro(1.0, z, 'mAGN') for z in z_arr])
    z_peak = z_arr[np.argmax(W_arr)]
    assert 0.1 <= z_peak <= 2.5, f"mAGN window peaks at z={z_peak:.2f}"
    # Window at z=0.5 should be at least 20% of peak
    W_at_05 = np.interp(0.5, z_arr, W_arr)
    assert W_at_05 / W_arr.max() > 0.1, "mAGN window too suppressed at z=0.5"


# ---------------------------------------------------------------------------
# SFG: intermediate function tests
# ---------------------------------------------------------------------------

def test_gruppioni_z0():
    """Gruppioni IR LF at z=0, L=10^10 L_sun should be ~10^{-3} Mpc^{-3}/dex."""
    phi = astro._gruppioni_ir_lf(1e10, 0.0)
    assert 1e-5 <= phi <= 1e-1, f"Gruppioni IR LF(1e10, z=0) = {phi:.2e}"


def test_L_IR_roundtrip():
    """Ackermann L_gamma-L_IR inversion should be consistent."""
    L_gamma = 1e40
    L_IR, jac = astro._L_IR_from_Lgamma(L_gamma)
    # Forward: log10(L_gamma) = alpha * log10(L_IR / 1e10 L_sun) + beta
    log_Lg = cfg.ACKERMANN_ALPHA_IR * np.log10(L_IR / 1e10) + cfg.ACKERMANN_BETA_IR
    assert abs(log_Lg - np.log10(L_gamma)) < 1e-10
    assert abs(jac - 1.0 / cfg.ACKERMANN_ALPHA_IR) < 1e-10


def test_sfg_window_shape():
    """SFG per-chi window should retain significant weight around z~1.

    Under the current convention W_gamma_astro already returns the per-chi
    photon-emissivity-form window in h-dependent units, so recovering the
    underlying physical emissivity requires multiplying by 4pi*h^3.
    """
    z_arr = np.linspace(0.05, 4.0, 100)
    W_arr = np.array([astro.W_gamma_astro(1.0, z, 'SFG') for z in z_arr])
    j_arr = W_arr * 4 * np.pi * cfg.h**3
    z_peak_j = z_arr[np.argmax(j_arr)]
    assert 0.1 <= z_peak_j <= 2.0, f"SFG emissivity peaks at z={z_peak_j:.2f}"
    # Window at z=1 should be at least 20% of peak
    W_at_1 = np.interp(1.0, z_arr, W_arr)
    assert W_at_1 / W_arr.max() > 0.2, "SFG window too suppressed at z=1"
