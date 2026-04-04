# Claim-by-Claim Evidence Matrix: FSRQ Window Function Pipeline

## Context

This document audits every equation, model choice, parameter value, and computational method in the FSRQ window function chain (`astro_sources.py`: `_FSRQ_PARAMS`, `_ldde_glf`, `_glf_FSRQ`, `W_gamma_astro`, `bias_astro`) against the source literature: Ajello+ (2012), Pinetti+ (2020), Pinetti (2022) thesis.

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
| Double power-law: $d\Phi/d\log L = A/[(L/L_c)^{\gamma_1}+(L/L_c)^{\gamma_2}]$ | Ajello+ (2012) Table 3 model | `_ldde_glf` line 404 | Same | **Match** | |
| Conversion $d\Phi/dL = d\Phi/d\log L / (L\ln 10)$ | Standard calculus | Line 407 | Same | **Match** | |
| Returns $d\Phi/dL$ [Mpc⁻³ (erg/s)⁻¹] | Standard GLF units | Line 435 | Same | **Match** | |
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
| $z_c(L) = z_c^\star (L/L_{\rm ref})^{\alpha_{\rm LDDE}}$ | Ajello+ (2012) Eq. 16; Pinetti C.3 | `_ldde_glf` line 410 | Same | **Match** | |
| $L_{\rm ref}=10^{48}$ erg/s reference | Ajello+ (2012) convention | Line 400 | Same | **Match** | |
| Floor $z_c\ge 0.01$ | Pipeline safeguard | Line 411 | Same | N/A | Prevents $1+z_c=0$ divergence |

---

## 4. Redshift Evolution — Smooth Inverse-Sum (Critical Deviation)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Evolution form: smooth inverse-sum (continuous around peak) | Ajello+ (2012) Eq. 15: $[r^{p_1}+r^{p_2}]^{-1}$ with $p_1>0, p_2<0$ | `_ldde_glf` line 422: $[r^{-p_1}+r^{-p_2}]^{-1}$ | Same | **Differs** (sign convention) | **Sign convention differs between Ajello and Pinetti.** Pipeline follows Pinetti thesis Eq. C.4 convention (negative exponents). With the same $(p_1,p_2)$ values, the two forms give **numerically different** evolution profiles. See `pinetti2022_evidence_matrix.md` D12 |
| $r = (1+z)/(1+z_c(L))$ | Standard definition | Line 414 | Same | **Match** | |
| Peaks at $r=1$ (i.e., $z=z_c$) with $e=0.5$ | Both conventions | Verified analytically | Same | **Match** | |
| Low-z and high-z suppression | Both conventions | Verified analytically | Same | **Match** | |
| **Numerical values** between the two forms | — | Differ at given $r\ne 1$ | Same as pipeline | **Differs** from Ajello | Example at $r=2$: Ajello form gives $e\approx 0.0061$; Pipeline form gives $e\approx 0.011$ — ~factor 2 difference |
| Alternative `piecewise` form retained (unused) | — | Lines 423-428 | Same | N/A | Deprecated; kept for comparison only |
| Alternative `sum` form retained (legacy) | — | Lines 429-431 | Same | N/A | Legacy; not used |

**Note on the sign convention controversy:** Ajello+ (2012) Eq. 15 literally writes $[r^{p_1} + r^{p_2}]^{-1}$ with the cited $(p_1=7.35, p_2=-6.51)$, which gives at $z=0$, $L=L_c$: $z_c\approx 1.47$, $r\approx 0.405$, Ajello evolution $e=1/(0.405^{7.35}+0.405^{-6.51})\approx 1/(5.7\text{e-}4 + 250)\approx 0.004$. Pipeline gives $e=1/(0.405^{-7.35}+0.405^{6.51})\approx 1/(1746+0.0047)\approx 5.7\text{e-}4$. So the pipeline **systematically underestimates low-z FSRQ density** relative to Ajello's literal formula. However, Pinetti (2022) Eq. C.4 explicitly uses the negative-exponent form and derives self-consistent SNR forecasts — the pipeline matches Pinetti, not Ajello.

---

## 5. FSRQ GLF Assembly

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $\Phi(L,z) = (d\Phi/dL)_{z=0} \times e(z,L)$ | Ajello+ (2012) Eq. 14 | Line 435: `phi_L * e_z` | Same | **Match** | |
| Non-negative output | Standard | Line 435: `max(..., 0.0)` | Same | N/A | Safeguard |
| `_glf_FSRQ()` dispatches to `_ldde_glf` with `ldde_inv` | — | Line 449 | Same | **Match** (convention) | |

---

## 6. Window Function Assembly (Pinetti+ Eq. 4.3)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $W = 1/(4\pi(1+z)^2)\int\Phi(L/\epsilon I_\alpha)E_{\rm rest}^{-\alpha}\,dL$ | Pinetti+ (2020) Eq. 4.3 | `W_gamma_astro` lines 509-569 | Same | **Match** | $d_L^2$ cancels against $dF/dE$'s $1/(4\pi d_L^2)$ |
| FSRQ spectral index $\alpha=2.44$ | Pinetti+ (2020) Table 3 | `ASTRO_SOURCES['FSRQ']['alpha']=2.44` | Same | **Match** | |
| $L_{\min}=10^{44}$ erg/s | Pinetti thesis Table 3.1 | `L_min=1e44` | Same | **Match** | |
| $L_{\max}=10^{52}$ erg/s | Pinetti thesis Table 3.1 | `L_max=1e52` | Same | **Match** | |
| $E_{\rm rest} = E_{\rm obs}(1+z)$ | Standard | Line 549 | Same | **Match** | |
| Energy normalization $I_\alpha$ over 0.1-100 GeV | Pinetti+ (2020) | Lines 538-546 | Same | **Match** | |
| Unresolved threshold $L_{\rm thr}=4\pi d_L^2 F_{\rm sens}$ | Pinetti+ (2020) | `L_sens(z)` | Same | **Match** | |
| $F_{\rm sens}=10^{-10}$ cm⁻²s⁻¹ (forecast) | Pinetti+ (2020) | `F_SENS=1e-10` | Same | **Match** | |
| Integration via `scipy.quad` in log-$L$ | — | Line 560, `epsrel=1e-5` | Same | N/A | Numerical choice |
| GeV→erg conversion: $1.602\times 10^{-3}$ | Standard | `GeV_to_erg=1.602e-3` | Same | **Match** | |

---

## 7. FSRQ Effective Halo Bias

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Fixed $M_{\rm halo}=10^{13}\,M_\odot$ for blazars | Pinetti+ (2020); standard blazar convention | `bias_astro(z, 'FSRQ')` line 628: `hm.bias(1e13, z)` | Same (inherits q=0.75 bias) | **Match** (convention); **Differs** in $q$ | Luminosity-dependence ignored (deliberate simplification). BL Lac and FSRQ use same fixed mass |
| No luminosity weighting | Pinetti+ (2020) | Fixed single mass | Same | **Differs** (simplification) | No mass-to-luminosity relation for blazars; using physically motivated ~group-scale halo mass |
| Sheth-Tormen bias $b(M,z)$ | Standard | `hm.bias(1e13, z)` | Uses q=0.75 via pinetti2022 | **Match** (structure) | |

---

## 8. Theoretical Deviations & Simplifications

| # | Item | Nature | Severity | Notes |
|---|------|--------|----------|-------|
| T1 | Inverse-sum sign convention: $r^{-p_1}$ vs $r^{+p_1}$ | Deliberate follow-thesis | Medium | Pipeline follows Pinetti (2022) Eq. C.4 (negative exps) vs Ajello (2012) Eq. 15 (positive exps). Evolution profiles differ by ~factor 2 at $r\ne 1$. Documented in `conventions.md` §D12 |
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
| C5 | $d_L$ computed in physical Mpc | Line 517 | Explicit h-factor handling |

---

## 10. Pipeline (Pinetti 2022) Parallel Summary

The Pinetti 2022 parallel implementation makes **no FSRQ-specific deviations** from the pipeline. All parameters and functional forms are identical (pipeline uses Pinetti's sign convention already). Only inherited differences from the halo model affect FSRQ:

- Halo bias uses $q=0.75$ (thesis) vs $q=0.707$ (pipeline default) via `pinetti2022.bias_pinetti()` → ~few-percent shift in FSRQ effective bias
- Limber $k$-substitution uses $k=\ell/\chi$ (thesis) vs $k=(\ell+1/2)/\chi$ (pipeline)

Neither affects the FSRQ window function $W_\gamma^{\rm FSRQ}(z)$ itself — only its projection into $C_\ell$ via the halo model.

---

## 11. Summary of All Deviations from Literature

| # | Item | Ajello+ (2012) | Pipeline | Nature | Severity |
|---|------|----------------|----------|--------|----------|
| 1 | Inverse-sum exponent signs | $[r^{p_1}+r^{p_2}]^{-1}$ (Eq. 15) | $[r^{-p_1}+r^{-p_2}]^{-1}$ | Follows Pinetti thesis Eq. C.4 | Medium |
| 2 | Photon index distribution | Gaussian about $\mu=2.44$ | Single $\alpha=2.44$ | Simplification | Low |
| 3 | Blazar bias mass | Not prescribed per source | Fixed $10^{13}\,M_\odot$ | Convention | Low |

---

## 12. Items Verified Correct

| Concern | Resolution |
|---------|-----------|
| Parameter values match Ajello Table 3 | All 9 parameters verified to match exactly (A, $\gamma_1$, $\gamma_2$, $L_c$, $z_c^\star$, $\alpha_{\rm LDDE}$, $p_1$, $p_2$, $\mu$) |
| LDDE formula structure | Double power-law in L ✓; $z_c(L)$ luminosity dependence ✓; inverse-sum evolution ✓ |
| Peak behavior at $r=1$ | Both Ajello and Pinetti forms give $e(r=1)=1/2$ ✓ |
| Asymptotic behavior | Both forms → 0 as $r\to 0$ or $r\to\infty$ ✓ |
| Sign of evolution exponents | $p_1>0, p_2<0$ both in Ajello and pipeline ✓ |
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
