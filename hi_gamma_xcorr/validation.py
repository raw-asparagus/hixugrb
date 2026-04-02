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
    print(f"  tau(100 GeV, z=1) = {tau100:.2f} (Dominguez: ~0.7)")
    print(f"  Delta^2(z=0, no boost) = {Delta2:.2e} (expect 1e4-1e5)")
    print()

    # Phase 6: Noise
    print("Phase 6 Validation:")
    Tsys = nm.T_sys(1000)
    print(f"  T_sys(1 GHz) = {Tsys:.1f} K")
    print(f"  Fermi N_gamma[0] = {nm.noise_fermi(0):.3e}")
    print()

    # Dimensional analysis
    print("Window Function Dimensional Analysis:")
    z_ref, E_ref = 0.5, 5.0
    W_hi = hi.W_HI(z_ref, 0.4, 1.45)
    W_dm = dm.W_gamma_DM(E_ref, z_ref, 100.0)
    W_bl = astro.W_gamma_astro(E_ref, z_ref, 'BL_Lac')
    print(f"  W_HI(z=0.5) = {W_hi:.3e} mK")
    print(f"  W_DM(E=5, z=0.5, m=100, thermal) = {W_dm:.3e} [(Mpc/h)^-3 s^-1 GeV^-1]")
    print(f"    (same units as W_astro; DM should be ~100x weaker than BL Lac)")
    print(f"  W_BL_Lac(E=5, z=0.5) = {W_bl:.3e} [ph/s/Mpc^3/GeV/sr]")
    # Quick UGRB sanity check
    I_total = sum(astro.mean_intensity(1.0, src, z_max=3.0, n_z=15)
                  for src in ['BL_Lac', 'FSRQ', 'mAGN', 'SFG'])
    print(f"  Total UGRB I(1 GeV) = {I_total:.2e} ph/cm^2/s/GeV/sr")
    print(f"    (Ackermann+2015 IGRB: ~1e-7; total ~10× higher due to BL Lac normalization)")
    print()

    # DM linearity check: C_l^DM should scale with sigma_v
    print("DM sigma_v linearity check:")
    ell_test = np.array([100.])
    C1 = ap.C_ell_HI_gamma(ell_test, E_ref, 0.4, 1.45, 'MeerKAT', 'UHF',
                            m_chi_GeV=100.0, sigma_v=3e-26,
                            source_classes=[], include_DM=True,
                            n_z=5, n_k_M=10)['DM'][0]
    C2 = ap.C_ell_HI_gamma(ell_test, E_ref, 0.4, 1.45, 'MeerKAT', 'UHF',
                            m_chi_GeV=100.0, sigma_v=3e-25,
                            source_classes=[], include_DM=True,
                            n_z=5, n_k_M=10)['DM'][0]
    if C1 > 0 and C2 > 0:
        ratio = C2 / C1
        print(f"  C_l(10x sigma_v) / C_l(1x sigma_v) = {ratio:.2f} (expect ~10)")
    else:
        print(f"  C_l values: {C1:.2e}, {C2:.2e} (check if zero)")
    print()

    print("=" * 60)
    print("Validation complete.")
    return {'phase1': r1, 'phase2': r2, 'phase3': r3}


# ---------------------------------------------------------------------------
# Step 5: Comprehensive scholarly validation
# ---------------------------------------------------------------------------

def validate_step5():
    """Comprehensive validation against Pinetti et al. (2020) and literature."""
    cosmo.init()
    from . import pppc4dmid, ebl, statistics as stat_mod

    print("=" * 70)
    print("Step 5: Comprehensive Validation Against Scholarly Sources")
    print("=" * 70)

    results = {}

    # --- A. PPPC4DMID cross-checks ---
    print("\nA. PPPC4DMID Photon Yields")
    for m, ch, lo, hi_exp in [(100, 'bb', 20, 40), (100, 'tautau', 1, 8),
                               (100, 'WW', 15, 35), (10, 'bb', 10, 25),
                               (1000, 'bb', 50, 100)]:
        mult = pppc4dmid.total_multiplicity(m, ch)
        ok = lo <= mult <= hi_exp
        tag = "PASS" if ok else "WARN"
        print(f"  [{tag}] N_gamma(m={m:4d}, {ch:7s}) = {mult:5.1f}  (expect {lo}-{hi_exp})")
        results[f'pppc_{ch}_{m}'] = (mult, ok)

    # --- B. EBL opacity ---
    print("\nB. EBL Opacity (Dominguez)")
    ebl_checks = [
        (10,   0.5,  0.0,  0.05, "transparent"),
        (100,  0.5,  0.05, 0.5,  "modest"),
        (100,  1.0,  0.3,  1.5,  "moderate"),
        (1000, 0.5,  3.0,  15.0, "opaque"),
        (1000, 1.0,  10.0, 50.0, "very opaque"),
    ]
    for E, z, lo, hi_exp, desc in ebl_checks:
        tau_val = ebl.tau(np.array([float(E)]), z)[0]
        ok = lo <= tau_val <= hi_exp
        tag = "PASS" if ok else "WARN"
        print(f"  [{tag}] tau({E:4d} GeV, z={z:.1f}) = {tau_val:6.3f}  ({desc}, expect {lo}-{hi_exp})")
        results[f'ebl_{E}_{z}'] = (tau_val, ok)

    # --- C. HI model trends ---
    print("\nC. HI Model Redshift Evolution")
    z_arr = [0.0, 0.5, 1.0, 2.0]
    omega_prev = 0
    b_prev = 0
    for z in z_arr:
        omega = hi.Omega_HI(z)
        b = hi.b_HI(z)
        Tb = hi.T_bar_b(z)
        b_ok = b > b_prev or z == 0.0  # bias should increase with z
        tag = "PASS" if b_ok else "WARN"
        print(f"  [{tag}] z={z:.1f}: Omega_HI={omega:.2e}, b_HI={b:.3f}, T_b={Tb*1000:.0f} uK")
        b_prev = b
        omega_prev = omega

    # --- D. Source counts ---
    print("\nD. Astrophysical Source Counts")
    from scipy.integrate import quad
    for src, n_expected_lo, n_expected_hi in [
        ('FSRQ', 1e-10, 1e-7), ('BL_Lac', 1e-8, 1e-4),
        ('mAGN', 1e-9, 1e-5), ('SFG', 1e-10, 1e-6)
    ]:
        params = cfg.ASTRO_SOURCES[src]
        n, _ = quad(lambda lnL: astro.glf(np.exp(lnL), 0.0, src) * np.exp(lnL),
                    np.log(params['L_min']), np.log(params['L_max']), limit=100)
        ok = n_expected_lo <= n <= n_expected_hi
        tag = "PASS" if ok else "WARN"
        print(f"  [{tag}] n({src:8s}, z=0) = {n:.2e} Mpc^{{-3}}  (expect {n_expected_lo:.0e}-{n_expected_hi:.0e})")

    # --- E. Noise model ---
    print("\nE. Noise Model Checks")
    Tsys_1GHz = nm.T_sys(1000)
    ok = 20 <= Tsys_1GHz <= 40
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] T_sys(1 GHz) = {Tsys_1GHz:.1f} K  (expect 20-40)")

    for ie in [0, 5, 11]:
        N = nm.noise_fermi(ie)
        N_expected = cfg.FERMI_N_GAMMA[ie]
        ok = abs(N - N_expected) < 1e-25
        tag = "PASS" if ok else "FAIL"
        print(f"  [{tag}] N_gamma[{ie}] = {N:.3e}  (Table 2: {N_expected:.3e})")

    # --- F. SNR Table 4 (partial) ---
    print("\nF. SNR Forecasts (Pinetti Table 4)")
    snr_configs = [
        ('MeerKAT', 'UHF', 3.7),
        ('SKA1', 'Band2', 5.7),
        ('SKA2', 'Band2', 8.2),
    ]
    for tel, band, target in snr_configs:
        import time
        t0 = time.time()
        snr = stat_mod.compute_SNR(
            tel, band, fermissimo=False,
            ell_min=10, ell_max=500, n_ell=20, n_z=8, n_M=12
        )
        dt = time.time() - t0
        ratio = snr / target
        ok = 0.2 <= ratio <= 5.0  # within factor of 5
        tag = "PASS" if ok else "WARN"
        print(f"  [{tag}] {tel:8s} {band:5s}: SNR = {snr:6.2f}  (target {target:.1f}, ratio {ratio:.2f}) [{dt:.0f}s]")
        results[f'snr_{tel}_{band}'] = (snr, target, ratio)

    # --- Summary ---
    n_pass = sum(1 for v in results.values() if (isinstance(v, tuple) and len(v) >= 2 and v[-1]))
    n_total = len(results)
    print(f"\n{'='*70}")
    print(f"Summary: {n_pass}/{n_total} checks passed")
    print(f"{'='*70}")
    return results
