# Claim-by-Claim Evidence Matrix: BL Lac Window Function Pipeline

## Context

This document audits every equation, model choice, parameter value, and computational method in the BL Lac window function chain (`astro_sources.py`: `_ldde_glf`, `_glf_BL_Lac`, `_BL_LAC_PARAMS`, `W_gamma_astro`, `L_sens`, `F_sens_energy`, `bias_astro`) against the source literature: Ajello+ (2014, ApJ 780, 73), Pinetti+ (2020, arXiv:1911.04989), Pinetti (2022) thesis (arXiv:2212.00125), Ammazzalorso+ (2018, arXiv:1808.09225), Dominguez+ (2011).

Two pipeline implementations are audited side-by-side:
- **Pipeline**: the main `hi_gamma_xcorr/` implementation (with deliberate improvements over the thesis)
- **Pipeline (Pinetti 2022)**: thesis-faithful helper paths from `pinetti2022.py`; there is no separate BL Lac GLF/window implementation in that module

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
| LDDE form: local LF × evolution $e(z, L)$ | Ajello+ (2014); Pinetti thesis Eq. C.4 | `_ldde_glf()` | Same implementation path; no BL Lac override in `pinetti2022.py` | **Match** | |
| Local LF: double power law in $L/L_c$ | Ajello+ (2014) Eq. C.2 | `_ldde_glf()` | Same | **Match** | Returns $d\Phi/d\log_{10}L$ |
| Conversion $d\Phi/d\log_{10}L \to d\Phi/dL$: divide by $L\ln 10$ | Standard calculus | `_ldde_glf()` | Same | **Match** | |
| Luminosity-dependent peak $z_c(L) = z_\star(L/L_{\rm ref})^{\beta}$ | Ajello+ (2014) | `_ldde_glf()` | Same | **Match** | Parameter `alpha` in code = $\beta$ in paper |
| $z_c$ clipped below at 0.01 | Numerical safety | `_ldde_glf()` | Same | **Match** | Avoids $z_c = 0$ singularity |
| Reference luminosity $L_{\rm ref} = 10^{48}$ erg/s | Ajello+ (2014); Pinetti thesis | `L_ref=1e48` in `_BL_LAC_PARAMS` | Same | **Match** | |

---

## 2. BL Lac Parameters (Ajello+ 2014 Table 3, LDDE1)

| Parameter | Literature | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-----------|-----------|----------|-------------------------|--------|-------|
| $A$ | $9.20\times 10^{-11}$ Mpc$^{-3}$ | `_BL_LAC_PARAMS['A']=9.20e-11` | Same | **Match** | |
| $L_c$ (= $L_\star$) | $2.43\times 10^{48}$ erg/s | `L_c=2.43e48` | Same | **Match** | |
| $\gamma_1$ | 1.12 | `gamma1=1.12` | Same | **Match** | |
| $\gamma_2$ | 3.71 | `gamma2=3.71` | Same | **Match** | |
| $z_\star$ | 1.67 | `z_c_star=1.67` | Same | **Match** | |
| $\beta$ (luminosity dep. of $z_c$) | $4.46\times 10^{-2}$ | `alpha=4.46e-2` | Same | **Match** | Note: code symbol `alpha` = paper symbol $\beta$ |
| $p_1$ | 4.50 | `p1=4.50` | Same | **Match** | |
| $p_2$ | $-12.88$ | `p2=-12.88` | Same | **Match** | |
| Photon index $\alpha$ | 2.11 (Pinetti+ 2020 Table 3) | `ASTRO_SOURCES['BL_Lac']['alpha']=2.11` | Same | **Match** | Ajello+ 2014 LDDE1 fit: $\mu_\star = 2.12\pm 0.03$ |
| $L_{\min}$ | $7\times 10^{43}$ erg/s (Pinetti+ 2020) | `ASTRO_SOURCES['BL_Lac']['L_min']=7e43` | Same | **Match** | |
| $L_{\max}$ | $10^{52}$ erg/s (Pinetti+ 2020) | `ASTRO_SOURCES['BL_Lac']['L_max']=1e52` | Same | **Match** | |

---

## 3. LDDE Evolution Form (Sign Convention)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Inverse-sum form: $e(z) = [r^{p_1} + r^{p_2}]^{-1}$ | Ajello+ (2014) Eq. 18; Pinetti Eq. C.4 writes $[r^{-p_1}+r^{-p_2}]^{-1}$ | `_ldde_glf()` evaluates `1.0 / (ratio**p1 + ratio**p2)` | Same implementation path; no BL Lac-specific override in `pinetti2022.py` | **Partial** | The active pipeline follows Ajello's fitted convention. The thesis sign flip is documented here as a literature-side deviation. |
| Alternative piecewise form available | — | `_ldde_glf(..., evolution_form='piecewise')` | Same | N/A | Not used for BL Lac; kept for comparison |
| Alternative sum form available | — | `_ldde_glf(..., evolution_form='sum')` | Same | N/A | Not used |
| Smooth (continuous) at $z=z_c$ | Inverse-sum form property | Verified analytically | Same | **Match** | |

---

## 4. Photon Spectral Energy Distribution

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Power-law SED $dN/dE \propto E^{-\alpha}$ | Pinetti+ (2020); Ajello+ (2014) population SED | `W_gamma_astro()` | Same | **Match** | |
| Single fixed $\alpha = 2.11$ for all BL Lacs | Pinetti+ (2020) Table 3 | `alpha = 2.11` | Same | **Partial** (simplification) | No scatter, no L-dependence, no log-parabola. Ajello+ 2014 shows $\mu_\star = 2.12\pm 0.03$ with intrinsic scatter $\sigma_\mu = 0.27$ |
| $dN/dE = L \cdot E_{\rm rest}^{-\alpha} / ({\rm GeV}_{\rm erg}\,I_\alpha)$ | Standard flux-luminosity relation | `W_gamma_astro()` | Same | **Match** | |
| ${\rm GeV}_{\rm erg} = 1.602\times 10^{-3}$ erg/GeV | Standard | `W_gamma_astro()` constant `GeV_to_erg = 1.602e-3` | Same | **Match** | |
| Energy band: 0.1-100 GeV | Pinetti+ (2020); Fermi-LAT standard | `W_gamma_astro()` with `E_min_band=0.1`, `E_max_band=100.0` | Same | **Match** | |
| $I_\alpha = \int_{0.1}^{100}E^{1-\alpha}\,dE$ | Standard normalization | `W_gamma_astro()` | Same | **Match** | Analytic formula with safe branch for $\alpha\to 2$ |
| $E_{\rm rest} = (1+z)E_{\rm obs}$ | Standard cosmological blueshift | `W_gamma_astro()` | Same | **Match** | |
| No EBL attenuation $e^{-\tau}$ applied | — | Not present in `W_gamma_astro` | Same | **Differs** (simplification) | EBL applied to $W_\gamma^{\rm DM}$ but not to astrophysical windows. Matters for $E \gt 30$ GeV at $z \gt 0.5$ |

---

## 5. Fermi-LAT Flux Sensitivity Threshold

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| $L_{\rm thr}(z) = 4\pi d_L^2(z)\,F_{\rm sens}$ | Pinetti+ (2020) | `L_sens(z)` | Same | **Match** | |
| $d_L$ in physical cm | Conversion required | Lines 41-42: `dL_Mpc = cosmo.d_L(z) / cfg.h` then $\times$ `MPC_TO_M * 100.0` | Same | **Match** | Correctly converts Mpc/h $\to$ Mpc $\to$ cm |
| $F_{\rm sens} = 10^{-10}$ cm$^{-2}$ s$^{-1}$ (forecast) | Pinetti+ (2020) | `config.py:F_SENS=1e-10` | Same | **Match** | |
| Energy-dependent $F_{\rm sens}(E)$ (data mode) | Ammazzalorso+ (2018) Eq. 1 | `F_sens_energy(E)` | Same | **Match** | |
| $F_{\rm sens}(E) \propto [\sigma_0(E)/\sigma_0(E_{\rm ref})]^2$ | PSF-area scaling | Line 67 | Same | **Partial** | Pipeline approximation of Ammazzalorso's masking criterion; Ammazzalorso Eq. 1 is more detailed (depends on faintest source flux ratio) |
| Reference energy $E_{\rm ref} = 5$ GeV | Pipeline convention | `F_sens_energy()` uses `E_ref = 5.0` | Same | **Differs** | Not specified in Ammazzalorso; pipeline choice near Fermi's optimal sensitivity |
| $\sigma_0(E)$ from Fermi PSF model | Ammazzalorso+ (2018) | `noise_model.sigma_psf_fermi(E)` | Same | **Match** | Energy-dependent 68% containment |

---

## 6. Window Function Assembly (Pinetti+ Eq. 4.3)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Formula $W = [d_L^2/(1+z)^2]\int\Phi\,(dF/dE)\,dL$ | Pinetti+ (2020) Eq. 4.3 | `W_gamma_astro()` returns the photon-emissivity form after the $d_L^2$ cancellation | Same | **Partial** | The active implementation keeps the equivalent final `val / (4\pi h^3)` form rather than an explicit $(1+z)^{-2}$ prefactor. |
| $d_L^2$ cancels with $1/(4\pi d_L^2)$ in $dF/dE$ | Algebra | Implicit (not written explicitly) | Same | **Match** | Pipeline computes the cancellation form directly |
| Prefactor $1/(4\pi)$ plus h-conversion | Flux-per-steradian convention and pipeline unit convention | `W_gamma_astro()` return value | Same | **Match** | The final `h^{-3}` converts the physical GLF density to [(Mpc/h)$^{-3}$]. |
| $L_{\rm up} = \min(L_{\max}, L_{\rm thr})$ | Pinetti+ (2020) unresolved selection | `W_gamma_astro()` | Same | **Match** | |
| Integration via `scipy.quad` in log-$L$ | Numerical choice | `W_gamma_astro()` with `epsrel=1e-5`, `limit=200` | Same | N/A | High accuracy |
| Integrand: $\phi \cdot dN/dE \cdot L$ (from $d\ln L$) | Change of variables | `W_gamma_astro()` | Same | **Match** | |
| Returns $[(\mathrm{Mpc}/h)^{-3}\,{\rm ph}\,{\rm s}^{-1}\,{\rm GeV}^{-1}\,{\rm sr}^{-1}]$ | Pipeline per-$\chi$ convention | `W_gamma_astro()` | Same | **Match** | `d_L` is computed in physical units, then the final `h^{-3}` converts the emissivity density to the pipeline convention. |
| Early return if $z \le 0$ | Numerical safety | `W_gamma_astro()` | Same | **Match** | |
| Early return if $L_{\rm up} \le L_{\min}$ | Numerical safety | `W_gamma_astro()` | Same | **Match** | |
| `unresolved_only=True` flag | Pipeline option | Default: True | Same | N/A | `False` gives total emission (survey-independent) |
| `unresolved_mode` ('forecast'/'data') flag | Pipeline option | Default: 'forecast' | Same | N/A | Determines $F_{\rm sens}(E)$ behavior |

---

## 7. Effective Halo Bias

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|-------------------------|--------|-------|
| Fixed halo mass for BL Lac: $M_{\rm halo} = 10^{13}\,M_\odot/h$ | Standard blazar clustering | `bias_astro(z, 'BL_Lac')`: `hm.bias(1e13, z)` | Same mass convention; thesis bias helper changes only $q$ when used | **Partial** (simplification) | No $L$- or $z$-dependence; standard in Pinetti 2022 and blazar clustering literature |
| Same mass used for FSRQ | — | `bias_astro()` branch `source_class in ('BL_Lac', 'FSRQ')` | Same | **Match** | Both blazar classes share the approximation |
| Sheth-Tormen bias $b(M, z)$ | Sheth & Tormen (1999) | `halo_model.bias` | `pinetti2022.bias_pinetti` with $q=0.75$ | **Match** (structure); **Differs** (q value) | Inherits halo model $q$ difference |

---

## 8. Theoretical Deviations & Simplifications

| # | Item | Nature | Severity | Notes |
|---|------|--------|----------|-------|
| T1 | Thesis Eq. C.4 flips the LDDE exponent signs relative to Ajello | Deliberate implementation choice | Medium | The active pipeline keeps Ajello+ (2014) Eq. 18 so the published LDDE1 fit is used in the convention in which it was calibrated. |
| T2 | Single fixed photon index $\alpha=2.11$ | Simplification | Low | Real BL Lac population has $\sigma_\mu \sim 0.27$ scatter and HSP/ISP/LSP sub-populations with different peak energies |
| T3 | No EBL attenuation on astrophysical window | Simplification | Medium | Matters for $E \gt 30$ GeV at $z \gt 0.5$ (up to factor ~10 suppression). DM window correctly includes $e^{-\tau}$; astro windows do not |
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
| C5 | $z_c$ lower-clipped at 0.01 | Line 411 | Prevents singularity at $L\to 0$ or $\beta \lt 0$ |
| C6 | $\max(\phi\cdot e, 0)$ safeguard | Line 435 | Prevents negative GLF from numerical edge cases |

---

## 10. Pipeline (Pinetti 2022) Parallel Summary

The `pinetti2022.py` module does **not** implement a separate BL Lac GLF or window-function path. For BL Lac, the main `astro_sources.py` implementation is the implemented source of truth. Relative to the thesis text, the active pipeline makes one explicit blazar-specific choice: it keeps Ajello+ (2014) Eq. 18 with positive exponents rather than the sign-flipped thesis Eq. C.4.

Shared infrastructure differences (inherited through the cross-power, not through $W_\gamma^{\rm BL\,Lac}$ itself):
- **Halo bias**: `pinetti2022.bias_pinetti()` uses $q=0.75$ (thesis) vs pipeline's $q=0.707$. Affects the Sheth-Tormen bias evaluated at $M_{\rm halo} = 10^{13}\,M_\odot/h$ (~5% effect on the 2-halo amplitude).
- **Limber $k$-substitution**: Pinetti 2022 uses $k=\ell/\chi$ (thesis) via `pinetti2022.limber_k()` vs pipeline's $k=(\ell+1/2)/\chi$ (LoVerde & Afshordi 2008). ~5% effect at $\ell=10$, negligible at $\ell > 100$.
- **Correa concentration (D2)**: Pipeline uses Planck Appendix B1 fit; thesis uses different cosmology fit. <5% effect on $c$. See [HI Evidence Matrix](hi_evidence_matrix.md).

None of these affect the BL Lac window function $W_\gamma^{\rm BL\,Lac}(E_\gamma, z)$ itself — only its projection into $C_\ell$ via `angular_power.P_HI_astro_2h`.

---

## 11. Summary of All Deviations from Literature/Thesis

| # | Item | Literature/Thesis | Pipeline | Pipeline (Pinetti 2022) | Nature | Severity |
|---|------|-------------------|----------|-------------------------|--------|----------|
| 1 | LDDE exponent signs | Ajello+ 2014 Eq. 18 uses $r^{+p_i}$; Pinetti thesis Eq. C.4 writes $r^{-p_i}$ | $r^{+p_i}$ | No separate BL Lac thesis override | Deliberate choice to preserve Ajello's fit convention | Medium |
| 2 | Single photon index $\alpha=2.11$ | Ajello+ 2014: $\mu_\star=2.12\pm 0.03$ | Fixed $\alpha=2.11$ | Same | Simplification | Low (below 1% on $\alpha$) |
| ~~3~~ | ~~No EBL attenuation~~ | — | **Resolved:** $e^{-\tau}$ now applied at observed energy in `W_gamma_astro` | Same | — | — |
| 4 | Fixed $M_{\rm halo} = 10^{13}\,M_\odot/h$ | Standard in thesis | Same | Same | Simplification | Minor |
| 5 | Data-mode $F_{\rm sens}(E) \propto [\sigma_0(E)]^2$ | Ammazzalorso Eq. 1: more complex masking | $[\sigma_0(E)]^2$ proxy | Same | Simplification | Low |
| 6 | $E_{\rm ref} = 5$ GeV (data mode) | Not specified | Pipeline choice | Same | Convention | None |
| 7 | Halo bias $q$ parameter | Thesis $q=0.75$ | Pipeline $q=0.707$ | $q=0.75$ | Calibration | ~5% on bias |
| 8 | Limber $k$-substitution | Thesis $k=\ell/\chi$ | $k=(\ell+1/2)/\chi$ | $k=\ell/\chi$ | Pipeline improvement | Negligible |

---

## 12. Items Verified Correct (Potential Concerns Dismissed)

| Concern | Resolution | Pipeline (Pinetti 2022) |
|---------|-----------|------------------------|
| Does $A$ normalize $d\Phi/dL$ or $d\Phi/d\log_{10}L$? | Normalizes $d\Phi/d\log_{10}L$ [Mpc$^{-3}$]; code divides by $L\ln 10$ inside `_ldde_glf()` to convert | Same |
| Is code symbol `alpha` the photon index or the $z_c(L)$ exponent $\beta$? | In `_BL_LAC_PARAMS['alpha']` it is the $z_c(L)$ exponent $\beta = 0.0446$. The photon index $\alpha = 2.11$ lives in `ASTRO_SOURCES['BL_Lac']['alpha']` | Same |
| $d_L$ physical or comoving? | Physical: `d_L(z) / cfg.h` converts Mpc/h $\to$ Mpc in `L_sens()` and `W_gamma_astro()` | Same |
| $d_L^2$ cancellation with $dF/dE$'s $1/(4\pi d_L^2)$? | The current implementation evaluates the emissivity integral directly and returns `val / (4\pi h^3)`, so no explicit $d_L^2$ or $(1+z)^{-2}$ prefactor remains in the final pipeline form; the extra `h^{-3}` is the pipeline unit conversion | Same |
| Observed vs rest-frame energy in $dN/dE$ | Rest-frame: $E_{\rm rest} = (1+z)E_{\rm obs}$, used in the `E_{\rm rest}^{-\alpha}` factor inside `W_gamma_astro()` | Same |
| $I_\alpha$ behavior at $\alpha \to 2$ | Separate log branch in `W_gamma_astro()` avoids division by zero | Same |
| LDDE at $L\to 0$ or $L\to\infty$ behavior | Double power law gives smooth cutoff both ways; $z_c$ clipped at 0.01 to avoid $\beta$-induced singularity | Same |
| Unit consistency in $W$ output | $\phi$ [Mpc$^{-3}$ (erg/s)$^{-1}$] $\times$ $dN/dE$ [ph/s/GeV] $\times$ $L$ [erg/s] = [Mpc$^{-3}$ ph s$^{-1}$ GeV$^{-1}$], and the final return is `val / (4\pi h^3)` in the photon-emissivity convention. Correct | Same |
