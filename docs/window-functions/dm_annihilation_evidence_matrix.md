# Claim-by-Claim Evidence Matrix: DM Annihilation Window Function Pipeline

## Context

This document audits every equation, model choice, parameter value, and computational method in the DM annihilation window function chain (`dm_model.py`, `pppc4dmid.py`, `ebl.py`) against the source literature: Pinetti+ (2020, arXiv:1911.04989), Pinetti (2022) thesis (arXiv:2212.00125), Moline et al. (2017, MNRAS 466, 4974), Cirelli et al. (2011, arXiv:1012.4515), Correa et al. (2015, arXiv:1502.00391), and Dominguez et al. (2011, arXiv:1007.1459).

Two pipeline implementations are audited side-by-side:
- **Pipeline**: the main `hi_gamma_xcorr/` implementation (with deliberate improvements over the thesis)
- **Pipeline (Pinetti 2022)**: the `pinetti2022.py` parallel implementation (faithful to thesis choices where they differ)

For the shared cosmological backbone (Layer 1) and halo model infrastructure (Layer 2), see the [HI Evidence Matrix](hi_evidence_matrix.md). This matrix focuses on DM-specific components and cross-cutting issues.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| **Match** | Pipeline agrees with literature |
| **Match (thesis)** | Pinetti 2022 parallel agrees with thesis |
| **Differs** | Pipeline uses a different choice (noted) |
| **Partial** | Partially matches; deviations noted |
| **Investigate** | Potential issue requiring verification |
| **Bug** | Confirmed error |

---

## 0. Cross-Cutting Issue: h-Factor Mass Conversion

**Resolved.** All mass conversions now use the correct $M_{\rm phys} = M_{\rm code}/h$ convention, consistent with the density unit identity $[M_\odot/h] = (1/h)\,M_\odot$ and with `v_circ`. The previous `M * h` bug in `concentration_correa`, `boost_moline`, `c_HI`, and `concentration_correa_thesis` has been fixed to `M / h`.

| Function | Conversion | Status |
|----------|------------|--------|
| `halo_model.py:v_circ` | `M / cfg.h` | **Correct** |
| `halo_model.py:concentration_correa` | `M / cfg.h` | **Correct** (fixed from `M * cfg.h`) |
| `pinetti2022.py:concentration_correa_thesis` | `M / cfg.h` | **Correct** (fixed from `M * cfg.h`) |
| `dm_model.py:boost_moline` | `M / cfg.h` | **Correct** (fixed from `M * cfg.h`) |
| `hi_model.py:c_HI` | `M / cfg.h` | **Correct** (fixed from `M * cfg.h`) |
| `conventions.md` (line 48) | `M / h` | **Correct** (fixed from `M * h`) |

**Note:** The $W_\gamma^{\rm DM}$ unit conversion chain (density $\to$ GeV/cm$^3$) uses $h^2$ and is **independently verified correct** -- it does not depend on the mass conversion convention.

---

## 1. Shared Infrastructure (reference)

The following shared components are audited in the [HI Evidence Matrix](hi_evidence_matrix.md):

- Planck 2018 cosmological parameters -- **Match** (both pipelines)
- $H(z)$, $\chi(z)$, $P_{\rm lin}(k,z)$ -- **Match** (both pipelines)
- SMT mass function ($q=0.707$ vs thesis $q=0.75$) -- **Differs**; Pinetti 2022 overrides bias only via `bias_pinetti()`
- Halo bias -- Pipeline $q=0.707$; Pinetti 2022 $q=0.75$
- $\Delta_{\rm vir}(z)$ Bryan & Norman -- **Match** (both pipelines)
- Transfer function -- **Match** (shared hmf backend now uses CAMB in both paths)

### DM-specific mass range

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| DM integral extends to free-streaming scale $\sim 10^{-6}\,M_\odot$ | Thesis Sec. 4.1 | `config.py:M_MIN_DM = 1e-6`, `M_MAX_DM = 1e18` | Same | **Match** | Config values match thesis; clumping factor now uses config values directly (former $[10^{-4}, 10^{17}]$ clamping resolved) |

---

## 2. NFW $\rho^2$ Profile (`dm_model.py`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $\rho_s = M/(4\pi r_s^3 f(c))$, $f(c) = \ln(1+c) - c/(1+c)$ | Standard NFW; thesis Eq. 3.24 | `dm_model.py:_rho_s` line 19 | Same | **Match** | |
| $r_s = R_{\rm vir}/c$, $c$ from Correa (2015) | Thesis Sec. 3.3 | `_rho_s` calls `hm.concentration` | Thesis Correa coefficients via `concentration_correa_thesis` (not yet wired into `_rho_s`) | **Match** | Default is `concentration_correa` via `c200_to_cvir` |
| $\int 4\pi r^2 \rho^2 dr = \frac{4\pi}{3}\rho_s^2 r_s^3[1 - 1/(1+c)^3]$ | Analytic NFW result | `rho2_integral_analytic` line 33 | Same | **Match** | Verified: $\int_0^c (1+x)^{-4} dx = \frac{1}{3}[1-(1+c)^{-3}]$ |
| $\tilde{v}(k \mid M) = (4\pi/\bar\rho^2)\int r^2 \rho^2 \sin(kr)/(kr) dr$ | Thesis Eq. 5.1 implicit | `v_tilde` line 54 | Same | **Match** | Normalization: $\tilde{v}(k\to 0) = \int\rho^2 d^3x / \bar\rho^2$ |
| $\tilde{v}$ numerical: $r_{\rm min} = 10^{-6} r_s$ | Implementation | line 88 | Same | **Match** | Negligible error: $\rho^2 r^2 \to 0$ as $r\to 0$ |
| Concentration below $10^{-2}\,M_\odot$ | Correa valid to $\sim 10^{-2}\,M_\odot$ | Code evaluates at $\sim 10^{-4}\,M_\odot/h$ | Same | **Investigate** | Smooth extrapolation but unvalidated |

---

## 3. Substructure Boost Factor (`dm_model.py:boost_moline`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $\log_{10} B = \sum_{i=0}^5 b_i [\log_{10}(M/M_\odot)]^i$ | Moline Eq. 18 | lines 128–130 | Same | **Match** | |
| Coefficients from Table 3, $\alpha=2$, tidal stripping | Moline Table 3 | `config.py:MOLINE_BOOST_COEFFS` | Same | **Match** | $[-0.186, 0.144, -8.8\times10^{-3}, 1.13\times10^{-3}, -3.7\times10^{-5}, -2\times10^{-7}]$ |
| $B(M,z) = B(M,z{=}0)/(1+z)$ | Moline thesis Eq. 3.48 | line 135 | Same | **Match** | |
| Polynomial argument in $M_\odot$ (not $M_\odot/h$) | Moline: masses in physical $M_\odot$ | `M_solar = M / cfg.h` line 116 | Same | **Match** | Resolved: now uses $M_{\rm phys} = M_{\rm code}/h$ consistently with `v_circ` |
| Valid range: $10^{-6} \lt M\,[M_\odot] \lt 10^{15}$ | Moline Sec. 3.2 | `np.clip(M_solar, 1e-6, 1e15)` line 127 | Same | **Match** | |
| Output clipped to $[0, 1000]$ | Not in literature | `np.clip(B, 0.0, 1000.0)` line 140 | Same | **Differs** | Numerical safety; $B$ never reaches 1000 in practice |
| Conservative: $B=0$ for $M \lt 10^7\,M_\odot$ | Pipeline design | lines 119–124 | Same | **Match** | |
| `optimistic` distinct from `intermediate` | Pipeline docs | Both map to $M_{\rm min,sub} = 10^{-6}$ | Same | **Bug** | Documented as having "enhanced substructure" but not implemented |

---

## 4. Clumping Factor $\Delta^2(z)$ (`dm_model.py:clumping_factor`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $\Delta^2 = (1/\bar\rho_m^2)\int (dn/dM)(1+B)\int\rho^2 d^3x\, dM$ | Pinetti Eq. 4.2 | `_clumping_compute` line 148 (cached via `@_cache_stable`) | Same | **Match** | |
| Integration via $d\ln M$: factor of $M$ in integrand | Standard | line 158: `dn * (1+B) * rho2 * M` | Same | **Match** | |
| Integration limits from config | `M_MIN_DM=1e-6`, `M_MAX_DM=1e18` | Uses config values directly at lines 193–196 | Same | **Match** | Resolved: silent clamping removed |
| Adaptive quadrature (`scipy.quad`, epsrel=1e-4) over $\ln M$ | Implementation | `_clumping_compute` uses `quad` over $[\ln M_{\min}, \ln M_{\max}]$ | Same | **Match** | Replaced former rectangle rule (n_M=200) with adaptive integration |
| Normalization by $\bar\rho_m^2$ and $(1+z)^3$ | Pinetti Eq. 4.2 | `cfg.RHO_BAR**2` and `(1+z)**3` line 163 | Same | **Match** | |

---

## 5. PPPC4DMID Photon Yield (`pppc4dmid.py`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| Tables from Cirelli et al. (2011) | PPPC4DMID arXiv:1012.4515 | `data/pppc4dmid/AtProduction_gammas.dat` | Same (thesis used private Pythia; unavailable) | **Match** | |
| Table columns: $[m_{\rm DM},\, \log_{10}x,\, {\rm channels}]$ | PPPC4DMID format | Parser at lines 49--89 | Same | **Match** | |
| $dN/d(\log_{10}x)$ is the tabulated quantity | PPPC4DMID convention | Interpolators on line 85 | Same | **Match** | |
| $dN/dx = dN/d(\log_{10}x) / (x\,\ln 10)$ | Standard calculus | line 211 | Same | **Match** | |
| $dN/dE = (dN/dx) / m_\chi$ | $x = E/m_\chi$ | line 244 | Same | **Match** | |
| Interpolation in $\log_{10}$ space | Implementation | `RectBivariateSpline` on $\log_{10}$ grid (lines 84--87) | Same | **Match** | Cubic $k=3$ |
| Mass range clamped to table | Implementation | `np.clip(log10m, ...)` line 136 | Same | **Match** | |
| Energy: $E' = (1+z)E_\gamma$ | Pinetti Eq. 4.1 | `E_emit = E_GeV * (1.0 + z)` dm_model.py:208 | Same | **Match** | |
| Early return if $dN/dE \le 0$ | Optimization | dm_model.py:210--211 | Same | **Match** | |

---

## 6. EBL Attenuation (`ebl.py`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| Model: Dominguez et al. (2011) | Pipeline default | `model='dominguez'` line 37 | Same | **Match** | |
| $\tau(E_\gamma, z)$ at **observed** energy | Dominguez / `ebltable` convention | dm_model.py:213 passes `E_GeV` | Same | **Match** | |
| `ebltable` API: energy in TeV | Package docs | `E_TeV = E_GeV / 1000.0` line 64 | Same | **Match** | |
| $e^{-\tau}$ attenuation factor | Standard | `np.exp(-tau(...))` line 72 | Same | **Match** | |
| $\tau \ge 0$ enforced | Physical | `np.maximum(result, 0.0)` line 67 | Same | **Match** | |
| $\tau(z \le 0) = 0$ | No local absorption | lines 57--58 | Same | **Match** | |
| Analytic fallback | Pipeline convenience | `_tau_analytic` line 79 | Same | **Differs** | Not from Dominguez; undocumented calibration |
| Alternative models available | Feature | `model` parameter (line 47--48) | Same | **Match** | Finke, Franceschini, Saldana-Lopez 2021 |

---

## 7. Window Function Assembly (`dm_model.py:W_gamma_DM` via `_W_gamma_DM_impl`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $1/(8\pi)$ prefactor | Pinetti Eq. 4.1: $1/(4\pi) \times 1/(2m_\chi^2)$ | `sigma_v / (8 * np.pi)` line 221 | Same (no override yet) | **Match** | $1/(4\pi) \times 1/2 = 1/(8\pi)$; Majorana DM |
| $(\rho_{\rm DM}/m_\chi)^2$ | Pinetti Eq. 4.1 | line 222 | Same | **Match** | |
| $\rho_{\rm DM} = \Omega_{\rm DM}\rho_c$ | Standard | `_W_gamma_DM_impl` | Same | **Match** | $\Omega_{\rm DM} = 0.2660$ |
| $M_{\odot,\rm GeV} = 1.116\times10^{57}$ | Standard conversion | `_W_gamma_DM_impl` | Same | **Match** | |
| $h^2$ in density conversion | Unit identity | `_W_gamma_DM_impl` | Same | **Match** | **Verified numerically**: $\rho_{\rm DM} = 1.27\times10^{-6}$ GeV/cm$^3$ |
| $(1+z)^3$ cosmological factor | Pinetti Eq. 4.1 | line 223 | Same | **Match** | |
| No baked-in $1/H(z)$ factor in `W_gamma_DM()` | Limber: $d\chi/dz = c/H(z)$ is supplied by the integration measure | `dm_model.py:W_gamma_DM` docstring and return expression | Same | **Match** | Current implementation keeps the emissivity factors in `W_gamma_DM()` and leaves the Jacobian to the Limber measure |
| $\sigma_v$ default: $3\times10^{-26}$ cm$^3$/s | Thermal relic | `cfg.SIGMA_V_THERMAL` | Same | **Match** | |
| Final unit conversion to $({\rm Mpc}/h)^{-3}$ | Per-$\chi$ convention | `W_cgs * Mpc_h_cm**3` line 227 | Same | **Match** | |
| $dN/dE$ at rest-frame energy | Pinetti Eq. 4.1 | `E_emit = E_GeV * (1+z)` line 208 | Same | **Match** | |
| EBL at observed energy | Standard convention | line 213 | Same | **Match** | |

---

## 8. Cross-Power Spectrum HI $\times$ DM (`angular_power.py:P_HI_DM_2h`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $P^{2h} = I_{\rm DM} \times I_{\rm HI} \times P_{\rm lin}$ | Pinetti Eqs. 5.1--5.2 | line 74 | Same (no override yet) | **Match** | |
| $I_{\rm DM} = \int (dn/dM)\,b\,\tilde{v}/\Delta^2\,dM$ | Eq. 5.1 | lines 50, 59 | Would use $q=0.75$ bias | **Match** | $\tilde{v}/\Delta^2$ is the correct normalization |
| $I_{\rm HI} = \int (dn/dM)\,b\,\tilde{u}_{\rm HI}\,M_{\rm HI}/\bar\rho_{\rm HI}\,dM$ | Eq. 5.2 | line 64 | Would use $q=0.75$ bias | **Match** | |
| Mass range: HI-relevant | $M_{\rm HI} = 0$ outside $[10^8, 10^{16}]$ | lines 47–48 | Same | **Match** | |
| Limber $k = (\ell+1/2)/\chi$ | LoVerde & Afshordi (2008) | line 206 | $k = \ell/\chi$ via `pinetti2022.limber_k()` | **Differs** | Pipeline improvement; ~5% at $\ell=10$, negligible at $\ell \gt 100$ |
| $d\chi/dz = c \cdot h / H(z)$ in [Mpc/h] | Standard | line 198 | Same | **Match** | |

---

## 9. Computational Simplifications Summary

| # | Item | Method | Pipeline (Pinetti 2022) | Impact |
|---|------|--------|------------------------|--------|
| C1 | $\rho^2$ volume integral | Analytic formula | Same | Exact |
| C2 | $\tilde{v}(k \mid M)$ Fourier transform | Numerical quadrature (`scipy.quad`, epsrel=1e-5) | Same | Accurate; performance bottleneck |
| C3 | $\Delta^2(z)$ mass integral | Adaptive quadrature (`scipy.quad`, epsrel=1e-4) over $\ln M$ | Same | High accuracy |
| C4 | $C_\ell$ Limber redshift integral | Rectangle rule, uniform grid ($n_z=200$) | Same | Sub-percent accuracy |
| C5 | Cross/auto power spectra | 2-halo term only | Same | Justified at $\ell \lt 1000$ |
| C6 | PPPC4DMID | Public tables (thesis used private Pythia) | Same (Pythia unavailable) | Percent-level, irreducible |
| ~~C7~~ | ~~Mass limits in $\Delta^2$~~ | ~~Clamped to $[10^{-4}, 10^{17}]$~~ | — | **Resolved:** now uses config values directly |

---

## 10. Summary of All Deviations from Thesis

| # | Item | Thesis | Pipeline | Pipeline (Pinetti 2022) | Nature | Severity |
|---|------|--------|----------|------------------------|--------|----------|
| 1 | SMT $q$ parameter | $q = 0.75$ (ST 2002) | $q = 0.707$ (SMT 1999) | $q = 0.75$ via `bias_pinetti()` | Different literature calibration | Minor (~5% on bias) |
| 2 | Correa concentration coefficients | Thesis Eq. 3.36 fit | Planck Appendix B1 fit | Thesis fit via `concentration_correa_thesis()` | Different cosmology fit | Minor (<5% on $c$) |
| 3 | Limber $k$ substitution | $k = \ell/\chi$ | $k = (\ell+1/2)/\chi$ | $k = \ell/\chi$ via `limber_k()` | Pipeline improvement | Negligible |
| 4 | PPPC4DMID | Private Pythia code | Public tables | Public tables (Pythia unavailable) | Data source | Low (percent-level) |
| ~~5~~ | ~~Clumping mass limits~~ | — | — | — | **Resolved:** now uses config values directly | — |
| 6 | `optimistic` boost | Presumably enhanced | = `intermediate` | Same | Not implemented | Bug |

---

## 11. Items Verified Correct (Potential Concerns Dismissed)

| Concern | Resolution | Pipeline (Pinetti 2022) |
|---------|-----------|------------------------|
| $1/(8\pi)$ vs $1/(4\pi)$: is the Majorana factor correct? | $1/(4\pi) \times 1/2 = 1/(8\pi)$ verified against Pinetti Eq. 4.1 | Same |
| $h^2$ in density conversion: correct h-power? | Verified numerically: gives $\rho_{\rm DM} = 1.27\times10^{-6}$ GeV/cm$^3$, matching known value | Same |
| $\tilde{v}/\Delta^2$ in two-halo term: division or multiplication? | Division is correct: normalizes DM density-squared field so $I_{\rm DM}(k\to 0) \sim 1$ | Same |
| EBL energy convention: observed or emitted? | Observed (confirmed by `ebltable` API and code comments at dm_model.py:213) | Same |
| $\rho^2$ integral formula | Verified analytically: $\int_0^c (1+x)^{-4}dx = \frac{1}{3}[1-(1+c)^{-3}]$ | Same |
| $dN/d\log_{10}x \to dN/dE$ chain | Verified: $dN/dx = dN/d\log_{10}x / (x \ln 10)$; $dN/dE = dN/dx / m_\chi$ | Same |
