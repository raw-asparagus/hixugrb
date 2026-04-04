# Claim-by-Claim Evidence Matrix: BL Lac Window Function Pipeline

## Context

This document audits every equation, model choice, parameter value, and computational method in the BL Lac window function chain (`astro_sources.py`: `_ldde_glf`, `_glf_BL_Lac`, `_BL_LAC_PARAMS`, `W_gamma_astro`, `L_sens`, `F_sens_energy`, `bias_astro`) against the source literature: Ajello+ (2014, ApJ 780, 73), Pinetti+ (2020, arXiv:1911.04989), Pinetti (2022) thesis (arXiv:2212.00125), Ammazzalorso+ (2018, arXiv:1806.10859), Dominguez+ (2011).

Two pipeline implementations are audited side-by-side:
- **Pipeline**: the main `hi_gamma_xcorr/` implementation (with deliberate improvements over the thesis)
- **Pipeline (Pinetti 2022)**: the `pinetti2022.py` parallel implementation (faithful to thesis choices where they differ)

For the shared cosmological backbone (Layer 1) and halo model infrastructure (halo bias), see the [HI Evidence Matrix](hi_evidence_matrix.md). This matrix focuses on BL Lac-specific components.

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

## 1. Ajello (2014) LDDE GLF Structure

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| LDDE form: local LF × evolution $e(z, L)$ | Ajello+ (2014); Pinetti thesis Eq. C.4 | `_ldde_glf` | Same (no override) | **Match** | |
| Local LF: double power law in $L/L_c$ | Ajello+ (2014) Eq. C.2 | Lines 402-404: $A / (x^{\gamma_1} + x^{\gamma_2})$ | Same | **Match** | Returns $d\Phi/d\log_{10}L$ |
| Conversion $d\Phi/d\log_{10}L \to d\Phi/dL$: divide by $L\ln 10$ | Standard calculus | Line 407 | Same | **Match** | |
| Luminosity-dependent peak $z_c(L) = z_\star(L/L_{\rm ref})^{\beta}$ | Ajello+ (2014) | Line 410 | Same | **Match** | Parameter `alpha` in code = $\beta$ in paper |
| $z_c$ clipped below at 0.01 | Numerical safety | Line 411 | Same | **Match** | Avoids $z_c = 0$ singularity |
| Reference luminosity $L_{\rm ref} = 10^{48}$ erg/s | Ajello+ (2014); Pinetti thesis | `L_ref=1e48` in `_BL_LAC_PARAMS` | Same | **Match** | |

---

## 2. BL Lac Parameters (Pinetti thesis Table C.1 / Ajello+ 2014 LDDE1)

| Parameter | Literature | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----------|-----------|----------|-------------------------|--------|
| $A$ | $9.20\times 10^{-11}$ Mpc$^{-3}$ | `_BL_LAC_PARAMS['A']=9.20e-11` | Same | **Match** |
| $L_c$ (= $L_\star$) | $2.43\times 10^{48}$ erg/s | `L_c=2.43e48` | Same | **Match** |
| $\gamma_1$ | 1.12 | `gamma1=1.12` | Same | **Match** |
| $\gamma_2$ | 3.71 | `gamma2=3.71` | Same | **Match** |
| $z_\star$ | 1.67 | `z_c_star=1.67` | Same | **Match** |
| $\beta$ (luminosity dep. of $z_c$) | $4.46\times 10^{-2}$ | `alpha=4.46e-2` | Same | **Match** | Note: code symbol `alpha` = paper symbol $\beta$ |
| $p_1$ | 4.50 | `p1=4.50` | Same | **Match** |
| $p_2$ | $-12.88$ | `p2=-12.88` | Same | **Match** |
| Photon index $\alpha$ | 2.11 (Pinetti+ 2020 Table 3) | `ASTRO_SOURCES['BL_Lac']['alpha']=2.11` | Same | **Match** | Ajello+ 2014 LDDE1 fit: $\mu_\star = 2.12\pm 0.03$ |
| $L_{\min}$ | $7\times 10^{43}$ erg/s (Pinetti+ 2020) | `ASTRO_SOURCES['BL_Lac']['L_min']=7e43` | Same | **Match** | |
| $L_{\max}$ | $10^{52}$ erg/s (Pinetti+ 2020) | `ASTRO_SOURCES['BL_Lac']['L_max']=1e52` | Same | **Match** | |

---

## 3. LDDE Evolution Form (Sign Convention)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Inverse-sum form: $e(z) = [r^{\pm p_1} + r^{\pm p_2}]^{-1}$ | Ajello+ (2014) Eq. 18 (positive); Pinetti Eq. C.4 (negative) | `evolution_form='ldde_inv'` | Same | **Partial** | Mathematically equivalent under sign flip of $p_i$ |
| **Negative-exponent form**: $e(z) = [r^{-p_1} + r^{-p_2}]^{-1}$ | Pinetti (2022) thesis Eq. C.4 | `e_z = 1.0 / (ratio**(-p1) + ratio**(-p2))` line 422 | Same | **Differs** (vs Ajello) | Pipeline and Pinetti 2022 both follow thesis negative-exponent convention. Ajello+ 2014 Eq. 18 uses positive exponents. Since $p_i$ values are taken from the same source, only the sign convention differs. See `pinetti2022_evidence_matrix.md` D12 |
| Alternative piecewise form available | — | `evolution_form='piecewise'` (legacy, lines 423-428) | Same | N/A | Not used for BL Lac; kept for comparison |
| Alternative sum form available | — | `evolution_form='sum'` (legacy, lines 429-431) | Same | N/A | Not used |
| Smooth (continuous) at $z=z_c$ | Inverse-sum form property | Lines 416-422 | Same | **Match** | |

---

## 4. Photon Spectral Energy Distribution

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Power-law SED $dN/dE \propto E^{-\alpha}$ | Pinetti+ (2020); Ajello+ (2014) population SED | Lines 551-556 | Same | **Match** | |
| Single fixed $\alpha = 2.11$ for all BL Lacs | Pinetti+ (2020) Table 3 | `alpha = 2.11` | Same | **Partial** (simplification) | No scatter, no L-dependence, no log-parabola. Ajello+ 2014 shows $\mu_\star = 2.12\pm 0.03$ with intrinsic scatter $\sigma_\mu = 0.27$ |
| $dN/dE = L \cdot E_{\rm rest}^{-\alpha} / ({\rm GeV}_{\rm erg}\,I_\alpha)$ | Standard flux-luminosity relation | Line 556 | Same | **Match** | |
| ${\rm GeV}_{\rm erg} = 1.602\times 10^{-3}$ erg/GeV | Standard | `GeV_to_erg = 1.602e-3` (line 540) | Same | **Match** | |
| Energy band: 0.1-100 GeV | Pinetti+ (2020); Fermi-LAT standard | `E_min_band=0.1, E_max_band=100.0` (lines 538-539) | Same | **Match** | |
| $I_\alpha = \int_{0.1}^{100}E^{1-\alpha}\,dE$ | Standard normalization | Line 544 (generic $\alpha$), Line 546 (log branch for $\alpha\approx 2$) | Same | **Match** | Analytic formula with safe branch for $\alpha\to 2$ |
| $E_{\rm rest} = (1+z)E_{\rm obs}$ | Standard cosmological blueshift | Line 549 | Same | **Match** | |
| No EBL attenuation $e^{-\tau}$ applied | — | Not present in `W_gamma_astro` | Same | **Differs** (simplification) | EBL applied to $W_\gamma^{\rm DM}$ but not to astrophysical windows. Matters for $E > 30$ GeV at $z > 0.5$ |

---

## 5. Fermi-LAT Flux Sensitivity Threshold

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $L_{\rm thr}(z) = 4\pi d_L^2(z)\,F_{\rm sens}$ | Pinetti+ (2020) | `L_sens(z)` line 49 | Same | **Match** | |
| $d_L$ in physical cm | Conversion required | Lines 41-42: `dL_Mpc = cosmo.d_L(z) / cfg.h` then $\times$ `MPC_TO_M * 100.0` | Same | **Match** | Correctly converts Mpc/h $\to$ Mpc $\to$ cm |
| $F_{\rm sens} = 10^{-10}$ cm$^{-2}$ s$^{-1}$ (forecast) | Pinetti+ (2020) | `config.py:F_SENS=1e-10` | Same | **Match** | |
| Energy-dependent $F_{\rm sens}(E)$ (data mode) | Ammazzalorso+ (2018) Eq. 1 | `F_sens_energy(E)` line 52 | Same | **Match** | |
| $F_{\rm sens}(E) \propto [\sigma_0(E)/\sigma_0(E_{\rm ref})]^2$ | PSF-area scaling | Line 67 | Same | **Partial** | Pipeline approximation of Ammazzalorso's masking criterion; Ammazzalorso Eq. 1 is more detailed (depends on faintest source flux ratio) |
| Reference energy $E_{\rm ref} = 5$ GeV | Pipeline convention | `E_ref = 5.0` (line 64) | Same | **Differs** | Not specified in Ammazzalorso; pipeline choice near Fermi's optimal sensitivity |
| $\sigma_0(E)$ from Fermi PSF model | Ammazzalorso+ (2018) | `noise_model.sigma_psf_fermi(E)` | Same | **Match** | Energy-dependent 68% containment |

---

## 6. Window Function Assembly (Pinetti+ Eq. 4.3)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Formula $W = [d_L^2/(1+z)^2]\int\Phi\,(dF/dE)\,dL$ | Pinetti+ (2020) Eq. 4.3 | `W_gamma_astro` lines 485-569 | Same | **Match** | |
| $d_L^2$ cancels with $1/(4\pi d_L^2)$ in $dF/dE$ | Algebra | Implicit (not written explicitly) | Same | **Match** | Pipeline computes the cancellation form directly |
| $(1+z)^{-2}$ cosmological dimming factor | Pinetti+ (2020) Eq. 4.3 | Line 569: `val / (4.0 * np.pi * (1.0 + z)**2)` | Same | **Match** | |
| Prefactor $1/(4\pi)$ | Flux-per-steradian convention | Line 569 | Same | **Match** | |
| $L_{\rm up} = \min(L_{\max}, L_{\rm thr})$ | Pinetti+ (2020) unresolved selection | Line 525 | Same | **Match** | |
| Integration via `scipy.quad` in log-$L$ | Numerical choice | Line 560: `epsrel=1e-5, limit=200` | Same | N/A | High accuracy |
| Integrand: $\phi \cdot dN/dE \cdot L$ (from $d\ln L$) | Change of variables | Line 558 | Same | **Match** | |
| Returns $[{\rm Mpc}^{-3}\,{\rm ph}\,{\rm s}^{-1}\,{\rm GeV}^{-1}\,{\rm sr}^{-1}]$ | Pipeline per-$\chi$ convention | Line 569 | Same | **Match** | Uses physical Mpc (from $d_L$ in physical units) |
| Early return if $z \le 0$ | Numerical safety | Lines 509-510 | Same | **Match** | |
| Early return if $L_{\rm up} \le L_{\min}$ | Numerical safety | Lines 529-530 | Same | **Match** | |
| `unresolved_only=True` flag | Pipeline option | Default: True | Same | N/A | `False` gives total emission (survey-independent) |
| `unresolved_mode` ('forecast'/'data') flag | Pipeline option | Default: 'forecast' | Same | N/A | Determines $F_{\rm sens}(E)$ behavior |

---

## 7. Effective Halo Bias

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Fixed halo mass for BL Lac: $M_{\rm halo} = 10^{13}\,M_\odot/h$ | Standard blazar clustering | `hm.bias(1e13, z)` line 628 | Same (but uses $q=0.75$ bias) | **Partial** (simplification) | No $L$- or $z$-dependence; standard in Pinetti 2022 and blazar clustering literature |
| Same mass used for FSRQ | — | Line 627: `source_class in ('BL_Lac', 'FSRQ')` | Same | **Match** | Both blazar classes share the approximation |
| Sheth-Tormen bias $b(M, z)$ | Sheth & Tormen (1999) | `halo_model.bias` | `pinetti2022.bias_pinetti` with $q=0.75$ | **Match** (structure); **Differs** (q value) | Inherits halo model $q$ difference |

---

## 8. Theoretical Deviations & Simplifications

| # | Item | Nature | Severity | Notes |
|---|------|--------|----------|-------|
| T1 | LDDE negative-exponent sign convention | Literature choice | Shape-level | Pipeline follows Pinetti (2022) thesis Eq. C.4 with $r^{-p_i}$; Ajello+ 2014 Eq. 18 uses $r^{+p_i}$. Parameter values unchanged. See deviation D12 |
| T2 | Single fixed photon index $\alpha=2.11$ | Simplification | Low | Real BL Lac population has $\sigma_\mu \sim 0.27$ scatter and HSP/ISP/LSP sub-populations with different peak energies |
| T3 | No EBL attenuation on astrophysical window | Simplification | Medium | Matters for $E > 30$ GeV at $z > 0.5$ (up to factor ~10 suppression). DM window correctly includes $e^{-\tau}$; astro windows do not |
| T4 | Fixed halo mass $10^{13}\,M_\odot/h$ (no $L$-dependence) | Simplification | Minor | $\sim 10$--$20\%$ on clustering amplitude. Standard in blazar literature |
| T5 | $E_{\rm ref}=5$ GeV for PSF scaling (data mode) | Convention | Low | Not specified in Ammazzalorso+ 2018; pipeline choice |
| T6 | Simplified PSF-area scaling vs Ammazzalorso Eq. 1 | Simplification | Low | Ammazzalorso's exact masking depends on bright-source distribution; pipeline uses $[\sigma_0(E)]^2$ proxy |
| T7 | No scatter in LDDE parameters | Literature choice | Low | Pipeline uses best-fit values; parameter uncertainties not propagated |
| T8 | Power-law SED (no log-parabola or cutoff) | Simplification | Low | Adequate for 0.1-100 GeV population-averaged spectrum |

---

## 9. Computational Simplifications

| # | Item | Method | Impact |
|---|------|--------|--------|
| C1 | LDDE GLF: direct function evaluation (no caching) | Per-call recomputation | Fine (cheap evaluation) |
| C2 | Window integral via `scipy.quad` in log-$L$ | `epsrel=1e-5`, `limit=200` | High accuracy |
| C3 | $I_\alpha$ computed analytically with log branch at $\alpha \approx 2$ | Lines 543-546 | Exact, safe near $\alpha=2$ |
| C4 | $d_L$ converted to physical cm | Lines 41-42, 517-518 | Explicit h-factor handling |
| C5 | $z_c$ lower-clipped at 0.01 | Line 411 | Prevents singularity at $L\to 0$ or $\beta < 0$ |
| C6 | $\max(\phi\cdot e, 0)$ safeguard | Line 435 | Prevents negative GLF from numerical edge cases |

---

## 10. Pipeline (Pinetti 2022) Parallel Summary

The Pinetti 2022 parallel implementation (`pinetti2022.py`) makes **no BL Lac-specific deviations** from the pipeline. The GLF structure, LDDE parameters, evolution form, photon SED, and window function assembly are identical between the two implementations.

Shared infrastructure differences (inherited through the cross-power, not through $W_\gamma^{\rm BL\,Lac}$ itself):
- **Halo bias**: `pinetti2022.bias_pinetti()` uses $q=0.75$ (thesis) vs pipeline's $q=0.707$. Affects the Sheth-Tormen bias evaluated at $M_{\rm halo} = 10^{13}\,M_\odot/h$ (~5% effect on the 2-halo amplitude).
- **Limber $k$-substitution**: Pinetti 2022 uses $k=\ell/\chi$ (thesis) via `pinetti2022.limber_k()` vs pipeline's $k=(\ell+1/2)/\chi$ (LoVerde & Afshordi 2008). ~5% effect at $\ell=10$, negligible at $\ell > 100$.

None of these affect the BL Lac window function $W_\gamma^{\rm BL\,Lac}(E_\gamma, z)$ itself — only its projection into $C_\ell$ via `angular_power.P_HI_astro_2h`.

---

## 11. Summary of All Deviations from Literature/Thesis

| # | Item | Literature/Thesis | Pipeline | Pipeline (Pinetti 2022) | Nature | Severity |
|---|------|-------------------|----------|-------------------------|--------|----------|
| 1 | LDDE exponent signs | Ajello+ 2014: $r^{+p_i}$ | $r^{-p_i}$ (thesis convention) | Same | Literature choice | Shape-level |
| 2 | Single photon index $\alpha=2.11$ | Ajello+ 2014: $\mu_\star=2.12\pm 0.03$ | Fixed $\alpha=2.11$ | Same | Simplification | Low (<1% on $\alpha$) |
| 3 | No EBL attenuation | Pinetti Eq. 4.3 does not include $e^{-\tau}$ explicitly; literature treats EBL separately | No $e^{-\tau}$ | Same | Simplification | Medium ($E > 30$ GeV) |
| 4 | Fixed $M_{\rm halo} = 10^{13}\,M_\odot/h$ | Standard in thesis | Same | Same | Simplification | Minor |
| 5 | Data-mode $F_{\rm sens}(E) \propto [\sigma_0(E)]^2$ | Ammazzalorso Eq. 1: more complex masking | $[\sigma_0(E)]^2$ proxy | Same | Simplification | Low |
| 6 | $E_{\rm ref} = 5$ GeV (data mode) | Not specified | Pipeline choice | Same | Convention | None |
| 7 | Halo bias $q$ parameter | Thesis $q=0.75$ | Pipeline $q=0.707$ | $q=0.75$ | Calibration | ~5% on bias |
| 8 | Limber $k$-substitution | Thesis $k=\ell/\chi$ | $k=(\ell+1/2)/\chi$ | $k=\ell/\chi$ | Pipeline improvement | Negligible |

---

## 12. Items Verified Correct (Potential Concerns Dismissed)

| Concern | Resolution | Pipeline (Pinetti 2022) |
|---------|-----------|------------------------|
| Does $A$ normalize $d\Phi/dL$ or $d\Phi/d\log_{10}L$? | Normalizes $d\Phi/d\log_{10}L$ [Mpc$^{-3}$]; code divides by $L\ln 10$ at line 407 to convert | Same |
| Is code symbol `alpha` the photon index or the $z_c(L)$ exponent $\beta$? | In `_BL_LAC_PARAMS['alpha']` it is the $z_c(L)$ exponent $\beta = 0.0446$. The photon index $\alpha = 2.11$ lives in `ASTRO_SOURCES['BL_Lac']['alpha']` | Same |
| $d_L$ physical or comoving? | Physical: `d_L(z) / cfg.h` converts Mpc/h $\to$ Mpc (lines 41, 517) | Same |
| $d_L^2$ cancellation with $dF/dE$'s $1/(4\pi d_L^2)$? | Yes: the pipeline integrand is $\phi \cdot dN/dE \cdot L$ (no explicit $d_L$), with $1/(4\pi(1+z)^2)$ prefactor at the end. Equivalent to Pinetti Eq. 4.3 after cancellation | Same |
| Observed vs rest-frame energy in $dN/dE$ | Rest-frame: $E_{\rm rest} = (1+z)E_{\rm obs}$ at line 549, used in $E_{\rm rest}^{-\alpha}$ at line 556 | Same |
| $I_\alpha$ behavior at $\alpha \to 2$ | Separate log branch (line 546); avoids division by zero | Same |
| LDDE at $L\to 0$ or $L\to\infty$ behavior | Double power law gives smooth cutoff both ways; $z_c$ clipped at 0.01 to avoid $\beta$-induced singularity | Same |
| Unit consistency in $W$ output | $\phi$ [Mpc$^{-3}$ (erg/s)$^{-1}$] $\times$ $dN/dE$ [ph/s/GeV] $\times$ $L$ [erg/s] = [Mpc$^{-3}$ ph s$^{-1}$ GeV$^{-1}$], divided by $4\pi(1+z)^2$ gives per-sr. Correct | Same |
