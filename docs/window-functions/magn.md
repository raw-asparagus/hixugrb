# mAGN Window Function: Complete Pipeline

## Target Quantity

The misaligned AGN (mAGN) window function enters the Limber integral for the angular cross-power spectrum (Pinetti+ 2020, Eq. 2.1). It shares the generic astrophysical gamma-ray source form (Pinetti+ 2020 Eq. 4.3):

$$W_\gamma^{\rm mAGN}(\chi) = \frac{1}{4\pi(1+z)^2}\int_{L_{\min}}^{L_{\rm up}}\Phi_\gamma^{\rm mAGN}(L,z)\;\frac{L}{E_{\rm GeV\to erg}\,I_\alpha}\;E_{\rm rest}^{-\alpha}\;dL$$

with $\alpha=2.37$ (Pinetti+ 2020 Table 3 mAGN photon index), $E_{\rm rest}=(1+z)\,E_{\rm obs}$, $I_\alpha=\int_{0.1}^{100}E^{1-\alpha}\,dE$ [GeV$^{2-\alpha}$], and $L_{\rm up}=\min(L_{\max}, L_{\rm thr}(z))$ with Fermi-LAT sensitivity threshold $L_{\rm thr}(z)=4\pi d_L^2(z)\,F_{\rm sens}$.

What makes mAGN unique is that $\Phi_\gamma^{\rm mAGN}$ is **not** fit directly to gamma-ray data (unlike BL Lac / FSRQ LDDE). Instead, it is derived from the much better-constrained 151 MHz **radio** luminosity function via a 3-step empirical conversion chain.

---

## Layer 1: Cosmological Backbone

Standard Planck 2018 cosmology: $h=0.6736$, $\Omega_M=0.3153$, $H(z)$, $\chi(z)$, $d_L(z)$.

**Implementation:** `cosmology.py`.

---

## Layer 2: Willott et al. (2001) Radio Luminosity Function at 151 MHz

Foundation: two-component steep-spectrum RLF from 356 combined radio sources (3CRR + 6CE + 7CRS):

$$\rho_r(L_{151}, z) = \rho_l(L_{151}, z) + \rho_h(L_{151}, z)$$

### Low-power component (FRI-like, Willott Eq. for $\rho_l$)

$$\rho_l = \rho_{l\star}\left(\frac{L_{151}}{L_{l\star}}\right)^{-\beta_l}\exp\!\left(-\frac{L_{151}}{L_{l\star}}\right) \times \begin{cases}(1+z)^{k_l} & z < z_{l\star}\\(1+z_{l\star})^{k_l} & z \ge z_{l\star}\end{cases}$$

### High-power component (FRII/quasar-like)

$$\rho_h = \rho_{h\star}\left(\frac{L_{151}}{L_{h\star}}\right)^{-\beta_h}\exp\!\left(-\frac{L_{h\star}}{L_{151}}\right)\exp\!\left\{-\frac{1}{2}\left(\frac{z - z_{h\star}}{z_{h0}}\right)^2\right\}$$

| Parameter | Low-power | High-power | Unit |
|-----------|-----------|-----------|------|
| $\rho_\star$ | $10^{-7.523}$ | $10^{-6.757}$ | Mpc⁻³ (Willott cosmology) |
| $\beta$ | 0.586 | 2.42 | — |
| $L_\star$ | $10^{26.48}$ | $10^{27.39}$ | W/Hz at 151 MHz |
| $k_l$, $z_{l\star}$ | 3.48, 0.710 | — | — |
| $z_{h\star}$, $z_{h0}$ | — | 2.03, 0.568/0.956 | — |

Returns $d\Phi/d(\log_{10}L_{151})$ in Mpc⁻³. These parameters are from Willott (2001) Table 1, in the Willott reference cosmology ($H_0=50$ km/s/Mpc, Einstein–de Sitter).

**Implementation:** `astro_sources.py:_willott_rlf()`; parameters in `config.py` (WILLOTT_*).

---

## Layer 3: Cosmology Volume Correction — Willott → Planck

The Willott RLF is defined in a reference cosmology with $H_0=50$ km/s/Mpc. To use it in Planck 2018, a comoving volume correction is applied:

$$\eta(z) = \left(\frac{d_C^{\rm Willott}}{d_C^{\rm Planck}}\right)^2 \frac{H^{\rm Planck}(z)}{H^{\rm Willott}(z)}$$

where $H^{\rm Willott}(z) = H_0^W(1+z)^{3/2}$ (Einstein–de Sitter) and $d_C^{\rm Willott}(z) = (c/H_0^W)\int_0^z dz'/(1+z')^{3/2}$.

**Implementation:** `astro_sources.py:_willott_volume_correction(z)` (LRU-cached with maxsize=512).

---

## Layer 4: Radio → Gamma-Ray Conversion Chain (Di Mauro+ 2014)

Central mAGN-specific machinery. Converts radio luminosity at 151 MHz to gamma-ray luminosity via three empirical correlations, all defined in log-space:

### Step 1 — Frequency scaling (Inoue 2011, $\alpha_r=0.80$)

$$L_r^{1.4\,\rm GHz} = L_r^{151\,\rm MHz}\times\left(\frac{1400}{151}\right)^{-0.80}$$

### Step 2 — Core-total relation (Lara+ 2004)

$$\log_{10} L_{r,\rm core}^{5\,\rm GHz} = 4.2 + 0.77\,\log_{10} L_{r,\rm tot}^{1.4\,\rm GHz}\quad[\text{W/Hz}]$$

### Step 3 — Radio-core → gamma correlation (Di Mauro+ 2014 Eq. C.13)

$$\log_{10}(L_\gamma) = 2.0 + 1.008\,\log_{10}\!\left[(\nu L_\nu)_{\rm core}^{5\,\rm GHz}\right]\quad[\text{erg/s}]$$

**Unit note:** Di Mauro's correlation uses $\nu L_\nu$ in erg/s, while Lara's uses $L_\nu$ in W/Hz. The conversion is $\nu L_\nu\,[{\rm erg/s}] = L_\nu\,[{\rm W/Hz}] \times \nu\,[{\rm Hz}]\times 10^7\,[{\rm erg\,s^{-1}\,W^{-1}}]$.

The pipeline **inverts** this chain: given $L_\gamma$, solve backward through all three steps to obtain $L_{151}$. The composite log-space Jacobian is:

$$\frac{d\log L_{151}}{d\log L_\gamma} = \frac{1}{1.008 \times 0.77} \approx 1.288$$

hence $dL_{151}/dL_\gamma = (L_{151}/L_\gamma) \times 1.288$.

**Implementation:** `astro_sources.py:_L151_from_Lgamma()`; parameters in `config.py` (DIMAURO_*, LARA_*, RADIO_ALPHA).

---

## Layer 5: mAGN Gamma-Ray Luminosity Function (Di Mauro+ 2014 Eq. C.19)

Combining the Willott RLF with the conversion chain:

$$\boxed{\Phi_\gamma^{\rm mAGN}(L_\gamma, z) = \frac{k\,\eta(z)}{(1+z)^{2-\Gamma}}\;\frac{1}{\ln(10)\,L_{151}}\;\left|\frac{dL_{151}}{dL_\gamma}\right|\;\rho_r\!\left(L_{151}(L_\gamma),\,z\right)}$$

| Factor | Value | Role |
|--------|-------|------|
| $k$ | 3.05 | Beaming/duty-cycle correction (fraction of radio galaxies with detectable gamma-ray emission) |
| $\Gamma$ | 2.37 | Mean photon spectral index |
| $(1+z)^{-(2-\Gamma)}$ | $(1+z)^{+0.37}$ | K-correction (observed-to-rest-frame energy shift) |
| $\eta(z)$ | (Layer 3) | Cosmology volume correction |
| $\rho_r/(\ln 10\,L_{151})$ | (Layer 2) | Converts $d\Phi/d\log_{10}L$ → $d\Phi/dL$ |
| $|dL_{151}/dL_\gamma|$ | (Layer 4) | Variable-change Jacobian |

**Implementation:** `astro_sources.py:_glf_mAGN()`.

---

## Layer 6: Window Function Assembly (Pinetti+ Eq. 4.3)

The per-chi astrophysical window function:

$$W_\gamma^{\rm mAGN}(z) = \frac{1}{4\pi(1+z)^2}\int_{L_{\min}}^{L_{\rm up}} \Phi_\gamma^{\rm mAGN}(L,z)\;\frac{L}{E_{\rm GeV\to erg}\,I_\alpha}\;E_{\rm rest}^{-\alpha}\;dL$$

with:
- $L_{\min}=10^{40}$ erg/s, $L_{\max}=10^{50}$ erg/s (Pinetti thesis Table 3.1)
- $L_{\rm thr}(z)=4\pi d_L^2(z)\,F_{\rm sens}$; $F_{\rm sens}=10^{-10}$ cm⁻²s⁻¹ (forecast mode) or energy-dependent (data mode)
- $L_{\rm up}=\min(L_{\max}, L_{\rm thr}(z))$ (unresolved sources only)
- Adaptive `scipy.quad` in log-$L$ space

**Implementation:** `astro_sources.py:W_gamma_astro(E_GeV, z, 'mAGN', ...)`.

---

## Layer 7: Effective Bias for Cross-Correlation

For HI × mAGN 2-halo cross-power, mAGN effective halo bias uses the Di Mauro+ 2014 Eqs. C.20-C.21 mass-luminosity relations evaluated at a characteristic luminosity $L_\gamma^{\rm char}=10^{44}$ erg/s:

$$M_\star = 10^9\,M_\odot\left(\frac{L_\gamma}{10^{48}\,\text{erg/s}}\right)^{0.36}$$

$$M_{\rm halo} = 10^{13}\,M_\odot\left(\frac{M_\star}{10^{8.8}(1+z)^{1.4}}\right)^{0.645}$$

Then $b_{\rm mAGN}(z) = b_{\rm ST}(M_{\rm halo}(z), z)$ using the Sheth-Tormen bias.

**Implementation:** `astro_sources.py:bias_astro(z, 'mAGN')`; parameters in `config.py` (MAGN_*).

---

## Complete Dependency Graph

```
W_gamma^mAGN(E_GeV, z)                              [astro_sources.py:485] W_gamma_astro
├── Phi_gamma^mAGN(L, z)                            [astro_sources.py:219] _glf_mAGN
│   ├── _L151_from_Lgamma(L_gamma)                  [astro_sources.py:172]
│   │   ├── Di Mauro Eq. C.13: L_gamma[erg/s] → nuL_nu_core[erg/s]
│   │   │   ├── DIMAURO_A = 2.0                     [config.py:154]
│   │   │   └── DIMAURO_B = 1.008                   [config.py:155]
│   │   ├── Unit: nuL_nu[erg/s] → L_core[W/Hz] at 5 GHz
│   │   ├── Lara Eq. C.14: L_core[W/Hz] → L_tot^1.4GHz[W/Hz]
│   │   │   ├── LARA_A = 4.2                        [config.py:147]
│   │   │   └── LARA_B = 0.77                       [config.py:148]
│   │   └── Inoue freq scaling: L_1.4GHz → L_151
│   │       └── RADIO_ALPHA = 0.80                  [config.py:157]
│   ├── _willott_rlf(L_151, z)                      [astro_sources.py:111]
│   │   ├── Low-power (FRI): rho_l with freeze at z_l*=0.710
│   │   └── High-power (FRII): rho_h Gaussian peak at z_h*=2.03
│   ├── _willott_volume_correction(z)               [astro_sources.py:145]
│   │   └── eta(z) = (d_C^W / d_C)^2 × (H / H_W)   [EdS H_W = H0*(1+z)^(3/2)]
│   ├── K-correction: (1+z)^{-(2-Gamma)} with Gamma=2.37
│   └── DIMAURO_K = 3.05                            [config.py:156]
├── alpha = 2.37 (photon index)                     [config.py:96]
├── L_min=1e40, L_max=1e50 erg/s                    [config.py:97-98]
├── L_thr(z) = 4*pi*d_L^2 * F_sens                  [astro_sources.py:25]
├── E_rest = E_obs*(1+z)                            [rest-frame energy]
├── I_alpha = integral E^{1-alpha} dE [0.1,100 GeV] [energy normalization]
└── (1+z)^{-2} / (4*pi)                             [cosmological dimming]

bias_mAGN(z)                                         [astro_sources.py:630]
├── L_char = 1e44 erg/s                              [characteristic luminosity]
├── M_star = 1e9 * (L/1e48)^0.36                    [Di Mauro Eq. C.21]
├── M_halo = 1e13 * (M_star / (10^8.8*(1+z)^1.4))^0.645 [Di Mauro Eq. C.20]
└── b_ST(M_halo, z)                                  [Sheth-Tormen bias]
```

---

## Literature Sources per Component

| Component | Primary Source | Supporting Sources |
|-----------|---------------|-------------------|
| RLF at 151 MHz | Willott+ (2001) Table 1 | 3CRR+6CE+7CRS combined sample (356 sources) |
| Frequency scaling 151→1400 MHz | Inoue (2011) | $\alpha_r=0.80$ spectral index |
| Core-total relation | Lara+ (2004) | VLBI observations of FRI/FRII galaxies |
| Radio-core → gamma correlation | Di Mauro+ (2014) | Fermi-LAT + radio core detections |
| Full mAGN GLF assembly | Di Mauro+ (2014) Eq. C.19 | Pinetti (2022) thesis Appendix C |
| Window function formula | Pinetti+ (2020) Eq. 4.3 | Generic for all astro sources |
| Mass-luminosity for bias | Di Mauro+ (2014) Eqs. C.20-C.21 | |
| Spectral index $\alpha=2.37$ | Pinetti+ (2020) Table 3 | Averaged from Fermi-LAT mAGN |
| $k=3.05$ beaming factor | Di Mauro+ (2014) | |

---

## Physical Intuition

The mAGN window function differs fundamentally from blazar (BL Lac, FSRQ) windows:

1. **Indirect GLF**: No direct gamma-ray LF exists — it is derived from the much better-constrained 151 MHz RLF via a 3-step empirical chain. Each step introduces scatter and systematic uncertainty.

2. **Numerous but faint**: mAGN are far more abundant than blazars (they are the parent population of misaligned jets), but individually much fainter in gamma-rays. The $k=3.05$ factor captures the beaming/duty-cycle fraction that emit detectably.

3. **Broad redshift coverage**: The high-power component peaks at $z\sim2$ (Gaussian), while the low-power component has milder evolution frozen at $z=0.71$. This gives mAGN a broad window function extending to higher redshifts than BL Lacs.

4. **K-correction**: $(1+z)^{-(2-\Gamma)} = (1+z)^{+0.37}$ mildly boosts high-$z$ contributions (softer spectra benefit from energy shift).

5. **Contribution to UGRB**: 10–63% of the isotropic gamma-ray background (Di Mauro+ 2014), making mAGN potentially the dominant or sub-dominant UGRB source class.
