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
# Virial overdensity — Bryan & Norman (1998)
# ---------------------------------------------------------------------------

def Delta_vir(z):
    """Virial overdensity Delta_vir(z) from Bryan & Norman (1998).

    Delta_vir = 18*pi^2 + 82*x - 39*x^2
    where x = Omega_M(z) - 1 and Omega_M(z) = Omega_M * (1+z)^3 / E(z)^2.

    For flat LCDM with Planck 2018 (Omega_M=0.3153):
      Delta_vir(z=0) ~ 337, approaching 18*pi^2 ~ 178 at high z.
    """
    Ez2 = cosmo.E(z)**2
    Omega_z = cfg.OMEGA_M * (1.0 + z)**3 / Ez2
    x = Omega_z - 1.0
    return 18.0 * np.pi**2 + 82.0 * x - 39.0 * x**2


# ---------------------------------------------------------------------------
# Virial radius and circular velocity
# ---------------------------------------------------------------------------

def R_vir(M, z=0.0):
    """Virial radius R_vir [Mpc/h] for halo of mass M [M_sun/h] at redshift z.

    Uses the Bryan & Norman (1998) z-dependent virial overdensity:
      M = (4/3) pi Delta_vir(z) * rho_crit(z) * R^3
    where rho_crit(z) = rho_crit,0 * E(z)^2.
    Returns the radius in Mpc/h units.
    """
    M = np.asarray(M, dtype=float)
    Ez2 = cosmo.E(z)**2
    rho_crit_z = cfg.RHO_CRIT * Ez2
    Dv = Delta_vir(z)
    return (3.0 * M / (4.0 * np.pi * Dv * rho_crit_z))**(1.0 / 3.0)


def R_200c(M, z=0.0):
    """Radius R_200c [Mpc/h] defined with fixed Delta=200 w.r.t. critical density.

    Needed for the Correa c_200 relation and for converting c_200 → c_vir.
    """
    M = np.asarray(M, dtype=float)
    Ez2 = cosmo.E(z)**2
    rho_crit_z = cfg.RHO_CRIT * Ez2
    return (3.0 * M / (4.0 * np.pi * 200.0 * rho_crit_z))**(1.0 / 3.0)


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

def concentration_correa(M, z):
    """Concentration c_200(M, z) from Correa et al. (2015) Appendix B1, Planck cosmology.

    Semi-analytic model based on halo MAH. Valid for log10(M/M_sun) in [-2, 16],
    z in [0, 20]. Uses two regimes: z <= 4 (with quadratic correction for the
    slope break at ~10^11 M_sun) and z > 4 (simple power law).

    M is in M_sun/h (pipeline convention); converted to M_sun for the polynomial.
    """
    M = np.asarray(M, dtype=float)
    z = float(z)

    # Convert M_sun/h → M_sun
    log_M = np.log10(np.clip(M * cfg.h, 1e-2, 1e16))

    if z <= 4:
        # Low-z regime (Appendix B1, Planck)
        zp1 = 1.0 + z
        alpha = 1.7543 - 0.2766 * zp1 + 0.02039 * zp1**2
        beta = 0.2753 + 0.00351 * zp1 - 0.3038 * zp1**0.0269
        gamma = -0.01537 + 0.02102 * zp1**(-0.1475)
        log_c = alpha + beta * log_M * (1.0 + gamma * log_M**2)
    else:
        # High-z regime (Appendix B1, Planck)
        zp1 = 1.0 + z
        alpha = 1.3081 - 0.1078 * zp1 + 0.00398 * zp1**2
        beta = 0.0223 - 0.0944 * zp1**(-0.3907)
        log_c = alpha + beta * log_M

    c = 10.0**log_c
    return np.maximum(c, 1.0)


def c200_to_cvir(c200, z):
    """Convert NFW concentration from c_200c to c_vir definition.

    For an NFW halo, the scale radius r_s is invariant between definitions.
    Given c_200 = R_200c / r_s, we need c_vir = R_vir / r_s where R_vir is
    defined via Delta_vir(z).

    The implicit relation is:
      (c_vir / c_200)^3 = (200 / Delta_vir) * f(c_vir) / f(c_200)
    where f(c) = ln(1+c) - c/(1+c).

    Solved iteratively via Newton's method.
    """
    c200 = np.asarray(c200, dtype=float)
    scalar = c200.ndim == 0
    c200 = np.atleast_1d(c200)

    Dv = Delta_vir(z)
    ratio = 200.0 / Dv  # < 1 when Dv > 200 (low z), so c_vir > c_200
    f200 = _f_nfw(c200)

    # Initial guess: c_vir ~ c_200 * (200 / Dv)^(1/3) * correction
    c_vir = c200 * ratio**(1.0 / 3.0) * 1.2

    # Newton iterations: solve g(c) = c^3 * f(c200) - ratio * c200^3 * f(c) = 0
    for _ in range(20):
        fc = _f_nfw(c_vir)
        g = c_vir**3 * f200 - ratio * c200**3 * fc
        # dg/dc = 3*c^2*f200 - ratio*c200^3 * f'(c)
        # f'(c) = c / (1+c)^2
        dgdc = 3.0 * c_vir**2 * f200 - ratio * c200**3 * c_vir / (1.0 + c_vir)**2
        dc = g / dgdc
        c_vir = c_vir - dc
        c_vir = np.clip(c_vir, 1.0, 1e4)
        if np.all(np.abs(dc) < 1e-8 * c_vir):
            break

    return float(c_vir[0]) if scalar else c_vir


def concentration_vir(M, z):
    """Virial concentration c_vir(M, z).

    Computes c_200 from Correa et al. (2015) then converts to c_vir
    using the Bryan & Norman Delta_vir(z).
    """
    c200 = concentration_correa(M, z)
    return c200_to_cvir(c200, z)


# Default concentration for DM halos (now returns c_vir)
concentration = concentration_vir


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
