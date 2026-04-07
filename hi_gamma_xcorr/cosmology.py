"""Cosmological backbone: P_lin(k,z), H(z), chi(z), D(z), sigma(M,z).

Uses CAMB as the Boltzmann solver.  All outputs are in h-dependent units:
  - k in h/Mpc, P(k) in (Mpc/h)^3, distances in Mpc/h, masses in M_sun/h.
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.integrate import quad

from . import config as cfg

# ---------------------------------------------------------------------------
# Module-level state: initialized on first call to init()
# ---------------------------------------------------------------------------
_camb_results = None
_Plin_interp = None   # 2D interpolator for P_lin(k, z)
_k_grid = None
_z_grid = None

# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def init(force=False):
    """Run CAMB and build interpolation tables. Idempotent unless force=True."""
    global _camb_results, _Plin_interp, _k_grid, _z_grid
    if _camb_results is not None and not force:
        return

    import camb

    pars = camb.CAMBparams()
    pars.set_cosmology(
        H0=cfg.H0,
        ombh2=cfg.OMEGA_B_H2,
        omch2=cfg.OMEGA_CDM_H2,
        omk=0.0,
        tau=0.0544,      # Planck 2018 reionization optical depth
        TCMB=cfg.T_CMB,
    )
    pars.InitPower.set_params(As=cfg.A_S, ns=cfg.N_S)

    # Request matter power at the redshifts we need (CAMB wants descending order)
    z_arr = np.sort(cfg.Z_GRID)[::-1]
    # Cap kmax at 500 h/Mpc (= 500*h 1/Mpc for CAMB) for reasonable init time.
    # This is sufficient for sigma(M) down to M ~ 10^6 M_sun/h and
    # for the Limber integral at l <= 2000.
    kmax_camb = min(cfg.K_MAX, 500.0) * cfg.h * 1.1
    pars.set_matter_power(
        redshifts=list(z_arr),
        kmax=kmax_camb,
        nonlinear=False,
    )
    pars.NonLinear = camb.model.NonLinear_none

    results = camb.get_results(pars)
    _camb_results = results

    # Build P_lin(k, z) on the config grids
    # CAMB returns k in 1/Mpc (no h); P in Mpc^3.  Convert to h-units.
    k_h = cfg.K_GRID                     # h/Mpc — our target grid
    k_camb = k_h * cfg.h                 # 1/Mpc — what CAMB expects

    # Ascending z for interpolation
    z_asc = np.sort(cfg.Z_GRID)
    _z_grid = z_asc
    _k_grid = k_h

    # Evaluate P(k, z) on the 2D grid
    # camb.get_matter_power_interpolator gives P(k[1/Mpc]) in Mpc^3
    PK = results.get_matter_power_interpolator(
        nonlinear=False, var1='delta_tot', var2='delta_tot',
        hubble_units=False, k_hunit=False,
    )

    Plin_grid = np.empty((len(z_asc), len(k_h)))
    for iz, z in enumerate(z_asc):
        # PK.P(z, k) with k in 1/Mpc → P in Mpc^3
        P_Mpc3 = PK.P(z, k_camb)
        # Convert: P [Mpc^3] → P [(Mpc/h)^3] = P * h^3
        Plin_grid[iz, :] = P_Mpc3 * cfg.h**3

    # 2D spline in log-log space for positivity and smoothness
    log_k = np.log10(k_h)
    log_P = np.log10(np.clip(Plin_grid, 1e-100, None))
    _Plin_interp = RectBivariateSpline(z_asc, log_k, log_P, kx=3, ky=3)


def _ensure_init():
    if _camb_results is None:
        init()


# ---------------------------------------------------------------------------
# Hubble rate and distances
# ---------------------------------------------------------------------------

def E(z):
    """Dimensionless Hubble rate E(z) = H(z)/H0."""
    z = np.asarray(z, dtype=float)
    return np.sqrt(cfg.OMEGA_M * (1.0 + z)**3 + cfg.OMEGA_LAMBDA)


def H(z):
    """Hubble rate H(z) [km/s/Mpc]."""
    return cfg.H0 * E(z)


def _chi_scalar(z):
    """Comoving distance for a single redshift [Mpc/h]."""
    val, _ = quad(lambda zp: cfg.C_LIGHT_KM_S / H(zp), 0.0, z)
    return val * cfg.h


def chi(z):
    """Comoving distance chi(z) [Mpc/h].

    Integrates c/H(z') from 0 to z.  Returns scalar or array matching input.
    """
    z = np.asarray(z, dtype=float)
    scalar = z.ndim == 0
    z = np.atleast_1d(z)
    result = np.array([_chi_scalar(float(zi)) for zi in z])
    return float(result[0]) if scalar else result


def d_L(z):
    """Luminosity distance [Mpc/h]."""
    z = np.asarray(z, dtype=float)
    return chi(z) * (1.0 + z)


# ---------------------------------------------------------------------------
# Growth factor
# ---------------------------------------------------------------------------

def _growth_unnorm(z):
    """Unnormalized growth integral at a single z."""
    ez = E(z)
    val, _ = quad(lambda zp: (1.0 + zp) / E(zp)**3, z, np.inf, limit=200)
    return ez * val


def growth_factor(z):
    """Linear growth factor D(z), normalized so D(0) = 1.

    Uses the integral form: D(z) proportional to E(z) * integral_z^inf dz'/(1+z')/E(z')^3,
    which is exact for flat LCDM.
    """
    z = np.asarray(z, dtype=float)
    scalar = z.ndim == 0
    z = np.atleast_1d(z)

    D0 = _growth_unnorm(0.0)
    result = np.array([_growth_unnorm(float(zi)) / D0 for zi in z])
    return float(result[0]) if scalar else result


# ---------------------------------------------------------------------------
# Linear matter power spectrum
# ---------------------------------------------------------------------------

def P_lin(k, z):
    """Linear matter power spectrum P_lin(k, z) [(Mpc/h)^3].

    Parameters
    ----------
    k : float or array
        Wavenumber(s) [h/Mpc].
    z : float
        Redshift (scalar).

    Returns
    -------
    P : array matching shape of k
    """
    _ensure_init()
    k = np.asarray(k, dtype=float)
    log_k = np.log10(np.clip(k, cfg.K_MIN, cfg.K_MAX))
    z_val = np.clip(float(z), _z_grid[0], _z_grid[-1])
    log_P = _Plin_interp(z_val, log_k, grid=False)
    return 10.0**log_P


# ---------------------------------------------------------------------------
# Variance of the density field
# ---------------------------------------------------------------------------

def _tophat_W(kR):
    """Fourier-space top-hat window function W(kR) = 3(sin x - x cos x)/x^3."""
    kR = np.asarray(kR, dtype=float)
    out = np.ones_like(kR)
    mask = kR > 1e-6
    x = kR[mask]
    out[mask] = 3.0 * (np.sin(x) - x * np.cos(x)) / x**3
    return out


def sigma_R(R, z):
    """RMS density fluctuation sigma(R, z) smoothed with top-hat of radius R [Mpc/h].

    Uses trapezoidal integration on the k-grid for speed (no quad).
    """
    _ensure_init()
    k = _k_grid
    Pk = P_lin(k, z)
    W = _tophat_W(k * R)
    integrand = k**3 * Pk * W**2 / (2.0 * np.pi**2)
    # Trapezoidal in log-k space
    lnk = np.log(k)
    from scipy.integrate import trapezoid
    val = trapezoid(integrand, lnk)
    return np.sqrt(max(val, 0.0))


# ---------------------------------------------------------------------------
# Tabulated sigma(M, z) with interpolation for fast access
# ---------------------------------------------------------------------------

_sigma_interp = {}  # keyed by round(z, 4): interpolator log_sigma(log_M)
_sigma_fine_M = np.logspace(np.log10(cfg.M_MIN), np.log10(cfg.M_MAX), 500)


def _build_sigma_interp(z):
    """Build a 1D interpolator for log sigma(log M) at redshift z."""
    from scipy.interpolate import interp1d
    z_key = round(float(z), 4)
    if z_key in _sigma_interp:
        return _sigma_interp[z_key]

    R_arr = (3.0 * _sigma_fine_M / (4.0 * np.pi * cfg.RHO_BAR))**(1.0 / 3.0)
    sig_arr = np.array([sigma_R(R, z) for R in R_arr])
    log_sig = np.log(np.maximum(sig_arr, 1e-30))
    log_M = np.log(_sigma_fine_M)
    interp = interp1d(log_M, log_sig, kind='cubic',
                       bounds_error=False,
                       fill_value=(log_sig[0], log_sig[-1]))
    _sigma_interp[z_key] = interp
    return interp


def sigma_M(M, z):
    """RMS density fluctuation sigma(M, z) using precomputed interpolation table."""
    _ensure_init()
    interp = _build_sigma_interp(z)
    return np.exp(interp(np.log(M)))
