# Equation Reference

Every equation, empirical relation, and scholarly result used in the pipeline, organized by module.

---

## 1. Cosmology (`cosmology.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 1.1 | $E(z) = \sqrt{\Omega_M(1+z)^3 + \Omega_\Lambda}$ | Flat ΛCDM | `E(z)` |
| 1.2 | $H(z) = H_0 E(z)$ | [Planck 2018](literature/planck2018.md): $H_0 = 67.36$ km/s/Mpc | `H(z)` |
| 1.3 | $\chi(z) = \frac{c}{H_0}\int_0^z \frac{dz'}{E(z')}$ | Standard cosmology | `chi(z)` |
| 1.4 | $d_L(z) = (1+z)\,\chi(z)$ | Standard cosmology | `d_L(z)` |
| 1.5 | $D(z) \propto E(z)\int_z^\infty \frac{dz'}{(1+z')E(z')^3}$, $D(0)=1$ | Exact flat ΛCDM | `growth_factor(z)` |
| 1.6 | $\rho_c = \frac{3H_0^2}{8\pi G} = 2.775\times10^{11}\;M_\odot h^{-1}\,(\text{Mpc}/h)^{-3}$ | Standard | `config.RHO_CRIT` |
| 1.7 | $\bar\rho_m = \Omega_M\,\rho_c$ | Standard | `config.RHO_BAR` |
| 1.8 | $P_\text{lin}(k,z)$ via CAMB Boltzmann solver | [Planck 2018](literature/planck2018.md) params | `P_lin(k, z)` |
| 1.9 | $\sigma^2(R,z) = \frac{1}{2\pi^2}\int dk\,k^2\,P_\text{lin}(k,z)\,W^2(kR)$ | Perturbation theory | `sigma_R(R, z)` |
| 1.10 | $W(x) = 3\frac{\sin x - x\cos x}{x^3}$ (top-hat window) | Standard | `_tophat_W(kR)` |
| 1.11 | $R(M) = (3M / 4\pi\bar\rho_m)^{1/3}$ | Mass–radius relation | `sigma_M(M, z)` |

**[Planck 2018](literature/planck2018.md) parameters** (`config.py`): $h=0.6736$, $\Omega_bh^2=0.02237$, $\Omega_ch^2=0.1200$, $n_s=0.9649$, $\sigma_8=0.8111$, $A_s=2.1\times10^{-9}$, $\Omega_M=0.3153$, $T_\text{CMB}=2.7255$ K, $\tau=0.0544$.

---

## 2. Halo Model (`halo_model.py`, `hmf_interface.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 2.1 | $R_\text{vir} = \left(\frac{3M}{4\pi\Delta_\text{vir}\rho_c(z)}\right)^{1/3}$, $\Delta_\text{vir}=200$ | M₂₀₀c definition; $\rho_c(z)=\rho_c(0)E^2(z)$ | `R_vir(M, z)` |
| 2.2 | $v_c = \sqrt{GM/R_\text{vir}}$ | Dynamical | `v_circ(M, z)` |
| 2.3 | $\nu = \delta_c^2/\sigma^2(M,z)$, $\delta_c=1.686$ | Spherical collapse | `nu(M, z)` |
| 2.4 | $\nu f(\nu) = A\left[1+(q\nu)^{-p}\right]\sqrt{\frac{q\nu}{2\pi}}\exp\left(-\frac{q\nu}{2}\right)$ | [Sheth, Mo & Tormen (2001)](literature/sheth_mo_tormen2001.md) | hmf `SMT` model |
|    | $q=0.707$, $p=0.3$, $A\approx0.3222$ | | |
| 2.5 | $b(\nu) = 1 + \frac{q\nu-1}{\delta_c} + \frac{2p}{\delta_c(1+(q\nu)^p)}$ | [Sheth & Tormen (1999)](literature/sheth_tormen1999.md) | `bias(M, z)` |
| 2.6 | $\log_{10}c = \alpha + \beta\log_{10}(M/M_\odot)[1+\gamma(\log_{10}M/M_\odot)^2]$ ($z \le 4$) | [Correa et al. (2015)](literature/correa2015.md) Appendix B1, Planck | `concentration_correa` |
|    | $\alpha{=}1.7543{-}0.2766(1{+}z){+}0.02039(1{+}z)^2$; $\beta{=}0.2753{+}0.00351(1{+}z){-}0.3038(1{+}z)^{0.0269}$; $\gamma{=}{-}0.01537{+}0.02102(1{+}z)^{-0.1475}$ | | |
| 2.7 | $f(c) = \ln(1+c) - c/(1+c)$ | NFW normalization | `_f_nfw(c)` |
| 2.8 | $\tilde u(k\|M) = \frac{1}{f(c)}\left[\sin(kr_s)[\text{Si}((1{+}c)kr_s){-}\text{Si}(kr_s)] + \cos(kr_s)[\text{Ci}((1{+}c)kr_s){-}\text{Ci}(kr_s)] - \frac{\sin(ckr_s)}{(1{+}c)kr_s}\right]$ | Analytic NFW FT; $r_s=R_\text{vir}/c$ | `u_nfw(k, M, z)` |

---

## 3. HI Model (`hi_model.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 3.1 | $M_\text{HI} = \alpha\,f_{H,c}\,M\left(\frac{M}{10^{11}h^{-1}M_\odot}\right)^\beta\exp\left[-\left(\frac{v_{c,0}}{v_c}\right)^3\right]$ | [Padmanabhan+ (2017)](literature/padmanabhan2017.md); [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.7 | `M_HI(M, z)` |
|   | $\alpha=0.176$, $\beta=-0.69$, $v_{c,0}=40.7$ km/s ([Padmanabhan+ 2017](literature/padmanabhan2017.md) Table A1, modified NFW) | | |
|   | $f_{H,c}=(1-Y_P)\Omega_B/\Omega_M$, $Y_P=0.24$ | | |
| 3.2 | $c_\text{HI} = c_{HI,0}\left(\frac{M}{10^{11}M_\odot}\right)^{-0.109}\frac{4}{(1+z)^\gamma}$, $c_{HI,0}=139$, $\gamma=0.13$ | [Padmanabhan+ (2017)](literature/padmanabhan2017.md) Table A1 | `c_HI(M, z)` |
| 3.3 | $\rho_\text{HI}(r) = \rho_0\,r_s^3 / [(r+0.75r_s)(r+r_s)^2]$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.9 (modified NFW) | (used inside `u_HI`) |
| 3.4 | $\rho_0$ from $\int_0^{R_\text{vir}}4\pi r^2\rho_\text{HI}\,dr = M_\text{HI}$ | Mass normalization | `rho0_HI` |
| 3.5 | $\tilde u_\text{HI}(k\|M) = \frac{4\pi}{M_\text{HI}}\int_0^{R_\text{vir}}r^2\rho_\text{HI}(r)\frac{\sin kr}{kr}dr$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.14 | `u_HI(k, M, z)` |
| 3.6 | $\bar\rho_\text{HI}(z) = \int\frac{dn}{dM}\,M_\text{HI}(M,z)\,dM$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.2 | `rho_HI_mean(z)` |
| 3.7 | $\Omega_\text{HI}(z) = (1+z)^{-3}\bar\rho_\text{HI}(z)/\rho_c$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.3 | `Omega_HI(z)` |
| 3.8 | $\bar T_b(z) = 188\,h\,\Omega_\text{HI}(z)\,\frac{(1+z)^2}{E(z)}$ mK | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.4 | `T_bar_b(z)` |
| 3.9 | $b_\text{HI}(z) = \frac{1}{\bar\rho_\text{HI}}\int\frac{dn}{dM}\,M_\text{HI}\,b(M,z)\,dM$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.6 | `b_HI(z)` |
| 3.10 | $P_\text{HI}^\text{1h}(k,z) = \frac{1}{\bar\rho_\text{HI}^2}\int\frac{dn}{dM}\,M_\text{HI}^2\,\tilde u_\text{HI}^2\,dM$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.12 | `P_HI_1h` |
| 3.11 | $P_\text{HI}^\text{2h}(k,z) = \left[\frac{1}{\bar\rho_\text{HI}}\int\frac{dn}{dM}\,b\,M_\text{HI}\,\tilde u_\text{HI}\,dM\right]^2 P_\text{lin}$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 3.13 | `P_HI_2h` |
| 3.12 | $W_\text{HI}(\chi) = \bar T_b(z)\,b_\text{HI}(z)\,\phi(z)\,\frac{H(z)}{ch}$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eqs. 3.15–3.16 | `W_HI(z, z_min, z_max)` |
|   | $\phi(z) = 1/(z_\text{max}-z_\text{min})$ (top-hat selection) | | |

---

## 4. Dark Matter Model (`dm_model.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 4.1 | $\rho_s = M / [4\pi r_s^3 f(c)]$ | NFW scale density | `_rho_s(M, z)` |
| 4.2 | $\int_0^{R_\text{vir}}4\pi r^2\rho_\text{NFW}^2\,dr = \frac{4\pi}{3}\rho_s^2 r_s^3[1-(1+c)^{-3}]$ | Analytic $\rho^2$ integral | `rho2_integral_analytic` |
| 4.3 | $\tilde v(k\|M) = \frac{4\pi}{\bar\rho_m^2}\int_0^{R_\text{vir}}r^2\rho_\text{NFW}^2\frac{\sin kr}{kr}dr$ | Fourier transform of $\rho^2$ | `v_tilde(k, M, z)` |
| 4.4a | $\log_{10}B(M,z{=}0) = \sum_{i=0}^{5}b_i[\log_{10}(M/M_\odot)]^i$ | [Moliné et al. (2017)](literature/moline2017.md) Eq. 18, Table 3 ($\alpha{=}2$) | `boost_moline` |
| 4.4b | $B(M,z) = B(M,z{=}0)/(1+z)$ | Thesis Eq. 3.48 | `boost_moline` |
| 4.5 | $\Delta^2(z) = \frac{1}{\bar\rho_m^2}\int\frac{dn}{dM}[1+B(M,z)]\int\rho^2\,d^3x\,dM$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 4.2 | `clumping_factor` |
| 4.6 | $W_\gamma^\text{DM}(\chi) = \frac{\langle\sigma v\rangle}{8\pi}\left(\frac{\rho_\text{DM}}{m_\chi}\right)^2(1+z)^3\frac{1}{H(z)}\Delta^2\frac{dN}{dE'}e^{-\tau}$ | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Eq. 4.1 | `W_gamma_DM` |
|   | $E'=(1+z)E_\gamma$; $\langle\sigma v\rangle_\text{thermal}=3\times10^{-26}$ cm³/s | | |
| 4.7 | $P_\text{DM}^\text{1h} = \int\frac{dn}{dM}[\tilde v/\Delta^2]^2\,dM$ | [Pinetti+](literature/pinetti2020.md) Eq. 4.4 | (not needed; pipeline uses cross-power only) |
| 4.8 | $P_\text{DM}^\text{2h} = [\int\frac{dn}{dM}\,b\,\tilde v/\Delta^2\,dM]^2\,P_\text{lin}$ | [Pinetti+](literature/pinetti2020.md) Eq. 4.5 | (not needed; pipeline uses cross-power only) |

---

## 5. Astrophysical Sources (`astro_sources.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 5.1 | $L_\text{sens}(z) = 4\pi d_L^2(z)\,F_\text{sens}$; $F_\text{sens}=10^{-10}$ cm⁻²s⁻¹ | Fermi-LAT sensitivity | `L_sens(z)` |
| 5.2 | $\frac{d\Phi}{d\log_{10}L} = \frac{A}{(L/L_c)^{\gamma_1}+(L/L_c)^{\gamma_2}}$ | LDDE double power-law | `_ldde_glf` |
|   | Conversion: $d\Phi/dL = (d\Phi/d\log L)/(L\ln10)$ | | |
| 5.3 | $z_c(L) = z_c^*(L/L_\text{ref})^\alpha$ | Luminosity-dependent peak | `_ldde_glf` |
| 5.4 | Piecewise evolution: $e(z) = [(1+z)/(1+z_c)]^{p_1}$ for $z\le z_c$, $^{p_2}$ for $z>z_c$ | FSRQ | `_ldde_glf` |
| 5.5 | LDDE inverse-sum: $e(z) = [r^{-p_1} + r^{-p_2}]^{-1}$, $r=(1+z)/(1+z_c)$ | BL Lac ([Ajello+ 2014](literature/ajello2014.md) Eq. C.4) | `_ldde_glf` |
| 5.6 | $W_\gamma^\text{astro}(\chi) = \frac{1}{4\pi(1+z)^2}\int_{L_\text{min}}^{L_\text{up}}\Phi(L,z)\,\frac{L}{E_\text{GeV\to erg}\,I_\alpha}\,E_\text{rest}^{-\alpha}\,dL$ | [Pinetti+](literature/pinetti2020.md) Eq. 4.3 (after $d_L^2$ cancellation) | `W_gamma_astro` |
|   | $I_\alpha = \int_{0.1}^{100}E^{1-\alpha}dE$; $E_\text{rest}=(1+z)E$ | | |

### LDDE GLF Parameters (FSRQ, BL Lac only)

| Source | $A$ (Mpc⁻³) | $L_c$ (erg/s) | $\gamma_1$ | $\gamma_2$ | $z_c^*$ | $\alpha$ | $p_1$ | $p_2$ | Evolution | Reference |
|--------|-------------|---------------|-----------|-----------|---------|---------|-------|-------|-----------|-----------|
| FSRQ | $3.06\times10^{-9}$ | $8.4\times10^{47}$ | 0.21 | 1.58 | 1.47 | 0.21 | 7.35 | −6.51 | piecewise | [Ajello+ (2012)](literature/ajello2012.md) Table 3 |
| BL Lac | $9.20\times10^{-11}$ | $2.43\times10^{48}$ | 1.12 | 3.71 | 1.67 | 0.0446 | 4.50 | −12.88 | ldde_inv | [Ajello+ (2014)](literature/ajello2014.md) Table C.1 |

*Note:* The $\alpha$ column is the luminosity dependence of $z_c$: $z_c(L) = z_c^*(L/L_\text{ref})^\alpha$. Code uses `alpha` for both sources; [Ajello+ (2014)](literature/ajello2014.md) calls the BL Lac parameter $\beta$.

### mAGN GLF — Radio→Gamma Conversion Chain ([Di Mauro+ 2014](literature/dimauro2014.md))

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 5.7 | $\rho_r(L_{151}, z) = \rho_l(L_{151}, z) + \rho_h(L_{151}, z)$ (two-component RLF at 151 MHz) | [Willott+ (2001)](literature/willott2001.md) | `_willott_rlf` |
| 5.8 | $\log_{10} L_\text{core}^{5\text{GHz}} = 4.2 + 0.77\,\log_{10} L_\text{tot}^{1.4\text{GHz}}$ | [Lara+ (2004)](literature/lara2004.md) | `_L151_from_Lgamma` |
| 5.9 | $L_r^{1.4\text{GHz}} = L_r^{151\text{MHz}} \times (1400/151)^{-0.80}$ | [Inoue (2011)](literature/inoue2011.md) | `_L151_from_Lgamma` |
| 5.10 | $\log_{10} L_\gamma = 2.0 + 1.008\,\log_{10} L_\text{core}^{5\text{GHz}}$ | [Di Mauro+ (2014)](literature/dimauro2014.md) | `_L151_from_Lgamma` |
| 5.11 | $\phi_\gamma = \frac{k\,\eta}{(1+z)^{2-\Gamma}}\,\frac{\rho_r}{\ln(10)\,L_{151}}\,\left\|\frac{dL_{151}}{dL_\gamma}\right\|$; $k{=}3.05$, $\Gamma{=}2.37$ | [Di Mauro+ (2014)](literature/dimauro2014.md) Eq. C.19 | `_glf_mAGN` |

### SFG GLF — IR→Gamma Conversion Chain ([Gruppioni+ 2013](literature/gruppioni2013.md))

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 5.12 | $\phi_\text{IR} = \phi_\text{spiral} + \phi_\text{starburst} + \phi_\text{SF-AGN}$ | [Gruppioni+ (2013)](literature/gruppioni2013.md) | `_gruppioni_ir_lf` |
| 5.13 | $\phi_i = \phi_{0,i}(z)(L_\text{IR}/L_{0,i})^{1-\gamma_i}\exp[-\log_{10}^2(1{+}L_\text{IR}/L_{0,i})/(2\sigma_i^2)]$ | [Gruppioni+ (2013)](literature/gruppioni2013.md) Eq. C.23 | `_gruppioni_component` |
| 5.14 | $\log_{10} L_\gamma = 1.09\,\log_{10}(L_\text{IR}/10^{10}L_\odot) + 39.19$ | [Ackermann+ (2012)](literature/ackermann2012_sfg.md) | `_L_IR_from_Lgamma` |
| 5.15 | $\phi_\gamma = \phi_\text{IR}\,|d\log_{10}L_\text{IR}/d\log_{10}L_\gamma| / (L_\gamma\ln10)$ | Eq. C.28 | `_glf_SFG` |

### Spectral Indices ([Pinetti+](literature/pinetti2020.md) Table 3)

| Source | $\alpha$ (photon index) |
|--------|------------------------|
| BL Lac | 2.11 |
| FSRQ | 2.44 |
| mAGN | 2.37 |
| SFG | 2.7 |

---

## 6. PPPC4DMID (`pppc4dmid.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 6.1 | $dN/dx$ tabulated; $x=E/m_\chi$ | [Cirelli et al. (2011)](literature/cirelli2011.md) PPPC4DMID tables | `dNdx(x, m_chi, ch)` |
| 6.2 | $dN/dE = (dN/dx)/m_\chi$ | Unit conversion | `dNdE(E, m_chi, ch)` |

Channels: bb̄, τ⁺τ⁻, W⁺W⁻, ZZ, cc̄, tt̄, ee, μμ, gg, hh, qq̄, γγ. Mass range: 5 GeV–100 TeV.

---

## 7. EBL (`ebl.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 7.1 | $\tau(E,z)$ tabulated | [[Dominguez](literature/dominguez2011.md) et al. (2011)](literature/dominguez2011.md) via `ebltable` | `tau(E, z)` |
| 7.2 | $A(E,z) = e^{-\tau(E,z)}$ | Pair-production absorption | `attenuation(E, z)` |
| 7.3 | Analytic fallback: $\tau \approx 2.5(E/100)^{1.0}(z/1)^{1.3}\times[1+(20/E)^4]^{-1}$ | Calibrated to [Dominguez](literature/dominguez2011.md) | `_tau_analytic` |

Models: `dominguez`, `franceschini`, `finke`, `saldana-lopez21`.

---

## 8. Noise & Beams (`noise_model.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 8.1 | $T_\text{sys}(\nu) = 30 + 60(300\text{ MHz}/\nu)^{2.55}$ K | Radio telescope formula | `T_sys(nu)` |
| 8.2 | $B_\ell^\text{HI} = \exp(-\ell^2\sigma_\text{beam}^2/2)$; $\sigma_\text{beam}=1.22\lambda/(D\sqrt{8\ln2})$ | Gaussian beam; [Pinetti+](literature/pinetti2020.md) Eq. 3.17 | `beam_radio` |
| 8.3 | $N_\text{dish}^\text{HI} = T_\text{sys}^2\,\Omega_S/(N_d\,t\,\Delta\nu\,N_b\,N_\text{pol}\,\eta^2)$ | [Pinetti+](literature/pinetti2020.md) Eq. 3.18 | `noise_dish` |
| 8.4 | $N_\text{interf}^\text{HI} = T_\text{sys}^2\,\Omega_S\,\text{FoV}/(n(u)\,t\,\Delta\nu\,N_b\,N_\text{pol}\,\eta^2)$ | [Pinetti+](literature/pinetti2020.md) Eq. 3.19 | `noise_interf` |
| 8.5 | $\ell_\text{cut} = \pi D_\text{short}/(1.22\lambda)$; $D_\text{short}=2D_\text{dish}$ | Shortest baseline limit | `ell_cut` |
| 8.6 | $N_\ell^\text{radio} = \min(N_\text{dish}, N_\text{interf})$ for $\ell\ge\ell_\text{cut}$ | Hybrid mode | `noise_radio_combined` |
| 8.7 | $\sigma_0^\text{Fermi}(E) = 1.20°\,(E/0.5\text{ GeV})^{-0.95} + 0.05°$ | [Pinetti+](literature/pinetti2020.md) Eq. 4.11 | `sigma_psf_fermi` |
| 8.8 | $B_\ell^\gamma = \exp(-\sigma_b^2\ell^2/2)$; $\sigma_b=\sigma_0/(1+0.25\sigma_0\ell)$ | [Pinetti+](literature/pinetti2020.md) Eqs. 4.9–4.10 | `beam_fermi` |
| 8.9 | $N^\gamma$ from [Pinetti+](literature/pinetti2020.md) Table 2 (12 energy bins) | [[Pinetti+](literature/pinetti2020.md) (2020)](literature/pinetti2020.md) Table 2 | `noise_fermi` |
| 8.10 | $f_\text{sky,eff} = \min(f_\text{sky}^\text{radio}, f_\text{sky}^\gamma)$ | Conservative overlap | `f_sky_effective` |

---

## 9. Angular Power Spectra (`angular_power.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 9.1 | $P_{\text{HI}\times\text{DM}}^\text{1h} = \int\frac{dn}{dM}\frac{\tilde v}{\Delta^2}\frac{\tilde u_\text{HI}\,M_\text{HI}}{\bar\rho_\text{HI}}dM$ | [Pinetti+](literature/pinetti2020.md) Eq. 5.1 | (subdominant; not computed) |
| 9.2 | $P_{\text{HI}\times\text{DM}}^\text{2h} = [\int\frac{dn}{dM}b\frac{\tilde v}{\Delta^2}dM][\int\frac{dn}{dM}b\frac{\tilde u_\text{HI}M_\text{HI}}{\bar\rho_\text{HI}}dM]\,P_\text{lin}$ | [Pinetti+](literature/pinetti2020.md) Eq. 5.2 | `P_HI_DM_2h` |
| 9.3 | $P_{\text{HI}\times\text{astro}}^\text{2h} = [\int\frac{dn}{dM}b\frac{\tilde u_\text{HI}M_\text{HI}}{\bar\rho_\text{HI}}dM]\,b_\text{astro}\,P_\text{lin}$ | [Pinetti+](literature/pinetti2020.md) Eqs. 5.3–5.4 | `P_HI_astro_2h` |
| 9.4 | $C_\ell^{ij} = \int\frac{d\chi}{\chi^2}\,W_i(\chi)\,W_j(\chi)\,P_{ij}(k{=}(\ell{+}\tfrac12)/\chi,\,z)$ | Limber approximation; [Pinetti+](literature/pinetti2020.md) Eq. 2.1 | `C_ell_HI_gamma` |

---

## 10. Statistics (`statistics.py`)

| # | Equation | Source | Function |
|---|----------|--------|----------|
| 10.1 | $(\Delta C_\ell)^2 = \frac{1}{(2\ell+1)f_\text{sky}}\frac{N^\gamma}{(B_\ell^\gamma)^2}\left[C_\ell^\text{HI}+\frac{N^\text{HI}}{(B_\ell^\text{HI})^2}\right]$ | [Pinetti+](literature/pinetti2020.md) Eq. 5.5 | `variance_Cl` |
| 10.2 | $\text{SNR}^2 = \sum_{\ell,E}\left[\frac{C_\ell^{\text{HI}\times\gamma_\star}}{\Delta C_\ell}\right]^2$ | [Pinetti+](literature/pinetti2020.md) Eq. 5.6 | `compute_SNR` |
| 10.3 | $\Delta\chi^2 = \sum_{\ell,E}\left[\frac{C_\ell^{\star+\text{DM}}}{\Delta C_\ell}\right]^2 - \left[\frac{C_\ell^\star}{\Delta C_\ell}\right]^2$ | [Pinetti+](literature/pinetti2020.md) Eq. 5.7 | `delta_chi2` |
| 10.4 | $\sigma_v^\text{excl} = \sigma_v^\text{test}\sqrt{\Delta\chi^2_\text{threshold}/\Delta\chi^2_\text{test}}$ | 95% CL: $\Delta\chi^2=4$; 5σ: $\Delta\chi^2=25$ | `exclusion_curve` |

---

## References

- [Ajello et al. (2012)](literature/ajello2012.md), ApJ 751, 108 — FSRQ luminosity function
- [Ajello et al. (2014)](literature/ajello2014.md), MNRAS 441, 1760 — BL Lac luminosity function
- [Cirelli et al. (2011)](literature/cirelli2011.md), JCAP 03, 051 — PPPC4DMID photon yield tables
- [Di Mauro et al. (2013, 2014)](literature/dimauro2014.md), ApJ 780, 161 — mAGN gamma-ray emission
- [[Dominguez](literature/dominguez2011.md) et al. (2011)](literature/dominguez2011.md), MNRAS 410, 2556 — EBL opacity model
- [Gruppioni et al. (2013)](literature/gruppioni2013.md), MNRAS 432, 23 — IR luminosity function (SFG)
- [Moliné et al. (2017)](literature/moline2017.md), MNRAS 466, 4974 — Substructure boost factor
- [Padmanabhan, Refregier & Amara (2017)](literature/padmanabhan2017.md), MNRAS 469, 2323 — HI halo model
- [Pinetti, Camera, Fornengo & Regis (2020)](literature/pinetti2020.md), arXiv:1911.04989 — Primary reference
- [Planck Collaboration (2018)](literature/planck2018.md), A&A 641, A6 — Cosmological parameters
- [Sheth & Tormen (1999)](literature/sheth_tormen1999.md), MNRAS 308, 119 — Halo bias
- [Sheth, Mo & Tormen (2001)](literature/sheth_mo_tormen2001.md), MNRAS 323, 1 — Halo mass function
