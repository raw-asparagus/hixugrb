"""Astrophysical gamma-ray source populations.

Implements gamma-ray luminosity functions (GLFs) and window functions
for BL Lacs, FSRQs, misaligned AGN, and star-forming galaxies.

GLF sources:
- BL Lac: Ajello et al. (2014) — LDDE
- FSRQ: Ajello et al. (2012) — LDDE
- mAGN: Di Mauro et al. (2014) — radio LF → gamma conversion chain
- SFG: Gruppioni et al. (2013) + Ackermann et al. (2012) — IR LF → gamma
"""

from functools import lru_cache

import numpy as np

from scipy.integrate import quad

from . import config as cfg
from . import cosmology as cosmo
from . import ebl as ebl_mod

# ---------------------------------------------------------------------------
# Luminosity threshold from Fermi sensitivity
# ---------------------------------------------------------------------------

def L_sens(z, E_GeV=None, alpha=None, F_sens_baseline=None):
    """Energy-luminosity threshold for Fermi-LAT detection at redshift z.

    Converts the integral photon-flux sensitivity F_SENS [cm^{-2} s^{-1}]
    into a rest-frame 0.1–100 GeV energy luminosity [erg/s] so that it can
    be compared directly with the GLF luminosity bounds.

    Following Pinetti (2022) thesis Eqs. 3.75–3.76:

        k_sens = F_SENS / J_alpha_EBL(z)
        L_sens = 4 pi d_L^2 * k_sens * (1+z)^{-(2-alpha)} * I_alpha * GeV_to_erg

    where:
        I_alpha = int_{0.1}^{100} E^{1-alpha} dE  (rest-frame luminosity band)
        J_alpha_EBL(z) = int_1^{100} E^{-alpha} exp(-tau(E, z)) dE
                         (Fermi sensitivity band with EBL; tau at observed energy E)

    The EBL factor in J_alpha accounts for the fact that photons from distant
    sources are absorbed before reaching the detector, raising the effective
    luminosity threshold at high z.

    Parameters
    ----------
    z : float
        Redshift.
    E_GeV : float, optional
        Photon energy [GeV] for energy-dependent sensitivity (data mode).
        If None, uses the constant baseline (forecast mode).
    alpha : float, optional
        Source spectral index for the K-correction.  Required for the
        photon-to-energy luminosity conversion.
    F_sens_baseline : float, optional
        Baseline F_sens value [cm^{-2} s^{-1}] used when E_GeV is None.
        Defaults to ``cfg.F_SENS`` (= cfg.F_SENS_PINETTI = 1e-10).
        Set to ``cfg.F_SENS_4FGL_DR4`` (= 4e-12) for the actually-measured
        4FGL-DR4 high-Galactic-latitude completeness threshold. Also passed
        through to ``F_sens_energy`` when E_GeV is given so the PSF-area
        scaling is anchored to the right baseline.
    """
    dL_Mpc = cosmo.d_L(z) / cfg.h  # physical Mpc
    dL_cm = dL_Mpc * cfg.MPC_TO_M * 100.0  # cm

    if F_sens_baseline is None:
        F_sens_baseline = cfg.F_SENS

    if E_GeV is not None:
        F_sens_E = F_sens_energy(E_GeV, F_sens_baseline=F_sens_baseline)
    else:
        F_sens_E = F_sens_baseline

    L_phot = 4.0 * np.pi * dL_cm**2 * F_sens_E  # [photons/s]

    if alpha is None:
        return L_phot  # legacy fallback (photon luminosity)

    # Convert photon luminosity to energy luminosity [erg/s].
    # I_alpha: rest-frame energy band 0.1–100 GeV (luminosity definition, Eq. 3.67)
    E_min_L, E_max_L = 0.1, 100.0
    # J_alpha: Fermi sensitivity band 1–100 GeV with EBL (Eq. 3.76)
    E_min_F, E_max_F = 1.0, 100.0
    if abs(alpha - 2.0) > 0.01:
        I_alpha = (E_max_L**(2.0 - alpha) - E_min_L**(2.0 - alpha)) / (2.0 - alpha)
    else:
        I_alpha = np.log(E_max_L / E_min_L)

    # J_alpha with EBL attenuation (Eq. 3.76): int E^{-alpha} exp(-tau) dE
    J_alpha = _J_alpha_ebl(z, alpha, E_min_F, E_max_F)

    K = (1.0 + z)**(2.0 - alpha)

    return F_sens_E * 4.0 * np.pi * dL_cm**2 * cfg.GEV_TO_ERG * I_alpha / (K * J_alpha)


def _J_alpha_ebl(z, alpha, E_min, E_max, n_pts=50):
    """Compute J_alpha = int E^{-alpha} exp(-tau(E, z)) dE over [E_min, E_max].

    Uses trapezoidal integration over a log-spaced energy grid.
    At z <= 0 or when EBL is negligible, falls back to the analytic integral.
    """
    if z <= 0:
        # No EBL at z=0
        if abs(alpha - 1.0) > 0.01:
            return (E_max**(1.0 - alpha) - E_min**(1.0 - alpha)) / (1.0 - alpha)
        else:
            return np.log(E_max / E_min)

    E_arr = np.logspace(np.log10(E_min), np.log10(E_max), n_pts)
    atten = ebl_mod.attenuation(E_arr, z)
    integrand = E_arr**(-alpha) * atten
    return np.trapezoid(integrand, E_arr)


def F_sens_energy(E_GeV, F_sens_baseline=None):
    """Energy-dependent Fermi-LAT flux sensitivity [cm^{-2} s^{-1}].

    Scales the reference baseline by the PSF solid-angle ratio (Ammazzalorso,
    Fornengo, Horiuchi & Regis 2018, arXiv:1808.09225, Sec. II.A — see
    docs/literature/ammazzalorso2018b_fermi_2mpz.md):

        F_sens(E) = F_sens_baseline * [sigma_0(E) / sigma_0(E_ref)]^2

    At low energies (poor PSF), fewer sources are resolved → higher threshold.
    At high energies (good PSF), more sources are resolved → lower threshold.

    Reference energy E_ref = 5 GeV chosen near Fermi's optimal sensitivity.

    Parameters
    ----------
    E_GeV : float
        Photon energy [GeV].
    F_sens_baseline : float, optional
        Baseline F_sens value [cm^{-2} s^{-1}] at E_ref. Defaults to
        ``cfg.F_SENS`` (= cfg.F_SENS_PINETTI = 1e-10). Set to
        ``cfg.F_SENS_4FGL_DR4`` (= 4e-12) for the actually-measured 4FGL-DR4
        14-year high-Galactic-latitude completeness threshold.
    """
    from . import noise_model as nm
    if F_sens_baseline is None:
        F_sens_baseline = cfg.F_SENS
    E_ref = 5.0  # GeV — near Fermi's optimal sensitivity
    sigma_E = nm.sigma_psf_fermi(E_GeV)
    sigma_ref = nm.sigma_psf_fermi(E_ref)
    return F_sens_baseline * (sigma_E / sigma_ref)**2


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

    Returns dPhi/d(log10 L_151) [Mpc^{-3}] in the Willott Model C cosmology
    (H0=50 km/s/Mpc, Omega_M=0, Omega_Lambda=0).

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


def _willott_volume_correction(z):
    """Comoving-volume ratio eta(z) = [d^2V_W/dz/dOmega] / [d^2V/dz/dOmega].

    Uses the Willott et al. (2001) Table 1 Model C background adopted by
    Di Mauro et al. (2014): H0_W = 50 km/s/Mpc, Omega_M = 0, Omega_Lambda = 0.
    In that empty/open cosmology the comoving volume element per steradian is

        d^2V_W / dz dOmega = c^3 z^2 (2 + z)^2 / [4 H0_W^3 (1 + z)^3]

    (Di Mauro et al. 2014 Eq. 18). The Planck-path volume element is computed
    from the repository cosmology via d^2V/dz/dOmega = c * d_L^2 / [H(z)(1+z)^2].
    """
    if z <= 0:
        return 1.0

    # Willott Model C / Di Mauro Eq. 18 volume element [Mpc^3 sr^-1].
    dV_W = (
        cfg.C_LIGHT_KM_S**3
        * z**2
        * (2.0 + z)**2
        / (4.0 * cfg.H0_WILLOTT**3 * (1.0 + z)**3)
    )

    # Repository Planck cosmology volume element [Mpc^3 sr^-1].
    dL = cosmo.d_L(z) / cfg.h  # physical Mpc
    H_pipeline = cosmo.H(z)    # [km/s/Mpc]
    dV = cfg.C_LIGHT_KM_S * dL**2 / (H_pipeline * (1.0 + z)**2)

    if dV <= 0 or dV_W <= 0:
        return 1.0

    return dV_W / dV


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

    Converts the Willott (2001) 151 MHz radio luminosity function into a
    gamma-ray luminosity function via the radio→gamma chain:
        L_gamma → L_core^{5GHz} → L_tot^{1.4GHz} → L_tot^{151MHz} → Willott RLF

    Includes the K-correction factor (1+z)^{-(2-Gamma)} from Pinetti (2022)
    Eq. C.19 / Di Mauro+ (2014), which accounts for the redshift-dependent
    mapping between observed-frame photon flux and rest-frame luminosity.

    Returns dPhi/dL_gamma [Mpc^{-3} (erg/s)^{-1}].
    """
    if L <= 0 or z < 0:
        return 0.0

    L_151, dL151_dLgamma = _L151_from_Lgamma(L)

    if L_151 <= 0:
        return 0.0

    rho_r = _willott_rlf(L_151, z)  # dPhi/d(log10 L) in Willott cosmology
    eta = _willott_volume_correction(z)

    # K-correction: (1+z)^{-(2-Gamma)} per Pinetti (2022) Eq. C.19
    alpha = cfg.ASTRO_SOURCES['mAGN']['alpha']
    K_corr = (1.0 + z)**(-(2.0 - alpha))

    dPhi_dL151 = rho_r / (np.log(10.0) * L_151)
    phi_gamma = (cfg.DIMAURO_K * eta * K_corr
                 * dPhi_dL151 * abs(dL151_dLgamma))

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

    # Luminosity evolution L_0(z)
    # Spiral: break at z=1.1, frozen above (kL,2=0.00 in Gruppioni Table 8)
    # Starburst, SF-AGN: single power law, no break (Table 8 has no kL,2/zb,L)
    if comp_name == 'spiral':
        if z <= 1.1:
            L_0 = L_star * ((1.0 + z) / 1.15)**k_L
        else:
            L_0 = L_star * (2.1 / 1.15)**k_L  # frozen above z=1.1
    else:
        L_0 = L_star * ((1.0 + z) / 1.15)**k_L  # continues at all z

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
        'ldde_inv' — LDDE inverse-sum (Ajello+ 2012 Eq. 15, 2014 Eq. 18):
            e = [r^{-p1} + r^{-p2}]^{-1}, r = (1+z)/(1+z_c)
            Low-z rise ~ r^{p1}, high-z decline ~ r^{p2}.
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
        # Smooth inverse-sum evolution from Ajello+ (2012) Eq. 15 /
        # Ajello+ (2014) Eq. 18 / Pinetti (2022) Eq. C.4:
        #   e = [r^{-p1} + r^{-p2}]^{-1},  r = (1+z)/(1+z_c)
        #
        # At low z (r << 1):  e ~ r^{p1}  (rises as (1+z)^{p1})
        # At high z (r >> 1): e ~ r^{p2}  (falls as (1+z)^{p2})
        # At z = z_c (r = 1): e = 0.5
        #
        # For BL Lac: p1=4.50 (moderate rise), p2=-12.88 (steep decline).
        # For FSRQ:  p1=7.35 (steep rise), p2=-6.51 (moderate decline).
        e_z = 1.0 / (ratio**(-p1) + ratio**(-p2))
    elif evolution_form == 'piecewise':
        # Piecewise LDDE (legacy, retained for comparison only)
        if z <= z_c:
            e_z = ratio**p1
        else:
            e_z = ratio**p2
    elif evolution_form == 'sum':
        # Legacy sum form
        e_z = ratio**p1 + ratio**p2
    else:
        raise ValueError(f"Unknown evolution_form: {evolution_form}")

    return max(phi_L * e_z, 0.0)


# ---------------------------------------------------------------------------
# Source-specific GLF functions (LDDE-based: FSRQ, BL Lac only)
# mAGN and SFG are defined above with dedicated conversion chains.
# ---------------------------------------------------------------------------

def _glf_FSRQ(L, z):
    """FSRQ GLF from Ajello et al. (2012), LDDE inverse-sum evolution.

    Both Ajello+ (2012) Eq. 15 and Pinetti (2022) Eq. C.4 use the smooth
    inverse-sum form (continuous around the redshift peak), not piecewise.
    """
    return _ldde_glf(L, z, _FSRQ_PARAMS, evolution_form='ldde_inv')


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

def W_gamma_astro(E_GeV, z, source_class, unresolved_only=True,
                  unresolved_mode='pinetti_constant'):
    """Astrophysical gamma-ray window function per comoving distance (Pinetti Eq. 4.3).

    Per-chi convention: W(chi) is returned in the pipeline's h-dependent
    comoving units [photons s^-1 sr^-1 GeV^-1 (Mpc/h)^-3].

    The luminosity functions in this module are defined in physical
    [Mpc^-3 (erg/s)^-1], so the final emissivity is converted to
    [(Mpc/h)^-3] before returning.

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
    unresolved_mode : str
        Controls how the unresolved threshold is computed (only used when
        unresolved_only=True). The pipeline ships with two canonical modes
        plus two legacy aliases:

        - ``'pinetti_constant'`` (alias ``'forecast'``): constant F_sens
          = ``cfg.F_SENS_PINETTI`` = 1e-10 cm^{-2} s^{-1}, the conservative
          early-Fermi 1FGL/2FGL completeness limit assumed by Pinetti+2020/2022.
          Used by the legacy MeerKAT/SKA1/SKA2 forecast entries for
          apples-to-apples comparison against Pinetti+2020 Table 4.

        - ``'4fgl_dr4_psf'`` (alias ``'data'``): the Ammazzalorso, Fornengo,
          Horiuchi & Regis (2018, arXiv:1808.09225) PSF-area scaling
          ``F_sens(E) = F_baseline * [sigma_0(E)/sigma_0(E_ref)]^2`` anchored
          at the 4FGL-DR4 14-year high-Galactic-latitude completeness
          threshold ``cfg.F_SENS_4FGL_DR4 = 7.3e-11 cm^-2 s^-1`` (1-100 GeV
          source-class average; converted from the directly-quoted
          ``cfg.F_SENS_4FGL_DR4_ERG_CGS = 1e-12 erg cm^-2 s^-1`` in the
          100 MeV - 100 GeV band, Ballet et al. 2023 §5/p12, arXiv:2307.12546;
          see docs/literature/ballet2023_4fgl_dr4.md). The 4FGL-DR4 baseline
          is only ~0.73x Pinetti's value (NOT 25x lower); with the PSF
          scaling on top, low-energy bins are additionally conservative
          due to PSF degradation. Used by the new ``MeerKLASS_*`` canonical
          entries.
    """
    return _W_gamma_astro_impl(float(E_GeV), float(z), source_class,
                               unresolved_only, unresolved_mode)


@lru_cache(maxsize=16384)
def _W_gamma_astro_impl(E_GeV, z, source_class, unresolved_only, unresolved_mode):
    """Core implementation of W_gamma_astro.

    Item 2.1 of clever-beaming-creek plan: in-memory lru_cache keyed on the
    five hashable scalars (E_GeV, z, source_class, unresolved_only, unresolved_mode).
    Cache is reset on every Python process start. Caveat: if `cfg` astro-source
    parameters or `cfg.F_SENS` are mutated at runtime, the cache becomes stale —
    callers should not mutate the config dict.
    """
    if z <= 0:
        return 0.0

    params = cfg.ASTRO_SOURCES[source_class]
    alpha = params['alpha']
    L_min = params['L_min']
    L_max = params['L_max']

    if unresolved_only:
        # Dispatch on unresolved_mode (see W_gamma_astro docstring for the
        # full mode list and per-mode rationale).
        if unresolved_mode in ('4fgl_dr4_psf', 'data'):
            # 4FGL-DR4 baseline + Ammazzalorso+2018b PSF-area scaling
            L_thr = L_sens(z, E_GeV=E_GeV, alpha=alpha,
                           F_sens_baseline=cfg.F_SENS_4FGL_DR4)
        elif unresolved_mode in ('pinetti_constant', 'forecast'):
            # Pinetti+2020/2022 constant baseline
            L_thr = L_sens(z, alpha=alpha,
                           F_sens_baseline=cfg.F_SENS_PINETTI)
        else:
            raise ValueError(
                f"unresolved_mode must be 'pinetti_constant' or '4fgl_dr4_psf' "
                f"(got {unresolved_mode!r})"
            )
        L_up = min(L_max, L_thr)
    else:
        L_up = L_max

    if L_up <= L_min:
        return 0.0

    # Compute the physical comoving emissivity j(E_rest, z)
    # [ph s^{-1} Mpc^{-3} GeV^{-1} sr^{-1}].
    #
    # Each source emits: dn/dE_rest = L / (GeV_to_erg * I_alpha) * E_rest^{-alpha}  [ph/s/GeV]
    # where L [erg/s] is the rest-frame 0.1-100 GeV energy luminosity.
    #
    # The emissivity is: j = (1/4pi) integral phi(L) * dn/dE_rest dL
    E_min_band = 0.1     # 100 MeV [GeV]
    E_max_band = 100.0   # 100 GeV [GeV]
    GeV_to_erg = cfg.GEV_TO_ERG

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
    # [Mpc^{-3} (erg/s)^{-1}] * [ph s^{-1} GeV^{-1}] * [erg/s]
    # = [Mpc^{-3} ph s^{-1} GeV^{-1}]
    #
    # Per-chi photon intensity window from a population of sources at comoving
    # distance chi: the photon-number flux from each source is
    #   dF_ph/dE_obs = (1+z)^2/(4 pi d_L^2) * dN/dE_em|_{E_em=(1+z)E_obs}
    # (Hogg 1999 "Distance measures" Sec. 4). Integrating over sources in the
    # shell chi^2 dchi per steradian, and using d_L^2 = chi^2 (1+z)^2, the
    # (1+z)^2 from the K-correction cancels the (1+z)^2 in d_L^2, leaving
    #   W^(chi) = (1/(4pi)) * integral phi(L) * dN/dE_em((1+z)E_obs) dL
    # with NO (1+z)^{-2} prefactor. The K-correction enters naturally through
    # E_rest = (1+z)*E_obs in the spectral factor. See Ando & Komatsu 2006
    # (PRD 73:023521) Eqs. 1-3 and Ando & Pavlidou 2009 (MNRAS 400:2122) Eq. 6.
    #
    # EBL attenuation at observed energy (same convention as W_gamma_DM)
    atten = ebl_mod.attenuation(np.atleast_1d(E_GeV), z)[0]

    # Convert the GLF/emissivity density from physical [Mpc^-3] to the
    # pipeline's h-dependent [(Mpc/h)^-3] convention so the Limber integral and
    # gamma-noise model share the same area/volume basis.
    return val / (4.0 * np.pi * cfg.h**3) * atten


# ---------------------------------------------------------------------------
# Mean unresolved gamma-ray intensity (for Figure 2 validation)
# ---------------------------------------------------------------------------

def mean_intensity(E_GeV, source_class, z_max=2.5, n_z=300):
    """Mean unresolved gamma-ray intensity from a source class.

    <I>(E) = integral dz (c*h/H(z)) * W_gamma_astro(E, z)

    where W_gamma_astro is the h-dependent per-chi window returned in
    [(Mpc/h)^-3]. The observed-energy dependence already enters through
    E_rest = (1+z) * E_obs inside W_gamma_astro, so no extra /(1+z) factor is
    applied here.

    Returns intensity in [photons cm^{-2} s^{-1} GeV^{-1} sr^{-1}].
    """
    z_arr = np.linspace(0.01, z_max, n_z)
    W_arr = np.array([W_gamma_astro(E_GeV, z, source_class) for z in z_arr])

    # Item 1.4: vectorised over z_arr
    H_arr = cosmo.H(np.asarray(z_arr, dtype=float))
    dchi_dz = cfg.C_LIGHT_KM_S * cfg.h / H_arr  # [Mpc/h]
    Mpc_h_cm = cfg.MPC_TO_M * 100.0 / cfg.h     # [cm / (Mpc/h)]

    # W_arr * dchi/dz gives an intensity in [(Mpc/h)^-2]. Convert the final
    # area unit to cm^-2 at the module boundary.
    integrand = W_arr * dchi_dz / Mpc_h_cm**2

    dz = z_arr[1] - z_arr[0]
    return np.sum(integrand) * dz


# ---------------------------------------------------------------------------
# Effective bias for astrophysical sources
# ---------------------------------------------------------------------------

def bias_astro(z, source_class):
    """Effective linear bias for an astrophysical source class.

    Blazars use fixed halo mass. mAGN and SFG use mass-luminosity relations
    evaluated at characteristic luminosities (Di Mauro Eqs. C.20-C.21, Eq. C.29).
    Those literature relations are written in physical M_sun, so masses are
    converted to the code's M_sun/h convention before calling hm.bias().
    """
    from . import halo_model as hm

    if source_class in ('BL_Lac', 'FSRQ'):
        return hm.bias(1e13, z)

    if source_class == 'mAGN':
        L_char = 1e44  # characteristic mAGN L_gamma [erg/s]
        M_star = cfg.MAGN_MSTAR_NORM * (L_char / cfg.MAGN_MSTAR_LNORM)**cfg.MAGN_MSTAR_SLOPE
        M_halo_phys = 1e13 * (
            M_star / (cfg.MAGN_MHALO_PIVOT * (1.0 + z)**cfg.MAGN_MHALO_Z_EXP)
        )**cfg.MAGN_MHALO_SLOPE
        M_halo_phys = max(M_halo_phys, 1e10)
        return hm.bias(M_halo_phys / cfg.h, z)

    if source_class == 'SFG':
        L_char = 1e39  # characteristic SFG L_gamma [erg/s]
        M_halo_phys = (
            cfg.SFG_MHALO_NORM
            / (1.0 + z)**cfg.SFG_MHALO_Z_EXP
            * (L_char / cfg.SFG_MHALO_LNORM)**cfg.SFG_MHALO_SLOPE
        )
        M_halo_phys = max(M_halo_phys, 1e10)
        return hm.bias(M_halo_phys / cfg.h, z)

    return hm.bias(1e12, z)
