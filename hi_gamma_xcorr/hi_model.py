"""HI modeling: M_HI(M,z), density profile, bias, power spectra.

Follows the Padmanabhan, Refregier & Amara (2017) prescription
as adopted by Pinetti et al. (2020).

All masses in M_sun/h, distances in Mpc/h, wavenumbers in h/Mpc.
"""

import numpy as np
from scipy.integrate import quad

from . import config as cfg
from . import cosmology as cosmo
from . import halo_model as hm
from .cache import _cache_stable

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

    c_HI = c_{HI,0} * (M / 10^{11} M_sun)^{-0.109} * 4 / (1+z)^gamma

    Padmanabhan+ (2017) Eq. 3, Table A1: c_HI,0=139, gamma=0.13.
    The mass pivot is 10^{11} M_sun (not M_sun/h), so M [M_sun/h] is
    converted to M_sun via M_phys = M / h before applying the exponent.
    """
    M = np.asarray(M, dtype=float)
    M_solar = M / cfg.h  # M_sun/h → M_sun: M_phys = M_code / h
    return cfg.HI_C0 * (M_solar / 1e11)**(-0.109) * 4.0 / (1.0 + z)**cfg.HI_GAMMA_CONC


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

@_cache_stable(module=__name__)
def _rho_HI_default(z):
    """rho_HI_mean at default mass limits."""
    def integrand(lnM):
        M = np.exp(lnM)
        return hm.dndM(M, z) * M_HI(M, z) * M
    val, _ = quad(integrand, np.log(cfg.M_MIN_HI), np.log(cfg.M_MAX_HI),
                  limit=200, epsrel=1e-5)
    return val


@_cache_stable(module=__name__)
def _rho_HI_scalar(z, M_min, M_max):
    """rho_HI_mean at explicit mass limits for scalar inputs."""
    def integrand(lnM):
        M = np.exp(lnM)
        return hm.dndM(M, z) * M_HI(M, z) * M

    val, _ = quad(integrand, np.log(M_min), np.log(M_max),
                  limit=200, epsrel=1e-5)
    return val


@_cache_stable(module=__name__)
def _b_HI_default(z):
    """b_HI at default mass limits.

    Cached via joblib (Item 1.3 of clever-beaming-creek plan): structurally
    identical to the cached _rho_HI_default above; deterministic in the
    single hashable float `z`. After source edits, run
    `rm -rf .joblib-cache` to flush stale entries.
    """
    rho = _rho_HI_default(z)
    if rho <= 0:
        return 0.0
    def integrand(lnM):
        M = np.exp(lnM)
        return hm.dndM(M, z) * M_HI(M, z) * hm.bias(M, z) * M
    val, _ = quad(integrand, np.log(cfg.M_MIN_HI), np.log(cfg.M_MAX_HI),
                  limit=200, epsrel=1e-5)
    return val / rho


def rho_HI_mean(z, M_min=None, M_max=None):
    """Mean comoving HI density rho_bar_HI(z) [M_sun/h / (Mpc/h)^3].

    rho_HI = integral (dn/dM) * M_HI(M, z) dM
    """
    z = float(z)

    if M_min is None and M_max is None:
        return _rho_HI_default(z)

    if M_min is None:
        M_min = cfg.M_MIN_HI
    if M_max is None:
        M_max = cfg.M_MAX_HI

    return _rho_HI_scalar(z, float(M_min), float(M_max))


def Omega_HI(z, **kwargs):
    """HI density parameter Omega_HI(z) (comoving fraction).

    Omega_HI(z) = rho_HI^com(z) / rho_crit,0

    `rho_HI_mean` returns the COMOVING HI density (halo integral uses comoving
    dn/dM), so no (1+z)^3 conversion is applied. This matches Bull+2015 Eq. 3
    and Chang+2008 convention, in which T_bar_b = 188 h Omega_HI (1+z)^2/E(z)
    mK gives a temperature that rises with z.
    """
    rho = rho_HI_mean(z, **kwargs)
    return rho / cfg.RHO_CRIT


def T_bar_b(z, **kwargs):
    """Mean 21-cm brightness temperature T_bar_b(z) [mK].

    T_bar_b = 188 * h * Omega_HI(z) * (1+z)^2 / E(z)  [mK]

    From Pinetti Eq. 3.4 / standard 21-cm cosmology.
    """
    OHI = Omega_HI(z, **kwargs)
    return 188.0 * cfg.h * OHI * (1.0 + z)**2 / cosmo.E(z)


def T_bar_b_fixed_omega(z, omega_hi=None):
    """Mean 21-cm brightness temperature for a fixed Omega_HI [mK]."""
    if omega_hi is None:
        omega_hi = cfg.OMEGA_HI_FIXED
    return 188.0 * cfg.h * float(omega_hi) * (1.0 + z)**2 / cosmo.E(z)


# ---------------------------------------------------------------------------
# Cunnington et al. (2025), arXiv:2510.27549, Appendix A.
# Polynomial models used by the public MeerFish forecast code, adapted from
# SKA Cosmology SWG (2020) and the latest MeerKLASS Omega_HI constraints
# (Cunnington et al. 2023a). See docs/literature/cunnington2025_meerklass_overview.md.
# Notably the brightness-temperature prefactor is 180 mK (Battye+2013), not the
# 188 mK form used by `T_bar_b` (Padmanabhan 2017 / Pinetti 2020 convention).
# ---------------------------------------------------------------------------


def Omega_HI_cunnington(z):
    """HI density polynomial from Cunnington et al. (2025), Eq. A5.

    Omega_HI(z) = 6.7432e-4 + 3.9e-4 * z - 6.5e-5 * z^2

    Adapted from SKA Cosmology SWG (2020) with the latest MeerKLASS
    constraints (Cunnington et al. 2023a).
    """
    z = np.asarray(z, dtype=float)
    return 6.7432e-4 + 3.9e-4 * z - 6.5e-5 * z * z


def b_HI_cunnington(z):
    """HI bias polynomial from Cunnington et al. (2025), Eq. A3.

    b_HI(z) = 0.842 + 0.693 * z - 0.0459 * z^2

    Fit to the Villaescusa-Navarro et al. (2018) hydrodynamic simulations.
    Provided as the MeerFish forecast default; included here for
    notebook plotting and cross-checks against the pipeline halo-integral
    `b_HI(z)` produced by the Padmanabhan+2017 modified-NFW halo model.
    """
    z = np.asarray(z, dtype=float)
    return 0.842 + 0.693 * z - 0.0459 * z * z


def T_bar_b_cunnington(z):
    """Mean 21-cm brightness temperature from Cunnington et al. (2025), Eq. A4.

    T_bar_HI(z) = 180 * Omega_HI(z) * h * (1 + z)^2 / (H(z) / H_0)  [mK]

    Uses the 180 mK Battye+2013 prefactor (NOT the 188 mK form in `T_bar_b`)
    and the MeerFish Omega_HI(z) polynomial of `Omega_HI_cunnington`. This is
    the brightness model adopted by all published MeerKLASS data analyses
    and by the public MeerFish Fisher forecast code.
    """
    OHI = Omega_HI_cunnington(z)
    return 180.0 * cfg.h * OHI * (1.0 + np.asarray(z, dtype=float))**2 / cosmo.E(z)


def _is_cunnington_mode(hi_brightness):
    """Return True if `hi_brightness` selects the Cunnington 2025 / MeerFish mode."""
    return hi_brightness in ('cunnington', 'meerfish', 'cunnington2025')


def _is_known_mode(hi_brightness):
    return (
        hi_brightness in ('padmanabhan', 'computed', 'halo_integral')
        or hi_brightness in ('fixed_omega', 'omega_fixed', 'pinetti_omega')
        or _is_cunnington_mode(hi_brightness)
    )


def T_bar_b_for_model(z, hi_brightness='padmanabhan'):
    """Mean brightness temperature for a named HI brightness prescription.

    Parameters
    ----------
    z : float or array
        Redshift.
    hi_brightness : str
        - 'padmanabhan' (also 'computed', 'halo_integral'):
          188 mK prefactor with halo-integral Omega_HI(z) from the
          Padmanabhan+2017 modified-NFW HI model. Pipeline default.
        - 'fixed_omega' (also 'omega_fixed', 'pinetti_omega'):
          188 mK prefactor with the fixed `cfg.OMEGA_HI_FIXED = 2.45e-4`
          (Pinetti 2020 / Battye+2013 44 uK form).
        - 'cunnington' (also 'meerfish', 'cunnington2025'):
          180 mK prefactor with the Cunnington et al. (2025), Eq. A5
          Omega_HI(z) polynomial. Convention used by all published
          MeerKLASS data analyses and the MeerFish forecast code.
          When this mode is selected, the HI bias and the HI 2-halo power
          spectrum also automatically switch to the matched Cunnington
          Eq. A3 polynomial b_HI(z), so the brightness and the clustering
          stay self-consistent across the whole pipeline.
    """
    if hi_brightness in ('padmanabhan', 'computed', 'halo_integral'):
        return T_bar_b(z)
    if hi_brightness in ('fixed_omega', 'omega_fixed', 'pinetti_omega'):
        return T_bar_b_fixed_omega(z)
    if _is_cunnington_mode(hi_brightness):
        return T_bar_b_cunnington(z)
    raise ValueError(
        "hi_brightness must be 'padmanabhan', 'fixed_omega' or 'cunnington' "
        f"(got {hi_brightness!r})"
    )


def b_HI(z, M_min=None, M_max=None, hi_brightness='padmanabhan'):
    """Mass-weighted effective HI bias b_HI(z).

    b_HI = (1/rho_HI) * integral (dn/dM) * M_HI * b(M) dM       (halo integral)

    When ``hi_brightness`` selects the Cunnington 2025 / MeerFish mode, this
    instead returns the data-calibrated polynomial

        b_HI(z) = 0.842 + 0.693 z - 0.0459 z^2

    from `b_HI_cunnington` (Cunnington et al. 2025, Eq. A3, fit to
    Villaescusa-Navarro et al. 2018 hydrodynamic simulations). The
    ``M_min``/``M_max`` arguments are silently ignored in that case because
    the polynomial does not carry mass-cut information.

    Parameters
    ----------
    z : float
        Redshift.
    M_min, M_max : float, optional
        Halo-mass integration bounds for the halo-integral mode. Ignored if
        ``hi_brightness`` is a Cunnington alias.
    hi_brightness : str, optional
        See ``T_bar_b_for_model`` for the full alias list.
    """
    if not _is_known_mode(hi_brightness):
        raise ValueError(
            "hi_brightness must be 'padmanabhan', 'fixed_omega' or 'cunnington' "
            f"(got {hi_brightness!r})"
        )

    if _is_cunnington_mode(hi_brightness):
        return float(b_HI_cunnington(float(z)))

    if M_min is None and M_max is None:
        return _b_HI_default(float(z))

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

def P_HI_1h(k, z, M_min=None, M_max=None, n_M=160):
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
        # Rectangle rule in log-mass
        result += dn * mhi**2 * u**2 * M  # M from d(lnM)

    dlnM = np.log(M_arr[1] / M_arr[0])
    return result * dlnM / rho**2


def P_HI_2h(k, z, M_min=None, M_max=None, n_M=160, hi_brightness='padmanabhan'):
    """Two-halo HI power spectrum P_HI^{2h}(k, z) [(Mpc/h)^3].

    P_HI^{2h} = [(1/rho_HI) * integral (dn/dM) * b(M) * M_HI * u_HI dM]^2 * P_lin(k,z)
              (halo integral, Padmanabhan / Pinetti convention)

    When ``hi_brightness`` selects the Cunnington 2025 / MeerFish mode, this
    collapses to the linear-bias form

        P_HI^{2h}(k, z) = b_HI_cunn(z)^2 * P_lin(k, z)

    using `b_HI_cunnington` (Cunnington et al. 2025, Eq. A3). The HI profile
    factor u_HI(k, M, z) is dropped: this approximation is valid in the linear
    regime k <~ 0.3 h/Mpc that MeerKLASS analyses target. ``M_min``/``M_max``/
    ``n_M`` are ignored in that case.
    """
    k = np.atleast_1d(np.asarray(k, dtype=float))

    if not _is_known_mode(hi_brightness):
        raise ValueError(
            "hi_brightness must be 'padmanabhan', 'fixed_omega' or 'cunnington' "
            f"(got {hi_brightness!r})"
        )

    if _is_cunnington_mode(hi_brightness):
        b = float(b_HI_cunnington(float(z)))
        return b * b * cosmo.P_lin(k, z)

    if M_min is None:
        M_min = cfg.M_MIN_HI
    if M_max is None:
        M_max = cfg.M_MAX_HI

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


# ---------------------------------------------------------------------------
# HI window function for Limber integration
# ---------------------------------------------------------------------------

def W_HI(z, z_min, z_max, hi_brightness='padmanabhan'):
    """HI window function W_HI(chi) per comoving distance (Pinetti 2020 Eq. 3.15-3.16).

    W_HI(chi) = T_bar_b(z) * phi(z) * H(z) / (c * h)

    where phi(z) = 1/(z_max - z_min) is the top-hat selection function and
    H/(c*h) converts from per-z to per-(Mpc/h) convention.

    IMPORTANT: per Pinetti+ 2020 Eq. 3.15, the HI window does NOT include b_HI.
    The bias enters only through the HI power spectrum P_HI(k,z) in the Limber
    integrand. Including b_HI here would double-count the bias in C_ell.

    Used with Limber weight (dchi/dz)/chi^2 * dz where dchi/dz = c*h/H.
    The H factors cancel in the product: weight * W_HI = T_bar_b * phi / chi^2.
    """
    if z < z_min or z > z_max:
        return 0.0
    H_over_ch = cosmo.H(z) / (cfg.C_LIGHT_KM_S * cfg.h)  # 1/(Mpc/h)
    return T_bar_b_for_model(z, hi_brightness) / (z_max - z_min) * H_over_ch
