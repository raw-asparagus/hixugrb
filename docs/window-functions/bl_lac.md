# BL Lac Window Function: Complete Pipeline

## Target Quantity

The BL Lac window function shares the generic astrophysical gamma-ray source form (Pinetti+ 2020, Eq. 4.3):

$$W_\gamma^{\rm BL\,Lac}(\chi) = \frac{1}{4\pi h^3}\int_{L_{\min}}^{L_{\rm up}}\Phi_\gamma^{\rm BL\,Lac}(L,z)\;\frac{L}{E_{\rm GeV\to erg}\,I_\alpha}\;E_{\rm rest}^{-\alpha}\;dL$$

with $\alpha = 2.11$ (Pinetti+ 2020 Table 3 BL Lac photon index — hardest among UGRB astrophysical components, reflecting Doppler-boosted inverse-Compton emission from the relativistic jet), $E_{\rm rest}=(1+z)E_{\rm obs}$, $I_\alpha=\int_{0.1}^{100}E^{1-\alpha}\,dE$, and $L_{\rm up}=\min(L_{\max}, L_{\rm thr}(z,E))$ with Fermi-LAT sensitivity threshold $L_{\rm thr}(z,E)=4\pi d_L^2(z)\,F_{\rm sens}(E)$.

Unlike SFGs (derived from IR LF via Ackermann calorimetric scaling) or mAGN (radio LF via multi-step conversion chain), BL Lacs have a **direct gamma-ray LDDE luminosity function** fit from Fermi-LAT source-count data (Ajello et al. 2014). The LDDE form captures the luminosity-dependent redshift evolution inherent to blazar populations: faint HSPs (high-synchrotron-peaked BL Lacs) show negative evolution (density rising toward $z=0$), while luminous LISPs peak near $z\sim 1.2$.

---

## Layer 1: Cosmological Backbone

Standard Planck 2018. Same as HI, DM, mAGN, and SFG.

**Implementation:** `cosmology.py`.

---

## Layer 2: Ajello (2014) LDDE Gamma-Ray Luminosity Function

### 2a. Local double power-law LF (Ajello+ 2014 Eq. C.2)

$$\frac{d\Phi}{d\log_{10}L}\bigg|_{z=0} = \frac{A}{(L/L_c)^{\gamma_1} + (L/L_c)^{\gamma_2}}$$

Gives the local LF in $d\Phi/d\log_{10}L$ [Mpc$^{-3}$]. Converted to $d\Phi/dL$ [Mpc$^{-3}$ (erg/s)$^{-1}$] via division by $L\ln 10$.

### 2b. Luminosity-Dependent Density Evolution (LDDE inverse-sum, Ajello+ 2014 Eq. 18)

$$e(z, L) = \left[\left(\frac{1+z}{1+z_c(L)}\right)^{p_1} + \left(\frac{1+z}{1+z_c(L)}\right)^{p_2}\right]^{-1}$$

with luminosity-dependent peak redshift:

$$z_c(L) = z_\star\left(\frac{L}{10^{48}\,{\rm erg/s}}\right)^{\beta}$$

### 2c. Parameters (Ajello+ 2014 Table 3, LDDE1)

| Parameter | Value | Meaning |
|-----------|-------|---------|
| $A$ | $9.20\times10^{-11}\,{\rm Mpc}^{-3}$ | Normalization of $d\Phi/d\log_{10}L$ |
| $L_c$ | $2.43\times10^{48}$ erg/s | Break luminosity $L_\star$ |
| $\gamma_1$ | 1.12 | Faint-end slope |
| $\gamma_2$ | 3.71 | Bright-end slope |
| $p_1$ | 4.50 | Low-$z$ evolution exponent |
| $p_2$ | $-12.88$ | Steep high-$z$ decline |
| $z_\star$ | 1.67 | Peak redshift at $L = 10^{48}$ erg/s |
| $\beta$ | $4.46\times10^{-2}$ | Luminosity dependence of $z_c$ |

### 2d. Sign Convention Remark

Ajello+ (2014) Eq. 18 writes the inverse-sum with **positive exponents** $[r^{p_1} + r^{p_2}]^{-1}$, and that is what the active implementation evaluates. [Pinetti (2022)](../literature/pinetti2022_thesis.md) Eq. C.4 rewrites the same inverse-sum with **negative exponents** $[r^{-p_1} + r^{-p_2}]^{-1}$. Because the BL Lac fit parameters are taken from Ajello+ (2014) Table 3, the repository intentionally keeps the Ajello sign convention rather than the thesis sign flip.

**Implementation:** `astro_sources._glf_BL_Lac()` calls `astro_sources._ldde_glf(..., evolution_form='ldde_inv')`, and the current `ldde_inv` branch evaluates `1.0 / (ratio**p1 + ratio**p2)`.

---

## Layer 3: Photon Spectral Energy Distribution

Each BL Lac is modeled as a **power-law source** over the 0.1-100 GeV band:

$$\frac{dN}{dE_{\rm rest}}(E_{\rm rest}, L) = \frac{L}{{\rm GeV}_{\rm erg}\;I_\alpha}\;E_{\rm rest}^{-\alpha}\quad[{\rm ph\,s^{-1}\,GeV^{-1}}]$$

where:
- $\alpha = 2.11$ is the photon spectral index (Pinetti+ 2020 Table 3; the Ajello+ 2014 LDDE1 fit gives $\mu_\star = 2.12 \pm 0.03$)
- ${\rm GeV}_{\rm erg} = 1.602\times10^{-3}$ erg/GeV
- $I_\alpha = \int_{0.1\,{\rm GeV}}^{100\,{\rm GeV}} E^{1-\alpha}\,dE$ is the spectral normalization integral
- $L$ [erg/s] is the rest-frame 0.1-100 GeV energy luminosity

This is a **single fixed index for the entire population** (no scatter in $\alpha$, no luminosity-dependence, no log-parabola curvature, no exponential cutoff). Real BL Lac SEDs show synchrotron + inverse-Compton double-hump structure with HSP/ISP/LSP peaks varying by population, but the population-averaged GLF-weighted SED is adequately described by a single power law within Fermi's 0.1-100 GeV band.

**Implementation:** embedded in `astro_sources.W_gamma_astro()`.

---

## Layer 4: Fermi-LAT Flux Sensitivity Threshold

The luminosity corresponding to the Fermi-LAT detection threshold at redshift $z$:

$$L_{\rm thr}(z, E) = 4\pi\,d_L^2(z)\;F_{\rm sens}(E)$$

where $d_L$ is the physical luminosity distance (code converts internal Mpc/h $\to$ physical Mpc via $\div h$, then Mpc $\to$ cm).

### Two operating modes

| Mode | $F_{\rm sens}(E)$ | Physics | Use case |
|------|-------------------|---------|----------|
| `forecast` | $10^{-10}\,{\rm cm}^{-2}\,{\rm s}^{-1}$ constant | Survey-independent | Pinetti 2020 SNR forecasts |
| `data` | $\propto [\sigma_0(E)/\sigma_0(E_{\rm ref})]^2$ | PSF-area-scaled | Ammazzalorso+ 2018 analysis |

In **data mode**, worse PSF at low energies means fewer sources can be resolved → higher threshold flux → more sources remain "unresolved" and contribute to the diffuse window. Reference energy $E_{\rm ref} = 5$ GeV near Fermi's optimal sensitivity.

**Implementation:** `astro_sources.L_sens()`, `astro_sources.F_sens_energy()`, and `config.F_SENS`.

---

## Layer 5: Window Function Assembly (Pinetti+ Eq. 4.3)

Putting Layers 2-4 together:

$$\boxed{W_\gamma^{\rm BL\,Lac}(E_\gamma, z) = \frac{1}{4\pi h^3}\int_{L_{\min}}^{L_{\rm up}}\Phi_\gamma^{\rm BL\,Lac}(L, z)\;\frac{L\,[(1+z)E_\gamma]^{-\alpha}}{{\rm GeV}_{\rm erg}\,I_\alpha}\;dL}$$

with:
- $L_{\min} = 7\times 10^{43}$ erg/s, $L_{\max} = 10^{52}$ erg/s (Pinetti+ 2020 Table 3)
- $L_{\rm up} = \min(L_{\max},\,L_{\rm thr}(z,E))$
- $\alpha = 2.11$
- $I_\alpha = \int_{0.1}^{100}E^{1-\alpha}\,dE$ (energy normalization, 0.1-100 GeV band)

**Derivation of the $d_L^2$ cancellation:** in the current implementation, the per-source photon spectrum is evaluated as a rest-frame photon-emission rate at $E_{\rm rest}=(1+z)E_{\rm obs}$. After the $d_L^2$ cancellation, the repository keeps the photon-number emissivity form and then converts the physical GLF density to the pipeline's h-dependent convention, yielding the overall $1/(4\pi h^3)$ prefactor.

**Integration:** `scipy.quad` in $\log L$, `epsrel=1e-5`, `limit=200`. Returns units of $[(\mathrm{Mpc}/h)^{-3}\,{\rm ph}\,{\rm s}^{-1}\,{\rm GeV}^{-1}\,{\rm sr}^{-1}]$ after the final `h^{-3}` conversion.

**Implementation:** `astro_sources.W_gamma_astro(E_GeV, z, 'BL_Lac', ...)`.

---

## Layer 6: Effective Halo Bias

For the HI $\times$ BL Lac 2-halo cross-power, the BL Lac effective bias uses a **fixed halo mass** assumption:

$$b_{\rm BL\,Lac}(z) = b_{\rm ST}(M_{\rm halo} = 10^{13}\,M_\odot/h,\, z)$$

via the standard Sheth-Tormen bias formula. This is a **simplification**: blazars are expected to live in massive AGN host halos ($\sim 10^{13}$-$10^{14}\,M_\odot$), but the pipeline does not use an explicit $M_{\rm halo}(L,z)$ mass-luminosity relation (as it does for mAGN and SFG). The fixed value $10^{13}\,M_\odot/h$ is standard in the literature for blazar clustering.

**Limitation:** No luminosity dependence, no redshift-scaling of the host mass, no scatter. Impact is $\sim 10$--$20\%$ on the clustering amplitude of the cross-correlation. Pinetti (2022) thesis uses the same approximation.

**Implementation:** `astro_sources.bias_astro(z, 'BL_Lac')` returns `hm.bias(1e13, z)`.

---

## Complete Dependency Graph

```text
W_gamma^BL_Lac(E_GeV, z)                             [astro_sources.W_gamma_astro]
├── Phi_gamma^BL_Lac(L, z)                           [astro_sources._glf_BL_Lac]
│   └── _ldde_glf(L, z, _BL_LAC_PARAMS, 'ldde_inv')
│       ├── Local: A / [(L/L_c)^g1 + (L/L_c)^g2] / (L ln10)
│       └── Evolution: e(z,L) = [r^p1 + r^p2]^{-1}
│           ├── r = (1+z)/(1+z_c)
│           ├── z_c = z_star * (L/L_ref)^beta
│           ├── z_star = 1.67, beta = 4.46e-2
│           ├── p1 = 4.50, p2 = -12.88
│           └── L_ref = 1e48 erg/s
├── alpha = 2.11                                     [config.ASTRO_SOURCES['BL_Lac']['alpha']]
├── L_min = 7e43, L_max = 1e52 erg/s                [config.ASTRO_SOURCES['BL_Lac']]
├── L_thr(z,E) = 4*pi*d_L^2 * F_sens(E)             [astro_sources.L_sens]
│   ├── forecast mode: F_sens = F_SENS = 1e-10      [config.F_SENS]
│   └── data mode:     F_sens ∝ [sigma_0(E)]^2      [astro_sources.F_sens_energy]
├── E_rest = E_obs * (1+z)                           [rest-frame energy]
├── I_alpha = integral E^{1-alpha} dE [0.1,100 GeV]
└── 1 / (4*pi*h^3)                                  [photon-emissivity prefactor after d_L^2 cancellation and Mpc^-3 -> (Mpc/h)^-3 conversion]

bias_BL_Lac(z)                                       [astro_sources.bias_astro]
├── M_halo = 1e13 M_sun/h                            [fixed]
└── b_ST(1e13, z)                                    [halo_model.bias]
```

---

## Literature Sources per Component

| Component | Primary Source | Supporting Sources |
|-----------|---------------|-------------------|
| BL Lac GLF structure | Ajello+ (2014) ApJ 780, 73 | LAT 2FGL sample, LDDE fit |
| LDDE functional form | Ajello+ (2014) Eq. 18 | Pinetti (2022) thesis Eq. C.4 writes the inverse-sum with opposite exponent signs |
| Parameter values | Ajello+ (2014) Table 3 (LDDE1) | Pinetti thesis Table C.1 reproduces the same LDDE1 values |
| Sign convention remark | Active pipeline follows Ajello+ positive exponents | Thesis Eq. C.4 uses negative exponents; the repository intentionally does not adopt that sign flip |
| Photon index $\alpha = 2.11$ | Pinetti+ (2020) Table 3 | Ajello+ 2014 LDDE1 $\mu_\star = 2.12 \pm 0.03$ |
| Window function formula | Pinetti+ (2020) Eq. 4.3 | Generic astro window |
| Halo mass assumption | Standard blazar clustering | Pinetti (2022) thesis; no explicit M-L relation |
| $L_{\min}, L_{\max}$ | Pinetti+ (2020) Table 3 | Pinetti thesis Table 3.1 |
| Energy-dependent sensitivity | Ammazzalorso+ (2018) Eq. 1 | Fermi-LAT PSF $\theta_{68}(E)$ |

---

## Physical Intuition

The BL Lac window function has distinctive features relative to other UGRB components:

1. **Hardest spectrum among astrophysical sources** ($\alpha = 2.11$ vs. 2.37 for mAGN, 2.44 for FSRQ, 2.7 for SFG): reflects Doppler-boosted inverse-Compton emission in the jet, peaking at high energies. BL Lacs dominate the UGRB at $E > 10$ GeV.

2. **Luminosity-dependent redshift peak**: fainter populations (HSPs) peak at $z \sim 0$, brighter populations (LISPs) at $z \sim 1.2$. The $z_c(L) = z_\star(L/10^{48})^{\beta}$ parameterization captures this with small $\beta = 0.045$ (weak dependence, consistent with all BL Lacs peaking in a similar range).

3. **Steep high-$z$ decline** ($p_2 = -12.88$): the population density drops rapidly above $z_c$, reflecting the finite duty cycle of AGN activity and the declining cosmic supermassive black hole accretion rate at $z > 2$.

4. **Broad luminosity range** ($L_{\min} = 7\times10^{43}$ to $L_{\max} = 10^{52}$ erg/s): spans 8 decades, with the population integral dominated by sources near $L_c \sim 10^{48}$ erg/s.

5. **No EBL attenuation applied** (simplification): unlike $W_\gamma^{\rm DM}$, the astrophysical window functions do not include $e^{-\tau}$ in the pipeline. This is a deliberate simplification valid at $E \lesssim 30$ GeV where $\tau \ll 1$. For high-energy analyses ($E > 30$ GeV, $z > 0.5$), EBL absorption would further suppress the BL Lac contribution by factors up to $\sim 10$.

---

## Pipeline (Pinetti 2022) Parallel

The `pinetti2022.py` parallel module provides **no BL Lac-specific GLF or window override**. For BL Lac, the implemented source of truth is the main `astro_sources.py` path. Relative to the thesis text, the active pipeline makes one explicit blazar-specific choice: it keeps Ajello+ (2014) Eq. 18 with positive exponents rather than the sign-flipped thesis Eq. C.4. Other differences enter only through the shared halo-model infrastructure used in the 2-halo cross-power:

- **Halo bias**: Pinetti 2022 uses $q=0.75$ (thesis) via `pinetti2022.bias_pinetti()` vs pipeline's $q=0.707$. Affects the Sheth-Tormen bias evaluated at $M_{\rm halo} = 10^{13}\,M_\odot/h$.
- **Limber $k$-substitution**: Pinetti 2022 uses $k=\ell/\chi$ (thesis) vs pipeline's $k=(\ell+1/2)/\chi$.

Neither affects the BL Lac window function $W_\gamma^{\rm BL\,Lac}(z)$ itself — only its projection into $C_\ell$.
