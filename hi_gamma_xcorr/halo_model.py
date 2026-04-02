"""Halo model machinery: mass function, bias, NFW profile Fourier transforms.

Uses the `hmf` package as backend for mass functions and sigma(M).
Retains manual implementations for virial radius, circular velocity,
concentration-mass relations, and NFW Fourier transforms.

All masses in M_sun/h, distances in Mpc/h, wavenumbers in h/Mpc.
"""

import numpy as np
from scipy.special import sici
from scipy.integrate import quad
from scipy.interpolate import interp1d

from . import config as cfg
from . import cosmology as cosmo
from . import hmf_interface as hmfi

# ---------------------------------------------------------------------------
# Virial radius and circular velocity
# ---------------------------------------------------------------------------

def R_vir(M, z=0.0):
    """Physical virial radius R_200c [Mpc/h] for halo of mass M [M_sun/h] at redshift z.

    Uses M_200c definition: M = (4/3) pi Delta * rho_crit(z) * R_phys^3
    where rho_crit(z) = rho_crit,0 * E(z)^2 is the physical critical density at z.
    Returns the physical radius in Mpc/h units (i.e., R_phys * h in Mpc).
    """
    M = np.asarray(M, dtype=float)
    Ez2 = cosmo.E(z)**2
    rho_crit_z = cfg.RHO_CRIT * Ez2  # physical rho_crit(z) in h-units
    return (3.0 * M / (4.0 * np.pi * cfg.DELTA_VIR * rho_crit_z))**(1.0 / 3.0)


# G in units of km^2/s^2 per (M_sun / Mpc): precomputed for efficiency
_G_COSMO = cfg.G_NEWTON * cfg.M_SUN / cfg.MPC_TO_M * 1e-6


def v_circ(M, z=0.0):
    """Circular velocity at R_vir [km/s].

    v_c = sqrt(G M_phys / R_phys) with physical M_sun and Mpc.
    """
    M = np.asarray(M, dtype=float)
    Rv = R_vir(M, z)       # physical Mpc/h
    M_phys = M / cfg.h     # M_sun
    R_phys = Rv / cfg.h    # Mpc
    return np.sqrt(_G_COSMO * M_phys / R_phys)


# ---------------------------------------------------------------------------
# Mass function and related quantities (delegated to hmf via hmf_interface)
# ---------------------------------------------------------------------------

def nu(M, z):
    """Peak height nu = delta_c^2 / sigma^2(M, z).  Uses hmf backend."""
    return hmfi.nu(M, z)


def dndM(M, z):
    """Halo mass function dn/dM [h^4 / (Mpc^3 M_sun)] at mass M [M_sun/h].

    Delegates to hmf package (Sheth-Mo-Tormen fitting function).
    """
    return hmfi.dndm(M, z)


def dndM_array(z):
    """Return full (M, dndM) arrays from hmf at redshift z."""
    return hmfi.dndm_array(z)


# ---------------------------------------------------------------------------
# Sheth-Tormen halo bias
# ---------------------------------------------------------------------------

def bias(M, z):
    """Linear halo bias b(M, z) from the Sheth-Tormen (1999) prescription.

    Uses hmf's sigma(M, z) for the peak height.
    """
    nu_val = nu(M, z)
    q, p = cfg.SMT_Q, cfg.SMT_P
    return 1.0 + (q * nu_val - 1.0) / cfg.DELTA_C + \
        2.0 * p / (cfg.DELTA_C * (1.0 + (q * nu_val)**p))


# ---------------------------------------------------------------------------
# Concentration-mass relations
# ---------------------------------------------------------------------------

def concentration_dutton_maccio(M, z):
    """Concentration c_200(M, z) from Dutton & Macciò (2014).

    Calibrated for Planck cosmology, M_200 in [1e10, 1e15] h^{-1} M_sun.
    Uses their Eqs. 10-11 for the z-dependent coefficients.
    Extrapolated as a power law below 1e10.
    """
    M = np.asarray(M, dtype=float)
    z = float(z)

    # Dutton & Macciò (2014) Eqs. 10-11, Planck cosmology
    b_z = -0.101 + 0.026 * z
    a_z = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * z**1.21) if z > 0 else 0.905

    log10_c = a_z + b_z * np.log10(M / 1e12)
    c = 10.0**log10_c
    return np.maximum(c, 1.0)


def concentration_munoz_cuartas(M, z):
    """Concentration from Muñoz-Cuartas et al. (2011) + Bullock extrapolation.

    Polynomial fit for M = 1e11 - 1e15 h^{-1} M_sun, extrapolated below
    using c proportional to (M/M_*)^{-0.13} (1+z)^{-1}.
    """
    M = np.asarray(M, dtype=float)
    z = float(z)

    # Muñoz-Cuartas et al. (2011) fit coefficients
    # log10(c) = a(z) + b(z) * log10(M_14) where M_14 = M / (1e14 h^{-1} M_sun)
    # a(z) = 0.537 + (1.025 - 0.537) * exp(-0.718 * z^1.08)
    # b(z) = -0.097 + 0.024 * z
    a_z = 0.537 + (1.025 - 0.537) * np.exp(-0.718 * z**1.08) if z > 0 else 1.025
    b_z = -0.097 + 0.024 * z

    log_M14 = np.log10(M / 1e14)
    log10_c = a_z + b_z * log_M14

    c = 10.0**log10_c

    # Bullock extrapolation for M < 1e10: c ~ (M/M_*)^{-0.13} * (1+z)^{-1}
    # Anchor at M = 1e10 and extend the power law
    M_anchor = 1e10
    mask = M < M_anchor
    if np.any(mask):
        log10_c_anchor = a_z + b_z * np.log10(M_anchor / 1e14)
        c_anchor = 10.0**log10_c_anchor
        c_extrap = c_anchor * (M[mask] / M_anchor)**(-0.13)
        if isinstance(c, np.ndarray):
            c[mask] = c_extrap
        else:
            c = c_extrap

    return np.maximum(c, 1.0)


# Default concentration for DM halos
concentration = concentration_dutton_maccio


# ---------------------------------------------------------------------------
# NFW profile Fourier transform (analytic)
# ---------------------------------------------------------------------------

def _f_nfw(c):
    """NFW normalization: f(c) = ln(1+c) - c/(1+c)."""
    c = np.asarray(c, dtype=float)
    return np.log(1.0 + c) - c / (1.0 + c)


def u_nfw(k, M, z=0.0, c_func=None):
    """Normalized Fourier transform of the NFW profile truncated at R_vir.

    u_tilde(k|M) → 1 as k → 0.

    Parameters
    ----------
    k : float or array  [h/Mpc]
    M : float           [M_sun/h]
    z : float
    c_func : callable, optional
        Concentration function c(M, z). Defaults to concentration_correa.

    Returns
    -------
    u : array matching shape of k
    """
    if c_func is None:
        c_func = concentration

    k = np.asarray(k, dtype=float)
    c = float(c_func(np.atleast_1d(M), z).ravel()[0])
    Rv = float(R_vir(M, z))
    rs = Rv / c

    fc = _f_nfw(c)
    krs = k * rs

    # Sine and cosine integrals
    Si_1c, Ci_1c = sici((1.0 + c) * krs)
    Si_1, Ci_1 = sici(krs)

    # Handle k → 0 separately to avoid 0/0
    result = np.ones_like(k)
    mask = krs > 1e-10
    km = krs[mask]
    Si_1c_m = Si_1c[mask] if isinstance(Si_1c, np.ndarray) else Si_1c
    Ci_1c_m = Ci_1c[mask] if isinstance(Ci_1c, np.ndarray) else Ci_1c
    Si_1_m = Si_1[mask] if isinstance(Si_1, np.ndarray) else Si_1
    Ci_1_m = Ci_1[mask] if isinstance(Ci_1, np.ndarray) else Ci_1

    term1 = np.sin(km) * (Si_1c_m - Si_1_m)
    term2 = np.cos(km) * (Ci_1c_m - Ci_1_m)
    term3 = -np.sin(c * km) / ((1.0 + c) * km)

    result[mask] = (term1 + term2 + term3) / fc

    return result


# ---------------------------------------------------------------------------
# Tabulated mass function and bias on the mass grid
# ---------------------------------------------------------------------------

def mass_function_table(z, M_grid=None):
    """Compute dn/dM on the mass grid at redshift z.

    Returns (M_grid, dndM_arr).
    """
    if M_grid is None:
        M_grid = cfg.M_GRID
    dndM_arr = np.array([dndM(m, z) for m in M_grid])
    return M_grid, dndM_arr


def bias_table(z, M_grid=None):
    """Compute halo bias on the mass grid at redshift z.

    Returns (M_grid, bias_arr).
    """
    if M_grid is None:
        M_grid = cfg.M_GRID
    b_arr = np.array([bias(m, z) for m in M_grid])
    return M_grid, b_arr


# ---------------------------------------------------------------------------
# Validation integrals
# ---------------------------------------------------------------------------

def check_mass_normalization(z=0.0, M_min=1e6, M_max=1e16):
    """Check integral (dn/dM) * (M/rho_bar) dM ≈ 1.  Uses hmf grid."""
    from scipy.integrate import trapezoid
    m_arr, dndm_arr = dndM_array(z)
    mask = (m_arr >= M_min) & (m_arr <= M_max)
    m = m_arr[mask]
    dn = dndm_arr[mask]
    rho_bar = hmfi.mean_density()
    integrand = dn * m**2 / rho_bar
    return trapezoid(integrand, np.log(m))


def check_bias_normalization(z=0.0, M_min=1e6, M_max=1e16):
    """Check integral (dn/dM) * (M/rho_bar) * b(M) dM ≈ 1.  Uses hmf grid."""
    from scipy.integrate import trapezoid
    m_arr, dndm_arr = dndM_array(z)
    mask = (m_arr >= M_min) & (m_arr <= M_max)
    m = m_arr[mask]
    dn = dndm_arr[mask]
    b_arr = np.array([bias(mi, z) for mi in m])
    rho_bar = hmfi.mean_density()
    integrand = dn * m**2 / rho_bar * b_arr
    return trapezoid(integrand, np.log(m))
