"""Statistical forecasting: variance, SNR, Delta chi^2, exclusion curves.

Implements the Gaussian variance approximation, signal-to-noise computation,
and dark matter exclusion curve generation.
"""

import numpy as np

from . import config as cfg
from . import angular_power as ap
from . import noise_model as nm

# ---------------------------------------------------------------------------
# Gaussian variance (Eq. 5.5)
# ---------------------------------------------------------------------------

def variance_Cl(ell, C_HI_auto, N_HI, B_HI, N_gamma, B_gamma, f_sky):
    """Gaussian variance of C_l^{HI x gamma}.

    (Delta C_l)^2 = [N^gamma / (B_l^gamma)^2] * [C_l^{HI} + N^HI / (B_l^HI)^2]
                    / ((2l+1) * f_sky)

    N^gamma from Pinetti Table 2 is in cm-based units [cm^{-4} s^{-2} sr^{-1}].
    The Limber integral computes C_l with gamma in (Mpc/h)-based units.
    We convert N^gamma to (Mpc/h)-based units for consistency.

    Parameters
    ----------
    ell : array
        Multipoles.
    C_HI_auto : array
        HI auto-power spectrum C_l^{HI,HI} [mK^2].
    N_HI : array
        Radio noise power N^HI [mK^2 sr].
    B_HI : array
        Radio beam function.
    N_gamma : float
        Fermi-LAT noise [cm^{-4} s^{-2} sr^{-1}] from Pinetti Table 2.
    B_gamma : array
        Fermi-LAT beam function.
    f_sky : float
        Effective sky fraction.

    Returns
    -------
    sigma_Cl : array
        Standard deviation of C_l.
    """
    ell = np.asarray(ell, dtype=float)

    # Convert N_gamma from cm-based to (Mpc/h)-based units:
    # N_gamma [cm^{-4} s^{-2} sr^{-1}] → [(Mpc/h)^{-4} s^{-2} sr^{-1}]
    # 1 cm^{-4} = (Mpc_h_cm)^4 (Mpc/h)^{-4}
    Mpc_h_cm = cfg.MPC_TO_M * 100.0 / cfg.h  # cm per (Mpc/h)
    N_gamma_Mpc = N_gamma * Mpc_h_cm**4

    noise_gamma_eff = N_gamma_Mpc / B_gamma**2
    noise_HI_eff = C_HI_auto + N_HI / B_HI**2

    var = noise_gamma_eff * noise_HI_eff / ((2.0 * ell + 1.0) * f_sky)
    return np.sqrt(np.maximum(var, 0.0))


# ---------------------------------------------------------------------------
# Signal-to-noise ratio (Eq. 5.6)
# ---------------------------------------------------------------------------

def compute_SNR(telescope, band_name, fermissimo=False,
                ell_min=10, ell_max=1000, n_ell=100,
                source_classes=None, n_z=30, n_M=30):
    """Compute the total signal-to-noise ratio for detecting the cross-correlation.

    SNR^2 = sum over (l, E-bins) of [C_l^{HI x gamma_astro} / Delta C_l]^2

    Parameters
    ----------
    telescope : str
        Radio telescope name.
    band_name : str
        Band name.
    fermissimo : bool
        Use Fermissimo specs instead of Fermi-LAT.

    Returns
    -------
    SNR : float
    """
    if source_classes is None:
        source_classes = ['BL_Lac', 'FSRQ', 'mAGN', 'SFG']

    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_min = band['z_min']
    z_max = band['z_max']
    z_mid = 0.5 * (z_min + z_max)

    # Multipole grid
    ell_arr = np.unique(np.logspace(
        np.log10(ell_min), np.log10(ell_max), n_ell
    ).astype(int)).astype(float)

    # HI auto-power
    C_HI = ap.C_ell_HI_auto(ell_arr, z_min, z_max, n_z=n_z, n_M=n_M)

    # Radio noise and beam
    N_HI = nm.noise_radio_combined(ell_arr, telescope, band_name)

    SNR2_total = 0.0

    for ie in range(cfg.FERMI_N_BINS):
        E_b = cfg.FERMI_E_B[ie]

        # Fermi noise and beam
        if fermissimo:
            N_gamma = nm.noise_fermissimo(ie)
            B_gamma = nm.beam_fermissimo(ell_arr, E_b)
            f_sky = nm.f_sky_effective(telescope, band_name, ie, fermissimo=True)
        else:
            N_gamma = nm.noise_fermi(ie)
            B_gamma = nm.beam_fermi(ell_arr, E_b)
            f_sky = nm.f_sky_effective(telescope, band_name, ie)

        # Radio beam (use dish diameter)
        B_HI = nm.beam_radio(ell_arr, z_mid, tel['d_dish_m'])

        # Variance
        sigma_Cl = variance_Cl(ell_arr, C_HI, N_HI, B_HI, N_gamma, B_gamma, f_sky)

        # Signal: C_l from astrophysical sources only
        C_signal = ap.C_ell_HI_gamma(
            ell_arr, E_b, z_min, z_max, telescope, band_name,
            source_classes=source_classes, include_DM=False,
            n_z=n_z, n_k_M=n_M
        )

        C_astro = C_signal['total']

        # SNR contribution
        mask = sigma_Cl > 0
        SNR2_total += np.sum((C_astro[mask] / sigma_Cl[mask])**2)

    return np.sqrt(SNR2_total)


# ---------------------------------------------------------------------------
# Delta chi^2 for DM exclusion (Eq. 5.7)
# ---------------------------------------------------------------------------

def delta_chi2(m_chi_GeV, sigma_v, telescope, band_name,
               channel='bb', fermissimo=False,
               ell_min=10, ell_max=1000, n_ell=50,
               n_z=20, n_M=20):
    """Compute Delta chi^2 for a given DM mass and cross-section.

    Delta chi^2 = sum_l,E [(C_l^{astro+DM} / sigma)^2 - (C_l^{astro} / sigma)^2]

    Since C_DM is proportional to sigma_v, this is a simple function.
    """
    tel = cfg.RADIO_TELESCOPES[telescope]
    band = tel['bands'][band_name]
    z_min = band['z_min']
    z_max = band['z_max']
    z_mid = 0.5 * (z_min + z_max)

    ell_arr = np.unique(np.logspace(
        np.log10(ell_min), np.log10(ell_max), n_ell
    ).astype(int)).astype(float)

    C_HI = ap.C_ell_HI_auto(ell_arr, z_min, z_max, n_z=n_z, n_M=n_M)
    N_HI = nm.noise_radio_combined(ell_arr, telescope, band_name)

    dchi2 = 0.0

    for ie in range(cfg.FERMI_N_BINS):
        E_b = cfg.FERMI_E_B[ie]

        if fermissimo:
            N_gamma = nm.noise_fermissimo(ie)
            B_gamma = nm.beam_fermissimo(ell_arr, E_b)
            f_sky = nm.f_sky_effective(telescope, band_name, ie, fermissimo=True)
        else:
            N_gamma = nm.noise_fermi(ie)
            B_gamma = nm.beam_fermi(ell_arr, E_b)
            f_sky = nm.f_sky_effective(telescope, band_name, ie)

        B_HI = nm.beam_radio(ell_arr, z_mid, tel['d_dish_m'])
        sigma_Cl = variance_Cl(ell_arr, C_HI, N_HI, B_HI, N_gamma, B_gamma, f_sky)

        # Compute C_l with and without DM
        C_with_DM = ap.C_ell_HI_gamma(
            ell_arr, E_b, z_min, z_max, telescope, band_name,
            m_chi_GeV=m_chi_GeV, sigma_v=sigma_v, channel=channel,
            include_DM=True, n_z=n_z, n_k_M=n_M
        )['total']

        C_no_DM = ap.C_ell_HI_gamma(
            ell_arr, E_b, z_min, z_max, telescope, band_name,
            include_DM=False, n_z=n_z, n_k_M=n_M
        )['total']

        mask = sigma_Cl > 0
        dchi2 += np.sum(
            (C_with_DM[mask] / sigma_Cl[mask])**2 -
            (C_no_DM[mask] / sigma_Cl[mask])**2
        )

    return dchi2


# ---------------------------------------------------------------------------
# DM exclusion curve
# ---------------------------------------------------------------------------

def exclusion_curve(telescope, band_name, channel='bb',
                    fermissimo=False, CL='95',
                    m_chi_arr=None, n_ell=30, n_z=15, n_M=15):
    """Compute the DM exclusion curve: sigma_v vs m_chi.

    For each m_chi, find sigma_v where Delta chi^2 = threshold.

    Parameters
    ----------
    CL : str
        '95' for 95% CL (Delta chi^2 = 4), '5sigma' (Delta chi^2 = 25).

    Returns
    -------
    m_chi_arr : array [GeV]
    sigma_v_arr : array [cm^3/s]
    """
    from scipy.optimize import brentq

    threshold = 4.0 if CL == '95' else 25.0

    if m_chi_arr is None:
        m_chi_arr = np.logspace(1, 4, 20)  # 10 GeV to 10 TeV

    sigma_v_arr = np.full_like(m_chi_arr, np.nan)

    for i, m_chi in enumerate(m_chi_arr):
        # Since C_DM ∝ sigma_v, Delta chi^2 ∝ sigma_v^2 (at leading order)
        # Test with thermal relic value
        sv_test = cfg.SIGMA_V_THERMAL
        dchi2_test = delta_chi2(
            m_chi, sv_test, telescope, band_name,
            channel=channel, fermissimo=fermissimo,
            n_ell=n_ell, n_z=n_z, n_M=n_M
        )

        if dchi2_test <= 0:
            continue

        # sigma_v scales: to get threshold, need sigma_v * sqrt(threshold / dchi2_test)
        # (approximate, since the relationship isn't exactly linear due to noise terms)
        sigma_v_arr[i] = sv_test * np.sqrt(threshold / dchi2_test)

    return m_chi_arr, sigma_v_arr
