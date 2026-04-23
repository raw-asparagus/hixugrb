"""EBL (Extragalactic Background Light) opacity models.

Uses the `ebltable` package for tabulated opacity models.
Primary model: Dominguez et al. (2011).
"""

import numpy as np

from . import config as cfg

# ---------------------------------------------------------------------------
# ebltable-based implementation
# ---------------------------------------------------------------------------

_od_cache = {}  # cache OptDepth objects by model name


def _get_optdepth(model=cfg.EBLModel.DOMINGUEZ):
    """Get (or create) an ebltable OptDepth object."""
    if model not in _od_cache:
        from ebltable.tau_from_model import OptDepth
        _od_cache[model] = OptDepth.readmodel(model=model)
    return _od_cache[model]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def tau(E_GeV, z, model=cfg.EBLModel.DOMINGUEZ):
    """EBL optical depth tau(E, z).

    Parameters
    ----------
    E_GeV : float or array
        Photon energy [GeV].
    z : float
        Redshift.
    model : str
        EBL model name passed to ebltable. Options: 'dominguez', 'finke',
        'franceschini', 'saldana-lopez21'.

    Returns
    -------
    tau : array matching E_GeV shape
    """
    E_GeV = np.atleast_1d(np.asarray(E_GeV, dtype=float))
    z = float(z)

    if z <= 0:
        return np.zeros_like(E_GeV)

    od = _get_optdepth(model)
    E_TeV = E_GeV / 1000.0  # ebltable uses TeV
    result = np.array([od.opt_depth(z, e) for e in E_TeV], dtype=float).ravel()
    return result


def attenuation(E_GeV, z, model=cfg.EBLModel.DOMINGUEZ):
    """EBL attenuation factor exp(-tau(E, z))."""
    return np.exp(-tau(E_GeV, z, model=model))
