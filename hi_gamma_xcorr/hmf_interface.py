"""Interface to the hmf package for halo mass function computations.

Provides cached MassFunction instances and drop-in replacement functions
matching the signatures used throughout the pipeline.  All outputs are in
h-dependent units (M_sun/h, Mpc/h, h/Mpc) consistent with config.py.
"""

import numpy as np
from scipy.interpolate import interp1d
import warnings

from . import config as cfg

# Suppress hmf's extrapolation warning
warnings.filterwarnings('ignore', message="'extrapolate_with_eh'")

# ---------------------------------------------------------------------------
# Lazy import and cached MassFunction instances
# ---------------------------------------------------------------------------

_mf_cache = {}      # keyed by round(z, 4)
_bias_cache = {}    # keyed by round(z, 4): interp1d for b(M)
_hmf_imported = False
_MassFunction = None

# hmf configuration matching our Planck 2018 cosmology
_HMF_KWARGS = dict(
    Mmin=np.log10(cfg.M_MIN) if cfg.M_MIN > 0 else 4.0,
    Mmax=np.log10(cfg.M_MAX) if cfg.M_MAX < 1e20 else 18.0,
    dlog10m=0.04,
    hmf_model='SMT',
    cosmo_params={
        'H0': cfg.H0,
        'Om0': cfg.OMEGA_M,
        'Ob0': cfg.OMEGA_B,
    },
    sigma_8=cfg.SIGMA_8,
    n=cfg.N_S,
    transfer_model='EH',
)


def _ensure_hmf():
    """Lazy import of hmf."""
    global _hmf_imported, _MassFunction
    if not _hmf_imported:
        from hmf import MassFunction as MF
        _MassFunction = MF
        _hmf_imported = True


def get_mass_function(z):
    """Get (or create and cache) a MassFunction instance at redshift z.

    Returns the hmf.MassFunction object with precomputed grids.
    """
    _ensure_hmf()
    z_key = round(float(z), 4)
    if z_key not in _mf_cache:
        if len(_mf_cache) == 0:
            # First call: create fresh instance
            mf = _MassFunction(z=float(z), **_HMF_KWARGS)
        else:
            # Subsequent calls: update existing (reuses transfer function)
            ref_key = next(iter(_mf_cache))
            mf = _mf_cache[ref_key].clone(z=float(z))
        _mf_cache[z_key] = mf
    return _mf_cache[z_key]


def clear_cache():
    """Clear all cached MassFunction instances."""
    _mf_cache.clear()
    _bias_cache.clear()


# ---------------------------------------------------------------------------
# Drop-in replacements for halo_model.py and cosmology.py functions
# ---------------------------------------------------------------------------

def dndm(M, z):
    """Halo mass function dn/dM [h^4 Mpc^-3 M_sun^-1] at mass M [M_sun/h].

    Interpolates from the hmf precomputed grid.
    """
    mf = get_mass_function(z)
    log_M = np.log10(float(M))
    log_m_grid = np.log10(mf.m)
    log_dndm_grid = np.log10(np.maximum(mf.dndm, 1e-100))
    return 10.0**np.interp(log_M, log_m_grid, log_dndm_grid)


def dndm_array(z):
    """Return the full (m, dndm) arrays from hmf at redshift z.

    Returns
    -------
    m : array [M_sun/h]
    dndm : array [h^4 Mpc^-3 M_sun^-1]
    """
    mf = get_mass_function(z)
    return mf.m.copy(), mf.dndm.copy()


def sigma(M, z):
    """RMS density fluctuation sigma(M, z) for mass M [M_sun/h]."""
    mf = get_mass_function(z)
    log_M = np.log10(float(M))
    log_m_grid = np.log10(mf.m)
    log_sig_grid = np.log(np.maximum(mf.sigma, 1e-30))
    return np.exp(np.interp(log_M, log_m_grid, log_sig_grid))


def dlnsigma_dlnm(M, z):
    """Numerical derivative d ln sigma / d ln M from hmf grid."""
    mf = get_mass_function(z)
    log_m = np.log(mf.m)
    log_sig = np.log(np.maximum(mf.sigma, 1e-30))
    deriv = np.gradient(log_sig, log_m)
    log_M = np.log(float(M))
    return float(np.interp(log_M, log_m, deriv))


def nu(M, z):
    """Peak height nu = delta_c^2 / sigma^2(M, z)."""
    sig = sigma(M, z)
    return cfg.DELTA_C**2 / sig**2


def mean_density():
    """Mean comoving matter density [M_sun/h / (Mpc/h)^3] from hmf."""
    mf = get_mass_function(0.0)
    return mf.mean_density


def bias_ST(M, z):
    """Sheth-Tormen halo bias b(M, z).

    Uses the analytic Sheth-Tormen (1999) formula directly,
    evaluated at the peak height from hmf's sigma(M, z).
    This is consistent with the SMT mass function.
    """
    nu_val = nu(M, z)
    q, p = cfg.SMT_Q, cfg.SMT_P
    return 1.0 + (q * nu_val - 1.0) / cfg.DELTA_C + \
        2.0 * p / (cfg.DELTA_C * (1.0 + (q * nu_val)**p))


def power_spectrum(z):
    """Linear matter power spectrum P(k, z) from hmf.

    Returns (k, P_k) in h-dependent units: k [h/Mpc], P [(Mpc/h)^3].
    """
    mf = get_mass_function(z)
    return mf.k.copy(), mf.power.copy()


# ---------------------------------------------------------------------------
# Vectorized mass integrals (performance optimization)
# ---------------------------------------------------------------------------

def integrate_over_mass(func_of_M, z, M_min=None, M_max=None):
    """Integrate func_of_M(M) * dndM * dM over the hmf mass grid.

    Parameters
    ----------
    func_of_M : callable
        Function taking mass array M [M_sun/h], returning array.
    z : float
        Redshift.
    M_min, M_max : float, optional
        Mass bounds (default: full hmf grid).

    Returns
    -------
    result : float
        Integral value.
    """
    from scipy.integrate import trapezoid

    m_arr, dndm_arr = dndm_array(z)

    if M_min is not None:
        mask = m_arr >= M_min
        m_arr = m_arr[mask]
        dndm_arr = dndm_arr[mask]
    if M_max is not None:
        mask = m_arr <= M_max
        m_arr = m_arr[mask]
        dndm_arr = dndm_arr[mask]

    if len(m_arr) < 2:
        return 0.0

    f_arr = np.array([func_of_M(m) for m in m_arr])
    integrand = dndm_arr * f_arr * m_arr  # extra M from d(lnM) Jacobian
    return trapezoid(integrand, np.log(m_arr))
