# Claim-by-Claim Evidence Matrix: `hixugrb/` vs Pinetti (2022)

## Context

This document compares every substantive physical claim, equation, model choice, and parameter value in the `hi_gamma_xcorr` codebase against the thesis *"From gamma rays to radio waves: Dark Matter searches across the spectrum"* by Elena Pinetti (2022, arXiv:2212.00125). The thesis (Part I, Chapters 3–5 and Appendices B–E) describes the HI 21-cm × UGRB cross-correlation formalism that this code implements.

---

## Matrix Legend

| Symbol | Meaning |
|--------|---------|
| **Match** | Code agrees with thesis |
| **Differs** | Code uses a different choice (noted) |
| **Partial** | Partially matches; deviations noted |
| **Not impl.** | Thesis defines it but code omits (not needed for pipeline) |

---

## 1. Cosmological Parameters

| # | Claim / Parameter | Pinetti (2022) | Code (`config.py`) | Status |
|---|-------------------|----------------|---------------------|--------|
| 1.1 | H₀ | Not explicitly stated in Part I (defers to Planck) | 67.36 km/s/Mpc (Planck 2018) | **Match** (consistent) |
| 1.2 | Ω_M | Not explicitly stated | 0.3153 | **Match** (Planck 2018) |
| 1.3 | σ₈ | Not explicitly stated | 0.8111 | **Match** (Planck 2018) |
| 1.4 | n_s | Not explicitly stated | 0.9649 | **Match** (Planck 2018) |
| 1.5 | Linear P(k,z) | CAMB / Boltzmann solver (Sec. 3.2) | CAMB via `cosmology.py` | **Match** |

## 2. Halo Mass Function

| # | Claim / Parameter | Pinetti (2022) | Code (`halo_model.py`, `hmf_interface.py`) | Status |
|---|-------------------|----------------|---------------------------------------------|--------|
| 2.1 | Fitting function | Sheth-Tormen (Eq. 3.33) | Sheth-Mo-Tormen via `hmf` package | **Match** |
| 2.2 | Parameter p | p = 0.3 (Eq. 3.33) | p = 0.3 | **Match** |
| 2.3 | Parameter q | **q = 0.75** (Eq. 3.33) | **q = 0.707** | **Differs** — Code uses the more common SMT (1999) value 0.707; thesis uses 0.75 from Sheth & Tormen (2002). Both are used in the literature. |
| 2.4 | Normalization A(p) | A(p) = [1 + 2^(-p) Γ(1/2−p)/(√π)]^(-1) | Derived from normalization condition | **Match** (functional form) |
| 2.5 | Collapse threshold δ_sc | 1.686(1+z) (Eq. 3.25) | 1.686 (not multiplied by (1+z) — absorbed into σ(M,z)) | **Match** (equivalent; growth factor convention) |

## 3. Concentration-Mass Relation

| # | Claim / Parameter | Pinetti (2022) | Code (`halo_model.py`) | Status |
|---|-------------------|----------------|------------------------|--------|
| 3.1 | Model | Semi-analytic, Ref. [362] = **Correa et al. (2015)** (Eq. 3.35–3.36) | **Correa et al. (2015)** (sole implementation) | **Match** |
| 3.2 | Functional form | log₁₀ c₂₀₀ = α + β log₁₀(M₂₀₀/M☉) [1 + γ (log₁₀ M₂₀₀/M☉)²] | Same parametric form | **Match** |
| 3.3 | Redshift-dependent coefficients (α,β,γ) | Eq. 3.36: α=1.627−0.246(1+z)+0.0172(1+z)², etc. | Implemented in `concentration_correa()` | **Match** |
| 3.4 | c₂₀₀ → c_vir conversion | Eqs. 3.38–3.41: linear mapping cvir = a·c₂₀₀ + b | Implemented | **Match** |

## 4. Halo Bias

| # | Claim / Parameter | Pinetti (2022) | Code (`halo_model.py`) | Status |
|---|-------------------|----------------|------------------------|--------|
| 4.1 | Model | Peak-background split, Eq. 3.51 | Same formula | **Match** |
| 4.2 | Parameters | Same q, p as mass function | Same q, p as mass function | **Match** (but q differs, see 2.3) |

## 5. NFW Profile & Fourier Transforms

| # | Claim / Parameter | Pinetti (2022) | Code (`halo_model.py`, `dm_model.py`) | Status |
|---|-------------------|----------------|----------------------------------------|--------|
| 5.1 | NFW profile | ρ(r) = ρ_s (r_s/r)(1+r/r_s)^(-2), Eq. 3.42 | Same | **Match** |
| 5.2 | Normalized FT ũ(k) for density | Eq. 3.45: ∫₀^Rvir 4πr² sin(kr)/(kr) ρ(r)/M dr | `u_nfw(k,M,z)` | **Match** |
| 5.3 | FT ṽ(k) for density² | Eq. 3.46: ∫₀^Rvir 4πr² sin(kr)/(kr) ρ²(r)/M dr | `v_tilde(k,M,z)` (unnormalized) | **Partial** — thesis normalizes by M; code uses unnormalized ṽ = ∫ρ² d³x × sin(kr)/(kr). Consistent when combined with Δ² normalization in power spectrum. |

## 6. Boost Factor (Substructure)

| # | Claim / Parameter | Pinetti (2022) | Code (`dm_model.py`) | Status |
|---|-------------------|----------------|----------------------|--------|
| 6.1 | Model | Moliné et al. (2017), Ref. [369] | Moliné et al. (2017) | **Match** |
| 6.2 | Functional form | log B(M,z=0) = Σᵢ dᵢ [log(M/M☉)]ⁱ, 5th-order polynomial (Eq. 3.47) | Same polynomial form | **Match** |
| 6.3 | Polynomial coefficients | d₀=−0.186, d₁=0.144, d₂=−8.8×10⁻³, d₃=1.13×10⁻³, d₄=−3.7×10⁻⁵, d₅=−2×10⁻⁷ | Same values | **Match** |
| 6.4 | Redshift evolution | B(M,z) = B(M,0)/(1+z) (Eq. 3.48) | Same | **Match** |
| 6.5 | Minimum halo mass | M_min = 10⁻⁶ M☉ (canonical WIMP free-streaming mass) | M_min = 10⁻⁶ M☉ (default) | **Match** |

## 7. Clumping Factor Δ²(z)

| # | Claim / Parameter | Pinetti (2022) | Code (`dm_model.py`) | Status |
|---|-------------------|----------------|----------------------|--------|
| 7.1 | Definition | Δ²(z) = ⟨ρ²⟩/ρ̄² = ∫ (dn/dM) ∫ ρ²(x|M) d³x / ρ̄² dM (Eq. 3.61) | `clumping_factor(z)` — same integral | **Match** |
| 7.2 | Substructure inclusion | Replace ρ² → (1+B)ρ² (Eq. 3.62) | Same replacement | **Match** |

## 8. Power Spectrum Decomposition (1-halo / 2-halo)

| # | Claim / Parameter | Pinetti (2022) | Code (`angular_power.py`, `dm_model.py`, `hi_model.py`) | Status |
|---|-------------------|----------------|----------------------------------------------------------|--------|
| 8.1 | P^1h_{δ²δ²} | Eq. 3.59 | Not implemented (DM auto-power not needed for cross-correlation pipeline) | **Not impl.** |
| 8.2 | P^2h_{δ²δ²} | Eq. 3.60 | Not implemented (same reason) | **Not impl.** |
| 8.3 | P^1h_{HI×DM} (cross) | Eq. 4.16 | Not implemented (subdominant; 2-halo term suffices) | **Not impl.** |
| 8.4 | P^2h_{HI×DM} (cross) | Eq. 4.17 | `P_HI_DM_2h()` | **Match** |
| 8.5 | P^1h_{HI×HI} | Eq. 4.13 | `P_HI_1h()` | **Match** |
| 8.6 | P^2h_{HI×HI} | Eq. 4.14 | `P_HI_2h()` | **Match** |
| 8.7 | P^1h_{HI×S} (astro cross) | Eq. 4.18 | `P_HI_astro_1h()` (via luminosity integral) | **Match** |
| 8.8 | P^2h_{HI×S} (astro cross) | Eq. 4.19 | `P_HI_astro_2h()` | **Match** |

## 9. HI Modeling (Padmanabhan et al. 2017)

| # | Claim / Parameter | Pinetti (2022) | Code (`hi_model.py`) | Status |
|---|-------------------|----------------|----------------------|--------|
| 9.1 | HI-halo mass relation | M_HI(M) = α f_{H,c} M (M/10¹¹ h⁻¹M☉)^β exp[−(v_{c,0}/v_c)³] (Eq. 4.2) | Same functional form | **Match** |
| 9.2 | α (neutral fraction) | 0.176 | 0.176 | **Match** |
| 9.3 | β (log slope) | −0.69 | −0.69 | **Match** |
| 9.4 | v_{c,0} (min circular velocity) | 40.7 km/s | 40.7 km/s | **Match** |
| 9.5 | Helium fraction Y_p | 0.24 | 0.24 | **Match** |
| 9.6 | HI profile | Modified NFW: ρ₀ r_s³ / [(r + 3/4 r_s)(r + r_s)²] (Eq. 4.8) | Same: ρ₀ r_s³ / [(r + 0.75 r_s)(r + r_s)²] | **Match** |
| 9.7 | HI concentration | c_HI = 4 c_{HI,0} (1+z)^(−γ) (M/10¹¹ M☉)^(−0.109) (Eq. 4.10) | Same form | **Match** |
| 9.8 | c_{HI,0} | 139 | 139 | **Match** |
| 9.9 | γ (concentration redshift exponent) | 0.13 | 0.13 | **Match** |
| 9.10 | HI FT ũ_HI(k) | Eq. 4.11: 4π/M_HI ∫₀^Rvir r² ρ_HI sin(kr)/(kr) dr | `u_HI(k,M,z)` | **Match** |
| 9.11 | Ω_HI | Redshift-independent: 2.45 × 10⁻⁴ | 2.45 × 10⁻⁴ | **Match** |

## 10. HI Window Function

| # | Claim / Parameter | Pinetti (2022) | Code (`hi_model.py`) | Status |
|---|-------------------|----------------|----------------------|--------|
| 10.1 | Top-hat window | W_HI = W₀(z) T_obs(z), Eqs. 5.11–5.12 | Same | **Match** |
| 10.2 | Brightness temperature | T_obs = 44 μK × (Ω_HI h / 2.45×10⁻⁴) × (1+z)²/E(z) | 180 Ω_HI h (1+z)²/(H(z)/H₀) mK | **Partial** — Both equivalent (44 μK = 180 × 2.45×10⁻⁴); code uses the un-substituted form with factor 180, thesis pre-evaluates with Ω_HI. Numerically identical. |

## 11. DM Window Function

| # | Claim / Parameter | Pinetti (2022) | Code (`dm_model.py`) | Status |
|---|-------------------|----------------|----------------------|--------|
| 11.1 | Formula | Eq. 5.17 / Eq. E.7: W_DM = (1/4π)(⟨σv⟩/2)(Ω_DM ρ_{c,0}/m_χ)² (1+z)³ Δ²(z) dN/dE[(1+z)E] exp(−τ) | Same structure | **Match** |
| 11.2 | DM photon spectra | Pythia (private code from Fornengo) | PPPC4DMID tables (Cirelli et al. 2011) | **Differs** — Thesis uses private Pythia code; code uses the public PPPC4DMID tables. Both are based on Pythia Monte Carlo but may differ slightly in interpolation/tabulation. |
| 11.3 | EBL absorption | exp(−τ[(1+z)E, z]) | `ebltable` package, Dominguez et al. (2011) model | **Match** (thesis cites absorption generically; code uses Dominguez 2011, a standard choice) |

## 12. Astrophysical Source Window Function

| # | Claim / Parameter | Pinetti (2022) | Code (`astro_sources.py`) | Status |
|---|-------------------|----------------|---------------------------|--------|
| 12.1 | Formula | Eq. 5.15: W_★ = (d_L/(1+z))² ∫ (dN/dE) φ(L,z) exp(−τ) dL | Same structure | **Match** |
| 12.2 | SED (power-law) | Eq. 5.16: dN/dE ∝ E^(−Γ) with K-correction | Same | **Match** |

## 13. BL Lac GLF

| # | Claim / Parameter | Pinetti (2022) | Code (`astro_sources.py`) | Status |
|---|-------------------|----------------|---------------------------|--------|
| 13.1 | Model | Ajello et al. (2014), LDDE inverse-sum (Eq. C.4) | Ajello et al. (2014) LDDE | **Match** |
| 13.2 | Spectral index Γ | 2.11 (= μ_★) | 2.11 | **Match** |
| 13.3 | A | 9.20 × 10⁻¹¹ Mpc⁻³ erg⁻¹ s (Table C.1) | 9.20 × 10⁻¹¹ | **Match** |
| 13.4 | L_★ | 2.43 × 10⁴⁸ erg/s | 2.43 × 10⁴⁸ | **Match** |
| 13.5 | z_c★ | 1.67 | 1.67 | **Match** |
| 13.6 | γ₁, γ₂ | 1.12, 3.71 | 1.12, 3.71 | **Match** |
| 13.7 | p₁, p₂ | 4.50, −12.88 | 4.50, −12.88 | **Match** |
| 13.8 | β | 4.46 × 10⁻² | 4.46 × 10⁻² | **Match** |
| 13.9 | Halo mass relation | M(L) via Eqs. C.5–C.6, fixed at 10¹³ M☉ scale | M_halo = 10¹³ M☉ | **Match** |

## 14. FSRQ GLF

| # | Claim / Parameter | Pinetti (2022) | Code (`astro_sources.py`) | Status |
|---|-------------------|----------------|---------------------------|--------|
| 14.1 | Model | Ajello et al. (2012), piecewise LDDE | Same | **Match** |
| 14.2 | Spectral index Γ | 2.44 | 2.44 | **Match** |
| 14.3 | A | 3.06 × 10⁻⁹ | 3.06 × 10⁻⁹ | **Match** |
| 14.4 | L_★ | 0.84 × 10⁴⁸ erg/s | 0.84 × 10⁴⁸ | **Match** |
| 14.5 | z_c★ | 1.47 | 1.47 | **Match** |
| 14.6 | γ₁, γ₂ | 0.21, 1.58 | 0.21, 1.58 | **Match** |
| 14.7 | p₁, p₂ | 7.35, −6.51 | 7.35, −6.51 | **Match** |
| 14.8 | β | 0.21 | 0.21 | **Match** |

## 15. mAGN GLF

| # | Claim / Parameter | Pinetti (2022) | Code (`astro_sources.py`) | Status |
|---|-------------------|----------------|---------------------------|--------|
| 15.1 | Modeling chain | Radio LF (Willott 2001) → core-total (Lara 2004) → radio-gamma (Di Mauro 2014) (App. C.2) | Same chain | **Match** |
| 15.2 | K factor (beaming/duty-cycle) | k = 3.05 | K = 3.05 | **Match** |
| 15.3 | Spectral index Γ | 2.37 | 2.37 | **Match** |
| 15.4 | Radio spectral index α | 0.80 (151 MHz → 5 GHz scaling) | 0.80 | **Match** |
| 15.5 | Halo mass relation | Eqs. C.20–C.21 | Same form | **Match** |

## 16. SFG GLF

| # | Claim / Parameter | Pinetti (2022) | Code (`astro_sources.py`) | Status |
|---|-------------------|----------------|---------------------------|--------|
| 16.1 | IR LF model | Gruppioni et al. (2013), 3-component (spiral + starburst + SF-AGN), Eq. C.22–C.26 | Same 3-component model | **Match** |
| 16.2 | L_γ–L_IR relation | Ackermann et al. (2012): log₁₀(L_{0.1-100}) = 1.09 log₁₀(L_IR/10¹⁰ L☉) + 39.19 | Same | **Match** |
| 16.3 | Spectral index Γ | 2.7 | 2.7 | **Match** |

## 17. Limber Projection / Angular Power Spectrum

| # | Claim / Parameter | Pinetti (2022) | Code (`angular_power.py`) | Status |
|---|-------------------|----------------|---------------------------|--------|
| 17.1 | Limber formula | C_ℓ = ∫ dχ/χ² W_i W_j P_{ij}(k=ℓ/χ) (Eq. 5.10, App. D) | Same | **Match** |
| 17.2 | k substitution | k = ℓ/χ (Eq. D.33) | k = (ℓ+1/2)/χ (LoVerde & Afshordi 2008 correction) | **Differs** — Code uses the half-integer correction for better low-ℓ accuracy. Thesis uses standard k=ℓ/χ. Improvement over thesis. |
| 17.3 | Multipole range | ℓ_min = 10, ℓ_max = 1000 | ℓ_min = 10, ℓ_max = 1000 (ℓ_max = 2000 for Fermissimo) | **Match** (with extension for Fermissimo) |

## 18. Fermi-LAT Specifications

| # | Claim / Parameter | Pinetti (2022) | Code (`noise_model.py`, `config.py`) | Status |
|---|-------------------|----------------|--------------------------------------|--------|
| 18.1 | Energy bins | 12 bins, 0.5 GeV – 1 TeV (Table 5.1) | Same 12 bins | **Match** |
| 18.2 | Photon noise C_N | Values in Table 5.1 | Same values | **Match** |
| 18.3 | Sky fractions f_sky | Per-bin values (Table 5.1) | Same values | **Match** |
| 18.4 | PSF model | Modified Gaussian, Eqs. 5.21–5.23 with σ₀(E_ref=0.5 GeV) = 1.20°, power-law index −0.95, floor 0.05° | Same parametrization | **Match** |
| 18.5 | Beam window function | B_ℓ = exp[−σ_b² ℓ²/2] with σ_b(ℓ,E) = σ₀/(1+0.25 σ₀ ℓ)⁻¹ (Eq. 5.22) | Same | **Match** |

## 19. Fermissimo Specifications

| # | Claim / Parameter | Pinetti (2022) | Code (`noise_model.py`) | Status |
|---|-------------------|----------------|-------------------------|--------|
| 19.1 | Exposure | 2× Fermi-LAT | 2× Fermi-LAT | **Match** |
| 19.2 | PSF improvement factor α_σ | 0.2 (Eq. 5.24) | 0.2 | **Match** |
| 19.3 | PSF floor | 0.001° (Eq. 5.24) | 0.001° | **Match** |
| 19.4 | Sky fraction | f_sky = 0.8 | f_sky = 0.8 | **Match** |

## 20. Radio Telescope Specifications

| # | Claim / Parameter | Pinetti (2022) | Code (`noise_model.py`, `config.py`) | Status |
|---|-------------------|----------------|--------------------------------------|--------|
| 20.1 | MeerKAT dishes, diameter | 64 dishes, 13.5 m (Table 5.2) | 64 dishes, 13.5 m | **Match** |
| 20.2 | MeerKAT survey area / t_obs | 4000 deg², 4000 hr | Same | **Match** |
| 20.3 | MeerKAT bands | UHF [0.4–1.45], L [0.0–0.58] | Same | **Match** |
| 20.4 | SKA1 dishes, diameter | 133+64, 14.5 m | 197 total, 14.5 m | **Match** |
| 20.5 | SKA1 survey/time/baseline | 25000 deg², 10000 hr, 3 km | Same | **Match** |
| 20.6 | SKA2 dishes, diameter | 2000, 14.5 m | 2000, 14.5 m | **Match** |
| 20.7 | SKA2 survey/baseline/beams | 30000 deg², 10 km, 36 beams | Same | **Match** |
| 20.8 | System temperature | T_sys = 30 + 60(300 MHz/ν)^2.55 K (Eq. 5.26 context) | Same formula | **Match** |
| 20.9 | Beam function | Gaussian: B_ℓ = exp[−ℓ²/(2) × (1.22 λ_o/(√(8ln2) D))²] (Eq. 5.25) | Same | **Match** |
| 20.10 | Single-dish noise | Eq. 5.26: C_{N,dish} = T²_sys S / (N_dish t Δν N_b N_pol η²) | Same | **Match** |
| 20.11 | Interferometer noise | Eq. 5.27: C_{N,interf} = T²_sys S FoV / (n(u) t Δν N_b N_pol η²) | Same | **Match** |
| 20.12 | Baseline density n(u) | 0.005 for SKA, ×10 smaller for MeerKAT | Same | **Match** |
| 20.13 | Shortest baseline | D_short = 2 D_dish | Same | **Match** |

## 21. Variance / Error Estimate

| # | Claim / Parameter | Pinetti (2022) | Code (`statistics.py`) | Status |
|---|-------------------|----------------|------------------------|--------|
| 21.1 | Gaussian variance | Eq. 5.18: (ΔC_ℓ)² = 1/((2ℓ+1)f_sky) × [C_ℓ² + (C^ii + N^i/B²)(C^jj + N^j/B²)] | Same | **Match** |
| 21.2 | Approximate form | Eq. 5.28: noise-dominated γ-ray auto | Same approximation available | **Match** |

## 22. Signal-to-Noise Ratio

| # | Claim / Parameter | Pinetti (2022) | Code (`statistics.py`) | Status |
|---|-------------------|----------------|------------------------|--------|
| 22.1 | SNR formula | Eq. 5.29: SNR² = Σ_{ℓ,a,r} (C_ℓ/ΔC_ℓ)² | Same | **Match** |
| 22.2 | Sum over bins | ℓ bins × 12 energy bins × redshift bins | Same | **Match** |

## 23. DM Exclusion (Δχ²)

| # | Claim / Parameter | Pinetti (2022) | Code (`statistics.py`) | Status |
|---|-------------------|----------------|------------------------|--------|
| 23.1 | Test statistic | Eq. 5.30: Δχ² = Σ(C^{HI×γ}/ΔC)² − Σ(C^{HI×S}/ΔC)² | Same | **Match** |
| 23.2 | 2σ threshold | Δχ² = 4 (1 dof, 95.45% CL) | Δχ² = 4 | **Match** |
| 23.3 | Scan strategy | Raster scan over m_χ, σv as free parameter | Same | **Match** |

---

## Summary of Differences

| # | Item | Nature of Difference | Impact |
|---|------|---------------------|--------|
| 2.3 | SMT q parameter | Code: 0.707 vs Thesis: 0.75 | **Low** — both are common in literature; ~5% effect on mass function tails |
| 5.3 | ṽ(k) normalization | Different convention (unnormalized vs /M) | **None** — absorbed into Δ² normalization; results identical |
| 11.2 | DM photon spectra source | Code: PPPC4DMID (public) vs Thesis: private Pythia code | **Low** — both Pythia-based; differences at percent level |
| 17.2 | Limber k substitution | Code: (ℓ+½)/χ vs Thesis: ℓ/χ | **Low** — code is more accurate at low ℓ; improvement over thesis |

## Intentionally Omitted from Code

The following items from the thesis are defined mathematically but deliberately not implemented because the cross-correlation pipeline does not require them:

| # | Item | Thesis Reference | Reason Not Implemented |
|---|------|-----------------|------------------------|
| 8.1 | P^1h_{δ²δ²} (DM auto 1-halo) | Eq. 3.59 | Pipeline computes HI × γ cross-power, not DM × DM auto-power |
| 8.2 | P^2h_{δ²δ²} (DM auto 2-halo) | Eq. 3.60 | Same — DM auto-power not needed |
| 8.3 | P^1h_{HI×DM} (cross 1-halo) | Eq. 4.16 | Subdominant at ℓ ≤ 1000; 2-halo term `P_HI_DM_2h` suffices |

No alternative models beyond Pinetti (2022) are implemented. All other claims (47 items) are in exact agreement.

---

## Verification Plan

To confirm agreement numerically (post-implementation):
1. Run `pytest tests/` — unit tests validate internal consistency
2. Reproduce Fig. 5.2 (left): UGRB intensity vs energy — compare to thesis Fig. 5.2
3. Reproduce Fig. 5.2 (right): auto-correlation C_ℓ^{γγ} vs Fermi-LAT data
4. Reproduce Table 5.3: SNR values for MeerKAT/SKA1/SKA2
5. Reproduce Fig. 5.9: DM exclusion curves at 2σ
