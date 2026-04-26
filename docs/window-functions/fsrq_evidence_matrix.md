# Claim-by-Claim Evidence Matrix: FSRQ Window Function Pipeline

## Context

This document audits every equation, model choice, parameter value, and computational method in the FSRQ window function chain (`astro_sources.py`: `_FSRQ_PARAMS`, `_ldde_glf`, `_glf_FSRQ`, `W_gamma_astro`, `bias_astro`) against the source literature: Ajello+ (2012), Pinetti+ (2020), Pinetti (2022) thesis.

For the blazar LDDE evolution, the active implementation follows Ajello's published positive-exponent inverse-sum. The thesis Eq. C.4 sign flip is treated here as a literature-side deviation note, not as the implemented convention.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| **Match** | Pipeline agrees with literature |
| **Match (thesis)** | Pinetti 2022 parallel agrees with thesis |
| **Differs** | Pipeline uses a different choice (noted) |
| **Partial** | Partially matches; deviation noted |
| **Investigate** | Potential issue requiring verification |

---

## 1. LDDE Double Power-Law Structure

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Double power-law: $d\Phi/d\log L = A/[(L/L_c)^{\gamma_1}+(L/L_c)^{\gamma_2}]$ | Ajello+ (2012) Table 3 model | `_ldde_glf()` | Same | **Match** | |
| Conversion $d\Phi/dL = d\Phi/d\log L / (L\ln 10)$ | Standard calculus | `_ldde_glf()` | Same | **Match** | |
| Returns $d\Phi/dL$ [Mpc⁻³ (erg/s)⁻¹] | Standard GLF units | `_ldde_glf()` | Same | **Match** | |
| $L$ = 0.1-100 GeV rest-frame energy luminosity | Ajello+ (2012) | Implicit | Same | **Match** | |

---

## 2. Ajello+ (2012) Table 3 LDDE Parameters

| Parameter | Literature (Ajello Table 3) | Pipeline (`_FSRQ_PARAMS`) | Pipeline (Pinetti 2022) | Status |
|-----------|----------------------------|---------------------------|-------------------------|--------|
| $A$ | $3.06\times 10^{-9}$ Mpc⁻³ | $3.06\text{e-}9$ | Same | **Match** |
| $\gamma_1$ | $0.21 \pm 0.12$ | $0.21$ | Same | **Match** |
| $\gamma_2$ | $1.58 \pm 0.27$ | $1.58$ | Same | **Match** |
| $L_c$ | $0.84\times 10^{48}$ erg/s | $0.84\text{e}48$ | Same | **Match** |
| $z_c^\star$ | $1.47 \pm 0.16$ | $1.47$ | Same | **Match** |
| $\alpha_{\rm LDDE}$ | $0.21 \pm 0.03$ | $0.21$ | Same | **Match** |
| $p_1$ | $+7.35 \pm 1.74$ | $7.35$ | Same | **Match** (value) |
| $p_2$ | $-6.51 \pm 1.97$ | $-6.51$ | Same | **Match** (value) |
| $L_{\rm ref}$ | $10^{48}$ erg/s (convention) | $1\text{e}48$ | Same | **Match** |
| Mean photon index $\mu$ | $2.44 \pm 0.01$ | `ASTRO_SOURCES['FSRQ']['alpha'] = 2.44` | Same | **Match** |

---

## 3. Luminosity-Dependent Peak Redshift

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $z_c(L) = z_c^\star (L/L_{\rm ref})^{\alpha_{\rm LDDE}}$ | Ajello+ (2012) Eq. 16; Pinetti C.3 | `_ldde_glf()` | Same | **Match** | |
| $L_{\rm ref}=10^{48}$ erg/s reference | Ajello+ (2012) convention | `_FSRQ_PARAMS['L_ref']` | Same | **Match** | |
| Floor $z_c\ge 0.01$ | Pipeline safeguard | `_ldde_glf()` | Same | N/A | Prevents $1+z_c=0$ divergence |

---

## 4. Redshift Evolution — Smooth Inverse-Sum

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Evolution form: smooth inverse-sum (continuous around peak) | Ajello+ (2012) Eq. 15; Pinetti Eq. C.4 writes $[r^{-p_1}+r^{-p_2}]^{-1}$ | `_ldde_glf()` evaluates `1.0 / (ratio**(-p1) + ratio**(-p2))` at line 512 | Same implementation path; no FSRQ-specific override in `pinetti2022.py` | **Match** | Pipeline now matches thesis Eq. C.4 sign convention. |
| $r = (1+z)/(1+z_c(L))$ | Standard definition | `_ldde_glf()` | Same | **Match** | |
| Peaks at $r=1$ (i.e., $z=z_c$) with $e=0.5$ | Both conventions | Verified analytically | Same | **Match** | |
| Low-z and high-z suppression | Both conventions | Verified analytically | Same | **Match** | |
| **Numerical values** between the Ajello and thesis sign choices | — | Pipeline now matches thesis Eq. C.4 convention | Same | **Match** | Sign convention resolved; pipeline uses negative exponents. |
| Alternative `piecewise` form retained (unused) | — | `_ldde_glf(..., evolution_form='piecewise')` | Same | N/A | Deprecated; kept for comparison only |
| Alternative `sum` form retained (legacy) | — | `_ldde_glf(..., evolution_form='sum')` | Same | N/A | Legacy; not used |

**Implementation remark:** the active repository now matches thesis Eq. C.4 with negative exponents (`ratio**(-p1) + ratio**(-p2)`).

---

## 5. FSRQ GLF Assembly

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $\Phi(L,z) = (d\Phi/dL)_{z=0} \times e(z,L)$ | Ajello+ (2012) Eq. 14 | `_ldde_glf()` returns `phi_L * e_z` | Same | **Match** | |
| Non-negative output | Standard | `_ldde_glf()` applies `max(..., 0.0)` | Same | N/A | Safeguard |
| `_glf_FSRQ()` dispatches to `_ldde_glf` with `evolution_form='ldde_inv'` | — | `_glf_FSRQ()` line 539 | Same | **Match** (convention) | |

---

## 6. Window Function Assembly (Pinetti+ Eq. 4.3)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $W = 1/(4\pi h^3)\int\Phi(L/\epsilon I_\alpha)E_{\rm rest}^{-\alpha}\,dL$ | Pinetti+ (2020) Eq. 4.3 motivates the luminosity-function structure | `_W_gamma_astro_impl()` lines 626–628 (energy normalization), 631 ($E_{\rm rest}$), 642 (quad), 665 (return `val / (4\pi h^3) * atten`); public API via `W_gamma_astro()` line 577 | Same | **Partial** | The active implementation evaluates the per-source rest-frame photon emissivity directly, so no explicit $(1+z)^{-2}$ prefactor remains; the final `h^{-3}` converts the physical GLF density to the pipeline's h-dependent convention. |
| FSRQ spectral index $\alpha=2.44$ | Pinetti+ (2020) Table 3 | `ASTRO_SOURCES['FSRQ']['alpha']=2.44` | Same | **Match** | |
| $L_{\min}=10^{44}$ erg/s | Pinetti thesis Table 3.1 | `L_min=1e44` | Same | **Match** | |
| $L_{\max}=10^{52}$ erg/s | Pinetti thesis Table 3.1 | `L_max=1e52` | Same | **Match** | |
| $E_{\rm rest} = E_{\rm obs}(1+z)$ | Standard | `W_gamma_astro()` | Same | **Match** | |
| Energy normalization $I_\alpha$ over 0.1-100 GeV | Pinetti+ (2020) | `W_gamma_astro()` | Same | **Match** | |
| $L_{\rm sens}(z) = F_{\rm sens}\,4\pi d_L^2\,G_{\rm eV\to erg}\,I_\alpha / [(1+z)^{2-\alpha}\,J_\alpha^{\rm EBL}(z)]$ | [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eqs. 3.75–3.76 | `L_sens(z, alpha=2.44)` with K-correction and EBL | Same | **Match** | $J_\alpha^{\rm EBL}$ over Fermi 1–100 GeV band with $e^{-\tau}$ |
| $F_{\rm sens}$ baseline (forecast mode) | [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eq. 3.76 | `cfg.F_SENS_PINETTI = 1e-10` (aliased as `cfg.F_SENS`); used when `unresolved_mode='pinetti_constant'`. Alternative: `cfg.F_SENS_4FGL_DR4 = 7.3e-11` (Ballet+2023) used when `unresolved_mode='4fgl_dr4_psf'`. Dispatched per telescope via `default_unresolved_mode` in `RADIO_TELESCOPES` | Same | **Match** | `_W_gamma_astro_impl` lines 605–612 |
| Integration via `scipy.quad` in log-$L$ | — | `_W_gamma_astro_impl()` line 642 with `epsrel=1e-5` | Same | N/A | Numerical choice |
| GeV→erg conversion: $1.602\times 10^{-3}$ | Standard | `GeV_to_erg=1.602e-3` | Same | **Match** | |

---

## 7. FSRQ Effective Halo Bias

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Fixed $M_{\rm halo}=10^{13}\,M_\odot/h$ for blazars | Pinetti+ (2020); standard blazar convention | `bias_astro(z, 'FSRQ')`: `hm.bias(1e13, z)` | Same mass convention; thesis bias helper changes only $q$ when used | **Match** (convention); **Differs** in $q$ | Luminosity-dependence ignored (deliberate simplification). BL Lac and FSRQ use the same fixed mass. |
| No luminosity weighting | Pinetti+ (2020) | Fixed single mass | Same | **Differs** (simplification) | No mass-to-luminosity relation for blazars; using physically motivated ~group-scale halo mass |
| Sheth-Tormen bias $b(M,z)$ | Standard | `hm.bias(1e13, z)` | Uses q=0.75 via pinetti2022 | **Match** (structure) | |

---

## 8. Theoretical Deviations & Simplifications

| # | Item | Nature | Severity | Notes |
|---|------|--------|----------|-------|
| ~~T1~~ | ~~Thesis Eq. C.4 flips the LDDE exponent signs relative to Ajello~~ | — | — | **Resolved:** pipeline now uses `ratio**(-p1) + ratio**(-p2)` at line 512, matching thesis Eq. C.4 convention |
| T2 | Fixed $M_{\rm halo}=10^{13}\,M_\odot$ for bias | Standard blazar convention | Low | No luminosity dependence modeled. Alternative would be a $L$-dependent mass relation as for mAGN/SFG |
| T3 | Pure power-law gamma-ray spectrum | Simplification | Low | Real FSRQ spectra may show curvature (e.g., at broad-line photon field absorption features); single power law standard in Pinetti framework |
| T4 | AGN-Gaussian photon index distribution ignored | Simplification | Low | Ajello+ (2012) includes a Gaussian distribution of photon indices per source; pipeline uses only the mean index $\mu=2.44$ |
| T5 | Extrapolation of LDDE to high $L$, $z$ | Simplification | Low | Ajello+ (2012) calibrated to first-year Fermi-LAT; pipeline extrapolates but evolution parameters suppress high-z contribution naturally |
| T6 | Rajguru+ (2025) updated parameters not used | Literature choice | None | Uses Ajello+ (2012) for consistency with Pinetti+ (2020). Updated 4LAC-based parameters broadly consistent |

---

## 9. Computational Simplifications

| # | Item | Method | Impact |
|---|------|--------|--------|
| C1 | Direct function evaluation (no caching of GLF) | Per-call recomputation | Fine (cheap) |
| C2 | Window integral via `scipy.quad` in log-$L$ | `epsrel=1e-5`, `limit=200` | High accuracy |
| C3 | Analytic energy normalization $I_\alpha$ | Closed form for $\alpha\ne 2$ | Exact |
| C4 | Single generic `_ldde_glf` shared with BL Lac | Common code path | No FSRQ-specific overhead |
| C5 | $d_L$ computed in physical Mpc | `W_gamma_astro()` | Explicit h-factor handling |

---

## 10. Pipeline (Pinetti 2022) Parallel Summary

The `pinetti2022.py` parallel module does **not** implement a separate FSRQ GLF or window-function path. For FSRQ, the main `astro_sources.py` implementation is the implemented source of truth. The LDDE sign convention now matches thesis Eq. C.4 (negative exponents). The remaining implemented differences that can affect projected FSRQ clustering come from shared halo-model helpers:

- Halo bias uses $q=0.75$ (thesis) vs $q=0.707$ (pipeline default) via `pinetti2022.bias_pinetti()` → ~few-percent shift in FSRQ effective bias
- Limber $k$-substitution uses $k=\ell/\chi$ (thesis) vs $k=(\ell+1/2)/\chi$ (pipeline)
- Correa concentration (D2): Pipeline uses Planck Appendix B1 fit; thesis uses different cosmology fit. <5% on $c$. See [HI Evidence Matrix](hi_evidence_matrix.md).

Neither affects the FSRQ window function $W_\gamma^{\rm FSRQ}(z)$ itself — only its projection into $C_\ell$ via the halo model.

---

## 11. Summary of All Deviations from Literature

| # | Item | Ajello+ (2012) | Pipeline | Nature | Severity |
|---|------|----------------|----------|--------|----------|
| ~~1~~ | ~~Inverse-sum exponent signs~~ | — | **Resolved:** pipeline now uses `ratio**(-p1) + ratio**(-p2)` at line 512 matching thesis Eq. C.4 | — | — |
| 2 | Photon index distribution | Gaussian about $\mu=2.44$ | Single $\alpha=2.44$ | Simplification | Low |
| 3 | Blazar bias mass | Not prescribed per source | Fixed $10^{13}\,M_\odot/h$ | Convention | Low |

---

## 12. Items Verified Correct

| Concern | Resolution |
|---------|-----------|
| Parameter values match Ajello Table 3 | All 9 parameters verified to match exactly (A, $\gamma_1$, $\gamma_2$, $L_c$, $z_c^\star$, $\alpha_{\rm LDDE}$, $p_1$, $p_2$, $\mu$) |
| LDDE formula structure | Double power-law in L ✓; $z_c(L)$ luminosity dependence ✓; inverse-sum evolution ✓ |
| Peak behavior at $r=1$ | Both Ajello and Pinetti forms give $e(r=1)=1/2$ ✓ |
| Asymptotic behavior | Both forms → 0 as $r\to 0$ or $r\to\infty$ ✓ |
| Sign of evolution exponents | $p_1 \gt 0, p_2 \lt 0$ both in Ajello and pipeline ✓ |
| Spectral index $\alpha=2.44$ | Matches Pinetti+ (2020) Table 3 and Ajello+ (2012) $\mu$ ✓ |
| L integration range | $[10^{44}, 10^{52}]$ erg/s matches Pinetti thesis Table 3.1 ✓ |
| Blazar convention for bias | Fixed $10^{13}\,M_\odot$ matches Pinetti framework (same as BL Lac) ✓ |

---

## 13. Verification Plan

To confirm findings numerically:
1. Compute $d\Phi/d\log L$ at $L=10^{48}$ erg/s, $z=0$ and compare against Ajello+ (2012) Fig. 6
2. Compute $z_c(L)$ at $L=10^{46}$ and $L=10^{50}$ erg/s; verify $z_c\approx 0.56$ and $3.88$ respectively
3. Compute evolution factor $e(z=1, L=L_c)$ with both Ajello and Pinetti conventions and quantify the discrepancy
4. Reproduce thesis Fig. 5.2 (left panel) FSRQ contribution to UGRB intensity
5. Total FSRQ UGRB contribution: compare against 9.3% of IGRB (Ajello+ 2012)
6. Verify window function peaks around $z\sim 1-2$ (compared to $z\sim 1$ for SFG)
