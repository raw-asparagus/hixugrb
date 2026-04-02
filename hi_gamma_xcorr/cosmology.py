"""Cosmological backbone: P_lin(k,z), H(z), chi(z), D(z), sigma(M,z).

Uses CAMB as the Boltzmann solver.  All outputs are in h-dependent units:
  - k in h/Mpc, P(k) in (Mpc/h)^3, distances in Mpc/h, masses in M_sun/h.
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.integrate import quad

from . import config as cfg

# ---------------------------------------------------------------------------
# Module-level cache: initialized on first call to init()
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
    pars.set_matter_power(
        redshifts=list(z_arr),
        kmax=cfg.K_MAX * 1.1,     # slight headroom
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


def chi(z):
    """Comoving distance chi(z) [Mpc/h].

    Integrates c/H(z') from 0 to z.  Returns scalar or array matching input.
    """
    z = np.asarray(z, dtype=float)
    scalar = z.ndim == 0
    z = np.atleast_1d(z)
    result = np.empty_like(z)
    for i, zi in enumerate(z):
        val, _ = quad(lambda zp: cfg.C_LIGHT_KM_S / H(zp), 0.0, zi)
        # val is in Mpc; convert to Mpc/h
        result[i] = val * cfg.h
    return float(result[0]) if scalar else result


def d_L(z):
    """Luminosity distance [Mpc/h]."""
    z = np.asarray(z, dtype=float)
    return chi(z) * (1.0 + z)


def d_A(z):
    """Angular diameter distance [Mpc/h]."""
    z = np.asarray(z, dtype=float)
    return chi(z) / (1.0 + z)


# ---------------------------------------------------------------------------
# Growth factor
# ---------------------------------------------------------------------------

def growth_factor(z):
    """Linear growth factor D(z), normalized so D(0) = 1.

    Uses the integral form: D(z) proportional to E(z) * integral_z^inf dz'/(1+z')/E(z')^3,
    which is exact for flat LCDM.
    """
    z = np.asarray(z, dtype=float)
    scalar = z.ndim == 0
    z = np.atleast_1d(z)

    def _D_unnorm(zi):
        ez = E(zi)
        integrand = lambda zp: (1.0 + zp) / E(zp)**3
        val, _ = quad(integrand, zi, np.inf, limit=200)
        return ez * val

    D0 = _D_unnorm(0.0)
    result = np.array([_D_unnorm(float(zi)) / D0 for zi in z])
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
    z_val = float(z)
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
    """RMS density fluctuation sigma(R, z) smoothed with top-hat of radius R [Mpc/h]."""
    _ensure_init()

    def integrand(lnk):
        k = np.exp(lnk)
        W = _tophat_W(k * R)
        return k**3 * P_lin(k, z) * W**2 / (2.0 * np.pi**2)

    lnk_min = np.log(cfg.K_MIN)
    lnk_max = np.log(cfg.K_MAX)
    val, _ = quad(integrand, lnk_min, lnk_max, limit=200, epsrel=1e-6)
    return np.sqrt(val)


def sigma_M(M, z):
    """RMS density fluctuation sigma(M, z) for top-hat enclosing mass M [M_sun/h].

    R = (3M / (4 pi rho_bar))^{1/3}  [Mpc/h].
    """
    R = (3.0 * M / (4.0 * np.pi * cfg.RHO_BAR))**(1.0 / 3.0)
    return sigma_R(R, z)


def dlnsigma_dlnM(M, z, dlog=0.01):
    """Numerical derivative d ln sigma / d ln M via central finite differences."""
    M_lo = M * 10**(-dlog)
    M_hi = M * 10**(+dlog)
    s_lo = sigma_M(M_lo, z)
    s_hi = sigma_M(M_hi, z)
    return (np.log(s_hi) - np.log(s_lo)) / (np.log(M_hi) - np.log(M_lo))


# ---------------------------------------------------------------------------
# Tabulated sigma(M) for fast access
# ---------------------------------------------------------------------------

_sigma_M_table = {}  # keyed by z


def sigma_M_table(z, M_grid=None):
    """Return (or compute and cache) sigma(M) on the mass grid at redshift z.

    Returns
    -------
    M_grid : array [M_sun/h]
    sigma_arr : array (same length)
    """
    _ensure_init()
    if M_grid is None:
        M_grid = cfg.M_GRID

    z_key = round(float(z), 6)
    if z_key not in _sigma_M_table:
        sig = np.array([sigma_M(m, z) for m in M_grid])
        _sigma_M_table[z_key] = (M_grid, sig)
    return _sigma_M_table[z_key]


# ---------------------------------------------------------------------------
# Convenience: mean matter density at redshift z
# ---------------------------------------------------------------------------

def rho_bar(z=0.0):
    """Mean comoving matter density [M_sun/h / (Mpc/h)^3].

    This is constant in comoving coordinates: rho_bar = Omega_m * rho_crit.
    """
    return cfg.RHO_BAR


def rho_crit(z=0.0):
    """Critical density at z=0 [M_sun/h / (Mpc/h)^3]."""
    return cfg.RHO_CRIT
