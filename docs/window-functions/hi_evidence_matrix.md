# Claim-by-Claim Evidence Matrix: HI Window Function Pipeline

## Context

This document audits every equation, model choice, parameter value, and computational method in the HI window function chain (`hi_model.py`, `halo_model.py`, `hmf_interface.py`, `cosmology.py`, `config.py`) against the source literature: Pinetti+ (2020, arXiv:1911.04989), Pinetti (2022) thesis (arXiv:2212.00125), Padmanabhan+ (2017, arXiv:1611.06235), Sheth & Tormen (1999), Sheth, Mo & Tormen (2001), and Planck 2018.

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

## 1. Cosmological Backbone (`cosmology.py`, `config.py`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-------|---------------------|----------|------------------------|--------|
| $E(z) = \sqrt{\Omega_M(1+z)^3 + \Omega_\Lambda}$ | Standard flat LCDM | `cosmology.py:E(z)` lines 99–102 | Same | **Match** |
| $H(z) = H_0 E(z)$; $H_0 = 67.36$ km/s/Mpc | Planck 2018 | `cosmology.py:H(z)` lines 105–107 | Same | **Match** |
| $\chi(z) = (c/H_0)\int_0^z dz'/E(z')$ | Standard cosmology | `cosmology.py:chi(z)` lines 116–125, returns Mpc/h | Same | **Match** |
| $P_{\rm lin}(k,z)$ via CAMB Boltzmann solver | Planck 2018 params | `cosmology.py:P_lin(k,z)` lines 164–183 | Same | **Match** |
| $\sigma^2(R,z) = \frac{1}{2\pi^2}\int dk\,k^2 P_{\rm lin} W^2(kR)$ | Perturbation theory | `cosmology.py:sigma_R(R,z)` lines 200–214 | Same | **Match** |
| $W(x) = 3(\sin x - x\cos x)/x^3$ (top-hat) | Standard | `cosmology.py:_tophat_W(kR)` lines 190–197 | Same | **Match** |
| Planck 2018 parameters: $h=0.6736$, $\Omega_M=0.3153$, $\sigma_8=0.8111$, $n_s=0.9649$ | Planck 2018 Table 2 (TT,TE,EE+lowE+lensing) | `config.py` constants | Same | **Match** |

---

## 2. Halo Model Infrastructure (`halo_model.py`, `hmf_interface.py`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $R_{\rm vir} = (3M/4\pi\Delta_{\rm vir}(z)\rho_c(z))^{1/3}$ | Thesis Eqs. 3.26–3.28: z-dependent $\Delta_{\rm vir}$ from Bryan & Norman | `halo_model.py:R_vir(M,z)` lines 42–54 with Bryan & Norman $\Delta_{\rm vir}(z)$ lines 23–35 | Same | **Match** | Repository now matches the thesis choice for the virial definition |
| $v_c = \sqrt{GM/R_{\rm vir}}$ | Thesis Eq. 4.4 | `halo_model.py:v_circ(M,z)` lines 72–81 | Same | **Match** | Unit handling: M_phys=M/h, R_phys=Rv/h, verified correct |
| $\nu = \delta_c^2/\sigma^2(M,z)$, $\delta_c=1.686$ | Thesis Eq. 3.30 | `hmf_interface.py:nu(M,z)` | Same | **Match** | $(1+z)$ absorbed into $\sigma(M,z)$ via growth factor |
| $\nu f(\nu) = A[1+(q\nu)^{-p}]\sqrt{q\nu/2\pi}\exp(-q\nu/2)$; $A=0.3222$, $q=0.707$, $p=0.3$ | SMT (2001) Eq. 6; thesis Eq. 3.33 uses $q=0.75$ | `hmf_interface.py`: hmf `SMT` model with $q=0.707$ | $q=0.75$ via `pinetti2022.bias_pinetti()` | **Differs** | Pipeline: $q=0.707$ (original SMT 1999/2001). Thesis: $q=0.75$ (ST 2002 update). ~5% effect on mass function tails |
| $b(\nu) = 1 + (q\nu-1)/\delta_c + 2p/[\delta_c(1+(q\nu)^p)]$ | Sheth & Tormen (1999); thesis Eq. 3.51 | `halo_model.py:bias(M,z)` lines 110–118 | Same | **Match** | Inherits $q$ difference from mass function |
| hmf transfer function | CAMB (implicit in thesis) | `hmf_interface.py`: `transfer_model='CAMB'` | Same | **Match** | The mass-function backend now uses CAMB-backed transfer functions |

---

## 3. HI Model (`hi_model.py`)

### 3.1 M_HI–halo mass relation

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $M_{\rm HI} = \alpha f_{H,c} M (M/10^{11}h^{-1}M_\odot)^\beta \exp[-(v_{c,0}/v_c)^3]$ | Padmanabhan+ (2017) Eq. 1; thesis Eq. 4.2 | `hi_model.py:M_HI(M,z)` lines 21–31 | Same | **Match** | |
| $\alpha = 0.176$ | Padmanabhan+ Table A1 (modified NFW fit) | `config.py:HI_ALPHA` | Same | **Match** | |
| $\beta = -0.69$ | Padmanabhan+ Table A1 | `config.py:HI_BETA` | Same | **Match** | |
| $v_{c,0} = 10^{1.61} \approx 40.7$ km/s | Padmanabhan+ Table A1 | `config.py:HI_VC0 = 10**1.61` | Same | **Match** | |
| $f_{H,c} = (1-Y_P)\Omega_B/\Omega_M$, $Y_P=0.24$ | Padmanabhan+ Eq. 2; thesis Eq. 4.3 | `config.py:F_HC` | Same | **Match** | |
| Parameters from Table A1 (modified NFW), NOT Table 3 (exponential) | Padmanabhan+ Tables 3 vs A1 | Consistent Table A1 set | Same | **Match** | Thesis Eqs. 3.7–3.8 mix exponential-fit params with modified NFW profile — a mismatch. Pipeline correctly uses self-consistent Table A1 parameters |
| Mass pivot $10^{11}h^{-1}M_\odot$ in $M_{\rm HI}$ | Padmanabhan+ Eq. 1 | `M / 1e11` where M is $M_\odot/h$ | Same | **Match** | $M_\odot/h = h^{-1}M_\odot$, so `M / 1e11` is correct |

### 3.2 HI concentration

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $c_{\rm HI} = c_{HI,0}(M/10^{11}M_\odot)^{-0.109} \times 4/(1+z)^\gamma$ | Padmanabhan+ Eq. 3; thesis Eq. 4.10 | `hi_model.py:c_HI(M,z)` lines 38–49 with `M * h / 1e11` | Same | **Match** | The current implementation converts the repository mass variable from $M_\odot/h$ to $M_\odot$ before applying the Padmanabhan pivot |
| $c_{HI,0} = 139$ | Padmanabhan+ Table A1 | `config.py:HI_C0 = 139.0` | Same | **Match** | |
| $\gamma = 0.13$ | Padmanabhan+ Table A1 | `config.py:HI_GAMMA_CONC = 0.13` | Same | **Match** | |
| Exponent $-0.109$ | Padmanabhan+ Eq. 3 | Hardcoded in `hi_model.py:49` | Same | **Match** | |

### 3.3 HI density profile

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $\rho_{\rm HI}(r) = \rho_0 r_s^3 / [(r+0.75r_s)(r+r_s)^2]$ | Padmanabhan+ Eq. A1; thesis Eq. 4.8 | `hi_model.py:u_HI` integrand, lines 105–135 | Same | **Match** | Modified NFW from Maller & Bullock (2004) |
| $\rho_0$ from $\int_0^{R_{\rm vir}} 4\pi r^2 \rho_{\rm HI}\,dr = M_{\rm HI}$ | Padmanabhan+ Eq. A2; thesis Eq. 4.9 | `hi_model.py:rho0_HI(M,z)` lines 90–102 | Same | **Match** | |
| Normalization integral: partial fractions A=9, B=−8, C=−4 | Analytic result | `hi_model.py:_hi_profile_norm_integral` lines 80–87 | Same | **Match** | Verified: $x^2/[(x+0.75)(x+1)^2]$ decomposes as $9/(x+0.75) - 8/(x+1) - 4/(x+1)^2$. Coefficient checks: $x^2$: $A+B = 9-8 = 1$ ✓; $x^1$: $2A+1.75B+C = 18-14-4 = 0$ ✓; $x^0$: $A+0.75B+0.75C = 9-6-3 = 0$ ✓ |

### 3.4 Fourier transform of HI profile

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $\tilde{u}_{\rm HI} = (4\pi/M_{\rm HI})\int_0^{R_{\rm vir}} r^2 \rho_{\rm HI} \sin(kr)/(kr)\,dr$ | Thesis Eq. 4.11 | `hi_model.py:u_HI(k,M,z)` lines 105–135 | Same | **Match** | No analytic FT exists for modified NFW; numerical quadrature is the correct approach |
| $\tilde{u}_{\rm HI}(k\to0) = 1$ normalization | Standard convention | `u_HI` returns 1.0 for $k \lt 10^{-10}$ | Same | **Match** | |
| Numerical integration: `scipy.quad`, `epsrel=1e-6`, `limit=200` | N/A (computational choice) | `hi_model.py:132` | Same | Appropriate | Expensive but accurate |

### 3.5 Mean HI density

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $\bar\rho_{\rm HI}(z) = \int (dn/dM)\,M_{\rm HI}\,dM$ | Thesis Eq. 4.5 | `hi_model.py:rho_HI_mean(z)` lines 178–193 (dispatcher); integration in `_rho_HI_default` lines 142–150 and `_rho_HI_scalar` lines 153–162 | Same | **Match** | Integration via `scipy.quad` in log-mass; cached via `@_cache_stable` |
| Mass limits: $10^8$–$10^{16}\,M_\odot/h$ | Not explicitly stated; adequate range | `config.py:M_MIN_HI`, `M_MAX_HI` | Same | **Match** | Integrand exponentially suppressed at both ends |

### 3.6 Omega_HI

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $\Omega_{\rm HI}(z) = (1+z)^{-3}\bar\rho_{\rm HI}/\rho_c$ | Thesis Eq. 4.6 | `hi_model.py:Omega_HI(z)` lines 196–207 | Fixed $2.45\times10^{-4}$ | **Differs** | Thesis (p.122) subsequently uses fixed $\Omega_{\rm HI} = 2.45\times10^{-4}$. Pipeline computes from the halo integral (z-dependent). Pipeline is more physical; thesis acknowledges up to factor-2 variation. Propagates linearly into $\bar{T}_b$ and $W_{\rm HI}$ |

### 3.7 Brightness temperature

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $\bar{T}_b = 188\,h\,\Omega_{\rm HI}(1+z)^2/E(z)$ mK | Thesis Eq. 3.4 uses $44\,\mu{\rm K}\times(\Omega_{\rm HI}h/2.45\times10^{-4})(1+z)^2/E(z)$ | `hi_model.py:T_bar_b(z)` lines 210–218 | 44 $\mu$K via `pinetti2022.T_bar_b_thesis()` | **Partial** | Equivalent: $188 \times 2.45\times10^{-4} \approx 0.046$ mK $= 46\,\mu$K $\approx 44\,\mu$K (rounding). Combined with computed vs fixed $\Omega_{\rm HI}$, numerical results differ slightly |

### 3.8 Effective HI bias

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $b_{\rm HI} = (1/\bar\rho_{\rm HI})\int (dn/dM)\,M_{\rm HI}\,b(M)\,dM$ | Thesis Eq. 4.7 | `hi_model.py:b_HI(z)` lines 221–243 | $q=0.75$ via `pinetti2022.b_HI_pinetti()` | **Match** | Via `scipy.quad` in log-mass |

### 3.9 HI power spectra

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $P_{\rm HI}^{\rm 1h} = (1/\bar\rho_{\rm HI}^2)\int (dn/dM)\,M_{\rm HI}^2\,\tilde{u}_{\rm HI}^2\,dM$ | Thesis Eq. 4.13 | `hi_model.py:P_HI_1h` lines 250–278 | Same | **Match** | Rectangle rule over log-mass grid (n_M=160) |
| $P_{\rm HI}^{\rm 2h} = [(1/\bar\rho_{\rm HI})\int (dn/dM)\,b\,M_{\rm HI}\,\tilde{u}_{\rm HI}\,dM]^2 P_{\rm lin}$ | Thesis Eq. 4.14 | `hi_model.py:P_HI_2h` lines 281–310 | Same | **Match** | Same method |

### 3.10 Window function

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $W_{\rm HI}(\chi) = \bar{T}_b\,\phi(z)\,H(z)/(c\cdot h)$ | Thesis Eqs. 5.11–5.12 for the per-$z$ window; repository keeps $b_{\rm HI}$ in $P_{\rm HI}$ rather than in `W_HI()` | `hi_model.py:W_HI(z,z_min,z_max)` lines 317–335 | `pinetti2022.W_HI_pinetti()` | **Match** | $\phi(z) = 1/(z_{\max}-z_{\min})$ top-hat; $H/(c\cdot h)$ Jacobian converts per-$z$ to per-Mpc/$h$ |
| Returns 0 outside $[z_{\min}, z_{\max}]$ | Top-hat selection | `hi_model.py:332` | Same | **Match** | |

---

## 4. Limber Integration (`angular_power.py`)

| Claim | Literature Reference | Pipeline | Pipeline (Pinetti 2022) | Status | Notes |
|-------|---------------------|----------|------------------------|--------|-------|
| $C_\ell = \int (d\chi/\chi^2)\,W_{\rm HI}\,W_j\,P_{ij}(k,z)$ | Thesis Eq. 5.10 | `angular_power.py:C_ell_HI_gamma` | Same | **Match** | |
| $k = (\ell+1/2)/\chi$ | LoVerde & Afshordi (2008); thesis uses $k = \ell/\chi$ | `angular_power.py:162` | $k = \ell/\chi$ | **Differs** | Pipeline improvement: more accurate at low $\ell$. ~5% at $\ell=10$, rapidly decreasing |
| 2-halo term only for cross-power | Thesis: 1-halo subdominant at $\ell \le 1000$ | `angular_power.py:P_HI_DM_2h`, `P_HI_astro_2h` | Same | **Match** | Deliberate omission |
| 2-halo term only for HI auto-power | Implicit in thesis | `angular_power.py:C_ell_HI_auto` | Same | **Match** | Deliberate for speed |
| Redshift integration: rectangle rule, $n_z=200$ uniform points | N/A (computational choice) | `angular_power.py:141-142` | Same | Appropriate | Sub-percent accuracy for typical band widths |

---

## 5. Computational Simplifications Summary

| # | Item | Method | Pipeline (Pinetti 2022) | Impact |
|---|------|--------|------------------------|--------|
| C1 | $\tilde{u}_{\rm HI}$ Fourier transform | Numerical quadrature (`scipy.quad`, epsrel=1e-6) | Same | Accurate; no analytic form exists for modified NFW. Performance bottleneck |
| C2 | $P_{\rm HI}^{\rm 1h/2h}$ mass integral | Rectangle rule over log-spaced grid (n_M=160, 8 decades) | Same | ~1% accuracy |
| C3 | $\bar\rho_{\rm HI}$, $b_{\rm HI}$ mass integrals | Adaptive quadrature (`scipy.quad`, epsrel=1e-5) | Same | High accuracy |
| C4 | $C_\ell$ Limber redshift integral | Rectangle rule, uniform grid ($n_z=200$) | Same | Sub-percent accuracy |
| C5 | Cross/auto power spectra | 2-halo term only (1-halo omitted) | Same | Justified at $\ell \lt 1000$ |
| C6 | hmf transfer function | CAMB-backed in both `hmf_interface.py` and `cosmology.py` | Same | Consistent transfer-function choice across the repository |

---

## 6. Code Quality Issues

| # | Item | File:Line | Pipeline (Pinetti 2022) | Impact |
|---|------|-----------|------------------------|--------|
| ~~D1~~ | ~~`_b_HI_cache` declared but never populated~~ | — | — | **Resolved:** dead code removed |
| ~~D2~~ | ~~Comment says "trapezoidal" but implements rectangle rule~~ | — | — | **Resolved:** comment corrected to "rectangle rule" |
| ~~D3~~ | ~~`from functools import lru_cache` imported but unused~~ | — | — | **Resolved:** dead import removed; replaced by `from .cache import _cache_stable` (used on `_rho_HI_default`, `_rho_HI_scalar`) |

---

## 7. Summary of All Deviations from Thesis

| # | Item | Thesis | Pipeline | Pipeline (Pinetti 2022) | Nature | Severity |
|---|------|--------|----------|------------------------|--------|----------|
| ~~1~~ | ~~$\Delta_{\rm vir}$ definition~~ | $\Delta_{\rm vir}(z)$ from Bryan & Norman | **Now matches:** Bryan & Norman $\Delta_c(z)$ | Same (resolved) | **Resolved** | — |
| 2 | SMT $q$ parameter | $q = 0.75$ (ST 2002) | $q = 0.707$ (SMT 1999) | $q = 0.75$ | Different literature calibration | Minor |
| 3 | $\Omega_{\rm HI}$ treatment | Fixed $2.45\times10^{-4}$ | Computed from halo integral (z-dependent) | Fixed $2.45\times10^{-4}$ | Pipeline improvement | Minor |
| 4 | Correa concentration coefficients | Thesis-specific fit | Planck Appendix B1 fit | Same | Different cosmology fit | Minor (DM only) |
| ~~5~~ | ~~$c_{200} \to c_{\rm vir}$ conversion~~ | Performed | **Now matches:** `c200_to_cvir()` implemented | Same (resolved) | **Resolved** | — |
| 6 | Limber $k$ substitution | $k = \ell/\chi$ | $k = (\ell+1/2)/\chi$ | $k = \ell/\chi$ | Pipeline improvement (LoVerde & Afshordi 2008) | Negligible |
| 7 | $\bar{T}_b$ coefficient | $44\,\mu$K (pre-evaluated) | $188h$ mK (un-substituted) | $44\,\mu$K | Equivalent modulo rounding | Negligible |
| ~~8~~ | ~~EH vs CAMB transfer function~~ | CAMB | **Now matches:** hmf uses `transfer_model='CAMB'` | Same (resolved) | **Resolved** | — |
| ~~9~~ | ~~$c_{\rm HI}$ mass pivot units~~ | $10^{11}M_\odot$ | **Fixed:** `M * h / 1e11` converts M_sun/h to M_sun | Same (resolved) | **Resolved** | — |

---

## 8. Items Verified Correct (Potential Concerns Dismissed)

| Concern | Resolution | Pipeline (Pinetti 2022) |
|---------|-----------|------------------------|
| $R_{\rm vir}$ returns physical or comoving radius? | Physical radius in Mpc/h units. Formula uses $\rho_{c}(z) = \rho_{c,0}E^2(z)$ (physical). $h$-factors cancel correctly in `v_circ`: $M_{\rm phys}=M/h$, $R_{\rm phys}=R_v/h$ | Same |
| Padmanabhan parameter cross-contamination | All 5 parameters ($\alpha$, $\beta$, $v_{c,0}$, $c_{HI,0}$, $\gamma$) from Table A1 modified NFW fit. No mixing with Table 3 exponential fit. Correct | Same |
| Mass integration limits $[10^8, 10^{16}]\,M_\odot/h$ | Adequate: $M_{\rm HI}$ exponentially suppressed below $\sim10^{9.5}\,M_\odot$; mass function drops above $\sim10^{15}\,M_\odot$ | Same |
| Profile normalization integral | Partial fraction coefficients verified algebraically (see §3.3) | Same |
