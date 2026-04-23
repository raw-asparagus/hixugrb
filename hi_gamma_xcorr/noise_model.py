"""Instrument noise models and beam functions.

Implements radio telescope noise (single-dish + interferometer),
Fermi-LAT noise and PSF, and Fermissimo specifications.

Two Fermi-LAT beam modes:
- Gaussian approximation (beam_fermi): forecasting-grade, from Pinetti+(2020)
- Exact King function (beam_fermi_exact): data-analysis-grade, from Ammazzalorso+(2018)
"""

from functools import lru_cache

import numpy as np
from scipy.integrate import quad
from scipy.special import eval_legendre

from . import config as cfg

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_RAYLEIGH = 1.22

_MEERKAT_T_SYS_MODELS = frozenset(('meerkat', 'cunnington2022', 'wang2021'))
_PINETTI_T_SYS_MODELS = frozenset(('pinetti', 'pinetti2020', 'pinetti_2022', 'camera2013'))

# ---------------------------------------------------------------------------
# Radio system temperature
# ---------------------------------------------------------------------------

def T_sys_pinetti(nu_MHz):
    """Pinetti+(2020/2022) generic-radio system temperature [K] at frequency nu [MHz].

    T_sys = 30 K + 60 K * (300 MHz / nu)^{2.55}

    Pinetti+2020 Eq. 3.18 / Pinetti+2022 thesis Eq. 5.26, originally from
    Camera, Santos, Ferreira & Ferramacho (2013), Phys. Rev. Lett. 111, 171302
    (arXiv:1305.6928). The 30 K constant approximates T_inst; the 60 K term is
    a Galactic synchrotron sky temperature with the Cane (1979) spectral index.

    Used by `noise_dish` / `noise_interf` for telescope entries with
    `T_sys_model = 'pinetti'` (the default), i.e. the legacy `MeerKAT`,
    `SKA1`, `SKA2` forecast targets that compare against Pinetti+2020 Table 4.
    """
    nu_MHz = np.asarray(nu_MHz, dtype=float)
    return 30.0 + cfg.T_SKY_COEFF * (cfg.T_SKY_NU_REF / nu_MHz)**cfg.T_SKY_INDEX


def T_sys_meerkat(nu_MHz):
    """Canonical MeerKAT system temperature [K] at frequency nu [MHz].

    Uses the explicit T_sys decomposition from Cunnington et al. (2025),
    arXiv:2510.27549, Appendix A, Eq. A19/A20:

        T_sys(nu) = T_rx(nu) + T_spl + T_CMB + T_gal(nu)

    with:
        T_rx(nu)  = 7.5 K + 10 K * (nu/GHz - 0.75)^2     receiver (Eq. A20;
                                                          tuned by Cunnington
                                                          2022 to match the
                                                          MeerKAT pilot, Wang
                                                          et al. 2021)
        T_spl     = 3 K                                  spillover
        T_CMB     = 2.725 K                              CMB
        T_gal(nu) = 15 K * (408 MHz / nu)^{2.75}         Galactic synchrotron,
                                                          tuned to match average
                                                          sky temperature for
                                                          |b| > 10 deg

    Returns ~14 K at the L-band cosmological window (971-1023 MHz) and ~16 K
    at the UHF cosmological window mid-frequency (~800 MHz). This is roughly
    factor-of-2 *lower* than the Pinetti generic formula, which translates
    into factor-of-4 *less* radio noise per mode (since N propto T_sys^2).

    Used by `noise_dish` / `noise_interf` for telescope entries with
    `T_sys_model = 'meerkat'`, i.e. the new `MeerKLASS_*` HI single-dish
    forecast entries that match the actually-measured MeerKAT receiver
    performance from Wang+2021 / Cunnington+2025.
    """
    nu_MHz = np.asarray(nu_MHz, dtype=float)
    nu_GHz = nu_MHz / 1000.0
    T_rx = 7.5 + 10.0 * (nu_GHz - 0.75)**2
    T_spl = cfg.T_SPL_MEERKAT_K
    T_CMB = cfg.T_CMB_K
    T_gal = cfg.T_GAL_COEFF_MEERKAT * (cfg.T_GAL_NU_REF_MEERKAT / nu_MHz)**cfg.T_GAL_INDEX_MEERKAT
    return T_rx + T_spl + T_CMB + T_gal


def T_sys(nu_MHz, model='pinetti'):
    """Dispatcher for system temperature models. See `T_sys_pinetti` and
    `T_sys_meerkat` for the two available implementations.

    `noise_dish` / `noise_interf` consult the per-telescope `T_sys_model`
    field in `cfg.RADIO_TELESCOPES[telescope]` to choose; the default is
    `'pinetti'` for back-compat.
    """
    if model in _MEERKAT_T_SYS_MODELS:
        return T_sys_meerkat(nu_MHz)
    if model in _PINETTI_T_SYS_MODELS:
        return T_sys_pinetti(nu_MHz)
    raise ValueError(
        f"T_sys_model must be 'pinetti' or 'meerkat' (got {model!r})"
    )


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
    theta_FWHM = _RAYLEIGH * lam / D_m  # radians
    sigma_beam = theta_FWHM / np.sqrt(8.0 * np.log(2.0))
    return np.exp(-ell**2 * sigma_beam**2 / 2.0)


# ---------------------------------------------------------------------------
# Radio noise power spectrum
# ---------------------------------------------------------------------------

def noise_dish(z, telescope, band_name):
    """Single-dish noise power spectrum N_dish^HI [mK^2 sr].

    N_dish = T_sys^2 * S / (N_d * t * Delta_nu * N_b * N_pol * eta^2)

    Returns a scalar noise level (ell-independent white noise).

    The T_sys model used is selected by the per-telescope
    `T_sys_model` field in cfg.RADIO_TELESCOPES (default 'pinetti'),
    so legacy MeerKAT/SKA1/SKA2 entries get the Pinetti+2020 generic
    formula and MeerKLASS_* entries get the canonical MeerKAT model
    from MeerKLASS Collab. 2025 / Wang+2021. See `T_sys_pinetti` and
    `T_sys_meerkat` for the two implementations.
    """
    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_mid = 0.5 * (band['z_min'] + band['z_max'])

    nu = nu_obs(z_mid)
    Tsys = T_sys(nu, model=tel.get('T_sys_model', 'pinetti'))

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

    Valid only for ell >= ell_cut. Same per-telescope T_sys_model dispatch
    as `noise_dish` (see its docstring).
    """
    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_mid = 0.5 * (band['z_min'] + band['z_max'])

    nu = nu_obs(z_mid)
    Tsys = T_sys(nu, model=tel.get('T_sys_model', 'pinetti'))
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
    return np.pi * D_short / (_RAYLEIGH * lam)


def noise_radio_combined(ell, telescope, band_name):
    """Combined radio noise: min(N_dish, N_interf) at each multipole.

    Returns N_l [mK^2 sr] as array matching ell.

    Item 2.2 of clever-beaming-creek plan: tuple-key lru_cache wrapper. The
    underlying computation depends only on (ell-tuple, telescope, band_name)
    and is independent of the HI brightness mode, so the cache is hit 3x
    across the (cunnington, padmanabhan, fixed_omega) modes for the same
    (telescope, band). The returned array is .copy()'d to prevent caller
    mutation aliasing into the cache.
    """
    ell_t = tuple(np.asarray(ell, dtype=float).tolist())
    return _noise_radio_combined_cached(ell_t, telescope, band_name).copy()


@lru_cache(maxsize=128)
def _noise_radio_combined_cached(ell_t, telescope, band_name):
    """Cached body of noise_radio_combined keyed on (tuple(ell), telescope, band_name)."""
    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_mid = 0.5 * (band['z_min'] + band['z_max'])

    ell = np.asarray(ell_t, dtype=float)
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
# Exact Fermi-LAT beam via King function PSF (Ammazzalorso Eq. 4)
# ---------------------------------------------------------------------------

def _king_psf(theta, sigma_king, gamma_king):
    """King function PSF normalized over the sphere.

    PSF(theta) = (1 - 1/gamma) / (2*pi*sigma^2) * [1 + theta^2/(2*gamma*sigma^2)]^{-gamma}

    Parameters
    ----------
    theta : float
        Angle [radians].
    sigma_king : float
        King function scale parameter [radians].
    gamma_king : float
        King function tail index.
    """
    norm = (1.0 - 1.0 / gamma_king) / (2.0 * np.pi * sigma_king**2)
    u = theta**2 / (2.0 * gamma_king * sigma_king**2)
    return norm * (1.0 + u)**(-gamma_king)


def _sigma_king_from_containment(theta_68, gamma_king):
    """Compute King function sigma from the 68% containment angle.

    For a King function, the cumulative integral over a cone of half-angle r is:
        F(r) = 1 - [1 + r^2/(2*gamma*sigma^2)]^{1-gamma}
    Setting F(theta_68) = 0.68 and solving for sigma.
    """
    # F(r) = 1 - [1 + r^2/(2*gamma*sigma^2)]^{1-gamma} = 0.68
    # [1 + r^2/(2*gamma*sigma^2)]^{1-gamma} = 0.32
    # 1 + r^2/(2*gamma*sigma^2) = 0.32^{1/(1-gamma)}
    # sigma^2 = r^2 / (2*gamma * (0.32^{1/(1-gamma)} - 1))
    exponent = 1.0 / (1.0 - gamma_king)
    factor = 0.32**exponent - 1.0
    sigma2 = theta_68**2 / (2.0 * gamma_king * factor)
    return np.sqrt(sigma2)


def beam_fermi_exact(ell, E_GeV):
    """Exact Fermi-LAT beam window function via Legendre transform of King PSF.

    Implements Ammazzalorso et al. (2018) Eq. 4:
        W_l(E) = 2*pi * integral_{-1}^{1} d(cos theta) * P_l(cos theta) * PSF(theta, E)

    Uses a King function PSF with gamma = FERMI_PSF_GAMMA_KING, calibrated from
    the 68% containment angle sigma_0(E).

    Parameters
    ----------
    ell : array-like
        Multipoles (integers).
    E_GeV : float
        Photon energy [GeV].

    Returns
    -------
    W_ell : array
        Beam window function at each multipole.

    Item 2.3 of clever-beaming-creek plan: tuple-key lru_cache wrapper. The
    integer ell values are stable, and E_GeV always comes from a fixed
    config array (FERMI_E_B / AMMAZZALORSO_E_B), so float keys compare equal
    on repeated reads. Returned array is .copy()'d to prevent aliasing.
    """
    ell_t = tuple(np.asarray(ell).astype(int).tolist())
    return _beam_fermi_exact_cached(ell_t, float(E_GeV)).copy()


@lru_cache(maxsize=512)
def _beam_fermi_exact_cached(ell_t, E_GeV):
    """Cached body of beam_fermi_exact keyed on (tuple(int_ell), float(E_GeV))."""
    ell = np.asarray(ell_t, dtype=float)
    gamma_king = cfg.FERMI_PSF_GAMMA_KING

    # 68% containment angle from the parametric formula
    theta_68 = sigma_psf_fermi(E_GeV)  # radians
    sigma_king = _sigma_king_from_containment(theta_68, gamma_king)

    W_ell = np.empty_like(ell)
    for i, l_val in enumerate(ell):
        l_int = int(round(l_val))

        def integrand(theta):
            # Integrate in theta (not cos_theta) for better numerics near theta=0
            # W_l = 2*pi * int_0^pi PSF(theta) * P_l(cos theta) * sin(theta) d(theta)
            if theta < 1e-12:
                return 0.0
            cos_t = np.cos(theta)
            return _king_psf(theta, sigma_king, gamma_king) * eval_legendre(l_int, cos_t) * np.sin(theta)

        # PSF is concentrated near theta=0; integrate with appropriate limits
        # King function drops to negligible beyond ~10*sigma_king
        theta_max = min(50.0 * sigma_king, np.pi)
        val, _ = quad(integrand, 0.0, theta_max, limit=300, epsrel=1e-7)
        W_ell[i] = 2.0 * np.pi * val

    return W_ell


def beam_fermi_bin_averaged(ell, E_min, E_max, alpha=2.3, n_E=10):
    """Energy-averaged beam window function per energy bin (Ammazzalorso Eq. 5).

    <W_l^k> = integral_{E_min}^{E_max} W_l(E) E^{-alpha} dE
              / integral_{E_min}^{E_max} E^{-alpha} dE

    Parameters
    ----------
    ell : array-like
        Multipoles.
    E_min, E_max : float
        Energy bin edges [GeV].
    alpha : float
        UGRB spectral index for weighting (default 2.3).
    n_E : int
        Number of energy points for numerical integration.
    """
    ell = np.asarray(ell, dtype=float)

    # Energy grid (log-spaced within bin)
    E_arr = np.logspace(np.log10(E_min), np.log10(E_max), n_E)

    # Compute W_l(E) at each energy
    W_arr = np.array([beam_fermi_exact(ell, E) for E in E_arr])  # shape (n_E, n_ell)

    # E^{-alpha} weights
    weights = E_arr**(-alpha)

    # Trapezoidal integration in log(E)
    dlogE = np.diff(np.log(E_arr))
    # W_avg = integral W(E) * E^{-alpha} * E * d(logE) / integral E^{-alpha} * E * d(logE)
    # = integral W(E) * E^{1-alpha} d(logE) / integral E^{1-alpha} d(logE)
    w_E = E_arr**(1.0 - alpha)  # = E * E^{-alpha} (Jacobian for d(logE))

    num = np.zeros_like(ell)
    den = 0.0
    for j in range(len(E_arr) - 1):
        dlog = dlogE[j]
        num += 0.5 * (W_arr[j] * w_E[j] + W_arr[j+1] * w_E[j+1]) * dlog
        den += 0.5 * (w_E[j] + w_E[j+1]) * dlog

    return num / den


def ell_max_fermi(E_bin_idx, threshold=0.61):
    """Energy-dependent maximum multipole from beam window threshold (Ammazzalorso Eq. 7).

    Returns l_max where beam_fermi_exact drops to the threshold, or 1000 (whichever is smaller).

    Uses Ammazzalorso bins.
    """
    return cfg.AMMAZZALORSO_ELL_MAX[E_bin_idx]


def pixel_window(ell, nside=1024):
    """HEALPix pixel window function (Gaussian approximation).

    W_pix(l) ≈ exp(-l^2 * theta_pix^2 / 2)
    where theta_pix ≈ sqrt(4*pi / (12 * nside^2)) is the pixel angular size.

    For N_side=1024, theta_pix ≈ 0.001 rad — negligible for l < 1000.
    """
    ell = np.asarray(ell, dtype=float)
    theta_pix = np.sqrt(4.0 * np.pi / (12.0 * nside**2))
    return np.exp(-ell**2 * theta_pix**2 / 2.0)


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
