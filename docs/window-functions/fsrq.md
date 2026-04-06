# FSRQ Window Function: Complete Pipeline

## Target Quantity

The Flat-Spectrum Radio Quasar (FSRQ) window function shares the generic astrophysical gamma-ray source form (Pinetti+ 2020, Eq. 4.3):

$$W_\gamma^{\rm FSRQ}(\chi) = \frac{1}{4\pi}\int_{L_{\min}}^{L_{\rm up}}\Phi_\gamma^{\rm FSRQ}(L,z)\;\frac{L}{E_{\rm GeV\to erg}\,I_\alpha}\;E_{\rm rest}^{-\alpha}\;dL$$

with $\alpha=2.44$ (Pinetti+ 2020 Table 3 FSRQ photon index — the softest blazar spectrum, reflecting external Compton scattering off broad-line-region photons), $E_{\rm rest}=(1+z)E_{\rm obs}$, $I_\alpha=\int_{0.1}^{100}E^{1-\alpha}\,dE$, and $L_{\rm up}=\min(L_{\max}, L_{\rm thr}(z))$ with Fermi-LAT sensitivity threshold $L_{\rm thr}(z)=4\pi d_L^2(z)\,F_{\rm sens}$.

Unlike SFGs (derived via IR→gamma calorimetric scaling) or mAGN (derived via radio→gamma conversion chain), FSRQs have a **direct Fermi-LAT gamma-ray luminosity function** fit by Ajello+ (2012) to 186 first-year catalog sources using the LDDE (Luminosity-Dependent Density Evolution) formalism.

---

## Layer 1: Cosmological Backbone

Standard Planck 2018 — same as HI, mAGN, SFG.

**Implementation:** `cosmology.py`.

---

## Layer 2: LDDE Double Power-Law Luminosity Dependence

Foundation: Ajello+ (2012) maximum-likelihood fit to 186 FSRQ sources from the first-year Fermi-LAT catalog (flux-limited sample $F_{100}\ge 10^{-8}$ ph/cm²/s, all spectroscopically confirmed). The intrinsic shape is a **double power-law** in log-space:

$$\frac{d\Phi}{d\log_{10}L} = \frac{A}{(L/L_c)^{\gamma_1} + (L/L_c)^{\gamma_2}}$$

This smoothly interpolates between a faint-end slope $\gamma_1$ and a bright-end slope $\gamma_2$ around the break luminosity $L_c$. Converted to $d\Phi/dL$ via division by $L\ln 10$.

| Parameter | Value | Role |
|-----------|-------|------|
| $A$ | $3.06\times 10^{-9}$ Mpc⁻³ | $d\Phi/d\log_{10}L$ normalization |
| $L_c$ | $0.84\times 10^{48}$ erg/s | Break luminosity |
| $\gamma_1$ | $0.21$ | Faint-end slope (very shallow) |
| $\gamma_2$ | $1.58$ | Bright-end slope |

**Implementation:** `astro_sources._FSRQ_PARAMS` and `astro_sources._ldde_glf()`.

---

## Layer 3: Luminosity-Dependent Peak Redshift (the "LD" in LDDE)

The defining feature of LDDE: more luminous sources peak at earlier cosmic times (downsizing — reflecting accretion-rate-dependent feedback). The peak redshift $z_c$ depends on luminosity as:

$$z_c(L) = z_c^\star \left(\frac{L}{L_{\rm ref}}\right)^{\alpha_{\rm LDDE}}$$

with $L_{\rm ref}=10^{48}$ erg/s (Ajello convention).

| Parameter | Value | Meaning |
|-----------|-------|---------|
| $z_c^\star$ | $1.47$ | Peak redshift at $L=L_{\rm ref}$ |
| $\alpha_{\rm LDDE}$ | $0.21$ | Luminosity dependence exponent |

Numerically: for $L=10^{46}$ erg/s (faint FSRQ), $z_c \approx 0.56$; for $L=10^{50}$ erg/s (bright), $z_c\approx 3.88$. The pipeline floors $z_c$ at 0.01 to avoid divergences.

**Implementation:** `_ldde_glf()` evaluates `z_c = z_c_star * (L/L_ref)**alpha`.

---

## Layer 4: Smooth Inverse-Sum Redshift Evolution

The FSRQ density evolution $e(z,L)$ is continuous around the peak. The active implementation follows [Ajello+ (2012)](../literature/ajello2012.md) Eq. 15:

$$e(z,L) = \left[\left(\frac{1+z}{1+z_c(L)}\right)^{p_1} + \left(\frac{1+z}{1+z_c(L)}\right)^{p_2}\right]^{-1}$$

with $r=(1+z)/(1+z_c(L))$.

**Implementation remark:** [Pinetti (2022)](../literature/pinetti2022.md) Eq. C.4 writes the same inverse-sum structure with negative exponents, $[r^{-p_1}+r^{-p_2}]^{-1}$. The repository intentionally keeps the Ajello sign convention because the published FSRQ fit parameters $(p_1,p_2)$ were calibrated in that convention.

| Parameter | Value | Role |
|-----------|-------|------|
| $p_1$ | $+7.35$ | Low-z evolution exponent |
| $p_2$ | $-6.51$ | High-z evolution exponent |

The GLF is then $\Phi(L,z) = (d\Phi/dL)_{z=0} \times e(z,L)$, peaking at $z=z_c(L)$ where $r=1$ and $e=1/2$.

**Implementation:** `_glf_FSRQ()` dispatches to `_ldde_glf(..., evolution_form='ldde_inv')`, and the current `ldde_inv` branch evaluates:
```python
e_z = 1.0 / (ratio**(p1) + ratio**(p2))
```

---

## Layer 5: FSRQ Gamma-Ray Luminosity Function Assembly

Combining the double-power-law intrinsic shape with the LDDE evolution:

$$\boxed{\Phi_\gamma^{\rm FSRQ}(L,z) = \frac{1}{L\ln 10}\cdot\frac{A}{(L/L_c)^{\gamma_1}+(L/L_c)^{\gamma_2}}\cdot\frac{1}{r^{p_1}+r^{p_2}}}$$

with $r = (1+z)/(1+z_c^\star (L/10^{48})^{0.21})$. Units: $d\Phi/dL$ in Mpc⁻³ (erg/s)⁻¹.

**Implementation:** `astro_sources._glf_FSRQ()` dispatches to `astro_sources._ldde_glf()` with `evolution_form='ldde_inv'`.

---

## Layer 6: Window Function Assembly (Pinetti+ Eq. 4.3)

Same generic astrophysical window formula:

$$W_\gamma^{\rm FSRQ}(z) = \frac{1}{4\pi h^3}\int_{L_{\min}}^{L_{\rm up}} \Phi_\gamma^{\rm FSRQ}(L,z)\;\frac{L}{E_{\rm GeV\to erg}\,I_\alpha}\;E_{\rm rest}^{-\alpha}\;dL$$

with:
- $L_{\min}=10^{44}$ erg/s, $L_{\max}=10^{52}$ erg/s (Pinetti thesis Table 3.1 — note the high $L_{\max}$ reflects FSRQs being among the most luminous gamma-ray sources)
- $\alpha=2.44$ (soft blazar spectrum due to EC cooling)
- $I_\alpha = \int_{0.1}^{100} E^{1-\alpha}\,dE$ (energy normalization, 0.1-100 GeV band)
- $L_{\rm thr}(z) = 4\pi d_L^2\,F_{\rm sens}$; $F_{\rm sens}=10^{-10}$ cm⁻²s⁻¹ (forecast mode) or energy-dependent (data mode)
- $L_{\rm up} = \min(L_{\max}, L_{\rm thr}(z))$ — unresolved sources only (resolved FSRQs excluded)

The current implementation uses the photon-number emissivity form, so the explicit redshift dependence enters through $E_{\rm rest}=(1+z)E_{\rm obs}$ and the luminosity-function factors rather than an additional $(1+z)^{-2}$ prefactor. After the emissivity integral is evaluated in physical Mpc$^{-3}$ units, the code converts it to the pipeline's h-dependent convention by returning `val / (4\pi h^3)`. Integration uses `scipy.quad` in log-$L$ with `epsrel=1e-5`.

**Implementation:** `astro_sources.W_gamma_astro(E_GeV, z, 'FSRQ', ...)`.

---

## Layer 7: Effective Bias for Cross-Correlation

For HI × FSRQ 2-halo cross-power, the FSRQ effective halo bias uses the **blazar convention**: a fixed characteristic halo mass:

$$b_{\rm FSRQ}(z) = b_{\rm ST}(M_{\rm halo}=10^{13}\,M_\odot/h,\, z)$$

This is motivated by the observation that blazars live in massive elliptical hosts ($M_\star\sim 10^{11}-10^{12}\,M_\odot$) residing in group-scale halos. Unlike mAGN/SFG (where $M_{\rm halo}(L)$ is derived via stellar mass or direct scaling), FSRQ bias ignores the luminosity dependence — a deliberate simplification standard in the UGRB literature.

**Implementation:** `astro_sources.bias_astro(z, 'FSRQ')` returns `hm.bias(1e13, z)`.

---

## Complete Dependency Graph

```text
W_gamma^FSRQ(E_GeV, z)                              [astro_sources.W_gamma_astro]
├── Phi_gamma^FSRQ(L, z)                            [astro_sources._glf_FSRQ]
│   └── _ldde_glf(L, z, _FSRQ_PARAMS, 'ldde_inv')
│       ├── d(Phi)/d(log L) = A / [(L/L_c)^g1 + (L/L_c)^g2]
│       ├── d(Phi)/dL = d(Phi)/d(logL) / (L * ln10)
│       ├── z_c(L) = z_c* * (L/L_ref)^alpha
│       └── e(z,L) = 1 / (r^p1 + r^p2)
│           ├── r = (1+z) / (1+z_c(L))
│           ├── p1 = 7.35
│           └── p2 = -6.51
├── alpha_spectral = 2.44                           [config.ASTRO_SOURCES['FSRQ']['alpha']]
├── L_min = 1e44 erg/s                              [config.ASTRO_SOURCES['FSRQ']['L_min']]
├── L_max = 1e52 erg/s                              [config.ASTRO_SOURCES['FSRQ']['L_max']]
├── L_thr(z) = 4*pi*d_L^2 * F_sens                  [astro_sources.L_sens]
├── E_rest = E_obs * (1+z)                          [rest-frame energy]
├── I_alpha = integral E^{1-alpha} dE [0.1,100 GeV]
└── 1 / (4*pi*h^3)                                  [photon-emissivity prefactor after d_L^2 cancellation and Mpc^-3 -> (Mpc/h)^-3 conversion]

bias_FSRQ(z)                                        [astro_sources.bias_astro]
└── b_ST(M_halo = 1e13 M_sun/h, z)                  [fixed blazar halo mass]
```

---

## Literature Sources per Component

| Component | Primary Source | Supporting Sources |
|-----------|---------------|-------------------|
| FSRQ GLF form (LDDE double power-law) | Ajello+ (2012) ApJ 751, 108 | 186 first-year Fermi-LAT sources, ML fitting |
| All 8 LDDE parameters | Ajello+ (2012) Table 3 | Sub-percent agreement with subsequent catalogs |
| LDDE inverse-sum evolution form | Ajello+ (2012) Eq. 15 (positive exps; pipeline uses this) | Pinetti (2022) Eq. C.4 writes the inverse-sum with negative exponents; the active implementation intentionally keeps the Ajello convention |
| Window function formula | Pinetti+ (2020) Eq. 4.3 | Generic astro window |
| Spectral index $\alpha=2.44$ | Pinetti+ (2020) Table 3 | Ajello+ (2012) $\mu=2.44\pm 0.01$ |
| Blazar halo mass $M=10^{13}\,M_\odot/h$ | Pinetti+ (2020); standard convention | |
| Fermi sensitivity $F_{\rm sens}$ | Pinetti+ (2020) | |

**Updated reference (not yet adopted):** Rajguru+ (2025, arXiv:2510.05515) provides an updated FSRQ GLF using 519 sources from the 4LAC catalog. The LDDE form is confirmed; parameters are refined. Pipeline retains Ajello+ (2012) for consistency with Pinetti+ (2020).

---

## Physical Intuition

FSRQs are the most luminous blazars — flat-spectrum radio quasars with strong broad emission lines, indicating high-accretion-rate disks with broad-line regions. Key features:

1. **Softest blazar spectrum**: $\alpha=2.44$ > BL Lac's 2.11. FSRQs have strong external Compton cooling off broad-line-region photons, which preferentially suppresses high-energy electrons.

2. **LDDE — downsizing**: brighter FSRQs peak at higher $z$ (e.g., $z_c\sim 3.9$ for $L=10^{50}$ erg/s vs $z_c\sim 0.6$ for $L=10^{46}$ erg/s). Mirrors AGN downsizing — most luminous sources trace peak of SMBH growth at $z\sim 2-3$.

3. **Strong evolution**: $p_1=+7.35$, $p_2=-6.51$ give FSRQs a sharply peaked redshift distribution around $z_c$, unlike SFG/mAGN with broader window functions.

4. **Window function shape**: peaks at $z\sim 1-2$, narrower than mAGN/SFG. Contributes only where bright enough sources peak.

5. **Contribution to UGRB**: ~9.3% (Ajello+ 2012); subdominant to BL Lac but with distinct redshift signature enabling tomographic separation.

6. **Bias convention**: fixed $M_{\rm halo}=10^{13}\,M_\odot$ assumes FSRQs inhabit group-scale halos — identical to BL Lac bias convention.
