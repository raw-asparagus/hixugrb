"""Angular power spectrum computation via Limber integration.

Computes C_l^{ij} for all cross-correlations between HI and gamma-ray sources.
"""

from functools import lru_cache

import numpy as np

from . import config as cfg
from . import cosmology as cosmo
from . import halo_model as hm
from . import hi_model as hi
from . import dm_model as dm
from . import astro_sources as astro
from .cache import _register_lru

# ---------------------------------------------------------------------------
# HI × DM 3D cross-power spectra (Eqs. 5.1–5.2)
# ---------------------------------------------------------------------------

def P_HI_DM_2h(k, z, n_M=120, hi_brightness=cfg.HiBrightness.PADMANABHAN):
    """Two-halo HI x DM cross-power spectrum [(Mpc/h)^3].

    Halo integral for Padmanabhan/fixed_omega; linear-bias polynomial for
    Cunnington mode. The DM kernel I_DM is mode-independent.
    """
    k = np.atleast_1d(np.asarray(k, dtype=float))
    hi_brightness = cfg.HiBrightness(hi_brightness)
    Delta2 = dm.clumping_factor(z)

    # DM bias-weighted rho^2 profile integral (unique to this function)
    M_min = max(cfg.M_MIN_HI, 1e8)
    M_max = min(cfg.M_MAX_HI, 1e16)
    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    I_DM = np.zeros_like(k)
    for M in M_arr:
        dn = hm.dndM(M, z)
        b = hm.bias(M, z)
        vt = dm.v_tilde(k, M, z)
        I_DM += dn * b * vt / Delta2 * M
    dlnM = np.log(M_arr[1] / M_arr[0])
    I_DM *= dlnM

    # HI bias integral — shared kernel (see hi.I_HI_2h)
    if hi_brightness is cfg.HiBrightness.CUNNINGTON:
        b_hi = float(hi.b_HI_cunnington(float(z)))
        return I_DM * b_hi * cosmo.P_lin(k, z)

    I_HI = hi.I_HI_2h(k, z, n_M=n_M)
    return I_DM * I_HI * cosmo.P_lin(k, z)


# ---------------------------------------------------------------------------
# HI × Astrophysical source 3D cross-power spectra (Eqs. 5.3–5.4)
# ---------------------------------------------------------------------------

def P_HI_astro_2h(k, z, source_class, n_M=120,
                   hi_brightness=cfg.HiBrightness.PADMANABHAN):
    """Two-halo HI x astrophysical source cross-power spectrum.

    Halo integral for Padmanabhan/fixed_omega; linear-bias polynomial for
    Cunnington mode.
    """
    k = np.atleast_1d(np.asarray(k, dtype=float))
    hi_brightness = cfg.HiBrightness(hi_brightness)

    # Astrophysical source bias (independent of HI mode)
    b_astro = astro.bias_astro(z, source_class)

    if hi_brightness is cfg.HiBrightness.CUNNINGTON:
        b_hi = float(hi.b_HI_cunnington(float(z)))
        return b_hi * b_astro * cosmo.P_lin(k, z)

    I_HI = hi.I_HI_2h(k, z, n_M=n_M)
    return I_HI * b_astro * cosmo.P_lin(k, z)


# ---------------------------------------------------------------------------
# Limber integration engine
# ---------------------------------------------------------------------------

def C_ell_HI_gamma(ell, E_GeV, z_min, z_max, telescope, band_name,
                   m_chi_GeV=100.0, sigma_v=None, channel='bb',
                   source_classes=None, include_DM=True,
                   n_z=200, n_k_M=100, hi_brightness=cfg.HiBrightness.PADMANABHAN):
    """Compute C_l^{HI x gamma} via Limber integration at a single energy.

    Thin wrapper around ``C_ell_HI_gamma_multi_E`` with a single-element
    energy array. See that function for full documentation.
    """
    results = C_ell_HI_gamma_multi_E(
        ell, [E_GeV], z_min, z_max, telescope, band_name,
        m_chi_GeV=m_chi_GeV, sigma_v=sigma_v, channel=channel,
        source_classes=source_classes, include_DM=include_DM,
        n_z=n_z, n_k_M=n_k_M, hi_brightness=hi_brightness,
    )
    return results[0]


# ---------------------------------------------------------------------------
# Multi-energy Limber driver — Item 3.1 of clever-beaming-creek plan
# ---------------------------------------------------------------------------

def C_ell_HI_gamma_multi_E(ell, E_arr, z_min, z_max, telescope, band_name,
                           m_chi_GeV=100.0, sigma_v=None, channel='bb',
                           source_classes=None, include_DM=True,
                           n_z=200, n_k_M=100, hi_brightness=cfg.HiBrightness.PADMANABHAN,
                           unresolved_mode=cfg.UnresolvedMode.PINETTI_CONSTANT):
    """Multi-energy Limber driver: computes ``C_ell_HI_gamma`` for each energy
    in ``E_arr`` while doing the redshift loop only once.

    The Limber kernel ``(chi, H, dchi/dz, W_HI, k_arr, P_HI_DM_2h, P_HI_astro_2h)``
    depends on ``(z, ell, telescope, band, hi_brightness)`` but **not** on the
    photon energy. Only the gamma-ray windows ``W_gamma_astro(E, z, src)`` and
    ``W_gamma_DM(E, z, m_chi, ...)`` vary with energy. By looping over redshift
    once and varying only the gamma-ray window in the inner energy loop, we
    avoid recomputing the (very expensive) halo-integral cross-power kernel
    once per energy bin.

    The per-energy result is mathematically identical to calling
    ``C_ell_HI_gamma`` once per energy, modulo floating-point accumulation order
    (rel-tol < 1e-13 typical).

    Parameters
    ----------
    ell : array
        Multipoles. Same `ell` array is used for every energy.
    E_arr : array
        Photon energies [GeV]. One Limber output per element.
    unresolved_mode : str
        Source-completeness threshold convention passed to
        ``astro.W_gamma_astro``. Default ``'pinetti_constant'`` matches the
        legacy Pinetti+2020/2022 forecast convention; use ``'4fgl_dr4_psf'``
        for the actually-measured 4FGL-DR4 baseline + Ammazzalorso+2018b
        PSF-area scaling. ``compute_SNR`` reads the canonical value from
        ``cfg.RADIO_TELESCOPES[telescope]['default_unresolved_mode']``.
    Other parameters: see ``C_ell_HI_gamma``.

    Returns
    -------
    results : list of dict
        ``results[i]`` is the same dict ``C_ell_HI_gamma`` would have returned
        for ``E_GeV = E_arr[i]``: keys ``'total'``, ``'DM'`` (if include_DM),
        ``'BL_Lac'``, ``'FSRQ'``, ``'mAGN'``, ``'SFG'`` (subset by source_classes).
    """
    if source_classes is None:
        source_classes = ['BL_Lac', 'FSRQ', 'mAGN', 'SFG']

    ell = np.atleast_1d(np.asarray(ell, dtype=float))
    E_arr = np.atleast_1d(np.asarray(E_arr, dtype=float))
    n_E = len(E_arr)

    z_arr = np.linspace(max(z_min, 0.01), z_max, n_z)
    dz = z_arr[1] - z_arr[0]

    # One result dict per energy
    results = []
    for _ in range(n_E):
        r = {src: np.zeros_like(ell) for src in source_classes}
        if include_DM:
            r['DM'] = np.zeros_like(ell)
        results.append(r)

    for z in z_arr:
        # ----- E-independent Limber kernel -----
        chi_z = cosmo.chi(z)  # Mpc/h
        H_z = cosmo.H(z)
        dchi_dz = cfg.C_LIGHT_KM_S / H_z * cfg.h

        W_hi = hi.W_HI(z, z_min, z_max, hi_brightness=hi_brightness)  # mK
        if W_hi <= 0:
            continue

        k_arr = (ell + 0.5) / chi_z
        weight = dchi_dz / chi_z**2 * dz

        # Per-source 2-halo cross-power (E-independent — depends only on z, k, hi_brightness)
        P_cross_by_src = {}
        for src in source_classes:
            P_cross_by_src[src] = P_HI_astro_2h(k_arr, z, src, n_M=n_k_M,
                                                hi_brightness=hi_brightness)

        # DM 2-halo cross-power (E-independent)
        if include_DM:
            P_dm = P_HI_DM_2h(k_arr, z, n_M=n_k_M, hi_brightness=hi_brightness)
        else:
            P_dm = None

        # ----- E-dependent inner loop -----
        for iE, E_GeV in enumerate(E_arr):
            E_GeV = float(E_GeV)
            r = results[iE]

            # Astrophysical contributions
            for src in source_classes:
                W_gamma = astro.W_gamma_astro(E_GeV, z, src,
                                              unresolved_mode=unresolved_mode)
                if W_gamma <= 0:
                    continue
                r[src] += W_hi * W_gamma * P_cross_by_src[src] * weight

            # DM contribution
            if include_DM:
                W_dm = dm.W_gamma_DM(E_GeV, z, m_chi_GeV, sigma_v, channel)
                if W_dm > 0:
                    r['DM'] += W_hi * W_dm * P_dm * weight

    # Total per energy
    for r in results:
        r['total'] = sum(r[k] for k in r)

    return results


# ---------------------------------------------------------------------------
# HI auto-power C_l^{HI,HI} (needed for noise/variance computation)
# ---------------------------------------------------------------------------

def C_ell_HI_auto(ell, z_min, z_max, n_z=200, n_M=100,
                  hi_brightness=cfg.HiBrightness.PADMANABHAN):
    """HI auto-correlation angular power spectrum C_l^{HI,HI}.

    Uses only the 2-halo term for efficiency. Cached so that compute_SNR
    and delta_chi2 (which call with identical arguments) share the result.
    """
    ell = np.atleast_1d(np.asarray(ell, dtype=float))
    hi_brightness = cfg.HiBrightness(hi_brightness)
    ell_key = tuple(ell.tolist())
    return _C_ell_HI_auto_cached(
        ell_key, float(z_min), float(z_max), n_z, n_M, hi_brightness
    ).copy()


@_register_lru
@lru_cache(maxsize=16)
def _C_ell_HI_auto_cached(ell_key, z_min, z_max, n_z, n_M, hi_brightness):
    """Cached core of C_ell_HI_auto."""
    ell = np.asarray(ell_key)
    z_arr = np.linspace(max(z_min, 0.01), z_max, n_z)
    dz = z_arr[1] - z_arr[0]

    result = np.zeros_like(ell)

    for z in z_arr:
        chi_z = cosmo.chi(z)
        H_z = cosmo.H(z)
        dchi_dz = cfg.C_LIGHT_KM_S / H_z * cfg.h

        W_hi = hi.W_HI(z, z_min, z_max, hi_brightness=hi_brightness)
        if W_hi <= 0:
            continue

        k_arr = (ell + 0.5) / chi_z
        weight = dchi_dz / chi_z**2 * dz

        P_hi = hi.P_HI_2h(k_arr, z, n_M=n_M, hi_brightness=hi_brightness)
        result += W_hi**2 * P_hi * weight

    return result


# ---------------------------------------------------------------------------
# Normalized window functions for plotting
# ---------------------------------------------------------------------------

_Z_NORM_MAX = 4.0    # normalization integral upper limit
_N_Z_NORM = 400      # number of points for normalization grid


def normalized_windows(z_arr, E_GeV=5.0, m_chi_GeV=100.0, sigma_v=None,
                       channel='bb', source_classes=None,
                       z_min_hi=None, z_max_hi=None,
                       unresolved_only=True, include_DM=True,
                       z_norm_max=None, hi_brightness=cfg.HiBrightness.PADMANABHAN):
    r"""Compute uniformly normalized window functions for all tracers.

    Returns $\hat{W}_i(z) = \frac{c\,h}{H(z)} \frac{W_i^{(\chi)}(z)}{\langle I_i \rangle}$

    for each tracer i. Windows are evaluated on ``z_arr`` but normalized by
    integrating over ``[0, z_norm_max]`` (default 4.0) so that the shape is
    independent of the plotting range.

    Parameters
    ----------
    z_arr : array
        Redshift grid for evaluation (plot range).
    E_GeV : float
        Gamma-ray energy [GeV] for gamma-ray windows.
    m_chi_GeV : float
        DM mass [GeV].
    sigma_v : float, optional
        DM cross-section. None = thermal relic.
    channel : str
        DM annihilation channel.
    source_classes : list of str, optional
        Astrophysical source classes. None = all four.
    z_min_hi, z_max_hi : float, optional
        HI band limits. If None, uses the full z_arr range (survey-independent).
    unresolved_only : bool
        If True, astro windows use unresolved sources only.
    include_DM : bool
        Whether to include DM window.
    z_norm_max : float, optional
        Upper limit for the normalization integral. Default ``_Z_NORM_MAX`` (4.0).
    hi_brightness : str
        HI prescription used for both the brightness and (where applicable)
        the bias. Aliases: ``'padmanabhan'``, ``'fixed_omega'``,
        ``'cunnington'`` (= ``'meerfish'``). The Cunnington mode uses the
        Eqs. A4 / A5 brightness and the Eq. A3 bias polynomial together so
        the windows are self-consistent with the MeerFish forecasts.

    Returns
    -------
    result : dict
        Keys: 'z', 'HI', source class names, optionally 'DM'.
        Each value is an array of normalized window function values on z_arr.
    """
    if source_classes is None:
        source_classes = ['BL_Lac', 'FSRQ', 'mAGN', 'SFG']
    if z_norm_max is None:
        z_norm_max = _Z_NORM_MAX

    z_arr = np.asarray(z_arr, dtype=float)

    # c*h/H(z) converts per-chi window to per-z: W^(z) = W^(chi) * dchi/dz
    # where dchi/dz = c*h/H in [Mpc/h per unit z].
    # Item 1.4: vectorised over z_arr (cosmo.H is array-aware)
    c_h_over_H = cfg.C_LIGHT_KM_S * cfg.h / cosmo.H(z_arr)

    # --- Build extended normalization grid [0, z_norm_max] ---
    z_ext = np.linspace(0.001, z_norm_max, _N_Z_NORM)
    dz_ext = z_ext[1] - z_ext[0]
    # Item 1.4: vectorised over z_ext
    c_h_over_H_ext = cfg.C_LIGHT_KM_S * cfg.h / cosmo.H(z_ext)

    result = {'z': z_arr}

    # --- HI ---
    survey_independent_hi = (z_min_hi is None and z_max_hi is None)
    if survey_independent_hi:
        W_hi_perz = np.array([
            hi.T_bar_b_for_model(z, hi_brightness) for z in z_arr
        ]) * c_h_over_H
        W_hi_ext = np.array([
            hi.T_bar_b_for_model(z, hi_brightness) for z in z_ext
        ]) * c_h_over_H_ext
    else:
        W_hi_perz = np.array([
            hi.W_HI(z, z_min_hi, z_max_hi, hi_brightness=hi_brightness)
            for z in z_arr
        ]) * c_h_over_H
        W_hi_ext = np.array([
            hi.W_HI(z, z_min_hi, z_max_hi, hi_brightness=hi_brightness)
            for z in z_ext
        ]) * c_h_over_H_ext

    I_hi = np.sum(W_hi_ext) * dz_ext
    result['HI'] = W_hi_perz / I_hi if I_hi > 0 else np.zeros_like(z_arr)

    # --- Astrophysical sources ---
    for src in source_classes:
        W_astro_perz = np.array([
            astro.W_gamma_astro(E_GeV, z, src, unresolved_only=unresolved_only)
            for z in z_arr
        ]) * c_h_over_H

        W_astro_ext = np.array([
            astro.W_gamma_astro(E_GeV, z, src, unresolved_only=unresolved_only)
            for z in z_ext
        ]) * c_h_over_H_ext

        I_src = np.sum(W_astro_ext) * dz_ext
        result[src] = W_astro_perz / I_src if I_src > 0 else np.zeros_like(z_arr)

    # --- DM ---
    if include_DM:
        W_dm_perz = np.array([
            dm.W_gamma_DM(E_GeV, z, m_chi_GeV, sigma_v, channel)
            for z in z_arr
        ]) * c_h_over_H

        W_dm_ext = np.array([
            dm.W_gamma_DM(E_GeV, z, m_chi_GeV, sigma_v, channel)
            for z in z_ext
        ]) * c_h_over_H_ext

        I_dm = np.sum(W_dm_ext) * dz_ext
        result['DM'] = W_dm_perz / I_dm if I_dm > 0 else np.zeros_like(z_arr)

    return result
