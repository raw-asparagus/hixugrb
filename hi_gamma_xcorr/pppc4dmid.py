"""PPPC4DMID photon yield tables reader and interpolator.

Provides dN/dE for DM annihilation photon spectra from Cirelli et al. (2011).
Loads tables from data/pppc4dmid/AtProduction_gammas.dat if available,
otherwise falls back to analytic approximations.
"""

import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.integrate import trapezoid
import os

_data_dir = os.path.join(os.path.dirname(__file__), 'data', 'pppc4dmid')
_table_file = os.path.join(_data_dir, 'AtProduction_gammas.dat')

# Module-level state
_tables_loaded = False
_log10_masses = None     # unique log10(mDM) values
_log10_x = None          # unique log10(x) values
_interpolators = {}      # RectBivariateSpline per channel name

# Channel name mapping: our names → PPPC4DMID table column names (Cirelli et al. 2011)
_CHANNEL_MAP = {
    'bb': 'b',
    'tautau': '\\[Tau]',
    'WW': 'W',
    'ZZ': 'Z',
    'cc': 'c',
    'tt': 't',
    'ee': 'e',
    'mumu': '\\[Mu]',
    'gg': 'g',
    'hh': 'h',
    'qq': 'q',
    'gammagamma': '\\[Gamma]',
}

# ---------------------------------------------------------------------------
# Table loading
# ---------------------------------------------------------------------------

def download_tables():
    """Download PPPC4DMID tables from GitHub mirror."""
    import urllib.request
    os.makedirs(_data_dir, exist_ok=True)
    url = 'https://raw.githubusercontent.com/carmeloevoli/PPPC4DMID-C/master/data/AtProduction_gammas.txt'
    print(f'Downloading PPPC4DMID tables from {url}...')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=60)
    data = resp.read()
    with open(_table_file, 'wb') as f:
        f.write(data)
    print(f'Saved to {_table_file} ({len(data)/1e6:.1f} MB)')


def _load_tables():
    """Parse the PPPC4DMID ASCII table and build interpolators."""
    global _tables_loaded, _log10_masses, _log10_x, _interpolators

    if not os.path.exists(_table_file):
        return False

    # Read header to get channel names
    with open(_table_file) as f:
        header = f.readline().split()

    # header[0] = 'mDM', header[1] = 'Log[10,x]', header[2:] = channel names
    channel_names = header[2:]

    # Load data (skip header row)
    data = np.loadtxt(_table_file, skiprows=1)
    # data columns: mDM, Log10(x), channel1, channel2, ...

    masses = data[:, 0]        # DM masses in GeV
    log10x = data[:, 1]        # Log10(x) = Log10(E/mDM)
    spectra = data[:, 2:]      # dN/dLog10(x) for each channel

    # Find unique masses and x-values
    unique_masses = np.unique(masses)
    unique_log10x = np.unique(log10x)
    n_mass = len(unique_masses)
    n_x = len(unique_log10x)

    _log10_masses = np.log10(unique_masses)
    _log10_x = unique_log10x

    # Reshape spectra into (n_mass, n_x, n_channels)
    n_channels = spectra.shape[1]
    spectra_3d = spectra.reshape(n_mass, n_x, n_channels)

    # Build interpolator for each channel
    _interpolators.clear()
    for ich, cname in enumerate(channel_names):
        # spectra_3d[:, :, ich] has shape (n_mass, n_x)
        grid = spectra_3d[:, :, ich]
        # Replace zeros/negatives with tiny value for log interpolation
        grid = np.maximum(grid, 1e-30)
        log_grid = np.log10(grid)
        _interpolators[cname] = RectBivariateSpline(
            _log10_masses, _log10_x, log_grid, kx=3, ky=3
        )

    _tables_loaded = True
    return True


def _ensure_tables():
    """Load tables if not already loaded."""
    global _tables_loaded
    if not _tables_loaded:
        _load_tables()


def _get_table_column(channel):
    """Get the table column name for a given channel."""
    if channel in _CHANNEL_MAP:
        return _CHANNEL_MAP[channel]
    return channel


# ---------------------------------------------------------------------------
# Table-based spectrum
# ---------------------------------------------------------------------------

def _dNdlog10x_table(log10x, m_chi_GeV, channel):
    """Interpolate dN/dLog10(x) from tables.

    Parameters
    ----------
    log10x : array
        Log10(E / m_chi).
    m_chi_GeV : float
        DM mass [GeV].
    channel : str
        Channel name (our convention).

    Returns
    -------
    dN/dLog10(x) : array
    """
    col = _get_table_column(channel)
    if col not in _interpolators:
        raise ValueError(f"Channel '{channel}' (column '{col}') not found in tables. "
                         f"Available: {list(_interpolators.keys())}")

    interp = _interpolators[col]
    log10m = np.log10(m_chi_GeV)

    # Clamp to table range
    log10m = np.clip(log10m, _log10_masses[0], _log10_masses[-1])
    log10x = np.asarray(log10x, dtype=float)
    log10x_clipped = np.clip(log10x, _log10_x[0], _log10_x[-1])

    log_val = interp(log10m, log10x_clipped, grid=False)
    return 10.0**log_val


# ---------------------------------------------------------------------------
# Analytic fallbacks (kept for when tables are unavailable)
# ---------------------------------------------------------------------------

def _bb_spectrum_analytic(x, m_chi_GeV):
    """Analytic approximation for bb-bar dN/dx."""
    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x)
    mask = (x > 1e-6) & (x < 1.0)
    xm = x[mask]
    log_x = np.log10(xm)
    a0 = 1.8 + 0.15 * np.log10(m_chi_GeV / 100.0)
    a1, a2 = -1.5, -0.25
    log_dNdx = a0 + a2 * (log_x - a1)**2
    log_dNdx -= 5.0 * np.maximum(log_x + 0.05, 0)**2
    log_dNdx -= 0.3 * np.maximum(-4.0 - log_x, 0)**2
    result[mask] = 10.0**log_dNdx
    return result


def _tautau_spectrum_analytic(x, m_chi_GeV):
    """Analytic approximation for tau+tau- dN/dx."""
    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x)
    mask = (x > 1e-6) & (x < 1.0)
    xm = x[mask]
    log_x = np.log10(xm)
    a0 = 0.8 + 0.15 * np.log10(m_chi_GeV / 100.0)
    a1, a2 = -0.8, -0.8
    log_dNdx = a0 + a2 * (log_x - a1)**2
    log_dNdx -= 5.0 * np.maximum(log_x + 0.05, 0)**2
    result[mask] = 10.0**log_dNdx
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def dNdx(x, m_chi_GeV, channel='bb'):
    """Photon spectrum dN/dx per annihilation.

    Uses PPPC4DMID tables if available, analytic approximation otherwise.

    Parameters
    ----------
    x : array
        E / m_chi (dimensionless).
    m_chi_GeV : float
        DM mass [GeV].
    channel : str
        Annihilation channel: 'bb', 'tautau', 'WW', etc.

    Returns
    -------
    dN/dx : array (photons per annihilation per unit x)
    """
    _ensure_tables()
    x = np.asarray(x, dtype=float)

    if _tables_loaded:
        # Table-based: dN/dLog10(x) → dN/dx = dN/dLog10(x) / (x * ln(10))
        mask = (x > 1e-9) & (x < 1.0)
        result = np.zeros_like(x)
        if np.any(mask):
            log10x = np.log10(x[mask])
            dNdlog10x = _dNdlog10x_table(log10x, m_chi_GeV, channel)
            result[mask] = dNdlog10x / (x[mask] * np.log(10.0))
        return result
    else:
        # Analytic fallback
        if channel == 'bb':
            return _bb_spectrum_analytic(x, m_chi_GeV)
        elif channel == 'tautau':
            return _tautau_spectrum_analytic(x, m_chi_GeV)
        elif channel == 'WW':
            return 0.7 * _bb_spectrum_analytic(x, m_chi_GeV)
        else:
            raise ValueError(f"No analytic fallback for channel '{channel}'. "
                             "Download tables with pppc4dmid.download_tables()")


def dNdE(E_GeV, m_chi_GeV, channel='bb'):
    """Differential photon yield dN/dE [GeV^{-1}] per annihilation.

    Parameters
    ----------
    E_GeV : float or array
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
    return dNdx(x, m_chi_GeV, channel) / m_chi_GeV


def total_multiplicity(m_chi_GeV, channel='bb', n_pts=500):
    """Total photon multiplicity: integral dN/dx dx."""
    x = np.logspace(-6, -0.001, n_pts)
    spectrum = dNdx(x, m_chi_GeV, channel)
    return trapezoid(spectrum, x)
