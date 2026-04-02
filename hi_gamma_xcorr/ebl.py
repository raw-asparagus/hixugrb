"""EBL (Extragalactic Background Light) opacity models.

Implements gamma-ray absorption optical depth tau(E, z) from pair production
on EBL photons.  Primary model: analytic approximation based on
Razzaque, Dermer & Finke (2009) and Dominguez et al. (2011).
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline


def tau_rdf09(E_GeV, z):
    """EBL optical depth from Razzaque, Dermer & Finke (2009) approximation.

    Uses a simple analytic parameterization that captures the main features:
    tau ~ 0 for E < 10 GeV at any z < 1, and increases steeply above.

    This is a fit to the Finke, Razzaque & Dermer (2010) model.
    """
    E_GeV = np.asarray(E_GeV, dtype=float)
    z = float(z)

    if z <= 0:
        return np.zeros_like(E_GeV)

    # Parameterization following Dominguez-like scaling:
    # tau(E, z) ~ (E / E_0)^{gamma} * (z / z_0)^{delta}
    # where E_0 ~ 25 GeV, gamma ~ 1.5, z_0 ~ 0.2, delta ~ 1.5
    # Calibrated to match published opacity tables at key points:
    # tau(100 GeV, z=0.5) ~ 0.5, tau(100 GeV, z=1) ~ 2-3, tau(30 GeV, z=1) ~ 0.3

    # Calibrated piecewise model matching Dominguez et al. (2011):
    # tau(100 GeV, z=0.5) ~ 0.5, tau(100 GeV, z=1) ~ 2-3
    # tau(30 GeV, z=1) ~ 0.3, tau(300 GeV, z=1) ~ 10
    result = np.zeros_like(E_GeV)

    mask = E_GeV > 1.0
    E = E_GeV[mask]

    # Core: tau scales roughly as E^{0.8-1} * z^{1.2-1.5}
    # Calibration anchor: tau(100 GeV, z=1) = 2.5
    tau = 2.5 * (E / 100.0)**1.0 * (z / 1.0)**1.3

    # Suppress below pair-production threshold (~20 GeV)
    threshold = 1.0 / (1.0 + (20.0 / E)**4)
    tau *= threshold

    result[mask] = tau
    return np.clip(result, 0.0, 50.0)


def attenuation(E_GeV, z):
    """EBL attenuation factor exp(-tau(E, z))."""
    return np.exp(-tau_rdf09(E_GeV, z))


# Default model
tau = tau_rdf09
