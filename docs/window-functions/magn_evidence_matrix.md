# Claim-by-Claim Evidence Matrix: mAGN Window Function Pipeline

## Context

This document audits every equation, model choice, parameter value, and computational method in the mAGN window function chain (`astro_sources.py`: `_willott_rlf`, `_willott_volume_correction`, `_L151_from_Lgamma`, `_glf_mAGN`, `W_gamma_astro`, `bias_astro`) against the source literature: Willott+ (2001), Inoue (2011), Lara+ (2004), Di Mauro+ (2014), Pinetti+ (2020/2022).

---

## Legend

| Symbol | Meaning |
|--------|---------|
| **Match** | Pipeline agrees with literature |
| **Match (thesis)** | Pinetti 2022 parallel agrees with thesis |
| **Differs** | Pipeline uses a different choice (noted) |
| **Partial** | Partially matches; deviations noted |
| **Investigate** | Potential issue requiring verification |

---

## 1. Willott (2001) Radio Luminosity Function at 151 MHz

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Two-component form: $\rho_r = \rho_l + \rho_h$ | Willott+ (2001) Table 1; Di Mauro+ (2014) Eq. C.9 | `_willott_rlf` lines 155–173 sums low + high components | Same | **Match** | |
| Low-power form: power-law × exp cutoff × density evolution | Willott Eq. for $\rho_l$; Di Mauro Eq. C.10 | `_willott_rlf` low-power branch | Same | **Match** | |
| Low-power frozen at $z \ge z_{l\star}$ | Willott (2001) text | `_willott_rlf` freeze at `Z_L_STAR` | Same | **Match** | |
| High-power form: power-law × inverse-exp cutoff × Gaussian | Willott Eqs. for $\rho_h$; Di Mauro Eqs. C.11-C.12 | `_willott_rlf` high-power branch | Same | **Match** | |
| High-power Gaussian width z-dependent | Willott (2001) | `_willott_rlf` switches between `WILLOTT_Z_H0_LO` and `WILLOTT_Z_H0_HI` | Same | **Match** | |
| $\rho_{l\star} = 10^{-7.523}$ Mpc⁻³ | Willott Table 1 | `WILLOTT_RHO_L_STAR` | Same | **Match** | |
| $\beta_l = 0.586$ | Willott Table 1 | `WILLOTT_BETA_L` | Same | **Match** | |
| $L_{l\star} = 10^{26.48}$ W/Hz | Willott Table 1 | `WILLOTT_L_L_STAR` | Same | **Match** | |
| $k_l = 3.48$ | Willott Table 1 | `WILLOTT_K_L` | Same | **Match** | |
| $z_{l\star} = 0.710$ | Willott Table 1 | `WILLOTT_Z_L_STAR` | Same | **Match** | |
| $\rho_{h\star} = 10^{-6.757}$ Mpc⁻³ | Willott Table 1 | `WILLOTT_RHO_H_STAR` | Same | **Match** | |
| $\beta_h = 2.42$ | Willott Table 1 | `WILLOTT_BETA_H` | Same | **Match** | |
| $L_{h\star} = 10^{27.39}$ W/Hz | Willott Table 1 | `WILLOTT_L_H_STAR` | Same | **Match** | |
| $z_{h\star} = 2.03$ | Willott Table 1 | `WILLOTT_Z_H_STAR` | Same | **Match** | |
| $z_{h0}^{\rm lo} = 0.568$ | Willott Table 1 | `WILLOTT_Z_H0_LO` | Same | **Match** | |
| $z_{h0}^{\rm hi} = 0.956$ | Willott Table 1 | `WILLOTT_Z_H0_HI` | Same | **Match** | |

---

## 2. Willott Cosmology Volume Correction

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $\eta(z) = (d_C^W/d_C)^2 \times (H/H_W)$ | Di Mauro+ (2014) Eqs. C.16-C.18 | `_willott_volume_correction` | Same | **Match** | |
| Willott reference cosmology | Willott (2001) Table 1 Model C: $H_0=50$ km/s/Mpc, $\Omega_M=0$, $\Omega_\Lambda=0$ | `H0_WILLOTT = 50.0` with Model C parameter values in `config.py` | Same | **Match** | |
| Willott Model C comoving volume element | Di Mauro+ (2014) Eq. 18 | `_willott_volume_correction` uses $d^2V_W/dz\,d\Omega = c^3 z^2 (2+z)^2 / [4 H_{0,W}^3 (1+z)^3]$ | Same | **Match** | Equivalent to the empty-universe Model C volume element reused from Di Mauro's mAGN construction |
| No caching | — | Direct function call (lru_cache removed) | Same | N/A | Simplification |

---

## 3. Radio → Gamma Conversion Chain

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Step 1: Di Mauro Eq. C.13: $\log L_\gamma = 2.0 + 1.008\log(\nu L_\nu)_{\rm core}$ [erg/s] | Di Mauro+ (2014) Eq. C.13 | `_L151_from_Lgamma` lines 231–234 | Same | **Match** | |
| Unit: Di Mauro correlation uses $\nu L_\nu$ [erg/s], not $L_\nu$ [W/Hz] | Di Mauro+ (2014) | Code correctly converts; `config.py` comment near `DIMAURO_GAMMA_RADIO_A/B` is still phrased in `W/Hz` terms | Same | **Partial** | **Config comment is misleading.** Code correctly handles the unit conversion inside `_L151_from_Lgamma`, but the nearby `config.py` comment should describe the Di Mauro relation as $\nu L_\nu$ [erg/s], not $L_\nu$ [W/Hz] |
| $L_\gamma$ intercept: 2.0 | Di Mauro+ (2014) Eq. C.13 | `DIMAURO_GAMMA_RADIO_A = 2.0` | Same | **Match** | |
| $L_\gamma$ slope: 1.008 | Di Mauro+ (2014) Eq. C.13 | `DIMAURO_GAMMA_RADIO_B = 1.008` | Same | **Match** | |
| Step 2: Lara Eq.: $\log L_{\rm core}^{5{\rm GHz}} = 4.2 + 0.77\log L_{\rm tot}^{1.4{\rm GHz}}$ [W/Hz] | Lara+ (2004) | `_L151_from_Lgamma` lines 236–238 | Same | **Match** | |
| $L_{\rm core}$ intercept: 4.2 | Lara+ (2004) | `LARA_A = 4.2` | Same | **Match** | |
| $L_{\rm core}$ slope: 0.77 | Lara+ (2004) | `LARA_B = 0.77` | Same | **Match** | |
| Step 3: Freq scaling $L_{1.4} = L_{151}(1400/151)^{-\alpha_r}$ | Inoue (2011) | `_L151_from_Lgamma` lines 240–242 | Same | **Match** | |
| Radio spectral index $\alpha_r = 0.80$ | Inoue (2011) | `RADIO_ALPHA = 0.80` | Same | **Match** | |
| Composite log-space Jacobian: $1/(0.77 \times 1.008)$ | Analytic from chain | `_L151_from_Lgamma` lines 244–246 with `1.0 / (DIMAURO_B * LARA_B)` | Same | **Match** | |
| $dL_{151}/dL_\gamma = (L_{151}/L_\gamma) \times {\rm dlog\ ratio}$ | Standard calculus | `_L151_from_Lgamma` lines 251–252 | Same | **Match** | |

---

## 4. mAGN Gamma-Ray LF Assembly (Di Mauro Eq. C.19)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Assembly formula $\phi_\gamma = k\eta(1+z)^{-(2-\Gamma)}\rho_r/(\ln 10\,L_{151})\,\lvert dL_{151}/dL_\gamma \rvert$ | [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eq. C.19 | `_glf_mAGN` lines 281–313 | Same | **Match** | Includes K-correction factor |
| Beaming factor $k = 3.05$ | Di Mauro+ (2014) | `DIMAURO_K = 3.05` | Same | **Match** | |
| Mean photon index $\Gamma = 2.37$ | Pinetti+ (2020) Table 3 | `ASTRO_SOURCES['mAGN']['alpha'] = 2.37` | Same | **Match** | |
| K-correction $(1+z)^{-(2-\Gamma)}$ | [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eq. C.19 | `_glf_mAGN` line 307: `K_corr = (1+z)**(-(2-alpha))` | Same | **Match** | Accounts for observed-to-rest-frame luminosity mapping |
| $d\Phi/dL$ from $d\Phi/d\log L$: divide by $L\ln 10$ | Standard | `_glf_mAGN` | Same | **Match** | |
| Spectral index extracted from source params | Pinetti+ Table 3 | `cfg.ASTRO_SOURCES['mAGN']['alpha']` | Same | **Match** | |

---

## 5. Window Function Assembly (Pinetti+ Eq. 4.3)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Formula $W = (1/(4\pi h^3))\int\Phi\,(L/\epsilon\,I_\alpha)\,E_{\rm rest}^{-\alpha}\,dL$ | Pinetti+ (2020) Eq. 4.3 motivates the luminosity-function structure; the active pipeline makes the final h-dependent volume conversion explicit | `W_gamma_astro` lines 598–600, 609, 620, 643 | Same | **Differs** (implementation form) | The current implementation returns the photon-emissivity form with no explicit external $(1+z)^{-2}$ prefactor and a final `h^{-3}` conversion to `[(Mpc/h)^-3]` |
| $E_{\rm rest} = E_{\rm obs}(1+z)$ | Standard | `W_gamma_astro` sets `E_rest = E_GeV * (1+z)` | Same | **Match** | |
| Energy normalization $I_\alpha = \int_{0.1}^{100} E^{1-\alpha}dE$ [GeV² band] | Pinetti+ (2020) | `W_gamma_astro` analytic `energy_integral` lines 603–606 | Same | **Match** | Analytic form for $\alpha\ne 2$ |
| 0.1–100 GeV band for $I_\alpha$ | Ackermann/Di Mauro convention | `W_gamma_astro` with `E_min_band=0.1`, `E_max_band=100.0` | Same | **Match** | |
| GeV→erg conversion: $1.602\times10^{-3}$ | Standard | `GeV_to_erg = 1.602e-3` | Same | **Match** | |
| $L_{\rm sens}(z) = F_{\rm sens}\,4\pi d_L^2\,G_{\rm eV\to erg}\,I_\alpha / [(1+z)^{2-\alpha}\,J_\alpha^{\rm EBL}(z)]$ | [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eqs. 3.75–3.76 | `L_sens(z, alpha=2.37)` with K-correction and EBL | Same | **Match** | $J_\alpha^{\rm EBL}$ over Fermi 1–100 GeV band with $e^{-\tau}$ |
| $F_{\rm sens}=10^{-10}$ cm⁻²s⁻¹ in 1–100 GeV band (forecast) | [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eq. 3.76 | `F_SENS = 1e-10` | Same | **Match** | |
| $L_{\rm up} = \min(L_{\max}, L_{\rm thr})$ | Pinetti+ (2020) | `W_gamma_astro` unresolved branch | Same | **Match** | |
| Integration via `scipy.quad` in log-$L$ | — | `W_gamma_astro` with `epsrel=1e-5` | Same | N/A | Numerical choice |
| Luminosity range $[10^{40}, 10^{50}]$ erg/s | Pinetti thesis Table 3.1 | `L_min=1e40`, `L_max=1e50` | Same | **Match** | |

---

## 6. mAGN Effective Halo Bias

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $M_\star = 10^9 M_\odot (L_\gamma/10^{48})^{0.36}$ | Di Mauro+ (2014) Eq. C.21 | `MAGN_MSTAR_*` in `bias_astro` line 681 | Same | **Match** | |
| $M_{\rm halo} = 10^{13} M_\odot (M_\star/[10^{8.8}(1+z)^{1.4}])^{0.645}$ | Di Mauro+ (2014) Eq. C.20 | `MAGN_MHALO_*` in `bias_astro` lines 695–701 | Same | **Match** | |
| Characteristic $L_\gamma^{\rm char} = 10^{44}$ erg/s | Ad-hoc choice | `L_char = 1e44` | Same | **Differs** (convention) | Not specified in literature; pipeline uses fixed value rather than luminosity-weighted integral |
| Bias via Sheth-Tormen $b(M_{\rm halo}, z)$ | Standard | `hm.bias(M_halo, z)` | Same | **Match** | Inherits $q$=0.707 vs 0.75 difference from halo model |
| $M_{\rm halo}$ floor at $10^{10}\,M_\odot$ | — | `max(M_halo, 1e10)` | Same | N/A | Pipeline safeguard |

---

## 7. Theoretical Deviations & Simplifications

| # | Item | Nature | Severity | Notes |
|---|------|--------|----------|-------|
| T1 | Fixed characteristic luminosity for bias | Simplification | Minor | `bias_astro` uses $L^{\rm char}=10^{44}$ erg/s rather than integrating $b(M(L))$ weighted by emissivity. This is a standard shorthand but differs from a fully luminosity-weighted effective bias |
| T2 | Pure power-law gamma-ray spectrum | Simplification | Minor | $dN/dE\propto E^{-\alpha}$ over 0.1–100 GeV with no break or curvature. Real AGN spectra often show curvature, but this is the standard Pinetti+ (2020) Table 3 choice |
| T3 | Single $\Gamma=2.37$ for all mAGN | Simplification | Minor | Di Mauro+ (2014) assumes a single photon index; in reality there is a distribution |
| T4 | Willott RLF extrapolated to high $z$ | Simplification | Minor | Willott calibrated up to $z\sim4$ (3CRR+6CE+7CRS). Pipeline extrapolates without warning; the Gaussian $\rho_h$ naturally decays at high $z$ |
| T5 | Unit mismatch in Di Mauro config comment | Documentation | Low | `config.py:152` says "W/Hz" but actual correlation is in erg/s ($\nu L_\nu$). Code handles correctly |
| ~~T6~~ | ~~K-correction $(1+z)^{-(2-\Gamma)}$ missing from `_glf_mAGN`~~ | — | — | **Resolved:** K-correction now included in `_glf_mAGN` (line 307) per Pinetti (2022) Eq. C.19 |

---

## 8. Computational Simplifications

| # | Item | Method | Impact |
|---|------|--------|--------|
| C1 | Volume correction $\eta(z)$ | Direct function call (no caching) | No performance impact (cheap analytic evaluation) |
| C2 | Volume correction via analytic formula | `_willott_volume_correction` uses analytic empty-universe volume element | Exact (no numerical integration needed) |
| C3 | Window integral via `scipy.quad` in log-$L$ | `epsrel=1e-5`, `limit=200` | High accuracy |
| C4 | Gamma-radio-core conversion in log-space | Analytic log-space Jacobian | Exact (no numerical diff) |
| C5 | $d_L$ computed in physical Mpc (divide by $h$) | `L_sens` uses `cosmo.d_L(z) / cfg.h` before converting to cm | Explicit h-factor handling |

---

## 9. Pipeline (Pinetti 2022) Parallel Summary

The Pinetti 2022 parallel implementation does **not** define a separate mAGN GLF or Willott-conversion path, so the active repository implementation is the effective source of truth for both columns here. The only inherited differences come from shared halo-model utilities:

- Halo bias uses $q=0.75$ (not 0.707) via `pinetti2022.bias_pinetti()` → affects mAGN effective bias by ~few percent at the characteristic halo mass
- Correa concentration (D2): Pipeline uses Planck Appendix B1 fit; thesis uses different cosmology fit. <5% on $c$. See [HI Evidence Matrix](hi_evidence_matrix.md).
- Limber $k$-substitution uses $k=\ell/\chi$ (thesis) vs $k=(\ell+1/2)/\chi$ (pipeline improvement)

None of these affect the mAGN window function $W_\gamma^{\rm mAGN}(z)$ itself — only its projection into $C_\ell$ via the halo model.

---

## 10. Summary of All Deviations from Literature/Thesis

| # | Item | Literature/Thesis | Pipeline | Nature | Severity |
|---|------|-------------------|----------|--------|----------|
| 1 | Di Mauro correlation units | Di Mauro Eq. C.13 uses $\nu L_\nu$ [erg/s] | Code correct, config comment wrong | Documentation | Low |
| 2 | Fixed $L^{\rm char}$ for bias | Not prescribed | $10^{44}$ erg/s | Simplification | Minor |
| 3 | Pure power-law spectrum | Standard choice | Same | Simplification | Minor |
| 4 | Extrapolation to high $z$ | Willott calibrated to $z\lesssim 4$ | Extrapolates silently | Simplification | Low |
| ~~5~~ | ~~K-correction $(1+z)^{-(2-\Gamma)}$ missing~~ | Di Mauro Eq. C.19 | Now present in `_glf_mAGN` | **Resolved** | — |

---

## 11. Items Verified Correct

| Concern | Resolution |
|---------|-----------|
| Willott parameters match which model? | Parameter values ($\rho_{l\star}=10^{-7.523}$, etc.) verified to match Willott Table 1 Model C ($\Omega_M=0$). `_willott_volume_correction` now follows the corresponding Di Mauro Eq. 18 volume element for the same Model C background |
| Log-space Jacobian correctness | Di Mauro (slope=1.008) × Lara (slope=0.77) = 0.776; inverse = 1.288. nuLnu↔W/Hz and freq scaling are log-space constant offsets (Jacobian=1). Verified analytically |
| K-correction sign | $(1+z)^{-(2-\Gamma)} = (1+z)^{-(2-2.37)} = (1+z)^{+0.37}$. This is a positive correction (boost at high $z$), as expected for $\Gamma \gt 2$. Now present in `_glf_mAGN` line 307 |
| h-factor handling in $d_L$ | `cosmo.d_L(z)/cfg.h` correctly converts Mpc/h → physical Mpc before conversion to cm |
| Unit dimensional check | $[\Phi]$=Mpc⁻³ (erg/s)⁻¹, $[L/I_\alpha]\cdot[E^{-\alpha}]$=ph·s⁻¹·GeV⁻¹·(erg/s)⁻¹·(erg/s)=ph·s⁻¹·GeV⁻¹. After $1/(4\pi)$ and the final h-dependent volume conversion: ph·s⁻¹·GeV⁻¹·sr⁻¹·(Mpc/h)⁻³. Consistent with the pipeline's per-chi emissivity convention |

---

## 12. Verification Plan

To confirm findings numerically:
1. Compute total mAGN UGRB contribution at $E=1$ GeV and compare to Di Mauro+ (2014) Fig. 9 (10–63% of IGRB range)
2. Compare $\Phi_\gamma^{\rm mAGN}(L_\gamma=10^{44}, z=1)$ against Di Mauro+ (2014) Fig. 5
3. Reproduce thesis Fig. 5.2 left panel (UGRB intensity breakdown by source class)
4. Spot-check $L_{151}(L_\gamma=10^{44})$ gives physically reasonable value (~$10^{25}$ W/Hz)
5. Verify $\eta(z=1)$ numerically for the Model C → Planck correction
6. Check integrated mAGN window function over $0<z<5$ matches Pinetti (2020) Fig. 2
