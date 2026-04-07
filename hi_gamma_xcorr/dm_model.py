"""Dark matter annihilation model: rho^2 profile, clumping factor, window function.

All masses in M_sun/h, distances in Mpc/h, wavenumbers in h/Mpc.
"""

import numpy as np
from scipy.integrate import quad

from . import config as cfg
from . import cosmology as cosmo
from . import halo_model as hm
from . import pppc4dmid
from . import ebl as ebl_mod

# ---------------------------------------------------------------------------
# NFW rho^2 profile: analytic expressions
# ---------------------------------------------------------------------------

def _rho_s(M, z, c_func=None):
    """NFW scale density rho_s [M_sun/h / (Mpc/h)^3].

    rho_s = M / (4 pi r_s^3 f(c))
    """
    if c_func is None:
        c_func = hm.concentration
    c = float(c_func(np.atleast_1d(M), z).ravel()[0])
    Rv = float(hm.R_vir(M, z))
    rs = Rv / c
    fc = np.log(1.0 + c) - c / (1.0 + c)
    return M / (4.0 * np.pi * rs**3 * fc)


def rho2_integral_analytic(M, z, c_func=None):
    """Analytic integral of rho_NFW^2 over the halo volume.

    integral_0^{R_vir} 4 pi r^2 rho_NFW^2(r) dr
    = (4 pi / 3) rho_s^2 r_s^3 [1 - 1/(1+c)^3]

    Returns the integral in units of [(M_sun/h)^2 / (Mpc/h)^3].
    """
    if c_func is None:
        c_func = hm.concentration
    c = float(c_func(np.atleast_1d(M), z).ravel()[0])
    Rv = float(hm.R_vir(M, z))
    rs = Rv / c
    rho_s_val = _rho_s(M, z, c_func)
    return (4.0 * np.pi / 3.0) * rho_s_val**2 * rs**3 * (1.0 - 1.0 / (1.0 + c)**3)


# ---------------------------------------------------------------------------
# Fourier transform of rho^2 profile (numerical)
# ---------------------------------------------------------------------------

def v_tilde(k, M, z, c_func=None):
    """Fourier transform of rho^2(r|M) / rho_bar^2  [(Mpc/h)^3].

    v_tilde(k|M) = (4 pi / rho_bar^2) integral_0^{R_vir} r^2 rho_NFW^2(r) sin(kr)/(kr) dr

    Returns [(Mpc/h)^3]: the volume-weighted profile transform, analogous to
    u_nfw but for rho^2.  At k→0, v_tilde = rho2_integral / rho_bar^2.
    """
    if c_func is None:
        c_func = hm.concentration

    k = np.asarray(k, dtype=float)
    c = float(c_func(np.atleast_1d(M), z).ravel()[0])
    Rv = float(hm.R_vir(M, z))
    rs = Rv / c
    rho_s_val = _rho_s(M, z, c_func)
    rho_bar2 = cfg.RHO_BAR**2

    result = np.empty_like(k)

    for ik, kk in enumerate(k.ravel()):
        if kk < 1e-10:
            # k→0 limit: just the volume integral
            result.ravel()[ik] = rho2_integral_analytic(M, z, c_func) / rho_bar2
            continue

        def integrand(r):
            if r < 1e-8 * rs:
                return 0.0
            x = r / rs
            rho2 = rho_s_val**2 / (x**2 * (1.0 + x)**4)
            return 4.0 * np.pi * r**2 * rho2 * np.sin(kk * r) / (kk * r)

        # Avoid singularity at r=0
        r_min = 1e-6 * rs
        val, _ = quad(integrand, r_min, Rv, limit=300, epsrel=1e-5)
        result.ravel()[ik] = val / rho_bar2

    return result


# ---------------------------------------------------------------------------
# Substructure boost factor (Moliné et al. 2017)
# ---------------------------------------------------------------------------

def boost_moline(M, z, M_min_sub=1e-6):
    """Substructure boost factor B(M, z) from Moliné et al. (2017).

    Full 5th-order polynomial (Eq. 18, Table 3, alpha=2) with z-scaling
    (Thesis Eq. 3.48):
        log10 B(M, z=0) = sum_i b_i [log10(M/M_sun)]^i
        B(M, z) = B(M, z=0) / (1 + z)

    B is a multiplicative enhancement: rho^2_eff = (1 + B) * rho^2_smooth.
    M is in M_sun/h (pipeline convention); converted to M_sun for polynomial.
    """
    M = np.asarray(M, dtype=float)

    if M_min_sub <= 0:
        return np.zeros_like(M)

    # Convert M_sun/h → M_sun: M_phys = M_code / h
    M_solar = M / cfg.h

    # For conservative scenario (M_min_sub = 1e7), zero out below threshold
    if M_min_sub >= 1e7:
        mask = M_solar > M_min_sub
        if not np.any(mask):
            return np.zeros_like(M)
    else:
        mask = np.ones_like(M, dtype=bool)

    # Full polynomial at z=0 (Moliné Eq. 18 / Thesis Eq. 3.47)
    log_M = np.log10(np.clip(M_solar, 1e-6, 1e15))
    log_B = np.zeros_like(log_M)
    for i, b_i in enumerate(cfg.MOLINE_BOOST_COEFFS):
        log_B += b_i * log_M**i

    B_z0 = 10.0**log_B

    # z-scaling (Thesis Eq. 3.48)
    B = B_z0 / (1.0 + z)

    # Zero out below M_min_sub for conservative scenario
    B = np.where(mask, B, 0.0)

    return np.clip(B, 0.0, 1000.0)


# ---------------------------------------------------------------------------
# Clumping factor Delta^2(z) (Eq. 4.2)
# ---------------------------------------------------------------------------

_clumping_cache = {}  # keyed by (round(z,4), boost_scenario)


def clumping_factor(z, M_min=None, M_max=None, boost_scenario='intermediate',
                    n_M=200):
    """Clumping factor Delta^2(z) = <rho^2>_phys / rho_bar_phys(z)^2.

    The physical-variable definition, consistent with Ullio+2002 Eq. 10 /
    Pinetti Eq. 4.1 where the formula is

        W_DM^(chi) propto (sigma v)/(8 pi m_chi^2) * rho_bar_com^2 * (1+z)^3
                          * Delta^2(z) * dN/dE * exp(-tau) / H(z)

    The halo integral gives <rho^2>_phys per comoving volume, which is
    (1+z)^3 smaller than <rho^2>_phys per physical volume. Dividing by
    rho_bar_com^2 rather than rho_bar_phys(z)^2 = rho_bar_com^2 (1+z)^6 then
    leaves a factor (1+z)^3 mismatch. Corrected by /(1+z)^3 at the end.

    Literature cross-check: at z=0 Delta^2 ~ 1e5-1e6 (dominated by halos),
    falling to ~1e4 at z=1 and ~1e3 at z=3 as structure is less collapsed
    (Taylor & Silk 2003; Ullio+2002; Cirelli+2011).

    Parameters
    ----------
    boost_scenario : str
        'none', 'conservative' (M_min_sub=1e7), 'intermediate' (M_min_sub=1e-6),
        'optimistic' (M_min_sub=1e-6 with enhanced substructure)
    """
    # Check cache
    cache_key = (round(float(z), 4), boost_scenario)
    if cache_key in _clumping_cache:
        return _clumping_cache[cache_key]

    if M_min is None:
        M_min = cfg.M_MIN_DM
    if M_max is None:
        M_max = cfg.M_MAX_DM

    M_min_sub_map = {
        'none': 0,
        'conservative': 1e7,
        'intermediate': 1e-6,
        'optimistic': 1e-6,
    }
    M_min_sub = M_min_sub_map.get(boost_scenario, 1e-6)

    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    integrand_arr = np.zeros(n_M)

    for i, M in enumerate(M_arr):
        dn = hm.dndM(M, z)
        if dn <= 0:
            continue
        rho2_int = rho2_integral_analytic(M, z)
        B = boost_moline(M, z, M_min_sub) if M_min_sub > 0 else 0.0
        integrand_arr[i] = dn * (1.0 + B) * rho2_int * M  # M from d(lnM)

    dlnM = np.log(M_arr[1] / M_arr[0])
    # Halo integral gives <rho^2>_phys per comoving volume; normalize by
    # physical rho_bar(z)^2 = rho_bar_com^2 (1+z)^6 while the (1+z)^3
    # physical-to-comoving volume factor leaves a net /(1+z)^3 correction.
    result = np.sum(integrand_arr) * dlnM / cfg.RHO_BAR**2 / (1.0 + z)**3
    _clumping_cache[cache_key] = result
    return result


# ---------------------------------------------------------------------------
# DM annihilation window function (Eq. 4.1)
# ---------------------------------------------------------------------------

def W_gamma_DM(E_GeV, z, m_chi_GeV, sigma_v=None, channel='bb',
               boost_scenario='intermediate'):
    """DM annihilation gamma-ray window function per comoving distance (Pinetti Eq. 4.1).

    W_DM(chi) = (1/(4pi)) * (sigma_v / 2) * (Omega_DM rho_c / m_chi)^2 * (1+z)^3
                * Delta^2(z) * dN/dE'|_{E'=(1+z)E} * exp(-tau)

    This is the PHYSICAL photon emissivity per steradian per energy, with NO
    1/H(z) factor. The mean intensity is obtained via the Pinetti convention
    <I_gamma> = integral dz * c/H(z) * W_gamma(z) (Eq. 4.1 text on p.9 of
    arXiv:1911.04989). The c/H Jacobian is supplied by the integration measure
    (dchi/dz) and the dchi/chi^2 weight in the Limber integrand, not baked into
    the window function.

    Parameters
    ----------
    E_GeV : float
        Observed photon energy [GeV].
    z : float
        Redshift.
    m_chi_GeV : float
        DM mass [GeV].
    sigma_v : float, optional
        Annihilation cross-section [cm^3/s]. Defaults to thermal relic.
    channel : str
        Annihilation channel.

    Returns
    -------
    W : float
        Window function value in [photons (Mpc/h)^{-3} s^{-1} sr^{-1} GeV^{-1}].
    """
    if sigma_v is None:
        sigma_v = cfg.SIGMA_V_THERMAL

    # Emitted energy
    E_emit = E_GeV * (1.0 + z)

    # Photon yield at emitted energy
    dNdE = pppc4dmid.dNdE(E_emit, m_chi_GeV, channel)
    if dNdE <= 0:
        return 0.0

    # EBL attenuation — evaluated at OBSERVED energy E_GeV, not emitted energy.
    # ebltable.opt_depth(z, E) takes the observed energy at Earth and integrates
    # the absorption along the full propagation path from z to 0.
    atten = ebl_mod.attenuation(np.atleast_1d(E_GeV), z)[0]

    Delta2 = clumping_factor(z, boost_scenario=boost_scenario)

    # DM density converted to GeV/cm^3
    M_sun_GeV = 1.116e57   # 1 M_sun in GeV
    Mpc_cm = cfg.MPC_TO_M * 100.0   # 1 Mpc in cm
    rho_DM = cfg.OMEGA_DM * cfg.RHO_CRIT  # [M_sun/h / (Mpc/h)^3]
    rho_DM_GeV_cm3 = rho_DM * M_sun_GeV * cfg.h**2 / Mpc_cm**3

    # Per-chi window function (Pinetti Eq. 4.1): physical emissivity
    prefactor = sigma_v / (8.0 * np.pi)  # sigma_v/2 / (4 pi) per Eq. 4.1
    particle = (rho_DM_GeV_cm3 / m_chi_GeV)**2
    cosmological = (1.0 + z)**3

    W_cgs = prefactor * particle * cosmological * Delta2 * float(dNdE) * atten
    # W_cgs units: [cm^3/s/sr] * [1/cm^6] * [1/GeV] = [cm^{-3} s^{-1} sr^{-1} GeV^{-1}]
    # — physical photon emissivity, matching Pinetti 2020 Eq. 4.1.

    # Convert cm^-3 to (Mpc/h)^-3
    Mpc_h_cm = Mpc_cm / cfg.h  # cm per (Mpc/h)
    return W_cgs * Mpc_h_cm**3


