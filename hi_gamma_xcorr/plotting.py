"""Plotting module for the HI x gamma-ray cross-correlation pipeline.

Generates diagnostic and publication figures for validation against
Pinetti et al. (2020) and other literature.
"""

import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend
import matplotlib.pyplot as plt

from . import config as cfg
from . import cosmology as cosmo
from . import halo_model as hm
from . import hi_model as hi
from . import dm_model as dm
from . import astro_sources as astro
from . import angular_power as ap
from . import noise_model as nm
from . import statistics as stats
from . import pppc4dmid
from . import ebl

_plot_dir = os.path.join(os.path.dirname(__file__), 'plots')


def _ensure_dir():
    os.makedirs(_plot_dir, exist_ok=True)


def _savefig(fig, name, dpi=150):
    _ensure_dir()
    path = os.path.join(_plot_dir, f'{name}.png')
    fig.savefig(path, dpi=dpi, bbox_inches='tight')
    print(f'  Saved: {path}')
    return path


def _load_cache(name):
    path = os.path.join(_plot_dir, f'{name}.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def _save_cache(name, data):
    _ensure_dir()
    path = os.path.join(_plot_dir, f'{name}.json')
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def setup_style():
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'legend.fontsize': 9,
        'figure.figsize': (8, 5),
        'lines.linewidth': 1.5,
    })


# =========================================================================
# Tier 1: Fast validation plots (<5s each)
# =========================================================================

def plot_hi_model(save=True):
    """Figure 1: HI model properties vs redshift."""
    cosmo.init()
    setup_style()

    z_arr = np.linspace(0.01, 3.0, 30)
    omega = np.array([hi.Omega_HI(z) for z in z_arr])
    bias = np.array([hi.b_HI(z) for z in z_arr])
    Tb = np.array([hi.T_bar_b(z) for z in z_arr])

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    axes[0].semilogy(z_arr, omega)
    axes[0].set_ylabel(r'$\Omega_{\rm HI}(z)$')
    axes[0].set_xlabel('Redshift $z$')
    axes[0].axhline(4e-4, ls='--', color='gray', alpha=0.5, label='ALFALFA')
    axes[0].legend()

    axes[1].plot(z_arr, bias)
    axes[1].set_ylabel(r'$b_{\rm HI}(z)$')
    axes[1].set_xlabel('Redshift $z$')

    axes[2].plot(z_arr, Tb * 1000)  # convert to uK
    axes[2].set_ylabel(r'$\bar{T}_b(z)$ [$\mu$K]')
    axes[2].set_xlabel('Redshift $z$')

    fig.suptitle('HI Model Properties (Padmanabhan+2017)', fontsize=13)
    fig.tight_layout()

    if save:
        _savefig(fig, 'fig1_hi_model')
    return fig


def plot_ugrb_spectrum(save=True):
    """Figure 2: Unresolved gamma-ray background mean intensity."""
    cosmo.init()
    setup_style()

    E_arr = cfg.FERMI_E_B
    sources = ['BL_Lac', 'FSRQ', 'mAGN', 'SFG']
    colors = {'BL_Lac': 'C0', 'FSRQ': 'C1', 'mAGN': 'C2', 'SFG': 'C3'}

    fig, ax = plt.subplots(figsize=(8, 5))

    total = np.zeros_like(E_arr)
    for src in sources:
        I_arr = np.array([astro.mean_intensity(E, src, z_max=4.0, n_z=20)
                          for E in E_arr])
        ax.loglog(E_arr, E_arr**2 * I_arr, label=src, color=colors[src])
        total += I_arr

    ax.loglog(E_arr, E_arr**2 * total, 'k-', lw=2, label='Total')

    # Ackermann+2015 IGRB reference band
    ax.axhspan(1e-8, 3e-7, alpha=0.1, color='gray', label='IGRB (Ackermann+2015)')

    ax.set_xlabel('Energy $E$ [GeV]')
    ax.set_ylabel(r'$E^2 \, dI/dE$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')
    ax.set_title('Unresolved Gamma-Ray Background')
    ax.legend(loc='upper right')
    ax.set_xlim(0.5, 1000)
    fig.tight_layout()

    if save:
        _savefig(fig, 'fig2_ugrb_spectrum')
    return fig


def plot_ebl_pppc(save=True):
    """Figure 3: EBL opacity and PPPC4DMID photon spectra."""
    cosmo.init()
    setup_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: EBL opacity
    E_arr = np.logspace(-0.5, 3.5, 100)  # 0.3 to 3000 GeV
    for z, ls in [(0.3, '-'), (0.5, '--'), (1.0, '-.'), (2.0, ':')]:
        tau_arr = ebl.tau(E_arr, z)
        ax1.semilogy(E_arr, tau_arr, ls=ls, label=f'z={z}')

    ax1.axhline(1.0, ls=':', color='gray', alpha=0.3)
    ax1.set_xlabel('Energy $E$ [GeV]')
    ax1.set_ylabel(r'$\tau(E, z)$')
    ax1.set_title('EBL Optical Depth (Dominguez+2011)')
    ax1.set_xscale('log')
    ax1.set_ylim(1e-3, 100)
    ax1.legend()

    # Right: PPPC4DMID spectra
    x_arr = np.logspace(-5, -0.01, 200)
    for m, color in [(10, 'C0'), (100, 'C1'), (1000, 'C2')]:
        dNdx = pppc4dmid.dNdx(x_arr, m, 'bb')
        ax2.loglog(x_arr, x_arr**2 * dNdx, color=color, label=f'$m_\\chi={m}$ GeV')

    ax2.set_xlabel('$x = E / m_\\chi$')
    ax2.set_ylabel(r'$x^2 \, dN/dx$')
    ax2.set_title(r'PPPC4DMID Photon Yield ($b\bar{b}$)')
    ax2.legend()
    ax2.set_xlim(1e-5, 1)

    fig.tight_layout()
    if save:
        _savefig(fig, 'fig3_ebl_pppc')
    return fig


def plot_noise_beam(save=True):
    """Figure 4: Instrument noise and beam functions."""
    setup_style()

    ell_arr = np.logspace(1, 3.3, 100)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Fermi noise/beam at different energies
    for ie, color in [(1, 'C0'), (5, 'C1'), (10, 'C2')]:
        E = cfg.FERMI_E_B[ie]
        B = nm.beam_fermi(ell_arr, E)
        N = nm.noise_fermi(ie)
        ax1.semilogy(ell_arr, N / B**2, color=color, label=f'E={E:.1f} GeV')

    ax1.set_xlabel(r'Multipole $\ell$')
    ax1.set_ylabel(r'$N^\gamma_\ell / (B^\gamma_\ell)^2$')
    ax1.set_title('Fermi-LAT Effective Noise')
    ax1.legend()
    ax1.set_xscale('log')

    # Right: Radio noise for different telescopes
    for tel, band, color, ls in [
        ('MeerKAT', 'UHF', 'C0', '-'),
        ('SKA1', 'Band2', 'C1', '--'),
        ('SKA2', 'Band2', 'C2', '-.'),
    ]:
        N_radio = nm.noise_radio_combined(ell_arr, tel, band)
        z_mid = 0.5 * (cfg.RADIO_TELESCOPES[tel]['bands'][band]['z_min'] +
                        cfg.RADIO_TELESCOPES[tel]['bands'][band]['z_max'])
        B_radio = nm.beam_radio(ell_arr, z_mid,
                                cfg.RADIO_TELESCOPES[tel]['d_dish_m'])
        ax2.semilogy(ell_arr, N_radio / B_radio**2, color=color, ls=ls,
                     label=f'{tel} {band}')

    ax2.set_xlabel(r'Multipole $\ell$')
    ax2.set_ylabel(r'$N^{\rm HI}_\ell / (B^{\rm HI}_\ell)^2$ [mK$^2$ sr]')
    ax2.set_title('Radio Effective Noise')
    ax2.legend()
    ax2.set_xscale('log')

    fig.tight_layout()
    if save:
        _savefig(fig, 'fig4_noise_beam')
    return fig


# =========================================================================
# Tier 2: Moderate cost (~30s each)
# =========================================================================

def plot_angular_power(telescope='MeerKAT', band='UHF', E_GeV=5.0, save=True):
    """Figure 5: Angular cross-power spectra C_ell by source class."""
    cosmo.init()
    setup_style()

    tel = cfg.RADIO_TELESCOPES[telescope]
    z_min = tel['bands'][band]['z_min']
    z_max = tel['bands'][band]['z_max']

    ell_arr = np.unique(np.logspace(1, 2.7, 30).astype(int)).astype(float)

    fig, ax = plt.subplots(figsize=(8, 6))

    colors = {'BL_Lac': 'C0', 'FSRQ': 'C1', 'mAGN': 'C2', 'SFG': 'C3', 'DM': 'C4'}

    result = ap.C_ell_HI_gamma(
        ell_arr, E_GeV, z_min, z_max, telescope, band,
        m_chi_GeV=100.0, sigma_v=cfg.SIGMA_V_THERMAL,
        include_DM=True, n_z=10, n_k_M=15
    )

    for key in ['BL_Lac', 'FSRQ', 'mAGN', 'SFG', 'DM']:
        if key in result:
            C = result[key]
            nonzero = np.abs(C) > 0
            if np.any(nonzero):
                y = ell_arr[nonzero] * (ell_arr[nonzero] + 1) * np.abs(C[nonzero]) / (2 * np.pi)
                ax.loglog(ell_arr[nonzero], y, label=key, color=colors.get(key, 'gray'))

    total = result['total']
    nonzero = np.abs(total) > 0
    if np.any(nonzero):
        y = ell_arr[nonzero] * (ell_arr[nonzero] + 1) * np.abs(total[nonzero]) / (2 * np.pi)
        ax.loglog(ell_arr[nonzero], y, 'k-', lw=2, label='Total')

    ax.set_xlabel(r'Multipole $\ell$')
    ax.set_ylabel(r'$\ell(\ell+1) C_\ell / 2\pi$')
    ax.set_title(f'Cross-Power Spectrum: {telescope} {band}, E={E_GeV} GeV')
    ax.legend()

    fig.tight_layout()
    if save:
        _savefig(fig, f'fig5_Cl_{telescope}_{band}_{E_GeV}GeV')
    return fig


def plot_window_functions(E_GeV=5.0, m_chi=100.0, save=True):
    """Figure 6: Window functions vs redshift."""
    cosmo.init()
    setup_style()

    z_arr = np.linspace(0.05, 3.0, 40)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # HI window (for MeerKAT UHF band)
    W_hi = np.array([hi.W_HI(z, 0.4, 1.45) for z in z_arr])
    ax1.plot(z_arr, W_hi, 'k-', label=r'$W_{\rm HI}$ (MeerKAT UHF)')
    ax1.set_ylabel(r'$W_{\rm HI}$ [mK]')
    ax1.set_xlabel('Redshift $z$')
    ax1.set_title('HI Window Function')
    ax1.legend()

    # Gamma windows
    for src, color in [('BL_Lac', 'C0'), ('FSRQ', 'C1'), ('SFG', 'C3')]:
        W_g = np.array([astro.W_gamma_astro(E_GeV, z, src) for z in z_arr])
        nonzero = W_g > 0
        if np.any(nonzero):
            ax2.semilogy(z_arr[nonzero], W_g[nonzero], color=color, label=src)

    W_dm = np.array([dm.W_gamma_DM(E_GeV, z, m_chi) for z in z_arr])
    nonzero = W_dm > 0
    if np.any(nonzero):
        ax2.semilogy(z_arr[nonzero], W_dm[nonzero], 'C4--',
                     label=f'DM ($m_\\chi$={m_chi} GeV)')

    ax2.set_ylabel(r'$W_\gamma$ [(Mpc/h)$^{-3}$ s$^{-1}$ GeV$^{-1}$]')
    ax2.set_xlabel('Redshift $z$')
    ax2.set_title(f'Gamma-Ray Windows (E={E_GeV} GeV)')
    ax2.legend()

    fig.tight_layout()
    if save:
        _savefig(fig, 'fig6_window_functions')
    return fig


# =========================================================================
# Tier 3: Expensive (cached)
# =========================================================================

def plot_snr_table(save=True, recompute=False):
    """Figure 7: SNR forecast summary table."""
    cosmo.init()
    setup_style()

    configs = [
        ('MeerKAT', 'UHF', 3.7),
        ('MeerKAT', 'L', 2.0),
        ('SKA1', 'Band1', None),
        ('SKA1', 'Band2', 5.7),
        ('SKA2', 'Band1', 8.2),
        ('SKA2', 'Band2', None),
    ]

    cache = _load_cache('snr_results')
    if cache is not None and not recompute:
        snr_data = cache
    else:
        snr_data = {}
        for tel, band, target in configs:
            key = f'{tel}_{band}'
            print(f'  Computing SNR for {tel} {band}...')
            snr = stats.compute_SNR(tel, band, fermissimo=False,
                                    ell_min=10, ell_max=500, n_ell=25,
                                    n_z=10, n_M=15)
            snr_data[key] = {'snr': snr, 'target': target}
        _save_cache('snr_results', snr_data)

    fig, ax = plt.subplots(figsize=(10, 5))

    labels = []
    snr_vals = []
    targets = []
    for tel, band, target in configs:
        key = f'{tel}_{band}'
        labels.append(f'{tel}\n{band}')
        snr_vals.append(snr_data[key]['snr'])
        targets.append(target)

    x = np.arange(len(labels))
    bars = ax.bar(x, snr_vals, color='steelblue', alpha=0.8, label='This work')

    # Overlay Pinetti targets
    for i, t in enumerate(targets):
        if t is not None:
            ax.plot(i, t, 'r*', ms=12, zorder=5)

    ax.scatter([], [], c='r', marker='*', s=100, label='Pinetti+2020')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Signal-to-Noise Ratio')
    ax.set_title('SNR Forecasts: HI x Gamma-Ray Cross-Correlation')
    ax.legend()
    ax.axhline(3.0, ls=':', color='gray', alpha=0.3, label='3σ threshold')

    fig.tight_layout()
    if save:
        _savefig(fig, 'fig7_snr_table')
    return fig


def plot_exclusion_curves(save=True, recompute=False):
    """Figure 8: DM exclusion curves (sigma_v vs m_chi)."""
    cosmo.init()
    setup_style()

    cache = _load_cache('exclusion_results')
    if cache is not None and not recompute:
        exc_data = cache
    else:
        exc_data = {}
        m_arr = np.logspace(1, 3.5, 15).tolist()  # 10 to ~3000 GeV
        for tel, band in [('MeerKAT', 'L'), ('SKA1', 'Band2'), ('SKA2', 'Band2')]:
            key = f'{tel}_{band}'
            print(f'  Computing exclusion for {tel} {band}...')
            m, sv = stats.exclusion_curve(
                tel, band, channel='bb', CL='95',
                m_chi_arr=np.array(m_arr),
                n_ell=15, n_z=8, n_M=10
            )
            exc_data[key] = {
                'm_chi': m.tolist(),
                'sigma_v': sv.tolist(),
            }
        _save_cache('exclusion_results', exc_data)

    fig, ax = plt.subplots(figsize=(8, 6))

    colors = {'MeerKAT_L': 'C0', 'SKA1_Band2': 'C1', 'SKA2_Band2': 'C2'}
    labels = {'MeerKAT_L': 'MeerKAT L', 'SKA1_Band2': 'SKA1 Band2', 'SKA2_Band2': 'SKA2 Band2'}

    for key in exc_data:
        m = np.array(exc_data[key]['m_chi'])
        sv = np.array(exc_data[key]['sigma_v'])
        valid = np.isfinite(sv) & (sv > 0)
        if np.any(valid):
            ax.loglog(m[valid], sv[valid], color=colors.get(key, 'gray'),
                     label=labels.get(key, key))

    # Thermal relic line
    ax.axhline(cfg.SIGMA_V_THERMAL, ls='--', color='k', alpha=0.5,
               label=r'Thermal relic $\langle\sigma v\rangle$')

    ax.set_xlabel(r'$m_\chi$ [GeV]')
    ax.set_ylabel(r'$\langle\sigma v\rangle$ [cm$^3$/s]')
    ax.set_title(r'95% CL Upper Limits ($b\bar{b}$ channel)')
    ax.legend()
    ax.set_xlim(10, 5000)
    ax.set_ylim(1e-28, 1e-22)

    fig.tight_layout()
    if save:
        _savefig(fig, 'fig8_exclusion_curves')
    return fig


# =========================================================================
# Master function
# =========================================================================

def make_all_plots(quick=False):
    """Generate all pipeline figures.

    Parameters
    ----------
    quick : bool
        If True, skip expensive Tier 3 plots (SNR table, exclusion curves).
    """
    cosmo.init()
    print("Generating pipeline figures...")
    print()

    # Tier 1 (fast)
    print("[Tier 1] Fast validation plots")
    plot_hi_model()
    plot_ugrb_spectrum()
    plot_ebl_pppc()
    plot_noise_beam()
    print()

    # Tier 2 (moderate)
    print("[Tier 2] Angular power spectra and windows")
    plot_angular_power('MeerKAT', 'UHF', 5.0)
    plot_window_functions()
    print()

    if not quick:
        # Tier 3 (expensive, cached)
        print("[Tier 3] SNR forecasts and exclusion curves")
        plot_snr_table()
        plot_exclusion_curves()
        print()

    print("All plots complete.")
    print(f"Output directory: {_plot_dir}")
