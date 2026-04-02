"""Angular power spectrum computation via Limber integration.

Computes C_l^{ij} for all cross-correlations between HI and gamma-ray sources.
"""

import numpy as np
from scipy.integrate import quad

from . import config as cfg
from . import cosmology as cosmo
from . import halo_model as hm
from . import hi_model as hi
from . import dm_model as dm
from . import astro_sources as astro
from . import noise_model as nm

# ---------------------------------------------------------------------------
# HI × DM 3D cross-power spectra (Eqs. 5.1–5.2)
# ---------------------------------------------------------------------------

def P_HI_DM_1h(k, z, n_M=60):
    """One-halo HI × DM cross-power spectrum.

    P^{1h} = integral (dn/dM) [v_tilde/Delta^2] [u_HI * M_HI/rho_HI] dM
    """
    k = np.atleast_1d(np.asarray(k, dtype=float))
    rho_HI = hi.rho_HI_mean(z)
    Delta2 = dm.clumping_factor(z)

    if rho_HI <= 0 or Delta2 <= 0:
        return np.zeros_like(k)

    M_min = max(cfg.M_MIN_HI, 1e8)
    M_max = min(cfg.M_MAX_HI, 1e16)
    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    result = np.zeros_like(k)

    for M in M_arr:
        dn = hm.dndM(M, z)
        m_hi = hi.M_HI(M, z)
        if dn <= 0 or m_hi <= 0:
            continue
        u_hi = hi.u_HI(k, M, z)
        vt = dm.v_tilde(k, M, z)
        result += dn * (vt / Delta2) * (u_hi * m_hi / rho_HI) * M

    dlnM = np.log(M_arr[1] / M_arr[0])
    return result * dlnM


def P_HI_DM_2h(k, z, n_M=60):
    """Two-halo HI × DM cross-power spectrum.

    P^{2h} = [integral dn * b * v_tilde/Delta^2 dM]
             × [integral dn * b * u_HI * M_HI/rho_HI dM] × P_lin
    """
    k = np.atleast_1d(np.asarray(k, dtype=float))
    rho_HI = hi.rho_HI_mean(z)
    Delta2 = dm.clumping_factor(z)

    if rho_HI <= 0 or Delta2 <= 0:
        return np.zeros_like(k)

    M_min = max(cfg.M_MIN_HI, 1e8)
    M_max = min(cfg.M_MAX_HI, 1e16)
    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    I_DM = np.zeros_like(k)
    I_HI = np.zeros_like(k)

    for M in M_arr:
        dn = hm.dndM(M, z)
        b = hm.bias(M, z)
        m_hi = hi.M_HI(M, z)
        if dn <= 0:
            continue
        u_hi = hi.u_HI(k, M, z) if m_hi > 0 else np.zeros_like(k)
        vt = dm.v_tilde(k, M, z)
        I_DM += dn * b * vt / Delta2 * M
        if m_hi > 0:
            I_HI += dn * b * u_hi * m_hi / rho_HI * M

    dlnM = np.log(M_arr[1] / M_arr[0])
    return I_DM * dlnM * I_HI * dlnM * cosmo.P_lin(k, z)


# ---------------------------------------------------------------------------
# HI × Astrophysical source 3D cross-power spectra (Eqs. 5.3–5.4)
# ---------------------------------------------------------------------------

def P_HI_astro_2h(k, z, source_class, n_M=60):
    """Two-halo HI × astrophysical source cross-power spectrum.

    P^{2h} = b_HI_integral × b_astro × P_lin

    For point sources, the 2-halo term dominates and is the product
    of the HI bias integral and the source effective bias times P_lin.
    """
    k = np.atleast_1d(np.asarray(k, dtype=float))
    rho_HI = hi.rho_HI_mean(z)
    if rho_HI <= 0:
        return np.zeros_like(k)

    # HI bias integral (same as P_HI_2h but just the integral part)
    M_min = max(cfg.M_MIN_HI, 1e8)
    M_max = min(cfg.M_MAX_HI, 1e16)
    M_arr = np.logspace(np.log10(M_min), np.log10(M_max), n_M)
    I_HI = np.zeros_like(k)

    for M in M_arr:
        dn = hm.dndM(M, z)
        b = hm.bias(M, z)
        m_hi = hi.M_HI(M, z)
        if dn <= 0 or m_hi <= 0:
            continue
        u_hi = hi.u_HI(k, M, z)
        I_HI += dn * b * m_hi * u_hi / rho_HI * M

    dlnM = np.log(M_arr[1] / M_arr[0])
    I_HI *= dlnM

    # Astrophysical source bias
    b_astro = astro.bias_astro(z, source_class)

    return I_HI * b_astro * cosmo.P_lin(k, z)


# ---------------------------------------------------------------------------
# Limber integration engine
# ---------------------------------------------------------------------------

def C_ell_HI_gamma(ell, E_GeV, z_min, z_max, telescope, band_name,
                   m_chi_GeV=100.0, sigma_v=None, channel='bb',
                   source_classes=None, include_DM=True,
                   n_z=50, n_k_M=40):
    """Compute C_l^{HI × gamma} via Limber integration.

    C_l = integral (dchi/chi^2) W_HI(chi) W_gamma(chi) P(k=(l+0.5)/chi, z)

    Parameters
    ----------
    ell : array
        Multipoles.
    E_GeV : float
        Gamma-ray energy [GeV].
    z_min, z_max : float
        Redshift bounds of the HI band.
    telescope : str
        Radio telescope name.
    band_name : str
        Band name.
    m_chi_GeV : float
        DM mass for DM contribution.
    sigma_v : float
        DM cross-section. None = thermal relic.
    source_classes : list of str
        Astrophysical source classes to include. None = all four.
    include_DM : bool
        Whether to include the DM contribution.

    Returns
    -------
    C_ell : dict with keys 'total', 'DM', 'BL_Lac', 'FSRQ', 'mAGN', 'SFG'
    """
    if source_classes is None:
        source_classes = ['BL_Lac', 'FSRQ', 'mAGN', 'SFG']

    ell = np.atleast_1d(np.asarray(ell, dtype=float))

    # Redshift grid for integration
    z_arr = np.linspace(max(z_min, 0.01), z_max, n_z)
    dz = z_arr[1] - z_arr[0]

    result = {src: np.zeros_like(ell) for src in source_classes}
    if include_DM:
        result['DM'] = np.zeros_like(ell)

    for z in z_arr:
        # Comoving distance and dchi/dz
        chi_z = cosmo.chi(z)  # Mpc/h
        if chi_z <= 0:
            continue
        H_z = cosmo.H(z)  # km/s/Mpc
        dchi_dz = cfg.C_LIGHT_KM_S / H_z * cfg.h  # Mpc/h per unit z

        # HI window function
        W_hi = hi.W_HI(z, z_min, z_max)  # mK
        if W_hi <= 0:
            continue

        # For each multipole, k = (l + 0.5) / chi
        k_arr = (ell + 0.5) / chi_z  # h/Mpc

        # Limber weight: dchi/chi^2 * dz = (dchi/dz) / chi^2 * dz
        weight = dchi_dz / chi_z**2 * dz

        # Astrophysical source contributions (2-halo term)
        for src in source_classes:
            W_gamma = astro.W_gamma_astro(E_GeV, z, src)
            if W_gamma <= 0:
                continue
            P_cross = P_HI_astro_2h(k_arr, z, src, n_M=n_k_M)
            result[src] += W_hi * W_gamma * P_cross * weight

        # DM contribution
        if include_DM:
            W_dm = dm.W_gamma_DM(E_GeV, z, m_chi_GeV, sigma_v, channel)
            if W_dm > 0:
                P_dm = P_HI_DM_2h(k_arr, z, n_M=n_k_M)
                result['DM'] += W_hi * W_dm * P_dm * weight

    # Total
    result['total'] = sum(result[key] for key in result)
    return result


# ---------------------------------------------------------------------------
# HI auto-power C_l^{HI,HI} (needed for noise/variance computation)
# ---------------------------------------------------------------------------

def C_ell_HI_auto(ell, z_min, z_max, n_z=30, n_M=40):
    """HI auto-correlation angular power spectrum C_l^{HI,HI}.

    Uses only the 2-halo term for efficiency.
    """
    ell = np.atleast_1d(np.asarray(ell, dtype=float))
    z_arr = np.linspace(max(z_min, 0.01), z_max, n_z)
    dz = z_arr[1] - z_arr[0]

    result = np.zeros_like(ell)

    for z in z_arr:
        chi_z = cosmo.chi(z)
        if chi_z <= 0:
            continue
        H_z = cosmo.H(z)
        dchi_dz = cfg.C_LIGHT_KM_S / H_z * cfg.h

        W_hi = hi.W_HI(z, z_min, z_max)
        if W_hi <= 0:
            continue

        k_arr = (ell + 0.5) / chi_z
        weight = dchi_dz / chi_z**2 * dz

        # P_HI (2-halo only for speed)
        P_hi = hi.P_HI_2h(k_arr, z, n_M=n_M)
        result += W_hi**2 * P_hi * weight

    return result
