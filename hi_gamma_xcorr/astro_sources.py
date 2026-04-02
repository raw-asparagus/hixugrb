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
# LDDE GLF parameters from the literature
#
# Convention: A is the normalization of dPhi/d(log10 L), NOT dPhi/dL.
# The conversion is: dPhi/dL = dPhi/d(log10 L) / (L * ln(10))
# All luminosities are gamma-ray (0.1-100 GeV band) in erg/s.
# ---------------------------------------------------------------------------

# FSRQ: Ajello et al. (2012), ApJ 751, 108, Table 3
_FSRQ_PARAMS = {
    'A': 3.06e-9,      # Mpc^{-3} (dPhi/d(logL) normalization)
    'L_c': 0.84e48,    # break luminosity [erg/s]
    'gamma1': 0.21,    # faint-end slope
    'gamma2': 1.58,    # bright-end slope
    'z_c_star': 1.47,  # peak redshift at L_ref
    'alpha': 0.21,     # luminosity dependence of z_c
    'p1': 7.35,        # positive evolution
    'p2': -6.51,       # negative evolution
    'L_ref': 1e48,     # reference luminosity for z_c(L)
}

# BL Lac: Ajello et al. (2014), MNRAS 441, 1760
# Single-component LDDE with piecewise evolution.
# Positive evolution (p1>0) up to z_c~1.2, then decline.
# Produces window peaking at z~1.0 as in Pinetti Fig. 5.1.
_BL_LAC_PARAMS = {
    'A': 5.0e-9,       # Mpc^{-3} (combined BL Lac population)
    'L_c': 1.0e46,     # erg/s (break luminosity)
    'gamma1': 0.60,    # faint-end slope
    'gamma2': 1.80,    # bright-end slope
    'z_c_star': 1.2,   # peak redshift (positive evolution, from Ajello+ 2014)
    'alpha': 0.15,     # luminosity dependence of z_c
    'p1': 4.0,         # positive evolution below z_c
    'p2': -2.0,        # negative evolution above z_c
    'L_ref': 1e48,
}

# mAGN: Di Mauro et al. (2014), ApJ 780, 161
# Derived from radio core LF via L_gamma-L_radio correlation.
# Contributes ~25-50% of IGRB intensity but negligible anisotropy.
_MAGN_PARAMS = {
    'A': 3.0e-8,       # Mpc^{-3} (calibrated to ~25% IGRB at 1 GeV)
    'L_c': 5e44,       # erg/s (characteristic gamma-ray luminosity)
    'gamma1': 0.60,
    'gamma2': 2.00,
    'z_c_star': 0.8,   # peak tracks radio AGN evolution
    'alpha': 0.15,
    'p1': 3.5,         # moderate positive evolution
    'p2': -2.0,
    'L_ref': 1e48,
}

# SFG: Gruppioni et al. (2013), MNRAS 432, 23
# IR LF converted via L_gamma = 10^{39.28} (L_IR/10^{10} L_sun)^{1.17}
# Simplified as LDDE with luminosity evolution (1+z)^{3.55} to z~2.
_SFG_PARAMS = {
    'A': 1e-8,         # Mpc^{-3} (calibrated to ~10-30% of IGRB at 1 GeV)
    'L_c': 5e40,       # erg/s (L* for gamma-ray SFGs)
    'gamma1': 0.4,     # faint end
    'gamma2': 2.5,     # bright end
    'z_c_star': 2.0,   # tracks cosmic SFR peak
    'alpha': 0.0,      # no luminosity dependence
    'p1': 3.55,        # strong positive evolution
    'p2': -4.0,        # rapid decline after z~2
    'L_ref': 1e48,
}


# ---------------------------------------------------------------------------
# Generic LDDE double power-law GLF
# ---------------------------------------------------------------------------

def _ldde_glf(L, z, params, evolution_form='piecewise'):
    """LDDE double power-law GLF returning dPhi/dL [Mpc^{-3} (erg/s)^{-1}].

    Parameters
    ----------
    L : float
        Luminosity [erg/s].
    z : float
        Redshift.
    params : dict
        GLF parameters (A, L_c, gamma1, gamma2, z_c_star, alpha, p1, p2, L_ref).
    evolution_form : str
        'piecewise' — standard LDDE (FSRQ, mAGN, SFG):
            e = [(1+z)/(1+z_c)]^p1 for z <= z_c, else [(1+z)/(1+z_c)]^p2
        'sum' — BL Lac form (Di Mauro et al.):
            e = [(1+z)/(1+z_c)]^p1 + [(1+z)/(1+z_c)]^p2
    """
    A = params['A']
    L_c = params['L_c']
    g1 = params['gamma1']
    g2 = params['gamma2']
    z_c_star = params['z_c_star']
    alpha = params['alpha']
    p1 = params['p1']
    p2 = params['p2']
    L_ref = params['L_ref']

    # Local LF: dPhi/d(log10 L) = A / [(L/L_c)^gamma1 + (L/L_c)^gamma2]
    x = L / L_c
    phi_logL = A / (x**g1 + x**g2)

    # Convert to dPhi/dL
    phi_L = phi_logL / (L * np.log(10.0))

    # Luminosity-dependent peak redshift
    z_c = z_c_star * (L / L_ref)**alpha
    z_c = max(z_c, 0.01)  # avoid z_c = 0

    # Redshift evolution
    ratio = (1.0 + z) / (1.0 + z_c)

    if evolution_form == 'sum':
        # BL Lac form: sum of two power laws
        e_z = ratio**p1 + ratio**p2
    else:
        # Standard piecewise LDDE
        if z <= z_c:
            e_z = ratio**p1
        else:
            e_z = ratio**p2

    return max(phi_L * e_z, 0.0)


# ---------------------------------------------------------------------------
# Source-specific GLF functions
# ---------------------------------------------------------------------------

def _glf_FSRQ(L, z):
    """FSRQ GLF from Ajello et al. (2012)."""
    return _ldde_glf(L, z, _FSRQ_PARAMS, evolution_form='piecewise')


def _glf_BL_Lac(L, z):
    """BL Lac GLF from Ajello et al. (2014), single-component LDDE."""
    return _ldde_glf(L, z, _BL_LAC_PARAMS, evolution_form='piecewise')


def _glf_mAGN(L, z):
    """mAGN GLF from Di Mauro et al. (2014)."""
    return _ldde_glf(L, z, _MAGN_PARAMS, evolution_form='piecewise')


def _glf_SFG(L, z):
    """SFG GLF from Gruppioni et al. (2013) IR LF with L_gamma scaling."""
    return _ldde_glf(L, z, _SFG_PARAMS, evolution_form='piecewise')


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
        return _glf_BL_Lac(L, z)
    elif source_class == 'FSRQ':
        return _glf_FSRQ(L, z)
    elif source_class == 'mAGN':
        return _glf_mAGN(L, z)
    elif source_class == 'SFG':
        return _glf_SFG(L, z)
    else:
        raise ValueError(f"Unknown source class: {source_class}")


# ---------------------------------------------------------------------------
# Astrophysical window function (Eq. 4.3)
# ---------------------------------------------------------------------------

def W_gamma_astro(E_GeV, z, source_class, unresolved_only=True):
    """Astrophysical gamma-ray window function per comoving distance (Pinetti Eq. 4.3).

    Per-chi convention: W(chi) = [d_L^2/(1+z)^2] * integral Phi * dF/dE dL

    Parameters
    ----------
    E_GeV : float
        Observed energy [GeV].
    z : float
        Redshift.
    source_class : str
        Source class name.
    unresolved_only : bool
        If True (default), integrate only up to L_sens (unresolved sources).
        If False, integrate over the full [L_min, L_max] range (total emission,
        survey-independent).
    """
    if z <= 0:
        return 0.0

    params = cfg.ASTRO_SOURCES[source_class]
    alpha = params['alpha']
    L_min = params['L_min']
    L_max = params['L_max']

    dL_Mpc = cosmo.d_L(z) / cfg.h  # physical Mpc
    dL_cm = dL_Mpc * cfg.MPC_TO_M * 100.0  # cm

    if unresolved_only:
        L_thr = L_sens(z)
        L_up = min(L_max, L_thr)
    else:
        L_up = L_max

    if L_up <= L_min:
        return 0.0

    # Compute the comoving volume emissivity j(E_rest, z) [ph s^{-1} Mpc^{-3} GeV^{-1} sr^{-1}]
    #
    # Each source emits: dn/dE_rest = L / (GeV_to_erg * I_alpha) * E_rest^{-alpha}  [ph/s/GeV]
    # where L [erg/s] is the rest-frame 0.1-100 GeV energy luminosity.
    #
    # The emissivity is: j = (1/4pi) integral phi(L) * dn/dE_rest dL
    E_min_band = 0.1     # 100 MeV [GeV]
    E_max_band = 100.0   # 100 GeV [GeV]
    GeV_to_erg = 1.602e-3  # 1 GeV in erg

    # Energy integral: integral E^{1-alpha} dE [GeV^{2-alpha}]
    if abs(alpha - 2.0) > 0.01:
        energy_integral = (E_max_band**(2.0 - alpha) - E_min_band**(2.0 - alpha)) / (2.0 - alpha)
    else:
        energy_integral = np.log(E_max_band / E_min_band)

    # Rest-frame energy of observed photon
    E_rest = E_GeV * (1.0 + z)

    def integrand(lnL):
        L = np.exp(lnL)
        phi = glf(L, z, source_class)  # [Mpc^{-3} (erg/s)^{-1}]
        # Photon emission rate per source at rest-frame energy E_rest:
        # dn/dE = L / (GeV_to_erg * I_alpha) * E_rest^{-alpha}  [ph/s/GeV]
        dn_dE = L / (GeV_to_erg * energy_integral) * E_rest**(-alpha)
        # Integrand: phi * dn_dE * L (extra L from d(lnL) Jacobian)
        return phi * dn_dE * L

    val, _ = quad(integrand, np.log(L_min), np.log(L_up), limit=200, epsrel=1e-5)

    # val = integral phi * dn/dE dL has units:
    # [Mpc^{-3} (erg/s)^{-1}] * [ph s^{-1} GeV^{-1}] * [erg/s] = [Mpc^{-3} ph s^{-1} GeV^{-1}]
    #
    # Pinetti Eq. 4.3 prescribes: W = [d_L^2/(1+z)^2] * integral Phi * dF/dE dL
    # Since dF/dE contains L/(4 pi d_L^2), the d_L^2 cancels, leaving:
    #   W = (1/(4pi)) * (1/(1+z)^2) * integral Phi * L * spectral dL
    # The (1+z)^{-2} factor suppresses high-z contributions (cosmological dimming).
    return val / (4.0 * np.pi * (1.0 + z)**2)


# ---------------------------------------------------------------------------
# Mean unresolved gamma-ray intensity (for Figure 2 validation)
# ---------------------------------------------------------------------------

def mean_intensity(E_GeV, source_class, z_max=5.0, n_z=100):
    """Mean unresolved gamma-ray intensity from a source class.

    <I>(E) = integral dz (c/H(z)) * j(E*(1+z), z) / (1+z)

    where j is the comoving emissivity [ph s^{-1} Mpc^{-3} GeV^{-1} sr^{-1}]
    returned by W_gamma_astro, and the 1/(1+z) accounts for cosmological
    energy loss and time dilation.

    Returns intensity in [photons cm^{-2} s^{-1} GeV^{-1} sr^{-1}].
    """
    z_arr = np.linspace(0.01, z_max, n_z)
    # W_gamma_astro already computes j at E_rest = E_obs*(1+z)
    j_arr = np.array([W_gamma_astro(E_GeV, z, source_class) for z in z_arr])

    # c/H(z) in Mpc (physical): this cancels the Mpc^{-3} in j
    # Then convert from Mpc^{-2} to cm^{-2}: (1 Mpc = 3.086e24 cm)
    H_arr = np.array([cosmo.H(z) for z in z_arr])
    c_over_H_Mpc = cfg.C_LIGHT_KM_S / H_arr  # [Mpc] (physical)
    Mpc_to_cm = cfg.MPC_TO_M * 100.0          # [cm/Mpc]

    # Cosmological dimming: 1/(1+z)
    dimming = 1.0 / (1.0 + z_arr)

    # Integrand: j [ph/s/Mpc^3/GeV/sr] * c/H [Mpc] * 1/(1+z) → [ph/s/Mpc^2/GeV/sr]
    # Convert Mpc^2 → cm^2: divide by Mpc_to_cm^2 → [ph/s/cm^2/GeV/sr] = [ph/cm^2/s/GeV/sr]
    # Wait: j * c/H has units ph/s/Mpc^2/GeV/sr. We need ph/cm^2/s/GeV/sr.
    # Since 1 Mpc^{-2} = 1/(Mpc_cm)^2 cm^{-2}, the integral already works
    # if we express distances consistently.
    #
    # Actually: j [ph s^{-1} Mpc^{-3} GeV^{-1} sr^{-1}] * c/H [Mpc] = [ph s^{-1} Mpc^{-2} GeV^{-1} sr^{-1}]
    # Convert to cm^{-2}: multiply by 1/Mpc_cm^2... no, [Mpc^{-2}] = [1/(Mpc_cm)^2 cm^{-2}]
    # So value in cm^{-2} = value_in_Mpc^{-2} / Mpc_cm^2
    integrand = j_arr * c_over_H_Mpc * dimming / Mpc_to_cm**2

    dz = z_arr[1] - z_arr[0]
    return np.sum(integrand) * dz


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
