"""Interface to the hmf package for halo mass function computations.

Provides cached MassFunction instances and drop-in replacement functions
matching the signatures used throughout the pipeline.  All outputs are in
h-dependent units (M_sun/h, Mpc/h, h/Mpc) consistent with config.py.
"""

import numpy as np
from scipy.interpolate import interp1d
import warnings

from . import config as cfg

# Suppress hmf's deprecation warnings
warnings.filterwarnings('ignore', message="'extrapolate_with_eh'")
warnings.filterwarnings('ignore', category=DeprecationWarning, module='hmf')

# ---------------------------------------------------------------------------
# Lazy import and cached MassFunction instances
# ---------------------------------------------------------------------------

_mf_cache = {}      # keyed by round(z, 4)
_bias_cache = {}    # keyed by round(z, 4): interp1d for b(M)
_hmf_imported = False
_MassFunction = None

# hmf configuration: Sheth-Mo-Tormen (2001) mass function (q=0.707, p=0.3, A=0.3222)
# with Planck 2018 cosmology. See docs/literature/sheth_mo_tormen2001.md.
_HMF_KWARGS = dict(
    Mmin=np.log10(cfg.M_MIN) if cfg.M_MIN > 0 else 4.0,
    Mmax=np.log10(cfg.M_MAX) if cfg.M_MAX < 1e20 else 18.0,
    dlog10m=0.02,
    hmf_model='SMT',
    cosmo_params={
        'H0': cfg.H0,
        'Om0': cfg.OMEGA_M,
        'Ob0': cfg.OMEGA_B,
    },
    sigma_8=cfg.SIGMA_8,
    n=cfg.N_S,
    transfer_model='CAMB',
    transfer_params={'extrapolate_with_eh': True},
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


def nu(M, z):
    """Peak height nu = delta_c^2 / sigma^2(M, z)."""
    sig = sigma(M, z)
    return cfg.DELTA_C**2 / sig**2


def mean_density():
    """Mean comoving matter density [M_sun/h / (Mpc/h)^3] from hmf."""
    mf = get_mass_function(0.0)
    return mf.mean_density


