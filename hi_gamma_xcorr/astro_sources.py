"""Astrophysical gamma-ray source populations.

Implements gamma-ray luminosity functions (GLFs) and window functions
for BL Lacs, FSRQs, misaligned AGN, and star-forming galaxies.

GLFs follow the LDDE parameterizations from:
- BL Lac: Ajello et al. (2014)
- FSRQ: Ajello et al. (2012)
- mAGN: Di Mauro et al. (2014)
- SFG: Gruppioni et al. (2013)
"""

import numpy as np
from scipy.integrate import quad

from . import config as cfg
from . import cosmology as cosmo

# ---------------------------------------------------------------------------
# Luminosity threshold from Fermi sensitivity
# ---------------------------------------------------------------------------

def L_sens(z):
    """Luminosity threshold [erg/s] for Fermi-LAT detection at redshift z.

    L_sens = 4 pi d_L^2 * F_sens, where d_L is in cm.
    """
    dL_Mpc = cosmo.d_L(z) / cfg.h  # physical Mpc
    dL_cm = dL_Mpc * cfg.MPC_TO_M * 100.0  # cm
    return 4.0 * np.pi * dL_cm**2 * cfg.F_SENS


# ---------------------------------------------------------------------------
# Simplified GLF models
#
# Each GLF returns the comoving number density phi(L, z) in
# units of [Mpc^{-3} (erg/s)^{-1}], i.e., the luminosity function
# per unit luminosity per unit comoving volume.
# ---------------------------------------------------------------------------

def _glf_blazar(L, z, subtype='BL_Lac'):
    """Simplified blazar GLF based on Ajello et al. (2012, 2014).

    Uses a broken power-law in L with LDDE redshift evolution.
    """
    # Break luminosity and slopes
    if subtype == 'BL_Lac':
        L_star = 1e46  # erg/s
        gamma1 = 0.6   # faint-end slope
        gamma2 = 2.2   # bright-end slope
        A = 2.5e-8     # normalization [Mpc^{-3} (erg/s)^{-1}]
        z_peak = 1.2
        p1 = 4.0       # positive evolution
        p2 = -1.5      # negative evolution
    else:  # FSRQ
        L_star = 5e47
        gamma1 = 1.0
        gamma2 = 2.5
        A = 8e-10
        z_peak = 1.5
        p1 = 7.0
        p2 = -4.0

    # Double power law
    phi_0 = A / ((L / L_star)**gamma1 + (L / L_star)**gamma2)

    # LDDE evolution
    if z <= z_peak:
        e_z = (1.0 + z)**p1
    else:
        e_z = (1.0 + z_peak)**p1 * ((1.0 + z) / (1.0 + z_peak))**p2

    return phi_0 * e_z


def _glf_mAGN(L, z):
    """Simplified mAGN GLF from Di Mauro et al. (2014)."""
    L_star = 1e44
    gamma1 = 0.8
    gamma2 = 2.0
    A = 5e-7
    z_peak = 0.8
    p1 = 3.0
    p2 = -2.0

    phi_0 = A / ((L / L_star)**gamma1 + (L / L_star)**gamma2)

    if z <= z_peak:
        e_z = (1.0 + z)**p1
    else:
        e_z = (1.0 + z_peak)**p1 * ((1.0 + z) / (1.0 + z_peak))**p2

    return phi_0 * e_z


def _glf_SFG(L, z):
    """Simplified SFG GLF from Gruppioni et al. (2013).

    Uses the IR luminosity function converted to gamma-ray via L_gamma ~ L_IR^{1.17}.
    """
    # SFG have a very steep faint end
    L_star = 5e39
    gamma1 = 0.3
    gamma2 = 2.5
    A = 1e-4
    p_evol = 3.55  # Strong positive evolution tracking cosmic SFR

    phi_0 = A / ((L / L_star)**gamma1 + (L / L_star)**gamma2)
    e_z = (1.0 + min(z, 2.0))**p_evol  # Saturate at z=2

    return phi_0 * e_z


def glf(L, z, source_class):
    """Gamma-ray luminosity function phi(L, z) [Mpc^{-3} (erg/s)^{-1}].

    Parameters
    ----------
    L : float
        Gamma-ray luminosity [erg/s].
    z : float
        Redshift.
    source_class : str
        One of 'BL_Lac', 'FSRQ', 'mAGN', 'SFG'.
    """
    if source_class == 'BL_Lac':
        return _glf_blazar(L, z, 'BL_Lac')
    elif source_class == 'FSRQ':
        return _glf_blazar(L, z, 'FSRQ')
    elif source_class == 'mAGN':
        return _glf_mAGN(L, z)
    elif source_class == 'SFG':
        return _glf_SFG(L, z)
    else:
        raise ValueError(f"Unknown source class: {source_class}")


# ---------------------------------------------------------------------------
# Astrophysical window function (Eq. 4.3)
# ---------------------------------------------------------------------------

def W_gamma_astro(E_GeV, z, source_class):
    """Astrophysical gamma-ray window function.

    W = [d_L^2(z) / (1+z)^2] * integral_{L_min}^{min(L_max, L_sens)} dL phi(L,z) (dF/dE)

    The differential flux follows a power law: dF/dE ~ E^{-alpha} * L / (4 pi d_L^2)

    Parameters
    ----------
    E_GeV : float
        Observed energy [GeV].
    z : float
        Redshift.
    source_class : str
        Source class name.

    Returns
    -------
    W : float [photons cm^{-2} s^{-1} GeV^{-1} Mpc^{-1}] (appropriate for Limber)
    """
    if z <= 0:
        return 0.0

    params = cfg.ASTRO_SOURCES[source_class]
    alpha = params['alpha']
    L_min = params['L_min']
    L_max = params['L_max']

    dL_Mpc = cosmo.d_L(z) / cfg.h  # physical Mpc
    dL_cm = dL_Mpc * cfg.MPC_TO_M * 100.0

    L_thr = L_sens(z)
    L_up = min(L_max, L_thr)

    if L_up <= L_min:
        return 0.0

    # Spectral shape: dF/dE = (alpha - 1) / E_ref * (E/E_ref)^{-alpha} * L / (4 pi d_L^2)
    # where E_ref = 1 GeV (normalization energy)
    E_ref = 1.0  # GeV
    spectral_factor = (alpha - 1.0) / E_ref * (E_GeV / E_ref)**(-alpha)

    def integrand(lnL):
        L = np.exp(lnL)
        phi = glf(L, z, source_class)
        flux = spectral_factor * L / (4.0 * np.pi * dL_cm**2)
        return phi * flux * L  # extra L from d(lnL)

    val, _ = quad(integrand, np.log(L_min), np.log(L_up), limit=200, epsrel=1e-5)

    # Multiply by d_L^2 / (1+z)^2 (the chi^2 factor from angular diameter distance)
    W = dL_cm**2 / (1.0 + z)**2 * val

    # Convert to appropriate units for Limber: need c/H(z) factor
    H_inv_cm = cfg.C_LIGHT * 100.0 / (cosmo.H(z) * 1e3 / cfg.MPC_TO_M)
    W *= 1.0 / H_inv_cm  # per unit comoving distance

    return W


# ---------------------------------------------------------------------------
# Mean unresolved gamma-ray intensity (for Figure 2 validation)
# ---------------------------------------------------------------------------

def mean_intensity(E_GeV, source_class, z_max=5.0, n_z=100):
    """Mean unresolved gamma-ray intensity from a source class.

    <I> = integral dz (c/H(z)) W_gamma(E, z)

    Returns intensity in [photons cm^{-2} s^{-1} GeV^{-1} sr^{-1}].
    """
    z_arr = np.linspace(0.01, z_max, n_z)
    integrand = np.array([W_gamma_astro(E_GeV, z, source_class) for z in z_arr])

    # c/H(z) in cm
    H_arr = np.array([cosmo.H(z) for z in z_arr])
    H_SI = H_arr * 1e3 / cfg.MPC_TO_M  # 1/s
    c_over_H = cfg.C_LIGHT * 100.0 / H_SI  # cm

    # The window function already includes the comoving distance factors
    # Integrate over dz
    dz = z_arr[1] - z_arr[0]
    return np.sum(integrand * c_over_H) * dz


# ---------------------------------------------------------------------------
# Effective bias for astrophysical sources
# ---------------------------------------------------------------------------

def bias_astro(z, source_class):
    """Effective linear bias for an astrophysical source class.

    Uses approximate halo mass assignments:
    - Blazars (BL Lac, FSRQ): hosted in ~10^{13} M_sun halos
    - mAGN: ~10^{13} M_sun halos
    - SFG: ~10^{11-12} M_sun halos
    """
    from . import halo_model as hm

    mass_map = {
        'BL_Lac': 1e13,
        'FSRQ': 1e13,
        'mAGN': 1e13,
        'SFG': 5e11,
    }
    M_host = mass_map.get(source_class, 1e12)
    return hm.bias(M_host, z)
