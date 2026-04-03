"""Astrophysical gamma-ray source populations.

Implements gamma-ray luminosity functions (GLFs) and window functions
for BL Lacs, FSRQs, misaligned AGN, and star-forming galaxies.

GLF sources:
- BL Lac: Ajello et al. (2014) — LDDE
- FSRQ: Ajello et al. (2012) — LDDE
- mAGN: Di Mauro et al. (2014) — radio LF → gamma conversion chain
- SFG: Gruppioni et al. (2013) + Ackermann et al. (2012) — IR LF → gamma
"""

import functools

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

# BL Lac: Ajello et al. (2014), ApJ 780, 73
# Combined BL Lac population with LDDE inverse-sum evolution (Eq. C.4).
# Parameters from thesis Table C.1 (originally from Ajello+ 2014).
_BL_LAC_PARAMS = {
    'A': 9.20e-11,     # Mpc^{-3} (dPhi/d(log10 L) normalization)
    'L_c': 2.43e48,    # erg/s (break luminosity L*)
    'gamma1': 1.12,    # faint-end slope
    'gamma2': 3.71,    # bright-end slope
    'z_c_star': 1.67,  # peak redshift z*
    'alpha': 4.46e-2,  # luminosity dependence beta of z_c
    'p1': 4.50,        # positive low-z evolution
    'p2': -12.88,      # steep negative high-z evolution
    'L_ref': 1e48,     # reference luminosity for z_c(L)
}

# ---------------------------------------------------------------------------
# mAGN: Di Mauro et al. (2014) radio→gamma conversion chain
# Willott (2001) RLF → Inoue (2011) freq → Lara (2004) core-total → Di Mauro
# ---------------------------------------------------------------------------

def _willott_rlf(L_151, z):
    """Willott et al. (2001) two-component radio luminosity function.

    Returns dPhi/d(log10 L_151) [Mpc^{-3}] in the Willott cosmology (H0=50).

    Parameters
    ----------
    L_151 : float
        Radio luminosity at 151 MHz [W/Hz].
    z : float
        Redshift.
    """
    # Low-power component (Eq. C.10)
    x_l = L_151 / cfg.WILLOTT_L_L_STAR
    rho_l = cfg.WILLOTT_RHO_L_STAR * x_l**(-cfg.WILLOTT_BETA_L) * np.exp(-x_l)
    if z < cfg.WILLOTT_Z_L_STAR:
        rho_l *= (1.0 + z)**cfg.WILLOTT_K_L
    else:
        rho_l *= (1.0 + cfg.WILLOTT_Z_L_STAR)**cfg.WILLOTT_K_L

    # High-power component (Eqs. C.11-C.12)
    x_h = L_151 / cfg.WILLOTT_L_H_STAR
    rho_h = cfg.WILLOTT_RHO_H_STAR * x_h**(-cfg.WILLOTT_BETA_H) * np.exp(-1.0 / x_h)
    if z < cfg.WILLOTT_Z_H_STAR:
        z_h0 = cfg.WILLOTT_Z_H0_LO
    else:
        z_h0 = cfg.WILLOTT_Z_H0_HI
    f_h = np.exp(-0.5 * ((z - cfg.WILLOTT_Z_H_STAR) / z_h0)**2)
    rho_h *= f_h

    return max(rho_l + rho_h, 0.0)


@functools.lru_cache(maxsize=512)
def _willott_volume_correction(z):
    """Comoving volume ratio eta(z) = (d_C^W / d_C)^2 * (H / H_W).

    Converts Willott (H0=50, Omega_M=1) Mpc^{-3} to Planck cosmology Mpc^{-3}.
    """
    if z <= 0:
        return 1.0

    # Willott cosmology: Einstein-de Sitter (H0=50, Omega_M=1)
    def _inv_H_W(zp):
        return 1.0 / (cfg.H0_WILLOTT * np.sqrt((1.0 + zp)**3))

    d_C_W, _ = quad(_inv_H_W, 0, z, limit=100)
    d_C_W *= cfg.C_LIGHT_KM_S  # [Mpc]
    H_W = cfg.H0_WILLOTT * np.sqrt((1.0 + z)**3)  # [km/s/Mpc]

    # Pipeline cosmology
    d_C = cosmo.chi(z) / cfg.h  # chi is in Mpc/h → physical Mpc
    H_pipeline = cosmo.H(z)     # [km/s/Mpc]

    if d_C <= 0 or d_C_W <= 0:
        return 1.0

    eta = (d_C_W / d_C)**2 * (H_pipeline / H_W)
    return eta


def _L151_from_Lgamma(L_gamma):
    """Invert the radio→gamma chain to get L_151 from L_gamma.

    Chain (Eqs. C.13-C.15):
      L_gamma [erg/s] → nuL_nu_core [erg/s] → L_core^{5GHz} [W/Hz]
      → L_tot^{1.4GHz} [W/Hz] → L_tot^{151MHz} [W/Hz]

    Note: Di Mauro Eq. C.13 uses luminosities in erg/s (i.e., nuL_nu),
    while Lara Eq. C.14 uses spectral luminosities in W/Hz.
    Conversion: L [erg/s] = L [W/Hz] * nu [Hz] * 1e7 [erg/s per W].

    Returns
    -------
    L_151 : float
        Total radio luminosity at 151 MHz [W/Hz].
    dL151_dLgamma : float
        Jacobian dL_151/dL_gamma.
    """
    NU_5GHZ = 5.0e9     # Hz
    W_TO_ERG = 1.0e7     # erg/s per W

    # Step 1: L_gamma [erg/s] → nuL_nu_core [erg/s] via Di Mauro Eq. C.13
    # log L_gamma = 2 + 1.008 * log(nuL_nu_core)  [both in erg/s]
    log_nuLnu_core = (np.log10(L_gamma) - cfg.DIMAURO_GAMMA_RADIO_A) / cfg.DIMAURO_GAMMA_RADIO_B
    nuLnu_core = 10.0**log_nuLnu_core  # erg/s

    # Convert nuL_nu [erg/s] → L_core [W/Hz]: L_WHZ = nuLnu / (nu * 1e7)
    L_core_WHZ = nuLnu_core / (NU_5GHZ * W_TO_ERG)
    log_Lcore_WHZ = np.log10(L_core_WHZ)

    # Step 2: L_core^{5GHz} [W/Hz] → L_tot^{1.4GHz} [W/Hz] via Lara Eq. C.14
    log_Ltot_1p4 = (log_Lcore_WHZ - cfg.LARA_A) / cfg.LARA_B
    L_tot_1p4 = 10.0**log_Ltot_1p4

    # Step 3: L_tot^{1.4GHz} → L_tot^{151MHz} using spectral index (Eq. C.15)
    freq_ratio = (1400.0 / 151.0)**cfg.RADIO_ALPHA
    L_151 = L_tot_1p4 * freq_ratio

    # Composite log-space Jacobian:
    # dlog L_151 / dlog L_gamma = 1 / (DIMAURO_B * LARA_B)
    # (the nuLnu↔W/Hz conversion is a constant offset in log-space, Jacobian = 1)
    dlog_ratio = 1.0 / (cfg.DIMAURO_GAMMA_RADIO_B * cfg.LARA_B)
    dL151_dLgamma = (L_151 / L_gamma) * dlog_ratio

    return L_151, dL151_dLgamma


def _glf_mAGN(L, z):
    """mAGN GLF from Di Mauro et al. (2014) via Willott RLF (Eq. C.19).

    phi_gamma = k * eta / (1+z)^{2-Gamma} * rho_r / (ln10 * L_151) * |dL_151/dL_gamma|

    Returns dPhi/dL_gamma [Mpc^{-3} (erg/s)^{-1}].
    """
    if L <= 0 or z < 0:
        return 0.0

    L_151, dL151_dLgamma = _L151_from_Lgamma(L)

    if L_151 <= 0:
        return 0.0

    rho_r = _willott_rlf(L_151, z)  # dPhi/d(log10 L) in Willott cosmology
    eta = _willott_volume_correction(z)

    Gamma = cfg.ASTRO_SOURCES['mAGN']['alpha']  # 2.37
    k_corr = (1.0 + z)**(2.0 - Gamma)  # K-correction

    # Eq. C.19: phi_gamma = k * eta / k_corr * (rho_r / (ln10 * L_151)) * |dL151/dLgamma|
    dPhi_dL151 = rho_r / (np.log(10.0) * L_151)
    phi_gamma = cfg.DIMAURO_K * eta / k_corr * dPhi_dL151 * abs(dL151_dLgamma)

    return max(phi_gamma, 0.0)


# ---------------------------------------------------------------------------
# SFG: Gruppioni et al. (2013) IR LF → Ackermann et al. (2012) L_gamma-L_IR
# ---------------------------------------------------------------------------

def _gruppioni_component(L_IR, z, comp_name):
    """Single component of the Gruppioni (2013) modified Schechter IR LF.

    Returns dPhi/d(log10 L_IR) [Mpc^{-3}].

    Parameters
    ----------
    L_IR : float
        Total infrared luminosity (8-1000 um) [L_sun].
    z : float
        Redshift.
    comp_name : str
        'spiral', 'starburst', or 'sf_agn'.
    """
    p = cfg.GRUPPIONI_PARAMS[comp_name]
    gamma = p['gamma']
    sigma = p['sigma']
    L_star = 10.0**p['log_Lstar']     # L_sun
    phi_star = 10.0**p['log_phistar']  # Mpc^{-3}
    k_L = p['k_L']
    k_R1 = p['k_R1']
    k_R2 = p['k_R2']

    # Luminosity evolution L_0(z) — break at z=1.1 for all components (Eq. C.24)
    if z <= 1.1:
        L_0 = L_star * ((1.0 + z) / 1.15)**k_L
    else:
        L_0 = L_star * (2.1 / 1.15)**k_L  # frozen above z=1.1

    # Density evolution phi_0(z) (Eqs. C.25-C.26)
    if comp_name == 'spiral':
        # Spiral: break at z=0.53
        if z <= 0.53:
            phi_0 = phi_star * ((1.0 + z) / 1.15)**k_R1
        else:
            phi_0 = phi_star * (1.53 / 1.15)**k_R1 * ((1.0 + z) / 1.53)**k_R2
    else:
        # Starburst and SF-AGN: break at z=1.1
        if z <= 1.1:
            phi_0 = phi_star * ((1.0 + z) / 1.15)**k_R1
        else:
            phi_0 = phi_star * (2.1 / 1.15)**k_R1 * ((1.0 + z) / 2.1)**k_R2

    # Modified Schechter form (Eq. C.23)
    ratio = L_IR / L_0
    log_arg = np.log10(1.0 + ratio)
    phi = phi_0 * ratio**(1.0 - gamma) * np.exp(-log_arg**2 / (2.0 * sigma**2))

    return max(phi, 0.0)


def _gruppioni_ir_lf(L_IR, z):
    """Gruppioni et al. (2013) three-component IR luminosity function.

    phi_IR = phi_spiral + phi_starburst + phi_SF-AGN

    Returns dPhi/d(log10 L_IR) [Mpc^{-3}].

    Parameters
    ----------
    L_IR : float
        Total infrared luminosity (8-1000 um) [L_sun].
    z : float
        Redshift.
    """
    return (_gruppioni_component(L_IR, z, 'spiral')
            + _gruppioni_component(L_IR, z, 'starburst')
            + _gruppioni_component(L_IR, z, 'sf_agn'))


def _L_IR_from_Lgamma(L_gamma):
    """Invert Ackermann et al. (2012) L_gamma-L_IR relation.

    log10(L_gamma/erg s^-1) = alpha * log10(L_IR / 10^10 L_sun) + beta

    Returns
    -------
    L_IR : float
        IR luminosity [L_sun].
    dlogLIR_dlogLgamma : float
        Jacobian d(log10 L_IR) / d(log10 L_gamma) = 1/alpha.
    """
    log_Lgamma = np.log10(L_gamma)
    log_x = (log_Lgamma - cfg.ACKERMANN_BETA_IR) / cfg.ACKERMANN_ALPHA_IR
    L_IR = 1e10 * cfg.L_SUN * 10.0**log_x  # [erg/s] → convert to L_sun below
    L_IR_Lsun = L_IR / cfg.L_SUN            # [L_sun]

    dlogLIR_dlogLgamma = 1.0 / cfg.ACKERMANN_ALPHA_IR

    return L_IR_Lsun, dlogLIR_dlogLgamma


def _glf_SFG(L, z):
    """SFG GLF from Gruppioni (2013) IR LF + Ackermann (2012) scaling (Eq. C.28).

    phi_gamma = phi_IR(L_IR(L_gamma), z) * |dlog10 L_IR / dlog10 L_gamma| / (L_gamma * ln10)

    Returns dPhi/dL_gamma [Mpc^{-3} (erg/s)^{-1}].
    """
    if L <= 0 or z < 0:
        return 0.0

    L_IR_Lsun, dlogLIR_dlogLgamma = _L_IR_from_Lgamma(L)

    if L_IR_Lsun <= 0:
        return 0.0

    phi_IR_logL = _gruppioni_ir_lf(L_IR_Lsun, z)  # dPhi/d(log10 L_IR)

    # Eq. C.28: phi_gamma in dPhi/d(log10 L_gamma) = phi_IR * |dlogLIR/dlogLgamma|
    phi_gamma_logL = phi_IR_logL * abs(dlogLIR_dlogLgamma)

    # Convert to dPhi/dL_gamma [Mpc^{-3} (erg/s)^{-1}]
    phi_gamma = phi_gamma_logL / (L * np.log(10.0))

    return max(phi_gamma, 0.0)


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
        'piecewise' — standard LDDE (FSRQ):
            e = [(1+z)/(1+z_c)]^p1 for z <= z_c, else [(1+z)/(1+z_c)]^p2
        'ldde_inv' — LDDE inverse-sum (Ajello+ 2014, Eq. C.4, BL Lac):
            e = [r^{-p1} + r^{-p2}]^{-1}, r = (1+z)/(1+z_c)
        'sum' — simple sum (legacy):
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

    if evolution_form == 'ldde_inv':
        # Ajello+ (2014) Eq. C.4: smooth double power-law
        # e = [r^{-p1} + r^{-p2}]^{-1}
        e_z = 1.0 / (ratio**(-p1) + ratio**(-p2))
    elif evolution_form == 'sum':
        # Legacy sum form
        e_z = ratio**p1 + ratio**p2
    else:
        # Standard piecewise LDDE (FSRQ)
        if z <= z_c:
            e_z = ratio**p1
        else:
            e_z = ratio**p2

    return max(phi_L * e_z, 0.0)


# ---------------------------------------------------------------------------
# Source-specific GLF functions (LDDE-based: FSRQ, BL Lac only)
# mAGN and SFG are defined above with dedicated conversion chains.
# ---------------------------------------------------------------------------

def _glf_FSRQ(L, z):
    """FSRQ GLF from Ajello et al. (2012)."""
    return _ldde_glf(L, z, _FSRQ_PARAMS, evolution_form='piecewise')


def _glf_BL_Lac(L, z):
    """BL Lac GLF from Ajello et al. (2014), LDDE inverse-sum evolution."""
    return _ldde_glf(L, z, _BL_LAC_PARAMS, evolution_form='ldde_inv')


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

def mean_intensity(E_GeV, source_class, z_max=5.0, n_z=300):
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

    Blazars use fixed halo mass. mAGN and SFG use mass-luminosity relations
    evaluated at characteristic luminosities (Di Mauro Eqs. C.20-C.21, Eq. C.29).
    """
    from . import halo_model as hm

    if source_class in ('BL_Lac', 'FSRQ'):
        return hm.bias(1e13, z)

    if source_class == 'mAGN':
        L_char = 1e44  # characteristic mAGN L_gamma [erg/s]
        M_star = cfg.MAGN_MSTAR_NORM * (L_char / cfg.MAGN_MSTAR_LNORM)**cfg.MAGN_MSTAR_SLOPE
        M_halo = 1e13 * (M_star / (cfg.MAGN_MHALO_PIVOT * (1.0 + z)**cfg.MAGN_MHALO_Z_EXP))**cfg.MAGN_MHALO_SLOPE
        M_halo = max(M_halo, 1e10)
        return hm.bias(M_halo, z)

    if source_class == 'SFG':
        L_char = 1e39  # characteristic SFG L_gamma [erg/s]
        M_halo = cfg.SFG_MHALO_NORM / (1.0 + z)**cfg.SFG_MHALO_Z_EXP * (L_char / cfg.SFG_MHALO_LNORM)**cfg.SFG_MHALO_SLOPE
        M_halo = max(M_halo, 1e10)
        return hm.bias(M_halo, z)

    return hm.bias(1e12, z)
