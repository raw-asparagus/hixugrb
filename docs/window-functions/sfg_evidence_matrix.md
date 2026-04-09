# Claim-by-Claim Evidence Matrix: SFG Window Function Pipeline

## Context

This document audits every equation, model choice, parameter value, and computational method in the SFG window function chain (`astro_sources.py`: `_gruppioni_component`, `_gruppioni_ir_lf`, `_L_IR_from_Lgamma`, `_glf_SFG`, `W_gamma_astro`, `bias_astro`) against the source literature: Gruppioni+ (2013), Ackermann+ (2012), Pinetti+ (2020), Pinetti (2022) thesis.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| **Match** | Pipeline agrees with literature |
| **Match (thesis)** | Pinetti 2022 parallel agrees with thesis |
| **Differs** | Pipeline uses a different choice (noted) |
| **Partial** | Partially matches; simplification noted |
| **Investigate** | Potential issue requiring verification |

---

## 1. Gruppioni (2013) Five-Component IR LF Structure (Three Used)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Three star-forming components used: spiral + starburst + SF-AGN (out of five total in Gruppioni) | Gruppioni+ (2013) Table 8 has five populations (spiral, starburst, SF-AGN, AGN1, AGN2); Pinetti Eq. C.22 selects three | `_gruppioni_ir_lf` line 347 sums three components | Same | **Match** | Pipeline uses the three star-forming populations, consistent with Pinetti's selection |
| Modified Schechter form | Gruppioni+ (2013) Eq. 8; Pinetti Eq. C.23 | `_gruppioni_component` line 296 | Same | **Match** | |
| Returns $d\Phi/d\log_{10}L_{\rm IR}$ [Mpc⁻³] | Gruppioni+ (2013) convention | `_gruppioni_component` | Same | **Match** | |
| $L_{\rm IR}$ in $L_\odot$ (8-1000 μm total IR) | Gruppioni+ (2013) | Arg convention | Same | **Match** | |

---

## 2. Gruppioni Component Parameters (Table 8 / Pinetti Table C.2)

### Spiral

| Parameter | Literature | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----------|-----------|----------|-------------------------|--------|
| $\gamma$ | 1.0 | `GRUPPIONI_PARAMS['spiral']['gamma']` = 1.0 | Same | **Match** |
| $\sigma$ | 0.50 | `sigma` = 0.50 | Same | **Match** |
| $\log_{10}(L_\star/L_\odot)$ | 9.78 | `log_Lstar` = 9.78 | Same | **Match** |
| $\log_{10}(\phi_\star/{\rm Mpc}^{-3})$ | −2.12 | `log_phistar` = -2.12 | Same | **Match** |
| $k_L$ | 4.49 | `k_L` = 4.49 | Same | **Match** |
| $k_{R1}$ | −0.54 | `k_R1` = -0.54 | Same | **Match** |
| $k_{R2}$ | −7.13 | `k_R2` = -7.13 | Same | **Match** |

### Starburst

| Parameter | Literature | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----------|-----------|----------|-------------------------|--------|
| $\gamma$ | 1.0 | 1.0 | Same | **Match** |
| $\sigma$ | 0.35 | 0.35 | Same | **Match** |
| $\log_{10}(L_\star/L_\odot)$ | 11.17 | 11.17 | Same | **Match** |
| $\log_{10}(\phi_\star/{\rm Mpc}^{-3})$ | −4.46 | -4.46 | Same | **Match** |
| $k_L$ | 1.96 | 1.96 | Same | **Match** |
| $k_{R1}$ | 3.79 | 3.79 | Same | **Match** |
| $k_{R2}$ | −1.06 | -1.06 | Same | **Match** |

### SF-AGN

| Parameter | Literature | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-----------|-----------|----------|-------------------------|--------|-------|
| $\gamma$ | 1.2 | 1.2 | Same | **Match** | |
| $\sigma$ | 0.40 | 0.40 | Same | **Match** | |
| $\log_{10}(L_\star/L_\odot)$ | 10.80 | 10.80 | Same | **Match** | |
| $\log_{10}(\phi_\star/{\rm Mpc}^{-3})$ | −3.20 | -3.20 | Same | **Match** | |
| $k_L$ | 3.17 | 3.17 | Same | **Match** | |
| $k_{R1}$ | 0.67 | 0.67 | Same | **Match** | |
| $k_{R2}$ | **−3.17** (Gruppioni original) | -3.17 | **−3.17 (thesis typo; follows original)** | **Match** (vs paper); **Differs** (vs thesis typo) | Pinetti thesis Table C.2 has typo +3.17; pipeline correctly uses -3.17 matching Gruppioni's original paper |

---

## 3. Redshift Evolution

### Luminosity evolution $L_0(z)$

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $L_0(z) = L_\star ((1+z)/1.15)^{k_L}$ | Gruppioni+ (2013); Pinetti Eq. C.24 | `_gruppioni_component` | Same | **Match** | |
| Break at $z=1.1$ for **spiral only** | Gruppioni Table 8 ($z_{b,L}=1.1$, $k_{L,2}=0$) | `_gruppioni_component` freezes $L_0$ above $z=1.1$ only for spiral; starburst and SF-AGN use single power law | Same | **Match** | Resolved: previously applied the break uniformly (D13) |
| Reference normalization $(1+z)/1.15$ | Pipeline convention (z=0.15 first-bin midpoint) | `(1.0+z)/1.15` | Same | N/A | Equivalent to paper's bin-by-bin parameterization |
| Frozen value $(2.1/1.15)^{k_L}$ at $z \gt 1.1$ | Standard freezing | `_gruppioni_component` | Same | **Match** | |

### Density evolution $\Phi_0(z)$

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Spiral: break at $z=0.53$ | Gruppioni+ (2013); Pinetti Eq. C.25 | `_gruppioni_component` spiral branch | Same | **Match** | |
| Spiral: pre-break $((1+z)/1.15)^{k_{R1}}$ | Gruppioni+ (2013) | `_gruppioni_component` spiral branch | Same | **Match** | |
| Spiral: post-break with pivot 1.53 | Gruppioni+ (2013) | `_gruppioni_component` spiral branch | Same | **Match** | |
| Starburst & SF-AGN: break at $z=1.1$ | Gruppioni+ (2013); Pinetti Eq. C.26 | `_gruppioni_component` starburst/SF-AGN branches | Same | **Match** | |
| Starburst & SF-AGN: post-break with pivot 2.1 | Gruppioni+ (2013) | `_gruppioni_component` starburst/SF-AGN branches | Same | **Match** | |

---

## 4. Ackermann (2012) $L_\gamma$-$L_{\rm IR}$ Scaling

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $\log L_\gamma = \alpha_{\rm IR}\log(L_{\rm IR}/10^{10}L_\odot) + \beta_{\rm IR}$ | Ackermann+ (2012) Table 5 (EM, AGN-excl) | `_L_IR_from_Lgamma` line 366 | Same | **Match** | |
| $\alpha_{\rm IR}=1.09$ | Ackermann+ (2012) EM method, AGN-excluded | `ACKERMANN_ALPHA_IR=1.09` | Same | **Match** | Full sample gives $\alpha=1.17\pm 0.07$; AGN-excluded subsample used for cleaner SFG calibration |
| $\beta_{\rm IR}=39.19$ | Ackermann+ (2012) | `ACKERMANN_BETA_IR=39.19` | Same | **Match** | |
| $L_\gamma$ band: 0.1-100 GeV | Ackermann+ (2012) | Implicit | Same | **Match** | |
| $L_{\rm IR}$ band: 8-1000 μm | Ackermann+ (2012) | Implicit | Same | **Match** | |
| Inversion: $L_{\rm IR} = 10^{10}L_\odot \times 10^{(\log L_\gamma - \beta)/\alpha}$ | Algebra | `_L_IR_from_Lgamma` | Same | **Match** | Code computes in erg/s then divides by `L_SUN` |
| Jacobian $d\log L_{\rm IR}/d\log L_\gamma = 1/\alpha = 0.917$ | Algebra | `_L_IR_from_Lgamma` | Same | **Match** | |

---

## 5. SFG Gamma-Ray LF Assembly (Pinetti Eq. C.28)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $\Phi_\gamma = \Phi_{\rm IR}(L_{\rm IR}(L_\gamma),z) \lvert d\log L_{\rm IR}/d\log L_\gamma \rvert / (L_\gamma\ln 10)$ | Pinetti thesis Eq. C.28; Ackermann+ (2012) | `_glf_SFG` line 388 | Same | **Match** | |
| Conversion from $d\Phi/d\log L$ to $d\Phi/dL$: divide by $L\ln 10$ | Standard calculus | `_glf_SFG` | Same | **Match** | |
| Jacobian appears as $\lvert d\log L_{\rm IR}/d\log L_\gamma \rvert$ (log-space) | Pinetti Eq. C.28 | `_glf_SFG` | Same | **Match** | |
| Returns $d\Phi/dL_\gamma$ [Mpc⁻³ (erg/s)⁻¹] | Standard GLF units | `_glf_SFG` | Same | **Match** | |

---

## 6. Window Function Assembly (Pinetti+ Eq. 4.3)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Formula $W = 1/(4\pi h^3) \int \Phi (L/\epsilon I_\alpha) E_{\rm rest}^{-\alpha} dL$ | Pinetti+ (2020) Eq. 4.3 motivates the luminosity-function structure; the active pipeline makes the final h-dependent volume conversion explicit | `W_gamma_astro` lines 536/569 | Same | **Differs** (implementation form) | The current implementation returns the photon-emissivity form with no explicit external $(1+z)^{-2}$ prefactor and a final `h^{-3}` conversion to `[(Mpc/h)^-3]` |
| SFG spectral index $\alpha=2.7$ | Pinetti+ (2020) Table 3 | `ASTRO_SOURCES['SFG']['alpha']=2.7` | Same | **Match** | |
| $L_{\min}=10^{37}$ erg/s | Pinetti thesis Table 3.1 | `L_min=1e37` | Same | **Match** | |
| $L_{\max}=10^{42}$ erg/s | Pinetti thesis Table 3.1 | `L_max=1e42` | Same | **Match** | |
| $E_{\rm rest} = E_{\rm obs}(1+z)$ | Standard | `W_gamma_astro` sets `E_rest = E_GeV * (1+z)` | Same | **Match** | |
| Energy normalization $I_\alpha$ over 0.1-100 GeV | Pinetti+ (2020) | `W_gamma_astro` analytic `energy_integral` | Same | **Match** | |
| $L_{\rm sens}(z) = F_{\rm sens}\,4\pi d_L^2\,G_{\rm eV\to erg}\,I_\alpha / [(1+z)^{2-\alpha}\,J_\alpha^{\rm EBL}(z)]$ | [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eqs. 3.75–3.76 | `L_sens(z, alpha=2.7)` with K-correction and EBL | Same | **Match** | $J_\alpha^{\rm EBL}$ over Fermi 1–100 GeV band with $e^{-\tau}$ |
| $F_{\rm sens}=10^{-10}$ cm⁻²s⁻¹ in 1–100 GeV band | [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eq. 3.76 | `F_SENS=1e-10` | Same | **Match** | |
| Integration via `scipy.quad` in log-$L$, epsrel=1e-5 | — | `W_gamma_astro` with `epsrel=1e-5` | Same | N/A | Numerical choice |

---

## 7. SFG Effective Halo Bias (Pinetti Eq. C.29)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $M_{\rm halo}(L,z) = (10^{12}M_\odot/(1+z)^{1.61})(L/6.8\times 10^{39})^{0.92}$ | Pinetti thesis Eq. C.29 | `bias_astro(z, 'SFG')` line 681/703 | Same | **Match** | |
| $M_{\rm halo}$ normalization $10^{12}\,M_\odot$ | Pinetti Eq. C.29 | `SFG_MHALO_NORM=1e12` | Same | **Match** | |
| Luminosity normalization $6.8\times 10^{39}$ erg/s | Pinetti Eq. C.29 | `SFG_MHALO_LNORM=6.8e39` | Same | **Match** | |
| Luminosity exponent 0.92 | Pinetti Eq. C.29 | `SFG_MHALO_SLOPE=0.92` | Same | **Match** | |
| Redshift exponent 1.61 | Pinetti Eq. C.29 | `SFG_MHALO_Z_EXP=1.61` | Same | **Match** | |
| Characteristic $L_\gamma^{\rm char}=10^{39}$ erg/s | Ad-hoc choice | `L_char=1e39` | Same | **Differs** (convention) | Not specified in literature; pipeline uses fixed value rather than luminosity-weighted integral |
| Sheth-Tormen bias $b(M_{\rm halo},z)$ | Standard | `hm.bias(M_halo, z)` | Pinetti uses q=0.75 | **Match** (structure); inherits halo model q difference | |
| $M_{\rm halo}$ floor at $10^{10}\,M_\odot$ | — | `max(M_halo, 1e10)` | Same | N/A | Pipeline safeguard |

---

## 8. Theoretical Deviations & Simplifications

| # | Item | Nature | Severity | Notes |
|---|------|--------|----------|-------|
| ~~T1~~ | ~~$L_0$ frozen at $z=1.1$ for ALL components~~ | — | — | **Resolved:** break now applied only to spiral per Gruppioni Table 8 |
| T2 | $(1+z)/1.15$ reference normalization | Pipeline convention | Low | Paper parameterizes per-bin; pipeline uses continuous $(1+z)/1.15$ normalization to $z=0.15$ midpoint. Mathematically equivalent |
| T3 | SF-AGN $k_{R2}=-3.17$ (pipeline correct; thesis typo) | Correction | Low | Pinetti thesis Table C.2 shows $+3.17$ (typo); pipeline uses $-3.17$ from Gruppioni original. Thesis typo would cause unphysical density growth at $z \gt 1.1$ |
| T4 | Fixed characteristic luminosity $L^{\rm char}=10^{39}$ erg/s for bias | Simplification | Minor | Not prescribed in literature; alternative would be luminosity-weighted effective bias integral |
| T5 | Pure power-law gamma-ray spectrum $\alpha=2.7$ | Simplification | Low | Real SFG spectra have pion-bump curvature; a single power law is the standard Pinetti Table 3 choice |
| T6 | AGN-excluded Ackermann calibration | Literature choice | Low | Pipeline uses $\alpha_{\rm IR}=1.09$, $\beta_{\rm IR}=39.19$ (EM method, AGN-excluded) rather than full-sample $\alpha=1.17\pm 0.07$ for cleaner SFG calibration |
| T7 | Extrapolation of Gruppioni LF beyond $z\sim 4$ | Simplification | Low | Gruppioni calibrated to $z\sim 4$ (Herschel PEP/HerMES); pipeline extrapolates silently. LF declines naturally due to evolution parameters |

---

## 9. Computational Simplifications

| # | Item | Method | Impact |
|---|------|--------|--------|
| C1 | Gruppioni LF: direct function evaluation (no caching) | Per-call recomputation | Fine (cheap computation) |
| C2 | Window integral via `scipy.quad` in log-$L$ | `epsrel=1e-5`, `limit=200` | High accuracy |
| C3 | L_IR inversion done in log-space | Analytic inverse | Exact |
| C4 | $d_L$ computed in physical Mpc | `L_sens` uses `cosmo.d_L(z) / cfg.h` before converting to cm | Explicit h-factor handling |
| C5 | No analytic form for modified Schechter — direct evaluation | `_gruppioni_component()` | Fine |

---

## 10. Pipeline (Pinetti 2022) Parallel Summary

The Pinetti 2022 parallel implementation makes **no SFG-specific deviations** from the pipeline except:

- **SF-AGN $k_{R2}$**: thesis Table C.2 has typo $+3.17$; the pipeline correctly uses $-3.17$ matching Gruppioni's original paper. The Pinetti parallel implementation should also use $-3.17$ (the thesis typo is unphysical and causes unphysical density growth).

Other inherited differences from the halo model:
- Halo bias uses $q=0.75$ (not 0.707) via `pinetti2022.bias_pinetti()` → affects SFG effective bias at the characteristic halo mass
- Limber $k$-substitution uses $k=\ell/\chi$ (thesis) vs $k=(\ell+1/2)/\chi$ (pipeline)
- Correa concentration (D2): Pipeline uses Planck Appendix B1 fit; thesis uses different cosmology fit. <5% on $c$. See [HI Evidence Matrix](hi_evidence_matrix.md).

None of these affect the SFG window function $W_\gamma^{\rm SFG}(z)$ itself — only its projection into $C_\ell$ via the halo model.

---

## 11. Summary of All Deviations from Literature/Thesis

| # | Item | Literature/Thesis | Pipeline | Nature | Severity |
|---|------|-------------------|----------|--------|----------|
| ~~1~~ | ~~$L_0$ break at $z=1.1$ applied uniformly~~ | Only for spiral (Gruppioni Table 8) | Now spiral only | **Resolved** | — |
| 2 | $(1+z)/1.15$ reference | Per-bin parameterization (paper) | Continuous normalization | Convention | None |
| 3 | SF-AGN $k_{R2}$ sign | Thesis $+3.17$ (typo) | $-3.17$ (paper original) | **Correction** | Resolved |
| 4 | Fixed $L^{\rm char}$ for bias | Not prescribed | $10^{39}$ erg/s | Simplification | Minor |
| 5 | AGN-excluded $L_\gamma$-$L_{\rm IR}$ calibration | Ackermann EM method | Same | Literature choice | Low |

---

## 12. Items Verified Correct

| Concern | Resolution |
|---------|-----------|
| Modified Schechter form implementation | Code lines 341–342: `phi_0 * ratio**(1-gamma) * exp(-log(1+ratio)^2 / (2*sigma^2))` matches Gruppioni Eq. 8 exactly |
| L_IR units in Gruppioni vs Ackermann | Gruppioni uses $L_\odot$; Ackermann formula uses $L_{\rm IR}/(10^{10}L_\odot)$ so units are consistent. Code correctly uses $L_\odot$ throughout |
| Jacobian sign | $d\log L_{\rm IR}/d\log L_\gamma = 1/\alpha_{\rm IR} = 0.917 \gt 0$ (positive, as expected for monotonic relation) |
| Unit dimensional check | $[\Phi_\gamma]$=Mpc⁻³·(erg/s)⁻¹ from $[\Phi_{\rm IR}]$·[dimensionless]·[erg/s]⁻¹ |
| Gruppioni parameter typo (SF-AGN $k_{R2}$) | Pipeline correctly uses $-3.17$ (Gruppioni original); thesis typo $+3.17$ would cause unphysical density growth at $z \gt 1.1$ |
| Integration range $[10^{37}, 10^{42}]$ erg/s | Matches Pinetti thesis Table 3.1 for SFG |
| Spectral index $\alpha=2.7$ | Matches Pinetti Table 3 (softest index, reflects pion-bump from CR-ISM interactions) |

---

## 13. Verification Plan

To confirm findings numerically:
1. Reproduce Gruppioni Fig. 14 (IR LF by component at several redshifts)
2. Reproduce Ackermann Fig. 5 ($L_\gamma$-$L_{\rm IR}$ scatter plot)
3. Compare $\Phi_\gamma^{\rm SFG}(L=10^{40}, z=1)$ against Pinetti thesis Fig. 3.6
4. Total SFG UGRB intensity at 1 GeV: compare against 5-20% of IGRB (literature range)
5. Check that SFG bias at $z=0$ is lower than mAGN and blazar bias (downsizing)
6. Verify the L_0 break uniformity simplification: compare W_gamma^SFG with and without break for starburst/SF-AGN
