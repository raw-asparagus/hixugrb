"""EBL (Extragalactic Background Light) opacity models.

Uses the `ebltable` package for tabulated opacity models when available,
with an analytic fallback.  Primary model: Dominguez et al. (2011).
"""

import numpy as np

# ---------------------------------------------------------------------------
# ebltable-based implementation
# ---------------------------------------------------------------------------

_od_cache = {}  # cache OptDepth objects by model name


def _get_optdepth(model='dominguez'):
    """Get (or create) an ebltable OptDepth object."""
    if model not in _od_cache:
        from ebltable.tau_from_model import OptDepth
        _od_cache[model] = OptDepth.readmodel(model=model)
    return _od_cache[model]


def _has_ebltable():
    """Check if ebltable is importable."""
    try:
        import ebltable  # noqa: F401
        return True
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def tau(E_GeV, z, model='dominguez'):
    """EBL optical depth tau(E, z).

    Parameters
    ----------
    E_GeV : float or array
        Photon energy [GeV].
    z : float
        Redshift.
    model : str
        EBL model name. Options: 'dominguez', 'finke', 'franceschini',
        'saldana-lopez21', or 'analytic' for the built-in approximation.

    Returns
    -------
    tau : array matching E_GeV shape
    """
    E_GeV = np.atleast_1d(np.asarray(E_GeV, dtype=float))
    z = float(z)

    if z <= 0:
        return np.zeros_like(E_GeV)

    if model == 'analytic' or not _has_ebltable():
        return _tau_analytic(E_GeV, z)

    od = _get_optdepth(model)
    E_TeV = E_GeV / 1000.0  # ebltable uses TeV
    # ebltable.opt_depth(z, E_TeV) — handles arrays
    result = np.array([od.opt_depth(z, e) for e in E_TeV], dtype=float).ravel()
    return np.maximum(result, 0.0)


def attenuation(E_GeV, z, model='dominguez'):
    """EBL attenuation factor exp(-tau(E, z))."""
    return np.exp(-tau(E_GeV, z, model=model))


# ---------------------------------------------------------------------------
# Analytic fallback
# ---------------------------------------------------------------------------

def _tau_analytic(E_GeV, z):
    """Simple analytic EBL approximation (fallback when ebltable unavailable).

    Calibrated to Dominguez et al. (2011) anchor points.
    """
    E_GeV = np.asarray(E_GeV, dtype=float)
    result = np.zeros_like(E_GeV)
    mask = E_GeV > 1.0
    E = E_GeV[mask]
    tau_val = 2.5 * (E / 100.0)**1.0 * (z / 1.0)**1.3
    threshold = 1.0 / (1.0 + (20.0 / E)**4)
    tau_val *= threshold
    result[mask] = tau_val
    return np.clip(result, 0.0, 50.0)
