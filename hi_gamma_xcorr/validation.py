"""Validation functions to reproduce Pinetti et al. (2020) results.

Each function reproduces a specific figure or table from the paper.
"""

import numpy as np

from . import config as cfg
from . import cosmology as cosmo
from . import halo_model as hm
from . import hi_model as hi
from . import dm_model as dm
from . import astro_sources as astro
from . import angular_power as ap
from . import noise_model as nm
from . import statistics as stats


def validate_phase1():
    """Validate cosmological backbone (Phase 1)."""
    cosmo.init()
    results = {}

    sig8 = cosmo.sigma_R(8.0, 0.0)
    results['sigma_8'] = sig8
    results['sigma_8_error_pct'] = abs(sig8 - cfg.SIGMA_8) / cfg.SIGMA_8 * 100

    results['H0'] = cosmo.H(0.0)
    results['chi_z1'] = cosmo.chi(1.0)
    results['D_z0'] = cosmo.growth_factor(0.0)
    results['D_z1'] = cosmo.growth_factor(1.0)

    print("Phase 1 Validation:")
    print(f"  sigma_8 = {sig8:.6f} (error: {results['sigma_8_error_pct']:.4f}%)")
    print(f"  H(0) = {results['H0']:.2f} km/s/Mpc")
    print(f"  chi(z=1) = {results['chi_z1']:.0f} Mpc/h")
    print(f"  D(0) = {results['D_z0']:.6f}, D(1) = {results['D_z1']:.4f}")
    return results


def validate_phase2():
    """Validate halo model (Phase 2)."""
    cosmo.init()
    results = {}

    results['mass_norm'] = hm.check_mass_normalization(z=0.0)
    results['bias_norm'] = hm.check_bias_normalization(z=0.0)
    results['c_1e12'] = float(hm.concentration(np.array([1e12]), 0.0)[0])

    u0 = hm.u_nfw(np.array([1e-6]), 1e12, z=0.0)[0]
    results['u_nfw_k0'] = u0

    print("Phase 2 Validation:")
    print(f"  Mass norm = {results['mass_norm']:.4f} (expect ~0.6-0.7)")
    print(f"  Bias norm = {results['bias_norm']:.4f}")
    print(f"  c(1e12, z=0) = {results['c_1e12']:.2f} (expect ~8)")
    print(f"  u_NFW(k→0) = {results['u_nfw_k0']:.8f} (expect 1)")
    return results


def validate_phase3():
    """Validate HI model (Phase 3)."""
    cosmo.init()
    results = {}

    results['Omega_HI_z0'] = hi.Omega_HI(0.0)
    results['b_HI_z0'] = hi.b_HI(0.0)
    results['Tbar_z0'] = hi.T_bar_b(0.0)

    print("Phase 3 Validation:")
    print(f"  Omega_HI(z=0) = {results['Omega_HI_z0']:.2e} (expect ~4e-4)")
    print(f"  b_HI(z=0) = {results['b_HI_z0']:.4f} (expect ~0.7-0.85)")
    print(f"  T_bar_b(z=0) = {results['Tbar_z0']*1000:.1f} μK (expect ~50-60)")
    return results


def validate_all():
    """Run all validation checks."""
    print("=" * 60)
    print("HI × Gamma-Ray Pipeline Validation")
    print("=" * 60)
    print()

    r1 = validate_phase1()
    print()
    r2 = validate_phase2()
    print()
    r3 = validate_phase3()
    print()

    # Phase 4: DM model
    print("Phase 4 Validation:")
    from . import pppc4dmid, ebl
    mult = pppc4dmid.total_multiplicity(100.0, 'bb')
    tau100 = ebl.tau(np.array([100.0]), 1.0)[0]
    Delta2 = dm.clumping_factor(0.0, n_M=50, boost_scenario='none')
    print(f"  bb-bar multiplicity (100 GeV) = {mult:.1f} (expect 25-30)")
    print(f"  tau(100 GeV, z=1) = {tau100:.2f} (expect 2-5)")
    print(f"  Delta^2(z=0, no boost) = {Delta2:.2e} (expect 1e4-1e5)")
    print()

    # Phase 6: Noise
    print("Phase 6 Validation:")
    Tsys = nm.T_sys(1000)
    print(f"  T_sys(1 GHz) = {Tsys:.1f} K")
    print(f"  Fermi N_gamma[0] = {nm.noise_fermi(0):.3e}")
    print()

    print("=" * 60)
    print("Validation complete.")
    return {'phase1': r1, 'phase2': r2, 'phase3': r3}
