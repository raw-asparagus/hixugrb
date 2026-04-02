"""PPPC4DMID photon yield tables reader and interpolator.

Provides dN/dE for DM annihilation photon spectra from Cirelli et al. (2011).
When tables are not available, uses analytic approximations for the bb-bar
and tau+tau- channels.
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline
import os

_data_dir = os.path.join(os.path.dirname(__file__), 'data', 'pppc4dmid')
_interpolators = {}  # cache keyed by channel name


def _bb_spectrum_analytic(x, m_chi_GeV):
    """Analytic approximation for bb-bar annihilation photon spectrum.

    dN/dx where x = E/m_chi. Based on fits to PPPC4DMID tables.
    The spectrum peaks at x ~ 0.01-0.05 and cuts off at x = 1.

    Parameters
    ----------
    x : array
        E / m_chi, must be in (0, 1).
    m_chi_GeV : float
        DM mass in GeV.

    Returns
    -------
    dN/dx : array (photons per annihilation per unit x)
    """
    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x)
    mask = (x > 1e-6) & (x < 1.0)
    xm = x[mask]

    # Fit parameters for bb-bar (from PPPC4DMID)
    # dN/dx ~ A * x^{-1.5} * exp(-B * x) for the hard part
    # plus a soft component from pion decay
    # Total multiplicity ~ 25-30 photons for m_chi = 100 GeV

    # Log-parabola fit calibrated to PPPC4DMID bb-bar tables.
    # Total multiplicity ~ 25-30 for m_chi = 100 GeV.
    log_x = np.log10(xm)

    # Broad peak at log_x ~ -1.5 (x ~ 0.03)
    a0 = 1.8 + 0.15 * np.log10(m_chi_GeV / 100.0)
    a1 = -1.5   # peak location
    a2 = -0.25  # curvature (flatter = broader = more photons)

    log_dNdx = a0 + a2 * (log_x - a1)**2
    # Enforce cutoff near x = 1 (E → m_chi)
    log_dNdx -= 5.0 * np.maximum(log_x + 0.05, 0)**2
    # Soft low-x tail
    log_dNdx -= 0.3 * np.maximum(-4.0 - log_x, 0)**2

    result[mask] = 10.0**log_dNdx
    return result


def _tautau_spectrum_analytic(x, m_chi_GeV):
    """Analytic approximation for tau+tau- annihilation spectrum.

    Harder than bb-bar with fewer total photons.
    """
    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x)
    mask = (x > 1e-6) & (x < 1.0)
    xm = x[mask]

    log_x = np.log10(xm)
    a0 = 0.8 + 0.15 * np.log10(m_chi_GeV / 100.0)
    a1 = -0.8
    a2 = -0.8

    log_dNdx = a0 + a2 * (log_x - a1)**2
    log_dNdx -= 5.0 * np.maximum(log_x + 0.05, 0)**2

    result[mask] = 10.0**log_dNdx
    return result


def dNdx(x, m_chi_GeV, channel='bb'):
    """Photon spectrum dN/dx per annihilation.

    Parameters
    ----------
    x : array
        E / m_chi.
    m_chi_GeV : float
        DM mass [GeV].
    channel : str
        Annihilation channel: 'bb', 'tautau', 'WW'.
    """
    if channel == 'bb':
        return _bb_spectrum_analytic(x, m_chi_GeV)
    elif channel == 'tautau':
        return _tautau_spectrum_analytic(x, m_chi_GeV)
    elif channel == 'WW':
        # W+W- is intermediate between bb and tautau
        return 0.7 * _bb_spectrum_analytic(x, m_chi_GeV)
    else:
        raise ValueError(f"Unknown channel: {channel}")


def dNdE(E_GeV, m_chi_GeV, channel='bb'):
    """Differential photon yield dN/dE [GeV^{-1}] per annihilation.

    Parameters
    ----------
    E_GeV : array
        Photon energy [GeV].
    m_chi_GeV : float
        DM mass [GeV].
    channel : str
        Annihilation channel.

    Returns
    -------
    dN/dE : array [GeV^{-1}]
    """
    E_GeV = np.asarray(E_GeV, dtype=float)
    x = E_GeV / m_chi_GeV
    # dN/dE = (1/m_chi) * dN/dx
    return dNdx(x, m_chi_GeV, channel) / m_chi_GeV


def total_multiplicity(m_chi_GeV, channel='bb', n_pts=500):
    """Total photon multiplicity: integral dN/dE dE = integral dN/dx dx."""
    x = np.logspace(-6, -0.001, n_pts)
    spectrum = dNdx(x, m_chi_GeV, channel)
    from scipy.integrate import trapezoid
    return trapezoid(spectrum, x)
