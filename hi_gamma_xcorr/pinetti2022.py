"""Pinetti (2022) thesis-faithful parameter overrides and window functions.

Provides a parallel implementation of key pipeline quantities using the
specific model choices from the PhD thesis "From gamma rays to radio waves:
Dark Matter searches across the spectrum" by Elena Pinetti (2022,
arXiv:2212.00125).

This module imports from the pipeline but never modifies it. Consumers call
these functions explicitly (e.g., pinetti2022.W_HI_pinetti()) to get
thesis-faithful values for comparison or validation.

Known limitations:
- Mass function dn/dM uses the pipeline's hmf backend (q=0.707 internally).
  The q=0.75 override enters only through the bias formula, not the mass
  function itself. This is a ~5% effect on mass function tails.
- PPPC4DMID public tables are used (private Pythia code unavailable).
- SFG SF-AGN k_R2 uses -3.17 (matching pipeline + original Gruppioni 2013),
  not +3.17 (thesis Table C.2 typo).
"""

import numpy as np
from scipy.integrate import quad

from . import config as cfg
from . import cosmology as cosmo
from . import halo_model as hm
from . import hmf_interface as hmfi
from . import hi_model as hi

# ---------------------------------------------------------------------------
# Thesis-specific constants
# ---------------------------------------------------------------------------

PINETTI_Q = 0.75               # Sheth & Tormen (2002) q parameter
PINETTI_P = 0.3                # Same as pipeline
PINETTI_OMEGA_HI = 2.45e-4     # Fixed Omega_HI (thesis p.122)
PINETTI_T_B_MK = 0.044         # 44 muK = 0.044 mK (thesis brightness temp)

# Thesis Correa coefficients (Eq. 3.36, p.99) — different cosmology fit
# from the same Correa et al. (2015) paper vs pipeline's Planck Appendix B1.
CORREA_THESIS_ALPHA_Z0 = 1.6280
CORREA_THESIS_ALPHA_Z1 = -0.2514
CORREA_THESIS_ALPHA_Z2 = 0.01825
CORREA_THESIS_BETA_Z0 = 1.6610
CORREA_THESIS_BETA_Z1 = -0.00495
CORREA_THESIS_BETA_Z2 = -1.6580
CORREA_THESIS_BETA_ZEXP = 0.02804
CORREA_THESIS_GAMMA_Z0 = -0.02002
CORREA_THESIS_GAMMA_Z1 = 0.01072
CORREA_THESIS_GAMMA_ZEXP = -0.3544


# ---------------------------------------------------------------------------
# Halo model overrides
# ---------------------------------------------------------------------------

def concentration_correa_thesis(M, z):
    """Correa c_200(M, z) with thesis-specific coefficients (Eq. 3.36, p.99).

    Same functional form as pipeline's concentration_correa, but with
    different fitting coefficients from a different cosmology within
    Correa et al. (2015).
    """
    M = np.asarray(M, dtype=float)
    z = float(z)
    log_M = np.log10(np.clip(M / cfg.h, 1e-2, 1e16))  # M_sun/h -> M_sun: M_phys = M_code / h

    if z <= 4:
        zp1 = 1.0 + z
        alpha = (CORREA_THESIS_ALPHA_Z0 + CORREA_THESIS_ALPHA_Z1 * zp1
                 + CORREA_THESIS_ALPHA_Z2 * zp1**2)
        beta = (CORREA_THESIS_BETA_Z0 + CORREA_THESIS_BETA_Z1 * zp1
                + CORREA_THESIS_BETA_Z2 * zp1**CORREA_THESIS_BETA_ZEXP)
        gamma = (CORREA_THESIS_GAMMA_Z0
                 + CORREA_THESIS_GAMMA_Z1 * zp1**CORREA_THESIS_GAMMA_ZEXP)
        log_c = alpha + beta * log_M * (1.0 + gamma * log_M**2)
    else:
        zp1 = 1.0 + z
        alpha = 1.3081 - 0.1078 * zp1 + 0.00398 * zp1**2
        beta = 0.0223 - 0.0944 * zp1**(-0.3907)
        log_c = alpha + beta * log_M

    return np.maximum(10.0**log_c, 1.0)


def bias_pinetti(M, z):
    """Sheth-Tormen halo bias with q=0.75 (thesis Eq. 3.51, p.102).

    Uses the same functional form as the pipeline but with q=0.75
    instead of q=0.707.
    """
    nu_val = hmfi.nu(M, z)
    q, p = PINETTI_Q, PINETTI_P
    return 1.0 + (q * nu_val - 1.0) / cfg.DELTA_C + \
        2.0 * p / (cfg.DELTA_C * (1.0 + (q * nu_val)**p))


def limber_k(ell, chi):
    """Thesis Limber k-substitution: k = ell/chi (no half-integer correction).

    The pipeline uses k = (ell + 0.5) / chi (LoVerde & Afshordi 2008).
    The thesis uses the standard k = ell / chi.
    """
    return ell / chi


# ---------------------------------------------------------------------------
# HI overrides
# ---------------------------------------------------------------------------

def T_bar_b_thesis(z):
    """Brightness temperature using thesis pre-evaluated form (p.122).

    T_b = 44 muK * (1+z)^2 / E(z)

    This assumes fixed Omega_HI = 2.45e-4 pre-substituted into the
    standard formula T_b = 188*h*Omega_HI*(1+z)^2/E(z).
    """
    return PINETTI_T_B_MK * (1.0 + z)**2 / cosmo.E(z)


def b_HI_pinetti(z, M_min=None, M_max=None):
    """HI bias using thesis bias formula (q=0.75).

    Same integral as pipeline's b_HI but with bias_pinetti() instead of
    hm.bias(). Uses the pipeline's dn/dM and M_HI (which are shared).
    """
    if M_min is None:
        M_min = cfg.M_MIN_HI
    if M_max is None:
        M_max = cfg.M_MAX_HI

    rho = hi.rho_HI_mean(z, M_min=M_min, M_max=M_max)
    if rho <= 0:
        return 0.0

    def integrand(lnM):
        M = np.exp(lnM)
        return hm.dndM(M, z) * hi.M_HI(M, z) * bias_pinetti(M, z) * M

    val, _ = quad(integrand, np.log(M_min), np.log(M_max),
                  limit=200, epsrel=1e-5)
    return val / rho


def W_HI_pinetti(z, z_min, z_max):
    """HI window function faithful to Pinetti (2022) thesis.

    Uses:
    - T_b: 44 muK pre-evaluated (fixed Omega_HI = 2.45e-4)
    - b_HI: q=0.75 bias
    - phi(z) = 1/(z_max - z_min) top-hat selection
    - H(z)/(c*h) per-chi Jacobian (same as pipeline)
    """
    if z < z_min or z > z_max:
        return 0.0
    T_b = T_bar_b_thesis(z)
    b = b_HI_pinetti(z)
    phi = 1.0 / (z_max - z_min)
    H_over_ch = cosmo.H(z) / (cfg.C_LIGHT_KM_S * cfg.h)
    return T_b * b * phi * H_over_ch


# ---------------------------------------------------------------------------
# Programmatic deviation registry
# ---------------------------------------------------------------------------

DEVIATIONS = {
    'smt_q': {
        'pipeline': cfg.SMT_Q,
        'pinetti': PINETTI_Q,
        'description': 'SMT mass function / bias q parameter',
        'affects': ['bias', 'hmf (bias only; dn/dM still uses pipeline q)'],
        'severity': 'Minor (~5% on mass function tails)',
    },
    'omega_hi': {
        'pipeline': 'computed from halo integral (z-dependent)',
        'pinetti': PINETTI_OMEGA_HI,
        'description': 'HI density parameter treatment',
        'affects': ['T_bar_b', 'W_HI'],
        'severity': 'Minor (few-percent in T_b)',
    },
    'correa_coeffs': {
        'pipeline': 'Planck Appendix B1 fit',
        'pinetti': 'thesis Eq. 3.36 fit',
        'description': 'Correa c(M,z) fitting coefficients',
        'affects': ['c_200 (DM NFW concentration)'],
        'severity': 'Minor (DM cross-power only)',
    },
    'limber_k': {
        'pipeline': '(ell + 0.5) / chi',
        'pinetti': 'ell / chi',
        'description': 'Limber k-substitution',
        'affects': ['C_ell at low ell'],
        'severity': 'Negligible (~5% at ell=10)',
    },
    'T_b_form': {
        'pipeline': '188*h*Omega_HI(z)*(1+z)^2/E(z) mK',
        'pinetti': '0.044*(1+z)^2/E(z) mK (44 muK pre-evaluated)',
        'description': 'Brightness temperature formula',
        'affects': ['W_HI'],
        'severity': 'Negligible (equivalent modulo Omega_HI treatment)',
    },
    'pppc4dmid': {
        'pipeline': 'PPPC4DMID public tables (Cirelli+ 2011)',
        'pinetti': 'private Pythia code (unavailable; using public tables)',
        'description': 'DM annihilation photon spectra',
        'affects': ['W_gamma_DM'],
        'severity': 'Low (percent-level, irreducible)',
    },
    'sfg_kr2_sign': {
        'pipeline': '-3.17 (Gruppioni+ 2013 original)',
        'pinetti': '-3.17 (thesis Table C.2 has typo +3.17; we follow original)',
        'description': 'SFG SF-AGN density evolution parameter k_R2',
        'affects': ['SFG GLF at z > 1.1'],
        'severity': 'Medium (thesis typo; both implementations use correct value)',
    },
}
