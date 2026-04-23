"""Dark matter annihilation model: rho^2 profile, clumping factor, window function.

All masses in M_sun/h, distances in Mpc/h, wavenumbers in h/Mpc.
"""

import numpy as np
from scipy.integrate import quad

from . import config as cfg
from . import halo_model as hm
from . import pppc4dmid
from . import ebl as ebl_mod
from .cache import _cache_stable

# ---------------------------------------------------------------------------
# NFW rho^2 profile: analytic expressions
# ---------------------------------------------------------------------------

def _rho_s(M, z):
    """NFW scale density rho_s [M_sun/h / (Mpc/h)^3].

    rho_s = M / (4 pi r_s^3 f(c))
    """
    c = float(hm.concentration(M, z))
    Rv = float(hm.R_vir(M, z))
    rs = Rv / c
    fc = np.log(1.0 + c) - c / (1.0 + c)
    return M / (4.0 * np.pi * rs**3 * fc)


def rho2_integral_analytic(M, z):
    """Analytic integral of rho_NFW^2 over the halo volume.

    integral_0^{R_vir} 4 pi r^2 rho_NFW^2(r) dr
    = (4 pi / 3) rho_s^2 r_s^3 [1 - 1/(1+c)^3]

    Returns the integral in units of [(M_sun/h)^2 / (Mpc/h)^3].
    """
    c = float(hm.concentration(M, z))
    Rv = float(hm.R_vir(M, z))
    rs = Rv / c
    rho_s_val = _rho_s(M, z)
    return (4.0 * np.pi / 3.0) * rho_s_val**2 * rs**3 * (1.0 - 1.0 / (1.0 + c)**3)


# ---------------------------------------------------------------------------
# Fourier transform of rho^2 profile (numerical)
# ---------------------------------------------------------------------------

def v_tilde(k, M, z):
    """Fourier transform of rho^2(r|M) / rho_bar^2  [(Mpc/h)^3].

    v_tilde(k|M) = (4 pi / rho_bar^2) integral_0^{R_vir} r^2 rho_NFW^2(r) sin(kr)/(kr) dr

    Returns [(Mpc/h)^3]: the volume-weighted profile transform, analogous to
    u_nfw but for rho^2.  At k→0, v_tilde = rho2_integral / rho_bar^2.
    """
    k = np.asarray(k, dtype=float)
    c = float(hm.concentration(M, z))
    Rv = float(hm.R_vir(M, z))
    rs = Rv / c
    rho_s_val = _rho_s(M, z)
    rho_bar2 = cfg.RHO_BAR**2

    result = np.empty_like(k)

    for ik, kk in enumerate(k.ravel()):
        if kk < 1e-10:
            # k→0 limit: just the volume integral
            result.ravel()[ik] = rho2_integral_analytic(M, z) / rho_bar2
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

    return np.where(mask, B, 0.0)


# ---------------------------------------------------------------------------
# Clumping factor Delta^2(z) (Eq. 4.2)
# ---------------------------------------------------------------------------

@_cache_stable(module=__name__)
def _clumping_compute(z, M_min, M_max, boost_scenario):
    """Core clumping computation using adaptive quadrature over ln M."""

    def integrand(lnM):
        M = np.exp(lnM)
        dn = hm.dndM(M, z)
        if dn <= 0:
            return 0.0
        rho2 = rho2_integral_analytic(M, z)
        B = boost_moline(M, z) if boost_scenario != 'no_boost' else 0.0
        return dn * (1.0 + B) * rho2 * M

    val, _ = quad(integrand, np.log(M_min), np.log(M_max),
                  limit=300, epsrel=1e-4)

    return val / cfg.RHO_BAR**2 / (1.0 + z)**3


def clumping_factor(z, M_min=None, M_max=None, boost_scenario='intermediate'):
    """Clumping factor Delta^2(z) = <rho^2>_phys / rho_bar_phys(z)^2.

    The physical-variable definition, consistent with Ullio+2002 Eq. 10 /
    Pinetti Eq. 4.1 where the formula is

        W_DM^(chi) propto (sigma v)/(8 pi m_chi^2) * rho_bar_com^2 * (1+z)^3
                          * Delta^2(z) * dN/dE * exp(-tau) / H(z)

    The halo integral gives <rho^2>_phys per comoving volume, which is
    (1+z)^3 smaller than <rho^2>_phys per physical volume. Dividing by
    rho_bar_com^2 rather than rho_bar_phys(z)^2 = rho_bar_com^2 (1+z)^6 then
    leaves a factor (1+z)^3 mismatch. Corrected by /(1+z)^3 at the end.

    Uses adaptive quadrature (scipy.quad) over ln M for high accuracy.

    Literature cross-check: at z=0 Delta^2 ~ 1e5-1e6 (dominated by halos),
    falling to ~1e4 at z=1 and ~1e3 at z=3 as structure is less collapsed
    (Taylor & Silk 2003; Ullio+2002; Cirelli+2011).

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

    return _clumping_compute(float(z), float(M_min), float(M_max),
                             boost_scenario)


# ---------------------------------------------------------------------------
# DM annihilation window function (Eq. 4.1)
# ---------------------------------------------------------------------------

def _W_gamma_DM_impl(E_GeV, z, m_chi_GeV, sigma_v, channel, boost_scenario):
    """DM window computation."""
    E_emit = E_GeV * (1.0 + z)
    dNdE = pppc4dmid.dNdE(E_emit, m_chi_GeV, channel)
    if dNdE <= 0:
        return 0.0

    atten = float(ebl_mod.attenuation(E_GeV, z)[0])
    Delta2 = clumping_factor(z, boost_scenario=boost_scenario)

    Mpc_cm = cfg.MPC_TO_M * 100.0
    rho_DM_GeV_cm3 = cfg.OMEGA_DM * cfg.RHO_CRIT * cfg.M_SUN_GEV * cfg.h**2 / Mpc_cm**3

    prefactor = sigma_v / (8.0 * np.pi)
    particle = (rho_DM_GeV_cm3 / m_chi_GeV)**2
    cosmological = (1.0 + z)**3

    W_cgs = prefactor * particle * cosmological * Delta2 * float(dNdE) * atten
    Mpc_h_cm = Mpc_cm / cfg.h
    return W_cgs * Mpc_h_cm**3


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
    return _W_gamma_DM_impl(float(E_GeV), float(z), float(m_chi_GeV),
                            float(sigma_v), channel, boost_scenario)
