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
    """Fourier transform of rho^2(r|M) / rho_bar^2.

    v_tilde(k|M) = (4 pi / rho_bar^2) integral_0^{R_vir} r^2 rho_NFW^2(r) sin(kr)/(kr) dr

    Normalized so v_tilde(k→0) = rho2_integral / rho_bar^2.
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

    B(M) is a multiplicative enhancement to the rho^2 integral:
    rho^2_eff = (1 + B) * rho^2_smooth.

    Uses a simplified parameterization.
    """
    M = np.asarray(M, dtype=float)
    # Simplified Moliné et al. fit: B ~ (M / M_min)^alpha with alpha ~ 0.12
    # B ~ 10-20 for M = 10^12 and M_min = 10^{-6}
    if M_min_sub <= 0 or M_min_sub >= 1e7:
        return np.zeros_like(M)

    log_ratio = np.log10(M / M_min_sub)
    # Moliné et al. parameterization (approximate)
    B = 1.6e-3 * log_ratio**2.5
    return np.clip(B, 0.0, 1000.0)


# ---------------------------------------------------------------------------
# Clumping factor Delta^2(z) (Eq. 4.2)
# ---------------------------------------------------------------------------

def clumping_factor(z, M_min=None, M_max=None, boost_scenario='intermediate',
                    n_M=100):
    """Clumping factor Delta^2(z) = <rho^2> / rho_bar^2.

    Delta^2 = (1/rho_bar^2) integral (dn/dM) * [1 + B(M)] * integral rho^2 d^3x dM

    Parameters
    ----------
    boost_scenario : str
        'none', 'conservative' (M_min_sub=1e7), 'intermediate' (M_min_sub=1e-6),
        'optimistic' (M_min_sub=1e-6 with enhanced substructure)
    """
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

    M_arr = np.logspace(np.log10(max(M_min, 1e-4)), np.log10(min(M_max, 1e17)), n_M)
    integrand_arr = np.zeros(n_M)

    for i, M in enumerate(M_arr):
        dn = hm.dndM(M, z)
        if dn <= 0:
            continue
        rho2_int = rho2_integral_analytic(M, z)
        B = boost_moline(M, z, M_min_sub) if M_min_sub > 0 else 0.0
        integrand_arr[i] = dn * (1.0 + B) * rho2_int * M  # M from d(lnM)

    dlnM = np.log(M_arr[1] / M_arr[0])
    return np.sum(integrand_arr) * dlnM / cfg.RHO_BAR**2


# ---------------------------------------------------------------------------
# DM annihilation window function (Eq. 4.1)
# ---------------------------------------------------------------------------

def W_gamma_DM(E_GeV, z, m_chi_GeV, sigma_v=None, channel='bb',
               boost_scenario='intermediate'):
    """DM annihilation gamma-ray window function W_gamma^DM(E, z).

    W = (1/4pi) * (sigma_v / 2) * Delta^2(z) * (Omega_DM * rho_c / m_chi)^2
        * (1+z)^3 * dN/dE'(E'=(1+z)*E) * exp(-tau(E*(1+z), z)) * c/H(z)

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
        Window function value.
    """
    if sigma_v is None:
        sigma_v = cfg.SIGMA_V_THERMAL

    # Emitted energy
    E_emit = E_GeV * (1.0 + z)

    # Photon yield at emitted energy
    dNdE = pppc4dmid.dNdE(E_emit, m_chi_GeV, channel)
    if dNdE <= 0:
        return 0.0

    # EBL attenuation
    atten = ebl_mod.attenuation(np.atleast_1d(E_emit), z)[0]

    # Clumping factor (expensive — should be cached in practice)
    # For now, use a simple power-law fit
    Delta2 = clumping_factor(z, boost_scenario=boost_scenario)

    # DM density in CGS-compatible units
    # Omega_DM * rho_c needs careful unit handling
    # rho_DM = Omega_DM * rho_crit [M_sun/h / (Mpc/h)^3]
    # Convert to GeV/cm^3 for the particle physics formula
    # 1 M_sun = 1.116e57 GeV
    # 1 Mpc = 3.086e24 cm
    M_sun_GeV = 1.116e57
    Mpc_cm = cfg.MPC_TO_M * 100.0
    rho_DM = cfg.OMEGA_DM * cfg.RHO_CRIT  # M_sun/h / (Mpc/h)^3
    # Convert: (M_sun/h) / (Mpc/h)^3 = (M_sun_GeV * h^{-1}) / (Mpc_cm * h^{-1})^3
    # = M_sun_GeV / h * h^3 / Mpc_cm^3 = M_sun_GeV * h^2 / Mpc_cm^3
    rho_DM_GeV_cm3 = rho_DM * M_sun_GeV * cfg.h**2 / (Mpc_cm / cfg.h)**3
    # Simplify: rho_DM [M_sun/h/(Mpc/h)^3] * M_sun_GeV/M_sun * (Mpc/h)^3/cm^3 / h
    # = rho_DM * M_sun_GeV * h^{-1} / (Mpc_cm / h)^3
    # = rho_DM * M_sun_GeV * h^{-1} * h^3 / Mpc_cm^3
    # = rho_DM * M_sun_GeV * h^2 / Mpc_cm^3
    rho_DM_GeV_cm3 = rho_DM * M_sun_GeV * cfg.h**2 / Mpc_cm**3

    # sigma_v in cm^3/s
    # c/H(z) in cm
    c_over_H = cfg.C_LIGHT * 100.0 / cosmo.H(z)  # cm/s / (km/s/Mpc) → cm ... need units
    # c [cm/s] / H [s^{-1}] = c/H [cm]... H in 1/s:
    H_SI = cosmo.H(z) * 1e3 / cfg.MPC_TO_M  # km/s/Mpc → 1/s
    c_over_H_cm = (cfg.C_LIGHT * 100.0) / H_SI  # cm

    # The window function
    # W = (sigma_v / (8*pi)) * (rho_DM / m_chi)^2 * (1+z)^3 * dN/dE * exp(-tau) * Delta^2 * c/H
    # Factor 1/(4pi) * 1/2 = 1/(8pi) for Majorana fermion
    prefactor = sigma_v / (8.0 * np.pi)
    particle = (rho_DM_GeV_cm3 / m_chi_GeV)**2
    cosmological = (1.0 + z)**3

    W = prefactor * particle * cosmological * Delta2 * float(dNdE) * atten * c_over_H_cm

    return W


# ---------------------------------------------------------------------------
# DM power spectra (Eqs. 4.4–4.5)
# ---------------------------------------------------------------------------

def P_DM_1h(k, z, M_min=None, M_max=None, n_M=60):
    """One-halo DM annihilation power spectrum.

    P_DM^{1h} = integral (dn/dM) * [v_tilde / Delta^2]^2 dM
    """
    if M_min is None:
        M_min = max(cfg.M_MIN_DM, 1e4)  # practical lower limit
    if M_max is None:
        M_max = min(cfg.M_MAX_DM, 1e16)

    k = np.atleast_1d(np.asarray(k, dtype=float))
    Delta2 = clumping_factor(z)

    if Delta2 <= 0:
        return np.zeros_like(k)

    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    result = np.zeros_like(k)

    for M in M_arr:
        dn = hm.dndM(M, z)
        if dn <= 0:
            continue
        vt = v_tilde(k, M, z)
        result += dn * (vt / Delta2)**2 * M  # M from d(lnM)

    dlnM = np.log(M_arr[1] / M_arr[0])
    return result * dlnM


def P_DM_2h(k, z, M_min=None, M_max=None, n_M=60):
    """Two-halo DM annihilation power spectrum.

    P_DM^{2h} = [integral (dn/dM) * b(M) * v_tilde / Delta^2 dM]^2 * P_lin
    """
    if M_min is None:
        M_min = max(cfg.M_MIN_DM, 1e4)
    if M_max is None:
        M_max = min(cfg.M_MAX_DM, 1e16)

    k = np.atleast_1d(np.asarray(k, dtype=float))
    Delta2 = clumping_factor(z)

    if Delta2 <= 0:
        return np.zeros_like(k)

    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    I_2h = np.zeros_like(k)

    for M in M_arr:
        dn = hm.dndM(M, z)
        b = hm.bias(M, z)
        if dn <= 0:
            continue
        vt = v_tilde(k, M, z)
        I_2h += dn * b * vt / Delta2 * M

    dlnM = np.log(M_arr[1] / M_arr[0])
    I_2h *= dlnM
    return I_2h**2 * cosmo.P_lin(k, z)
