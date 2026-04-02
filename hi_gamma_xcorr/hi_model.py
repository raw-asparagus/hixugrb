"""HI modeling: M_HI(M,z), density profile, bias, power spectra.

Follows the Padmanabhan, Refregier & Amara (2017) prescription
as adopted by Pinetti et al. (2020).

All masses in M_sun/h, distances in Mpc/h, wavenumbers in h/Mpc.
"""

import numpy as np
from scipy.integrate import quad
from functools import lru_cache

from . import config as cfg
from . import cosmology as cosmo
from . import halo_model as hm

# ---------------------------------------------------------------------------
# HI mass–halo mass relation (Pinetti et al. Eq. 3.7)
# ---------------------------------------------------------------------------

def M_HI(M, z):
    """HI mass [M_sun/h] in a halo of mass M [M_sun/h] at redshift z.

    M_HI = alpha * f_{H,c} * M * (M / 10^{11} h^{-1} M_sun)^beta
            * exp[-(v_{c,0} / v_c(M,z))^3]
    """
    M = np.asarray(M, dtype=float)
    vc = hm.v_circ(M, z)   # km/s
    ratio = M / 1e11        # M is already in M_sun/h = h^{-1} M_sun
    return cfg.HI_ALPHA * cfg.F_HC * M * ratio**cfg.HI_BETA * \
        np.exp(-(cfg.HI_VC0 / vc)**3)


# ---------------------------------------------------------------------------
# HI concentration
# ---------------------------------------------------------------------------

def c_HI(M, z):
    """HI concentration parameter c_HI(M, z).

    c_HI = c_{HI,0} * (M h^{-1} / 10^{11} M_sun)^{-0.109} * 4 / (1+z)^{0.13}

    M is in M_sun/h (= h^{-1} M_sun), so M h^{-1} = M / h^2? No:
    M_sun/h IS h^{-1} M_sun. So M [M_sun/h] = M [h^{-1} M_sun].
    """
    M = np.asarray(M, dtype=float)
    return cfg.HI_C0 * (M / 1e11)**(-0.109) * 4.0 / (1.0 + z)**0.13


# ---------------------------------------------------------------------------
# Altered NFW HI profile (Eq. 3.9) and its Fourier transform
# ---------------------------------------------------------------------------

def _hi_profile_norm_integral(c_hi):
    """Analytic integral of rho_HI(r) * 4*pi*r^2 dr / (rho_0 * r_s^3) from 0 to R_vir.

    rho_HI = rho_0 * r_s^3 / [(r + 0.75*r_s)(r + r_s)^2]

    With substitution x = r / r_s and R_vir/r_s = c_HI:
    integral = 4*pi * r_s^3 * integral_0^c (rho_0 * r_s^3 * x^2) /
               [(x + 0.75)(x + 1)^2 * r_s^3] * r_s dx / (rho_0 * r_s^3)
    = 4*pi * integral_0^c x^2 / [(x + 0.75)(x + 1)^2] dx

    Use partial fraction decomposition:
    x^2 / [(x + 0.75)(x + 1)^2] = A/(x+0.75) + B/(x+1) + C/(x+1)^2

    Solving: A = (0.75)^2 / (0.75-1)^2... let me just do this numerically.
    Actually: x^2 / [(x+a)(x+1)^2] where a=0.75.
    A = a^2 / (a-1)^2 = 0.5625 / 0.0625 = 9
    For B and C, expand: x^2 = A(x+1)^2 + B(x+0.75)(x+1) + C(x+0.75)
    At x=-1: 1 = C*(-1+0.75) = -0.25*C → C = -4
    At x=0: 0 = A + 0.75*B + 0.75*C → 0 = 9 + 0.75*B - 3 → B = -8
    Check: A+B = 9-8 = 1, and 2A + 1.75B + 0.75C = 18-14-3 = 1... hmm.
    Let me verify: coefficient of x^2: A + B = 9 + (-8) = 1 ✓
    coefficient of x: 2A + (0.75+1)B + C = 18 + (-8)*1.75 + (-4) = 18 - 14 - 4 = 0 ✓
    constant: A + 0.75B + 0.75C = 9 - 6 - 3 = 0 ✓

    So integral = 4*pi * [9*ln(x+0.75) - 8*ln(x+1) + 4/(x+1)]_0^c
    """
    c = float(c_hi)
    a = 0.75
    val = (9.0 * np.log((c + a) / a)
           - 8.0 * np.log((c + 1.0) / 1.0)
           + 4.0 * (1.0 / (c + 1.0) - 1.0))
    return 4.0 * np.pi * val


def rho0_HI(M, z):
    """Normalization rho_0 of the HI profile [M_sun/h / (Mpc/h)^3].

    Determined by integral of rho_HI * 4*pi*r^2 dr = M_HI.
    """
    m_hi = M_HI(M, z)
    if m_hi <= 0:
        return 0.0
    c_h = c_HI(M, z)
    Rv = hm.R_vir(M, z)
    rs = Rv / c_h
    norm_int = _hi_profile_norm_integral(c_h)
    return m_hi / (rs**3 * norm_int)


def rho_HI_profile(r, M, z):
    """HI density profile rho_HI(r) [M_sun/h / (Mpc/h)^3].

    rho_HI(r) = rho_0 * r_s^3 / [(r + 0.75*r_s)(r + r_s)^2]
    """
    r = np.asarray(r, dtype=float)
    rho_0 = rho0_HI(M, z)
    c_h = c_HI(M, z)
    Rv = hm.R_vir(M, z)
    rs = Rv / c_h
    return rho_0 * rs**3 / ((r + 0.75 * rs) * (r + rs)**2)


def u_HI(k, M, z):
    """Normalized Fourier transform of the HI profile: u_tilde_HI(k | M, z).

    u_tilde_HI = (4*pi / M_HI) * integral_0^{R_vir} r^2 rho_HI(r) sin(kr)/(kr) dr

    Normalized so u_tilde_HI(k→0) = 1.
    """
    k = np.asarray(k, dtype=float)
    m_hi = M_HI(M, z)
    if m_hi <= 0:
        return np.zeros_like(k)

    c_h = c_HI(M, z)
    Rv = float(hm.R_vir(M, z))
    rs = Rv / c_h
    rho_0 = rho0_HI(M, z)

    result = np.empty_like(k)
    for ik, kk in enumerate(k.ravel()):
        if kk < 1e-10:
            result.ravel()[ik] = 1.0
            continue

        def integrand(r):
            rho = rho_0 * rs**3 / ((r + 0.75 * rs) * (r + rs)**2)
            return r**2 * rho * np.sin(kk * r) / (kk * r)

        val, _ = quad(integrand, 0.0, Rv, limit=200, epsrel=1e-6)
        result.ravel()[ik] = 4.0 * np.pi * val / m_hi

    return result


# ---------------------------------------------------------------------------
# Mean HI density, Omega_HI, brightness temperature, bias
# ---------------------------------------------------------------------------

_rho_HI_cache = {}  # keyed by round(z, 4)
_b_HI_cache = {}


def rho_HI_mean(z, M_min=None, M_max=None):
    """Mean comoving HI density rho_bar_HI(z) [M_sun/h / (Mpc/h)^3].

    rho_HI = integral (dn/dM) * M_HI(M, z) dM
    """
    cache_key = round(float(z), 4)
    if M_min is None and M_max is None and cache_key in _rho_HI_cache:
        return _rho_HI_cache[cache_key]

    if M_min is None:
        M_min = cfg.M_MIN_HI
    if M_max is None:
        M_max = cfg.M_MAX_HI

    def integrand(lnM):
        M = np.exp(lnM)
        return hm.dndM(M, z) * M_HI(M, z) * M  # extra M from d(lnM) = dM/M

    val, _ = quad(integrand, np.log(M_min), np.log(M_max), limit=200, epsrel=1e-5)

    if M_min == cfg.M_MIN_HI and M_max == cfg.M_MAX_HI:
        _rho_HI_cache[cache_key] = val
    return val


def Omega_HI(z, **kwargs):
    """HI density parameter Omega_HI(z).

    Omega_HI = (1+z)^{-3} * rho_HI(z) / rho_crit
    """
    rho = rho_HI_mean(z, **kwargs)
    return rho / ((1.0 + z)**3 * cfg.RHO_CRIT)


def T_bar_b(z, **kwargs):
    """Mean 21-cm brightness temperature T_bar_b(z) [mK].

    T_bar_b = 44 μK * (Omega_HI * h / 2.45e-4) * (1+z)^2 / E(z)
            = 0.044 mK * (Omega_HI * h / 2.45e-4) * (1+z)^2 / E(z)
    """
    OHI = Omega_HI(z, **kwargs)
    return 0.044 * (OHI * cfg.h / 2.45e-4) * (1.0 + z)**2 / cosmo.E(z)


def b_HI(z, M_min=None, M_max=None):
    """Mass-weighted effective HI bias b_HI(z).

    b_HI = (1/rho_HI) * integral (dn/dM) * M_HI * b(M) dM
    """
    if M_min is None:
        M_min = cfg.M_MIN_HI
    if M_max is None:
        M_max = cfg.M_MAX_HI

    rho = rho_HI_mean(z, M_min=M_min, M_max=M_max)
    if rho <= 0:
        return 0.0

    def integrand(lnM):
        M = np.exp(lnM)
        return hm.dndM(M, z) * M_HI(M, z) * hm.bias(M, z) * M

    val, _ = quad(integrand, np.log(M_min), np.log(M_max), limit=200, epsrel=1e-5)
    return val / rho


# ---------------------------------------------------------------------------
# HI power spectra (Eqs. 3.12–3.13)
# ---------------------------------------------------------------------------

def P_HI_1h(k, z, M_min=None, M_max=None, n_M=80):
    """One-halo HI power spectrum P_HI^{1h}(k, z) [(Mpc/h)^3].

    P_HI^{1h} = (1/rho_HI^2) * integral (dn/dM) * M_HI^2 * u_HI^2 dM
    """
    if M_min is None:
        M_min = cfg.M_MIN_HI
    if M_max is None:
        M_max = cfg.M_MAX_HI

    k = np.atleast_1d(np.asarray(k, dtype=float))
    rho = rho_HI_mean(z, M_min=M_min, M_max=M_max)
    if rho <= 0:
        return np.zeros_like(k)

    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    result = np.zeros_like(k)

    for M in M_arr:
        dn = hm.dndM(M, z)
        mhi = M_HI(M, z)
        if mhi <= 0 or dn <= 0:
            continue
        u = u_HI(k, M, z)
        # Trapezoidal weight in log-mass
        result += dn * mhi**2 * u**2 * M  # M from d(lnM)

    dlnM = np.log(M_arr[1] / M_arr[0])
    return result * dlnM / rho**2


def P_HI_2h(k, z, M_min=None, M_max=None, n_M=80):
    """Two-halo HI power spectrum P_HI^{2h}(k, z) [(Mpc/h)^3].

    P_HI^{2h} = [(1/rho_HI) * integral (dn/dM) * b(M) * M_HI * u_HI dM]^2 * P_lin(k,z)
    """
    if M_min is None:
        M_min = cfg.M_MIN_HI
    if M_max is None:
        M_max = cfg.M_MAX_HI

    k = np.atleast_1d(np.asarray(k, dtype=float))
    rho = rho_HI_mean(z, M_min=M_min, M_max=M_max)
    if rho <= 0:
        return np.zeros_like(k)

    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    I_2h = np.zeros_like(k)

    for M in M_arr:
        dn = hm.dndM(M, z)
        mhi = M_HI(M, z)
        b = hm.bias(M, z)
        if mhi <= 0 or dn <= 0:
            continue
        u = u_HI(k, M, z)
        I_2h += dn * b * mhi * u * M  # M from d(lnM)

    dlnM = np.log(M_arr[1] / M_arr[0])
    I_2h *= dlnM / rho
    return I_2h**2 * cosmo.P_lin(k, z)


def P_HI(k, z, **kwargs):
    """Total HI power spectrum P_HI(k, z) = P^{1h} + P^{2h} [(Mpc/h)^3]."""
    return P_HI_1h(k, z, **kwargs) + P_HI_2h(k, z, **kwargs)


# ---------------------------------------------------------------------------
# HI window function for Limber integration
# ---------------------------------------------------------------------------

def W_HI(z, z_min, z_max):
    """HI window function W_HI(chi) per comoving distance (Pinetti Eq. 3.15-3.16).

    W_HI(chi) = T_bar_b(z) * b_HI(z) * phi(z) * H(z) / (c * h)

    where phi(z) = 1/(z_max - z_min) is the top-hat selection function and
    H/(c*h) converts from per-z to per-(Mpc/h) convention.

    Used with Limber weight (dchi/dz)/chi^2 * dz where dchi/dz = c*h/H.
    The H factors cancel in the product: weight * W_HI = T_bar_b * b_HI * phi / chi^2.
    """
    if z < z_min or z > z_max:
        return 0.0
    H_over_ch = cosmo.H(z) / (cfg.C_LIGHT_KM_S * cfg.h)  # 1/(Mpc/h)
    return T_bar_b(z) * b_HI(z) / (z_max - z_min) * H_over_ch
