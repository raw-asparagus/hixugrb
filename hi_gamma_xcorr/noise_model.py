"""Instrument noise models and beam functions.

Implements radio telescope noise (single-dish + interferometer),
Fermi-LAT noise and PSF, and Fermissimo specifications.
"""

import numpy as np
from . import config as cfg
from . import cosmology as cosmo

# ---------------------------------------------------------------------------
# Radio system temperature
# ---------------------------------------------------------------------------

def T_sys(nu_MHz):
    """System temperature [K] at observing frequency nu [MHz].

    T_sys = T_inst + T_sky, where T_sky = 60 * (300/nu)^{2.55}.
    T_inst is absorbed into the constant (the formula already includes it).
    """
    nu_MHz = np.asarray(nu_MHz, dtype=float)
    return 30.0 + cfg.T_SKY_COEFF * (cfg.T_SKY_NU_REF / nu_MHz)**cfg.T_SKY_INDEX


def nu_obs(z):
    """Observed 21-cm frequency [MHz] at redshift z."""
    return cfg.NU_21CM / (1.0 + z)


def lambda_obs(z):
    """Observed 21-cm wavelength [m] at redshift z."""
    return cfg.LAMBDA_21CM * (1.0 + z)


# ---------------------------------------------------------------------------
# Radio beam function (Eq. 3.17)
# ---------------------------------------------------------------------------

def beam_radio(ell, z, D_m):
    """Radio beam window function B_l^HI.

    B_l = exp(-l^2 / (2 sigma_beam^2))
    where sigma_beam = theta_FWHM / sqrt(8 ln 2)
    and theta_FWHM = 1.22 * lambda / D  [radians]

    Parameters
    ----------
    ell : array-like
        Multipoles.
    z : float
        Redshift (determines observing wavelength).
    D_m : float
        Effective diameter [m] (D_dish for single-dish, D_interf for interferometer).
    """
    ell = np.asarray(ell, dtype=float)
    lam = lambda_obs(z)
    theta_FWHM = 1.22 * lam / D_m  # radians
    sigma_beam = theta_FWHM / np.sqrt(8.0 * np.log(2.0))
    return np.exp(-ell**2 * sigma_beam**2 / 2.0)


# ---------------------------------------------------------------------------
# Radio noise power spectrum
# ---------------------------------------------------------------------------

def noise_dish(z, telescope, band_name):
    """Single-dish noise power spectrum N_dish^HI [mK^2 sr].

    N_dish = T_sys^2 * S / (N_d * t * Delta_nu * N_b * N_pol * eta^2)

    Returns a scalar noise level (ell-independent white noise).
    """
    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_mid = 0.5 * (band['z_min'] + band['z_max'])

    nu = nu_obs(z_mid)
    Tsys = T_sys(nu)

    # Survey area in steradians
    S_sr = tel['survey_area_deg2'] * (np.pi / 180.0)**2

    # Observation time in seconds
    t_sec = tel['t_obs_hours'] * 3600.0

    # Bandwidth: frequency range corresponding to the redshift bin
    nu_min = cfg.NU_21CM / (1.0 + band['z_max'])
    nu_max = cfg.NU_21CM / (1.0 + band['z_min'])
    delta_nu = (nu_max - nu_min) * 1e6  # Hz

    N_d = tel['n_dishes']
    N_b = tel['n_beams']
    N_pol = tel['n_pol']
    eta = tel['eta']

    # T_sys^2 * Omega_survey / (N_d * t * delta_nu * N_b * N_pol * eta^2)
    # Units: K^2 * sr / (1 * s * Hz * 1 * 1 * 1) = K^2 sr s^{-1} Hz^{-1}
    # But we want mK^2 sr, so convert K^2 → mK^2: multiply by 1e6
    noise = Tsys**2 * S_sr / (N_d * t_sec * delta_nu * N_b * N_pol * eta**2)
    return noise * 1e6  # mK^2 sr


def noise_interf(z, ell, telescope, band_name):
    """Interferometer noise power spectrum N_interf^HI(ell) [mK^2 sr].

    N_interf = T_sys^2 * S * FoV / (n(u) * t * Delta_nu * N_b * N_pol * eta^2)

    Valid only for ell >= ell_cut.
    """
    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_mid = 0.5 * (band['z_min'] + band['z_max'])

    nu = nu_obs(z_mid)
    Tsys = T_sys(nu)
    lam = lambda_obs(z_mid)

    S_sr = tel['survey_area_deg2'] * (np.pi / 180.0)**2
    t_sec = tel['t_obs_hours'] * 3600.0

    nu_min = cfg.NU_21CM / (1.0 + band['z_max'])
    nu_max = cfg.NU_21CM / (1.0 + band['z_min'])
    delta_nu = (nu_max - nu_min) * 1e6  # Hz

    N_b = tel['n_beams']
    N_pol = tel['n_pol']
    eta = tel['eta']
    n_u = tel['n_u']

    # Field of view: FoV = lambda^2 / D_dish^2 [sr]
    FoV = lam**2 / tel['d_dish_m']**2

    noise = Tsys**2 * S_sr * FoV / (n_u * t_sec * delta_nu * N_b * N_pol * eta**2)
    return noise * 1e6  # mK^2 sr


def ell_cut(telescope, band_name):
    """Minimum multipole for interferometric mode.

    ell_cut = pi * D_short / (1.22 * lambda_o)
    where D_short = 2 * D_dish (shortest baseline).
    """
    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_mid = 0.5 * (band['z_min'] + band['z_max'])
    lam = lambda_obs(z_mid)
    D_short = 2.0 * tel['d_dish_m']
    return np.pi * D_short / (1.22 * lam)


def noise_radio_combined(ell, telescope, band_name):
    """Combined radio noise: min(N_dish, N_interf) at each multipole.

    Returns N_l [mK^2 sr] as array matching ell.
    """
    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_mid = 0.5 * (band['z_min'] + band['z_max'])

    ell = np.asarray(ell, dtype=float)
    N_d = noise_dish(z_mid, telescope, band_name)
    N_i = noise_interf(z_mid, ell, telescope, band_name)
    l_cut = ell_cut(telescope, band_name)

    result = np.full_like(ell, N_d)
    mask = ell >= l_cut
    result[mask] = np.minimum(N_d, N_i)
    return result


# ---------------------------------------------------------------------------
# Fermi-LAT beam function (Eqs. 4.9–4.11)
# ---------------------------------------------------------------------------

def sigma_psf_fermi(E_GeV):
    """Fermi-LAT 68% containment angle sigma_0(E) [radians].

    sigma_0(E) = sigma_0(E_ref) * (E/E_ref)^{-0.95} + 0.05 deg
    """
    E_GeV = np.asarray(E_GeV, dtype=float)
    sigma_deg = cfg.FERMI_SIGMA0_REF * (E_GeV / cfg.FERMI_E_REF)**(-0.95) + cfg.FERMI_PSF_FLOOR
    return sigma_deg * np.pi / 180.0  # convert to radians


def beam_fermi(ell, E_GeV):
    """Fermi-LAT beam window function B_l^gamma(E).

    B_l = exp(-sigma_b^2 * l^2 / 2)
    sigma_b(l, E) = sigma_0(E) / (1 + 0.25 * sigma_0(E) * l)
    """
    ell = np.asarray(ell, dtype=float)
    sig0 = sigma_psf_fermi(E_GeV)  # radians
    sigma_b = sig0 / (1.0 + 0.25 * sig0 * ell)
    return np.exp(-sigma_b**2 * ell**2 / 2.0)


# ---------------------------------------------------------------------------
# Fermissimo beam function
# ---------------------------------------------------------------------------

def sigma_psf_fermissimo(E_GeV):
    """Fermissimo 68% containment angle [radians]."""
    E_GeV = np.asarray(E_GeV, dtype=float)
    sigma_deg = (cfg.FERMISSIMO_PSF_ALPHA * cfg.FERMI_SIGMA0_REF *
                 (E_GeV / cfg.FERMI_E_REF)**(-0.95) + cfg.FERMISSIMO_PSF_FLOOR)
    return sigma_deg * np.pi / 180.0


def beam_fermissimo(ell, E_GeV):
    """Fermissimo beam window function."""
    ell = np.asarray(ell, dtype=float)
    sig0 = sigma_psf_fermissimo(E_GeV)
    sigma_b = sig0 / (1.0 + 0.25 * sig0 * ell)
    return np.exp(-sigma_b**2 * ell**2 / 2.0)


# ---------------------------------------------------------------------------
# Fermi-LAT noise
# ---------------------------------------------------------------------------

def noise_fermi(energy_bin_idx):
    """Fermi-LAT noise N^gamma for a given energy bin.

    Returns N^gamma [cm^{-4} s^{-2} sr^{-1}] from Pinetti Table 2.
    """
    return cfg.FERMI_N_GAMMA[energy_bin_idx]


def noise_fermissimo(energy_bin_idx):
    """Fermissimo noise: Fermi noise reduced by the exposure factor."""
    return cfg.FERMI_N_GAMMA[energy_bin_idx] / cfg.FERMISSIMO_EXPOSURE_FACTOR


# ---------------------------------------------------------------------------
# Effective sky fraction
# ---------------------------------------------------------------------------

def f_sky_effective(telescope, band_name, energy_bin_idx, fermissimo=False):
    """Effective sky fraction: min(f_sky_radio, f_sky_gamma)."""
    tel = cfg.RADIO_TELESCOPES[telescope]
    f_radio = tel['f_sky']
    if fermissimo:
        f_gamma = cfg.FERMISSIMO_F_SKY
    else:
        f_gamma = cfg.FERMI_F_SKY[energy_bin_idx]
    return min(f_radio, f_gamma)
