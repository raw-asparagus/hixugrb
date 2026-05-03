"""Cosmological backbone: P_lin(k,z), H(z), chi(z), D(z), sigma(M,z).

Uses CAMB as the Boltzmann solver.  All outputs are in h-dependent units:
  - k in h/Mpc, P(k) in (Mpc/h)^3, distances in Mpc/h, masses in M_sun/h.
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline, CubicSpline
from scipy.integrate import quad, cumulative_simpson, simpson

from . import config as cfg
from .cache import clear_all_lru_caches

# ---------------------------------------------------------------------------
# Module-level state: initialized on first call to init()
# ---------------------------------------------------------------------------
_camb_results = None
_Plin_interp = None   # 2D interpolator for P_lin(k, z)
_k_grid = None
_z_grid = None

# Distance and growth-factor splines built lazily by init() and used by chi(z)
# and growth_factor(z). They cover [0, _DIST_Z_MAX] with 4096 points (chi) and
# [0, _GROWTH_Z_MAX] with 2048 points (growth). Out-of-range z falls through to
# the original quad-based scalar implementations as a safety net.
_chi_interp = None
_growth_interp = None
_growth_norm = None  # = _growth_unnorm(0)
_DIST_Z_MAX = cfg.Z_MAX + 0.5  # 0.5 z headroom for d_L callers
_GROWTH_Z_MAX = 5.0
_DIST_Z_GRID_N = 4096
_GROWTH_Z_GRID_N = 2048

# Item 4.2 of clever-beaming-creek plan: fingerprint of the cfg cosmology
# parameters that CAMB depends on. _ensure_init() compares this to the live
# cfg values and forces re-init if they have changed at runtime.
_cosmo_fingerprint = None


def _current_cosmo_fingerprint():
    return (cfg.H0, cfg.OMEGA_B_H2, cfg.OMEGA_CDM_H2,
            cfg.A_S, cfg.N_S, cfg.T_CMB, cfg.TAU_REIO)

# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def init(force=False):
    """Run CAMB and build interpolation tables. Idempotent unless force=True."""
    global _camb_results, _Plin_interp, _k_grid, _z_grid
    global _chi_interp, _growth_interp, _growth_norm
    global _cosmo_fingerprint
    if _camb_results is not None and not force:
        return
    _cosmo_fingerprint = _current_cosmo_fingerprint()
    clear_all_lru_caches()

    import camb

    pars = camb.CAMBparams()
    pars.set_cosmology(
        H0=cfg.H0,
        ombh2=cfg.OMEGA_B_H2,
        omch2=cfg.OMEGA_CDM_H2,
        omk=0.0,
        tau=cfg.TAU_REIO,
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

    # ----------------------------------------------------------------------
    # Comoving-distance spline (Item 1.1 of clever-beaming-creek plan).
    # chi(z) = (h * c) * integral_0^z dz' / H(z')
    # Built by cumulative-Simpson on a dense uniform grid that covers
    # [0, _DIST_Z_MAX]. Simpson's rule has O(h^4) error vs trapezoid's O(h^2),
    # giving ~14 digits of accuracy at 4096 points on this smooth integrand
    # — well below the 1e-12 regression tolerance the rest of the pipeline uses.
    # Out-of-range z falls through to the original quad-based _chi_scalar.
    # ----------------------------------------------------------------------
    z_dense = np.linspace(0.0, _DIST_Z_MAX, _DIST_Z_GRID_N)
    integrand = cfg.C_LIGHT_KM_S / H(z_dense)            # H is already vectorised
    chi_vals = cumulative_simpson(integrand, x=z_dense, initial=0.0) * cfg.h
    _chi_interp = CubicSpline(z_dense, chi_vals, bc_type='natural', extrapolate=False)

    # ----------------------------------------------------------------------
    # Growth-factor spline (Item 1.2 of clever-beaming-creek plan).
    # D(z) = E(z) * integral_z^inf (1+z') / E(z')^3 dz', normalised so D(0)=1.
    # Per-grid-point values are computed once at init via the same quad as
    # the legacy code, so grid-aligned points are bit-identical; only between-
    # grid interpolation is new.
    # ----------------------------------------------------------------------
    z_growth = np.linspace(0.0, _GROWTH_Z_MAX, _GROWTH_Z_GRID_N)
    growth_unnorm_vals = np.array([_growth_unnorm(float(zi)) for zi in z_growth])
    _growth_norm = float(growth_unnorm_vals[0])
    growth_vals = growth_unnorm_vals / _growth_norm
    _growth_interp = CubicSpline(z_growth, growth_vals, bc_type='natural', extrapolate=False)


def _ensure_init():
    """Initialise CAMB-backed state on first call.

    Item 4.2: also re-init if the cfg cosmology fingerprint has changed
    since the last init() (e.g., a test or notebook mutated cfg.H0).
    """
    if _camb_results is None:
        init()
        return
    if _cosmo_fingerprint != _current_cosmo_fingerprint():
        init(force=True)


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
    """Comoving distance for a single redshift [Mpc/h] via direct quadrature.

    Used as a fallback for z outside the precomputed _chi_interp range.
    """
    val, _ = quad(lambda zp: cfg.C_LIGHT_KM_S / H(zp), 0.0, z)
    return val * cfg.h


def chi(z):
    """Comoving distance chi(z) [Mpc/h].

    Integrates c/H(z') from 0 to z. Returns scalar or array matching input.
    Uses the precomputed _chi_interp spline (built in init()) for z within
    [0, _DIST_Z_MAX]; falls through to _chi_scalar for any out-of-range z.
    """
    _ensure_init()
    z = np.asarray(z, dtype=float)

    in_range = (z >= 0.0) & (z <= _DIST_Z_MAX)
    if np.all(in_range):
        return _chi_interp(z)

    # Spline for in-range points; quad fallback for the rest
    z_arr = np.atleast_1d(z)
    result = np.empty_like(z_arr)
    in_range_1d = np.atleast_1d(in_range)
    result[in_range_1d] = _chi_interp(z_arr[in_range_1d])
    for i in np.where(~in_range_1d)[0]:
        result[i] = _chi_scalar(float(z_arr[i]))
    return result if z.ndim > 0 else float(result[0])


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
    which is exact for flat LCDM. Implementation uses the precomputed
    _growth_interp spline (built in init()) for z within [0, _GROWTH_Z_MAX];
    falls through to direct quadrature for out-of-range z.
    """
    _ensure_init()
    z = np.asarray(z, dtype=float)

    in_range = (z >= 0.0) & (z <= _GROWTH_Z_MAX)
    if np.all(in_range):
        return _growth_interp(z)

    # Spline for in-range points; quad fallback for the rest
    z_arr = np.atleast_1d(z)
    result = np.empty_like(z_arr)
    in_range_1d = np.atleast_1d(in_range)
    result[in_range_1d] = _growth_interp(z_arr[in_range_1d])
    for i in np.where(~in_range_1d)[0]:
        result[i] = _growth_unnorm(float(z_arr[i])) / _growth_norm
    return result if z.ndim > 0 else float(result[0])


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

    Uses Simpson's rule on the fixed log-k grid (O(h^4) vs trapezoid's O(h^2))
    to keep P_lin in its vectorised path; quad would force per-point spline
    evaluations.
    """
    _ensure_init()
    k = _k_grid
    Pk = P_lin(k, z)
    W = _tophat_W(k * R)
    integrand = k**3 * Pk * W**2 / (2.0 * np.pi**2)
    lnk = np.log(k)
    val = simpson(integrand, x=lnk)
    return np.sqrt(val)


