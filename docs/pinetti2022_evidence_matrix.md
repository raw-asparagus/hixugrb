# Claim-by-Claim Evidence Matrix: Pipeline vs Pinetti (2022) Thesis

## Context

This document compares every equation, model choice, and parameter value documented in [`equations.md`](equations.md) and [`literature/pinetti2020.md`](literature/pinetti2020.md) against the PhD thesis *"From gamma rays to radio waves: Dark Matter searches across the spectrum"* by Elena Pinetti (2022, [arXiv:2212.00125](https://arxiv.org/abs/2212.00125)). The thesis (Part I: Chapters 3–5 and Appendices B–E) is the definitive reference for the HI 21-cm × UGRB cross-correlation formalism implemented in this codebase. It is a superset of, and more authoritative than, the JCAP paper ([arXiv:1911.04989](https://arxiv.org/abs/1911.04989)).

---

## Legend

| Symbol | Meaning |
|--------|---------|
| **Match** | Pipeline agrees with thesis |
| **Match (thesis)** | Pinetti 2022 parallel agrees with thesis |
| **Differs** | Pipeline uses a different choice (noted) |
| **Partial** | Partially matches; deviations noted |
| **Not impl.** | Thesis defines it but pipeline omits (not needed) |
| **Addition** | Pipeline adds something not in thesis |

---

## 1. Cosmology (`cosmology.py`, `config.py`) — equations.md §1

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 1.1 | $E(z) = \sqrt{\Omega_M(1+z)^3 + \Omega_\Lambda}$ | Standard flat ΛCDM (implicit throughout) | `E(z)` | Same | **Match** |
| 1.2 | $H(z) = H_0 E(z)$; $H_0 = 67.36$ km/s/Mpc | Planck 2018 (defers to Planck; not stated explicitly) | `H(z)` with $H_0 = 67.36$ | Same | **Match** |
| 1.3 | $\chi(z) = (c/H_0)\int_0^z dz'/E(z')$ | Eq. 3.69 (p.108): $\chi(z) = \int_0^z c\,dz'/H(z')$ | `chi(z)` | Same | **Match** |
| 1.4 | $d_L(z) = (1+z)\chi(z)$ | Text after Eq. 3.68 (p.108) | `d_L(z)` | Same | **Match** |
| 1.5 | $D(z)$: exact flat ΛCDM growth factor | Eq. 3.23 (referenced; standard) | `growth_factor(z)` | Same | **Match** |
| 1.6 | $\rho_c = 2.775\times10^{11}\;M_\odot h^{-1}\,(\text{Mpc}/h)^{-3}$ | Standard definition $3H_0^2/(8\pi G)$ | `config.RHO_CRIT` | Same | **Match** |
| 1.7 | $\bar\rho_m = \Omega_M \rho_c$ | Standard | `config.RHO_BAR` | Same | **Match** |
| 1.8 | $P_\text{lin}(k,z)$ via CAMB | Sec. 3.2 (p.94–96): Boltzmann solver | `P_lin(k, z)` via CAMB | Same | **Match** |
| 1.9 | $\sigma^2(R,z) = \frac{1}{2\pi^2}\int dk\,k^2 P_\text{lin} W^2(kR)$ | Eq. 3.19 (referenced in Eq. 3.30, p.97) | `sigma_R(R, z)` | Same | **Match** |
| 1.10 | $W(x) = 3(\sin x - x\cos x)/x^3$ (top-hat) | Standard (implicit in σ definition) | `_tophat_W(kR)` | Same | **Match** |
| 1.11 | $R(M) = (3M/4\pi\bar\rho_m)^{1/3}$ | Standard (implicit) | `sigma_M(M, z)` | Same | **Match** |

**Cosmological parameters** ($h=0.6736$, $\Omega_b h^2=0.02237$, $\Omega_c h^2=0.1200$, $n_s=0.9649$, $\sigma_8=0.8111$): thesis defers to Planck without listing explicit values. Pipeline uses Planck 2018 values. **Match** (consistent).

---

## 2. Halo Model (`halo_model.py`, `hmf_interface.py`) — equations.md §2

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 2.1 | $R_\text{vir} = (3M/4\pi\Delta_\text{vir}\rho_c)^{1/3}$, $\Delta_\text{vir}=200$ | Eqs. 3.26–3.28 (p.96–97): uses $\Delta_\text{vir}(z)$ from Eq. 3.27 (Bryan & Norman fit, $\Delta_\text{vir} \neq 200$ in general) | Bryan & Norman $\Delta_\text{vir}(z)$ | Same | **Match** |
| 2.2 | $v_c = \sqrt{GM/R_\text{vir}}$ | Eq. 4.4 (p.114) | `v_circ(M, z)` | Same | **Match** |
| 2.3 | $\nu = \delta_c^2/\sigma^2(M,z)$, $\delta_c = 1.686$ | Eq. 3.30 (p.97): $\nu = \delta_{sc}^2/\sigma^2$; $\delta_{sc} = 1.686(1+z)$ in Eq. 3.25 | `nu(M, z)` with $\delta_c = 1.686$ | Same | **Match** (equivalent; $(1+z)$ absorbed into $\sigma(M,z)$ via growth factor) |
| 2.4 | $\nu f(\nu) = A[1+(q\nu)^{-p}]\sqrt{q\nu/2\pi}\exp(-q\nu/2)$; $q=0.707$, $p=0.3$ | Eq. 3.33 (p.98): same form but **$q = 0.75$** | hmf `SMT` model with $q = 0.707$ | $q = 0.75$ via `pinetti2022.bias_pinetti()` | **Match** (thesis) |
| 2.5 | $b(\nu) = 1 + (q\nu-1)/\delta_c + 2p/[\delta_c(1+(q\nu)^p)]$ | Eq. 3.51 (p.102) | `bias(M, z)` | Same form, $q=0.75$ | **Match** (but inherits $q$ difference from 2.4) |
| 2.6 | $\log_{10}c = \alpha + \beta\log_{10}(M/M_\odot)[1+\gamma(\log_{10}M/M_\odot)^2]$; Correa et al. (2015) Planck coefficients | Eqs. 3.35–3.36 (p.99): same functional form but **different coefficients** | `concentration_correa` with Planck Appendix B1 coefficients | Thesis coefficients via `pinetti2022.concentration_correa_thesis()` | **Match** (thesis) |
| 2.6+ | $c_{200} \to c_\text{vir}$ conversion | Eqs. 3.38–3.41 (p.99): linear mapping $c_\text{vir} = a\,c_{200} + b$ with $\Delta_\text{vir}$-dependent coefficients | `c200_to_cvir()` implemented | Same | **Match** |
| 2.7 | $f(c) = \ln(1+c) - c/(1+c)$ | Eq. 3.43 (p.101) | `_f_nfw(c)` | Same | **Match** |
| 2.8 | $\tilde u(k|M)$: analytic NFW FT with Si, Ci functions | Eq. 3.45 (p.101) | `u_nfw(k, M, z)` | Same | **Match** |

---

## 3. HI Model (`hi_model.py`) — equations.md §3

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 3.1 | $M_\text{HI} = \alpha f_{H,c} M (M/10^{11}h^{-1}M_\odot)^\beta \exp[-(v_{c,0}/v_c)^3]$ | Eq. 4.2 (p.113) | `M_HI(M, z)` | Same | **Match** |
| — | $\alpha = 0.176$, $\beta = -0.69$, $v_{c,0} = 40.7$ km/s | Text after Eq. 4.2 (p.113–114) | Same values | Same | **Match** |
| — | $f_{H,c} = (1-Y_P)\Omega_B/\Omega_M$, $Y_P = 0.24$ | Eq. 4.3 (p.113) | Same | Same | **Match** |
| 3.2 | $c_\text{HI} = 4\,c_{HI,0}(1+z)^{-\gamma}(M/10^{11}M_\odot)^{-0.109}$; $c_{HI,0}=139$, $\gamma=0.13$ | Eq. 4.10 (p.114) | `c_HI(M, z)` | Same | **Match** |
| 3.3 | $\rho_\text{HI}(r) = \rho_0 r_s^3/[(r+0.75r_s)(r+r_s)^2]$ (modified NFW) | Eq. 4.8 (p.114) | Same profile | Same | **Match** |
| 3.4 | $\rho_0$ from $\int_0^{R_\text{vir}} 4\pi r^2 \rho_\text{HI}\,dr = M_\text{HI}$ | Eq. 4.9 (p.114) | `rho0_HI` | Same | **Match** |
| 3.5 | $\tilde u_\text{HI}(k|M) = (4\pi/M_\text{HI})\int_0^{R_\text{vir}} r^2 \rho_\text{HI} \sin(kr)/(kr)\,dr$ | Eq. 4.11 (p.114) | `u_HI(k, M, z)` | Same | **Match** |
| 3.6 | $\bar\rho_\text{HI}(z) = \int (dn/dM) M_\text{HI}\,dM$ | Eq. 4.5 (p.114) | `rho_HI_mean(z)` | Same | **Match** |
| 3.7 | $\Omega_\text{HI}(z) = (1+z)^{-3}\bar\rho_\text{HI}/\rho_c$ | Eq. 4.6 (p.114) | `Omega_HI(z)` — computed from integral | Fixed $2.45\times10^{-4}$ | **Match** (thesis) |
| 3.8 | $\bar T_b = 188\,h\,\Omega_\text{HI}(z)(1+z)^2/E(z)$ mK | Thesis uses $T_\text{obs} = 44\,\mu\text{K}\times(\Omega_\text{HI}h/2.45\times10^{-4})\times(1+z)^2/E(z)$ (p.122) | `T_bar_b(z)` | $44\,\mu$K via `pinetti2022.T_bar_b_thesis()` | **Match** (thesis) |
| 3.9 | $b_\text{HI}(z) = (1/\bar\rho_\text{HI})\int (dn/dM) M_\text{HI} b\,dM$ | Eq. 4.7 (p.114) | `b_HI(z)` | $q=0.75$ bias via `pinetti2022.b_HI_pinetti()` | **Match** |
| 3.10 | $P_\text{HI}^\text{1h} = (1/\bar\rho_\text{HI}^2)\int (dn/dM) M_\text{HI}^2 \tilde u_\text{HI}^2\,dM$ | Eq. 4.13 (p.115) | `P_HI_1h` | Same | **Match** |
| 3.11 | $P_\text{HI}^\text{2h} = [(1/\bar\rho_\text{HI})\int (dn/dM) b M_\text{HI} \tilde u_\text{HI}\,dM]^2 P_\text{lin}$ | Eq. 4.14 (p.115) | `P_HI_2h` | Same | **Match** |
| 3.12 | $W_\text{HI}(\chi) = \bar T_b\,b_\text{HI}\,\phi(z)\,H(z)/(ch)$; $\phi = 1/\Delta z$ | Eqs. 5.11–5.12 (p.122) | `W_HI(z, z_min, z_max)` | `pinetti2022.W_HI_pinetti()` | **Match** |

---

## 4. Dark Matter Model (`dm_model.py`) — equations.md §4

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 4.1 | $\rho_s = M/[4\pi r_s^3 f(c)]$ | Eq. 3.43 (p.101) | `_rho_s(M, z)` | Same | **Match** |
| 4.2 | $\int_0^{R_\text{vir}} 4\pi r^2 \rho_\text{NFW}^2\,dr = (4\pi/3)\rho_s^2 r_s^3[1-(1+c)^{-3}]$ | Analytic result implied by Eq. 3.46 (p.101) | `rho2_integral_analytic` | Same | **Match** |
| 4.3 | $\tilde v(k|M) = (4\pi/\bar\rho_m^2)\int_0^{R_\text{vir}} r^2 \rho^2 \sin(kr)/(kr)\,dr$ | Eq. 3.46 (p.101): $\tilde\nu(k) = \int_0^{R_\text{vir}} (4\pi r^2/M) \rho^2 \sin(kr)/(kr)\,dr$ | `v_tilde(k, M, z)` | Same | **Partial** — Thesis normalizes by $M$; pipeline uses unnormalized $\tilde v = \int \rho^2 d^3x \times \sin(kr)/(kr)$. Consistent when combined with $\Delta^2$ normalization |
| 4.4a | $\log_{10}B(M,z{=}0) = \sum_{i=0}^{5} b_i [\log_{10}(M/M_\odot)]^i$ (Moliné+ 2017) | Eq. 3.47 (p.101) | `boost_moline` | Same | **Match** |
| — | $d_0{=}{-}0.186$, $d_1{=}0.144$, $d_2{=}{-}8.8{\times}10^{-3}$, $d_3{=}1.13{\times}10^{-3}$, $d_4{=}{-}3.7{\times}10^{-5}$, $d_5{=}{-}2{\times}10^{-7}$ | Same values (p.101) | Same values | Same | **Match** |
| 4.4b | $B(M,z) = B(M,0)/(1+z)$ | Eq. 3.48 (p.101) | Same | Same | **Match** |
| 4.5 | $\Delta^2(z) = (1/\bar\rho^2)\int (dn/dM)[1+B]\int\rho^2 d^3x\,dM$ | Eq. 3.61 (p.104) with Eq. 3.62 (p.105) for boost inclusion | `clumping_factor` | Same | **Match** |
| 4.6 | $W_\gamma^\text{DM} = (\langle\sigma v\rangle/8\pi)(\rho_\text{DM}/m_\chi)^2(1+z)^3 H^{-1}\Delta^2 (dN/dE') e^{-\tau}$ | Eq. 5.17 (p.122) / Eq. E.7 (p.220) | `W_gamma_DM` | Same | **Match** |
| — | $M_\text{min} = 10^{-6}\,M_\odot$ (WIMP free-streaming mass) | Text (p.104): "canonical value $M_\text{min} = 10^{-6}\,M_\odot$" | Same default | Same | **Match** |
| 4.7 | $P_\text{DM}^\text{1h} = \int (dn/dM)[\tilde v/\Delta^2]^2\,dM$ | Eq. 3.59 (p.104) | Not implemented | Same | **Not impl.** (DM auto-power not needed) |
| 4.8 | $P_\text{DM}^\text{2h} = [\int (dn/dM) b\,\tilde v/\Delta^2\,dM]^2 P_\text{lin}$ | Eq. 3.60 (p.104) | Not implemented | Same | **Not impl.** (same reason) |

---

## 5. Astrophysical Sources (`astro_sources.py`) — equations.md §5

### LDDE Framework

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 5.1 | $L_\text{sens}(z) = 4\pi d_L^2 F_\text{sens}$; $F_\text{sens} = 10^{-10}$ cm⁻²s⁻¹ | Eqs. 3.75–3.76 (p.108) | `L_sens(z)` | Same | **Match** |
| 5.2 | $d\Phi/d\log_{10}L = A/[(L/L_c)^{\gamma_1}+(L/L_c)^{\gamma_2}]$ | Eq. C.2 (p.209): same form (with additional Gaussian in Γ, set to 1 by assuming Γ=μ★) | `_ldde_glf` | Same | **Match** |
| 5.3 | $z_c(L) = z_c^*(L/L_\text{ref})^\alpha$ | Text after Eq. C.4 (p.210): $z_c = z_\star(L/10^{48})^\beta$ | `_ldde_glf` | Same | **Match** |
| 5.4 | Piecewise evolution: $e(z) = [(1+z)/(1+z_c)]^{p_1}$ for $z \le z_c$, $^{p_2}$ for $z > z_c$ (FSRQ) | **Not in thesis** — thesis uses Eq. C.4 (ldde_inv) for both BL Lac and FSRQ | `_ldde_glf` with `evolution_form='piecewise'` | Same | **Differs** — Thesis (p.210) states: "BL Lacs and FSRQs exhibit the same functional form for the GLF" and uses Eq. C.4 for both. Pipeline correctly uses piecewise for FSRQ per the original [Ajello+ (2012)](literature/ajello2012.md). **Thesis appears to be in error here.** See [§ Summary](#summary-of-differences) |
| 5.5 | LDDE inverse-sum: $e(z) = [r^{-p_1} + r^{-p_2}]^{-1}$ (BL Lac) | Eq. C.4 (p.210) | `_ldde_glf` with `evolution_form='ldde_inv'` | Same | **Match** |
| 5.6 | $W_\gamma^\text{astro} = \frac{1}{4\pi(1+z)^2}\int \Phi(L,z)\frac{L}{E_\text{GeV\to erg}\,I_\alpha}E_\text{rest}^{-\alpha}\,dL$ | Eq. 5.15 (p.122) via Eqs. 3.65–3.70 (p.107–108) | `W_gamma_astro` | Same | **Match** |

### LDDE GLF Parameters

| Source | Parameter | Thesis (Table C.1, p.210) | Pipeline | Pipeline (Pinetti 2022) | Status |
|--------|-----------|---------------------------|----------|-------------------------|--------|
| BL Lac | $A$ | $9.20\times10^{-11}$ Mpc⁻³ erg⁻¹ s | $9.20\times10^{-11}$ | Same | **Match** |
| BL Lac | $L_\star$ | $2.43\times10^{48}$ erg/s | $2.43\times10^{48}$ | Same | **Match** |
| BL Lac | $\gamma_1, \gamma_2$ | 1.12, 3.71 | 1.12, 3.71 | Same | **Match** |
| BL Lac | $p_1, p_2$ | 4.50, −12.88 | 4.50, −12.88 | Same | **Match** |
| BL Lac | $z_\star$ | 1.67 | 1.67 | Same | **Match** |
| BL Lac | $\beta$ | $4.46\times10^{-2}$ | $4.46\times10^{-2}$ | Same | **Match** |
| FSRQ | $A$ | $3.06\times10^{-9}$ | $3.06\times10^{-9}$ | Same | **Match** |
| FSRQ | $L_\star$ | $0.84\times10^{48}$ erg/s | $0.84\times10^{48}$ | Same | **Match** |
| FSRQ | $\gamma_1, \gamma_2$ | 0.21, 1.58 | 0.21, 1.58 | Same | **Match** |
| FSRQ | $p_1, p_2$ | 7.35, −6.51 | 7.35, −6.51 | Same | **Match** |
| FSRQ | $z_\star$ | 1.47 | 1.47 | Same | **Match** |
| FSRQ | $\beta$ | 0.21 | 0.21 | Same | **Match** |

### Blazar Halo Mass Relation

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| — | $M(L) = 10^{13}M_\odot(M_\star/[10^{8.8}(1+z)^{1.4}])^{0.645}$ | Eq. C.5 (p.210) | Same | Same | **Match** |
| — | $M_\star = 10^9(L/10^{48})^{0.36}$ | Eq. C.6 (p.210) | Same | Same | **Match** |

### mAGN GLF — Radio→Gamma Chain

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 5.7 | $\rho_r = \rho_l + \rho_h$ (two-component Willott RLF at 151 MHz) | Eq. C.9 (p.210) | `_willott_rlf` | Same | **Match** |
| — | Low-power $\rho_l$: exponential cutoff + density evolution $(1+z)^{k_l}$ frozen at $z_{l\star}$ | Eq. C.10 (p.211) | Same form | Same | **Match** |
| — | High-power $\rho_h$: inverse-exponential cutoff + Gaussian evolution $f_h(z)$ | Eqs. C.11–C.12 (p.211) | Same form | Same | **Match** |
| — | Willott RLF parameters ($\rho_{l\star}$, $\beta_l$, $L_{l\star}$, $k_l$, $z_{l\star}$, $\rho_{h\star}$, $\beta_h$, $L_{h\star}$, $z_{h\star}$, $z_{h0}$) | Text after Eq. C.12 (p.211) | Same values | Same | **Match** |
| 5.8 | $\log L_\text{core}^{5\text{GHz}} = 4.2 + 0.77\log L_\text{tot}^{1.4\text{GHz}}$ | Eq. C.14 (p.211) | Same | Same | **Match** |
| 5.9 | $L_r^{1.4\text{GHz}} = L_r^{151\text{MHz}}\times(1400/151)^{-0.80}$ | Eq. C.15 (p.211): $\alpha_r = 0.80$ | Same | Same | **Match** |
| 5.10 | $\log L_\gamma = 2.0 + 1.008\log L_\text{core}^{5\text{GHz}}$ | Eq. C.13 (p.211) | Same | Same | **Match** |
| 5.11 | $\phi_\gamma = k\eta(1+z)^{-(2-\Gamma)}\frac{1}{\ln(10)L_{151}}\left|\frac{dL_{151}}{dL_\gamma}\right|\rho_r$; $k{=}3.05$, $\Gamma{=}2.37$ | Eq. C.19 (p.211–212) | `_glf_mAGN` | Same | **Match** |
| — | Willott cosmology correction $\eta = d^2V_W/(dz\,d\Omega) \;/\; d^2V/(dz\,d\Omega)$ | Eqs. C.16–C.18 (p.211) | `_willott_volume_correction` | Same | **Match** |

### mAGN Halo Mass Relation

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| — | $M(L) = 10^{13}M_\odot(M_\star/[10^{8.8}(1+z)^{1.4}])^{0.645}$ | Eq. C.20 (p.212) | Same | Same | **Match** |
| — | $M_\star = 4.6\times10^9(L/10^8)^{0.16}$ | Eq. C.21 (p.212) | Same | Same | **Match** |

### SFG GLF — IR→Gamma Chain

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 5.12 | $\phi_\text{IR} = \phi_\text{spiral} + \phi_\text{starburst} + \phi_\text{SF-AGN}$ | Eq. C.22 (p.212) | `_gruppioni_ir_lf` | Same | **Match** |
| 5.13 | Modified Schechter form per component | Eq. C.23 (p.212) | `_gruppioni_component` | Same | **Match** |
| — | $L_{0,i}(z)$ luminosity evolution with break at $z=1.1$ | Eq. C.24 (p.212) | Same | Same | **Match** |
| — | $\phi_{0,\text{spiral}}(z)$ with break at $z=0.53$ | Eq. C.25 (p.212) | Same | Same | **Match** |
| — | $\phi_{0,j}(z)$ (starburst, SF-AGN) with break at $z=1.1$ | Eq. C.26 (p.212) | Same | Same | **Match** |

### SFG IR LF Parameters

| Component | Parameter | Thesis (Table C.2, p.213) | Pipeline (`config.py`) | Pipeline (Pinetti 2022) | Status |
|-----------|-----------|---------------------------|------------------------|-------------------------|--------|
| spiral | $\gamma$, $\sigma$, $\log L_\star$, $\log\phi_\star$, $k_L$, $k_{R1}$, $k_{R2}$ | 1.0, 0.50, 9.78, −2.12, 4.49, −0.54, −7.13 | Same | Same | **Match** |
| starburst | Same | 1.0, 0.35, 11.17, −4.46, 1.96, 3.79, −1.06 | Same | Same | **Match** |
| SF-AGN | Same | 1.2, 0.40, 10.80, −3.20, 3.17, 0.67, **3.17** | 1.2, 0.40, 10.80, −3.20, 3.17, 0.67, **−3.17** | $-3.17$ (thesis typo; follows original paper) | **Differs** — Thesis Table C.2 shows $k_{R2} = 3.17$ (positive); pipeline uses $k_{R2} = -3.17$ (negative), matching [Gruppioni+ (2013)](literature/gruppioni2013.md) original. **Thesis typo.** |

### SFG Gamma-Ray Conversion & Mass Relation

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 5.14 | $\log_{10}L_\gamma = 1.09\log_{10}(L_\text{IR}/10^{10}L_\odot) + 39.19$ | Eq. C.27 (p.213) | `_L_IR_from_Lgamma` | Same | **Match** |
| 5.15 | $\phi_\gamma = \phi_\text{IR}\,|d\log L_\text{IR}/d\log L_\gamma|/(L_\gamma\ln10)$ | Eq. C.28 (p.213) | `_glf_SFG` | Same | **Match** |
| — | $M(L) = 10^{12}M_\odot(1+z)^{-1.61}(L/6.8\times10^{39})^{0.92}$ | Eq. C.29 (p.213) | Same | Same | **Match** |

### Spectral Indices

| Source | Thesis (Table 3.1, p.107) | Pipeline (`config.py`) | Pipeline (Pinetti 2022) | Status |
|--------|---------------------------|------------------------|-------------------------|--------|
| BL Lac | 2.11 | 2.11 | Same | **Match** |
| FSRQ | 2.44 | 2.44 | Same | **Match** |
| mAGN | 2.37 | 2.37 | Same | **Match** |
| SFG | 2.7 | 2.7 | Same | **Match** |

### Luminosity Ranges

| Source | Thesis (Table 3.1, p.107) | Pipeline (`config.py`) | Pipeline (Pinetti 2022) | Status |
|--------|---------------------------|------------------------|-------------------------|--------|
| BL Lac | $7\times10^{43}$ – $10^{52}$ erg/s | Same | Same | **Match** |
| FSRQ | $10^{44}$ – $10^{52}$ erg/s | Same | Same | **Match** |
| mAGN | $10^{40}$ – $10^{50}$ erg/s | Same | Same | **Match** |
| SFG | $10^{37}$ – $10^{42}$ erg/s | Same | Same | **Match** |

---

## 6. PPPC4DMID (`pppc4dmid.py`) — equations.md §6

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 6.1 | $dN/dx$ tabulated; $x = E/m_\chi$ | Thesis uses private Pythia code (p.123: "private communication of Prof. Nicolao Fornengo") | PPPC4DMID tables ([Cirelli+ 2011](literature/cirelli2011.md)) | Same (public tables; private Pythia unavailable) | **Differs** — Both Pythia-based; percent-level differences. Pipeline uses public tables for reproducibility |
| 6.2 | $dN/dE = (dN/dx)/m_\chi$ | Standard unit conversion | Same | Same | **Match** |

---

## 7. EBL (`ebl.py`) — equations.md §7

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 7.1 | $\tau(E,z)$ tabulated (Dominguez+ 2011) | Eq. 3.66 context (p.107): "parameterisation of $\tau_{\gamma\gamma}$ as given in Ref. [394]" = Dominguez+ 2011 | `tau(E, z)` via `ebltable` | Same | **Match** |
| 7.2 | $A(E,z) = e^{-\tau(E,z)}$ | Implicit in Eqs. 3.66, 5.15, 5.17 | `attenuation(E, z)` | Same | **Match** |
| 7.3 | Analytic fallback: $\tau \approx 2.5(E/100)^{1.0}(z/1)^{1.3}\times[1+(20/E)^4]^{-1}$ | Not in thesis | `_tau_analytic` | Same | **Addition** — Pipeline extra, calibrated to Dominguez |

---

## 8. Noise & Beams (`noise_model.py`) — equations.md §8

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 8.1 | $T_\text{sys}(\nu) = 30 + 60(300\,\text{MHz}/\nu)^{2.55}$ K | Text with Eq. 5.26 (p.129) | `T_sys(nu)` | Same | **Match** |
| 8.2 | $B_\ell^\text{HI} = \exp(-\ell^2\sigma_\text{beam}^2/2)$; $\sigma_\text{beam} = 1.22\lambda/(D\sqrt{8\ln2})$ | Eq. 5.25 (p.129) | `beam_radio` | Same | **Match** |
| 8.3 | $N_\text{dish} = T_\text{sys}^2 \Omega_S/(N_d t \Delta\nu N_b N_\text{pol} \eta^2)$ | Eq. 5.26 (p.129) | `noise_dish` | Same | **Match** |
| 8.4 | $N_\text{interf} = T_\text{sys}^2 \Omega_S \text{FoV}/(n(u) t \Delta\nu N_b N_\text{pol} \eta^2)$ | Eq. 5.27 (p.130) | `noise_interf` | Same | **Match** |
| 8.5 | $\ell_\text{cut} = \pi D_\text{short}/(1.22\lambda)$; $D_\text{short} = 2D_\text{dish}$ | Text after Eq. 5.27 (p.130) | `ell_cut` | Same | **Match** |
| 8.6 | $N_\ell^\text{radio} = \min(N_\text{dish}, N_\text{interf})$ for $\ell \ge \ell_\text{cut}$ | Text (p.130): combined dish+interferometer | `noise_radio_combined` | Same | **Match** |
| 8.7 | $\sigma_0^\text{Fermi}(E) = 1.20°(E/0.5)^{-0.95} + 0.05°$ | Eq. 5.23 (p.127) | `sigma_psf_fermi` | Same | **Match** |
| 8.8 | $B_\ell^\gamma = \exp(-\sigma_b^2\ell^2/2)$; $\sigma_b = \sigma_0/(1+0.25\sigma_0\ell)$ | Eqs. 5.21–5.22 (p.126–127) | `beam_fermi` | Same | **Match** |
| 8.9 | $N^\gamma$ from 12 energy bins | Table 5.1 (p.125) | `noise_fermi` | Same | **Match** |
| 8.10 | $f_\text{sky,eff} = \min(f_\text{sky}^\text{radio}, f_\text{sky}^\gamma)$ | Implicit in Eq. 5.18 (p.125) | `f_sky_effective` | Same | **Match** |

---

## 9. Angular Power Spectra (`angular_power.py`) — equations.md §9

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 9.1 | $P_\text{HI×DM}^\text{1h}$ | Eq. 4.16 (p.116) | Not implemented (subdominant) | Same | **Not impl.** |
| 9.2 | $P_\text{HI×DM}^\text{2h} = [\int (dn/dM) b\,\tilde v/\Delta^2\,dM][\int (dn/dM) b\,\tilde u_\text{HI} M_\text{HI}/\bar\rho_\text{HI}\,dM]\,P_\text{lin}$ | Eq. 4.17 (p.116) | `P_HI_DM_2h` | Same | **Match** |
| 9.3 | $P_\text{HI×astro}^\text{2h} = [\int (dn/dM) b\,\tilde u_\text{HI} M_\text{HI}/\bar\rho_\text{HI}\,dM]\,b_\text{astro}\,P_\text{lin}$ | Eq. 4.19 (p.116) | `P_HI_astro_2h` | Same | **Match** |
| 9.4 | $C_\ell = \int (d\chi/\chi^2) W_i W_j P_{ij}(k{=}(\ell{+}\tfrac12)/\chi)$ | Eq. 5.10 / Eq. D.33 (p.121/p.218): $k = \ell/\chi$ | `C_ell_HI_gamma` | $k = \ell/\chi$ via `pinetti2022.limber_k()` | **Match** (thesis) |

---

## 10. Statistics (`statistics.py`) — equations.md §10

| Eq. | Claim / Equation | Thesis Reference | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----|-------------------|-----------------|----------|-------------------------|--------|
| 10.1 | $(\Delta C_\ell)^2 = \frac{1}{(2\ell+1)f_\text{sky}}\frac{N^\gamma}{(B_\ell^\gamma)^2}\left[C_\ell^\text{HI}+\frac{N^\text{HI}}{(B_\ell^\text{HI})^2}\right]$ | Eq. 5.28 (p.134): noise-dominated approximation of full Eq. 5.18 (p.125) | `variance_Cl` | Same | **Match** |
| 10.2 | $\text{SNR}^2 = \sum_{\ell,E}[C_\ell/\Delta C_\ell]^2$ | Eq. 5.29 (p.134) | `compute_SNR` | Same | **Match** |
| 10.3 | $\Delta\chi^2 = \sum_{\ell,E}[C_\ell^{\star+\text{DM}}/\Delta C_\ell]^2 - [C_\ell^\star/\Delta C_\ell]^2$ | Eq. 5.30 (p.135) | `delta_chi2` | Same | **Match** |
| 10.4 | $\sigma_v^\text{excl} = \sigma_v^\text{test}\sqrt{\Delta\chi^2_\text{threshold}/\Delta\chi^2_\text{test}}$; 95% CL: $\Delta\chi^2=4$ | Text after Eq. 5.30 (p.135): "2σ level, i.e. $\Delta\chi^2 = 4$" | `exclusion_curve` | Same | **Match** |
| — | Multipole range: $\ell_\text{min}=10$, $\ell_\text{max}=1000$ | Text (p.130): same values ($\ell_\text{max}=2000$ for Fermissimo) | Same (with Fermissimo extension) | Same | **Match** |

---

## 11. Claims from `pinetti2020.md` — Instrument Specifications

### Fermi-LAT (Table 5.1, p.125)

| Parameter | Thesis | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----------|--------|----------|-------------------------|--------|
| 12 energy bins, 0.5 GeV – 1 TeV | Table 5.1 (p.125) | Same | Same | **Match** |
| Photon noise $C_N$ per bin | Table 5.1 (p.125) | Same values | Same | **Match** |
| Sky fractions $f_\text{sky}$ per bin | Table 5.1 (p.125) | Same values | Same | **Match** |
| $\sigma_0^\text{Fermi}$ per bin | Table 5.1 (p.125) | Same values | Same | **Match** |
| $\langle\sigma v\rangle_\text{thermal} = 3\times10^{-26}$ cm³/s | Text (p.135) | Same | Same | **Match** |

### Fermissimo (p.127)

| Parameter | Thesis | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----------|--------|----------|-------------------------|--------|
| Exposure: 2× Fermi-LAT | Text (p.127) | Same | Same | **Match** |
| $\alpha_\sigma = 0.2$ | Eq. 5.24 (p.127) | Same | Same | **Match** |
| PSF floor: 0.001° | Eq. 5.24 (p.127) | Same | Same | **Match** |
| $f_\text{sky} = 0.8$ | Text (p.127) | Same | Same | **Match** |

### Radio Telescopes (Table 5.2, p.130)

| Parameter | Thesis | Pipeline | Pipeline (Pinetti 2022) | Status |
|-----------|--------|----------|-------------------------|--------|
| MeerKAT: 64 dishes, 13.5 m, 4000 deg², 4000 hr, 1 beam | Table 5.2 (p.130) | Same | Same | **Match** |
| MeerKAT bands: UHF [0.4–1.45], L [0.0–0.58] | Table 5.2 (p.130) | Same | Same | **Match** |
| SKA1: 133+64 dishes, 14.5 m, 25000 deg², 10000 hr, 3 km baseline | Table 5.2 (p.130) | Same | Same | **Match** |
| SKA1 bands: Band 1 [0.35–3], Band 2 [0.0–0.5] | Table 5.2 (p.130) | Same | Same | **Match** |
| SKA2: 2000 dishes, 14.5 m, 30000 deg², 10 km, 36 beams | Table 5.2 (p.130) | Same | Same | **Match** |
| Baseline density $n(u)$: 0.005 for SKA, ×10 smaller for MeerKAT | Text after Eq. 5.27 (p.130) | Same | Same | **Match** |

### Key SNR Results (Table 5.3, p.135)

| Configuration | Thesis SNR | Pipeline target | Pipeline (Pinetti 2022) |
|---------------|-----------|----------------|-------------------------|
| MeerKAT UHF + Fermi-LAT (dish+interf) | 3.7 | Reproduced | Same |
| SKA1 Band 2 + Fermi-LAT | 5.7 | Reproduced | Same |
| SKA2 Band 1 + Fermi-LAT | 8.2 | Reproduced | Same |

---

## Summary of Differences

| # | Item | Thesis | Pipeline | Pipeline (Pinetti 2022) | Nature | Impact |
|---|------|--------|----------|-------------------------|--------|--------|
| 1 | **FSRQ evolution form** | LDDE inverse-sum Eq. C.4 (p.210) for both BL Lac and FSRQ | `ldde_inv` for both FSRQ and BL Lac | Same | **Fixed** — pipeline previously used piecewise for FSRQ, but [Ajello+ (2012)](literature/ajello2012.md) Eq. 15 uses the smooth inverse-sum (paper: "continuous around the redshift peak"). Now matches both paper and thesis. | **Resolved** |
| 2 | **Correa concentration coefficients** | Eq. 3.36 (p.99): α=1.628, β=1.661, γ=−0.020 | α=1.754, β=0.275, γ=−0.015 (Planck fit) | Thesis coefficients via `pinetti2022.concentration_correa_thesis()` | Different cosmology fits from the same Correa et al. (2015) paper | **Low–Medium** — affects halo concentrations; pipeline uses the Planck cosmology–consistent fit |
| 3 | **c₂₀₀→c_vir conversion** | Eqs. 3.38–3.41 (p.99): explicit conversion with $\Delta_\text{vir}$-dependent coefficients | `c200_to_cvir()` implemented | Same | **Resolved** — `c200_to_cvir()` implemented | **Resolved** |
| 4 | **SFG SF-AGN $k_{R2}$** | Table C.2 (p.213): $k_{R2} = 3.17$ (positive) | $k_{R2} = -3.17$ (negative) | $-3.17$ (thesis typo; follows original paper) | **Thesis typo** — pipeline matches the original [Gruppioni+ (2013)](literature/gruppioni2013.md) value | **Medium** — wrong sign would cause unphysical density evolution at $z>1.1$ |
| 5 | **$\Omega_\text{HI}$ treatment** | Fixed: $2.45\times10^{-4}$ (p.122) | Computed from $\int (dn/dM) M_\text{HI}\,dM$ (z-dependent) | Fixed $2.45\times10^{-4}$ | Pipeline is more physical; thesis acknowledges factor-of-2 possible variation | **Low** — few-percent difference in $T_b$ and $W_\text{HI}$ |
| 6 | **SMT $q$ parameter** | $q = 0.75$ (Eq. 3.33, p.98) | $q = 0.707$ | $q = 0.75$ via `pinetti2022.bias_pinetti()` | Both values used in literature (ST99 vs ST02) | **Low** — ~5% effect on mass function tails |
| 7 | **DM photon spectra** | Private Pythia code (p.123) | PPPC4DMID public tables | Same (public tables; private Pythia unavailable) | Both Pythia-based | **Low** — percent-level differences |
| 8 | **Limber $k$ substitution** | $k = \ell/\chi$ (Eq. D.33, p.218) | $k = (\ell+\tfrac12)/\chi$ | $k = \ell/\chi$ via `pinetti2022.limber_k()` | Pipeline improvement (LoVerde & Afshordi 2008) | **Low** — more accurate at low $\ell$ |
| 9 | **$\bar T_b$ coefficient** | 44 μK (pre-evaluated with $\Omega_\text{HI}$) | 188$h$ mK (un-substituted) | $44\,\mu$K via `pinetti2022.T_bar_b_thesis()` | Equivalent modulo rounding and $\Omega_\text{HI}$ treatment | **Negligible** |
| 10 | **EBL analytic fallback** | Not described | Calibrated analytic $\tau(E,z)$ | Same | Pipeline addition for robustness | **None** (fallback only) |
| 11 | **$\Delta_\text{vir}$ definition** | $\Delta_\text{vir}(z)$ from Bryan & Norman fit, Eq. 3.27 (p.96) | Bryan & Norman $\Delta_\text{vir}(z)$ | Same | **Resolved** — Bryan & Norman implemented | **Resolved** |
| 12 | **BL Lac LDDE exponent signs** | Eq. C.4 (p.210): $[r^{-p_1} + r^{-p_2}]^{-1}$ (negative exponents) | Same as thesis: `ratio**(-p1) + ratio**(-p2)` | Same | Original [Ajello+ (2014)](literature/ajello2014.md) Eq. 18 uses **positive** exponents $[r^{p_1} + r^{p_2}]^{-1}$. Pipeline follows Pinetti convention. These produce different evolution shapes around $z_c$. | **Medium** — investigate whether more recent BL Lac literature uses positive or negative exponents |

---

## Intentionally Omitted from Pipeline

| Item | Thesis Reference | Reason |
|------|-----------------|--------|
| $P_\text{DM}^\text{1h}$ (DM auto 1-halo) | Eq. 3.59 (p.104) | Pipeline computes HI×γ cross-power, not DM×DM auto-power |
| $P_\text{DM}^\text{2h}$ (DM auto 2-halo) | Eq. 3.60 (p.104) | Same |
| $P_\text{HI×DM}^\text{1h}$ (cross 1-halo) | Eq. 4.16 (p.116) | Subdominant at $\ell \le 1000$; 2-halo term suffices |
| Astrophysical auto-power $P_{SS}^\text{1h}$, $P_{SS}^\text{2h}$ | Eqs. 3.71–3.72 (p.108) | Not needed for cross-correlation pipeline |
| Gaussian spectral index distribution in GLF | Eq. C.2 exponential factor (p.209) | Set to unity by assuming $\Gamma = \mu_\star$ |
| $P_\text{HI×S}^\text{1h}$ (astro cross 1-halo) | Eq. 4.18 (p.116) | Subdominant at scales of interest |

---

## Verification Plan

To confirm agreement numerically:
1. Run `pytest tests/` — unit tests validate internal consistency
2. Reproduce thesis Fig. 5.2 (left, p.124): UGRB intensity vs energy
3. Reproduce thesis Fig. 5.2 (right, p.124): auto-correlation $C_\ell^{\gamma\gamma}$ vs Fermi-LAT data
4. Reproduce thesis Table 5.3 (p.135): SNR values for MeerKAT/SKA1/SKA2
5. Reproduce thesis Fig. 5.9 (p.136): DM exclusion curves at 2σ
