# Pipeline Conventions

Definitive reference for unit systems, frame conventions, and notation used throughout the pipeline. When in doubt, this document takes precedence over individual literature reviews (which describe what papers say, not necessarily what the pipeline does).

---

## 1. Unit System

### Internal (cosmological) units

All internal calculations use **h-dependent comoving units**:

| Quantity | Unit | Example |
|----------|------|---------|
| Distances | Mpc/h (comoving) | χ(z), R_vir |
| Masses | M_sun/h | M, M_HI |
| Wavenumbers | h/Mpc | k |
| Densities | M_sun/h / (Mpc/h)³ | ρ_crit, ρ̄, ρ_HI |
| Power spectra | (Mpc/h)³ | P_lin(k, z), P_HI |
| Mass function | (Mpc/h)⁻³ (M_sun/h)⁻¹ | dn/dM |

**Key identity:** [h⁴ Mpc⁻³ M_sun⁻¹] ≡ [(Mpc/h)⁻³ (M_sun/h)⁻¹], since (Mpc/h)⁻³ = h³ Mpc⁻³ and (M_sun/h)⁻¹ = h M_sun⁻¹.

### External (physical) units

Physical units appear only at module boundaries:

| Quantity | Unit | Where |
|----------|------|-------|
| Hubble rate H(z) | km/s/Mpc | `cosmology.H(z)` |
| Luminosities | erg/s | `astro_sources.py` GLFs, L_sens |
| Fermi-LAT noise N^γ | cm⁻⁴ s⁻² sr⁻¹ | `config.FERMI_N_GAMMA` |
| System temperature | K | `noise_model.T_sys` |
| Radio noise | mK² sr | `noise_model.noise_dish` |
| Brightness temperature | mK | `hi_model.T_bar_b` |
| Beam functions | dimensionless | B_ℓ |
| Survey areas | deg² | `config.RADIO_TELESCOPES` |
| PSF angles | degrees (stored), radians (computed) | `config.FERMI_SIGMA0`, `noise_model.sigma_psf_fermi` |
| Circular velocity | km/s | `halo_model.v_circ` |

### Conversion at boundaries

When h-dependent and physical units meet, explicit conversion is required:

```
d_L [physical Mpc] = d_L [Mpc/h] / h          (cosmology.d_L → astro_sources.L_sens)
dχ/dz [Mpc/h]     = (c/H) × h                 (angular_power.py Limber integral)
M [M_sun]          = M [M_sun/h] × h           (halo_model.concentration_correa)
R [Mpc]            = R [Mpc/h] / h              (halo_model.v_circ)
N^γ [(Mpc/h)⁻⁴]   = N^γ [cm⁻⁴] × (Mpc_h_cm)⁴ (statistics.variance_Cl)
```

### Known h-factor mixing

The astrophysical window function `W_gamma_astro` returns values in **physical Mpc⁻³** (because the GLFs from the literature are in physical Mpc⁻³), while `W_HI` is in **h-dependent (Mpc/h)⁻¹** units. These h factors cancel in the SNR ratio C_ℓ/σ(C_ℓ) but affect the absolute C_ℓ normalization. For data analysis against measured angular power spectra, this needs to be resolved by converting W_astro to (Mpc/h)⁻³.

---

## 2. Frame Conventions

### Energy: observed vs rest-frame

| Quantity | Frame | Rationale |
|----------|-------|-----------|
| `E_GeV` argument to window functions | **Observed** | Detector sees photons at observed energy |
| `E_rest = E_GeV * (1+z)` inside `W_gamma_astro` | **Rest-frame** | Source spectrum evaluated at emission energy |
| `E_emit = E_GeV * (1+z)` inside `W_gamma_DM` | **Rest-frame** | PPPC4DMID dN/dE evaluated at emission energy |
| `ebl.tau(E, z)` / `ebl.attenuation(E, z)` | **Observed** | `ebltable` convention: E is the photon energy at Earth |
| `sigma_psf_fermi(E)`, `beam_fermi(ell, E)` | **Observed** | PSF depends on observed photon energy |
| `F_sens_energy(E)` | **Observed** | Detection threshold depends on observed energy |
| `L_sens(z, E_GeV)` | **Observed** (for E) | F_sens evaluated at observed energy; d_L converts flux→luminosity |

### Distance: comoving vs proper

All distances are **comoving**. Proper quantities appear only where physics requires them:

| Quantity | Convention |
|----------|------------|
| χ(z), d_L(z) | Comoving [Mpc/h] |
| R_vir(M, z) | [Mpc/h], defined via Δ_vir(z) × ρ_crit(z), Bryan & Norman (1998) |
| v_circ(M, z) | Physical [km/s], explicitly converts M and R to physical units |
| (1+z)³ in W_DM | Proper density evolution: ρ_DM,proper = ρ_DM,comoving × (1+z)³ |

### Density: comoving vs proper

All densities are **comoving** unless explicitly noted:

| Quantity | Convention |
|----------|------------|
| ρ̄_m, ρ_crit | Comoving (z=0 values) |
| ρ_HI_mean(z) | Comoving (integrated from dn/dM × M_HI) |
| dn/dM | Comoving number density per unit mass |
| NFW ρ(r) | Comoving profile (r is comoving) |
| Clumping Δ²(z) | Ratio of comoving ∫ρ²d³x to ρ̄² — dimensionless |

---

## 3. Window Function Conventions

### Per-χ vs per-z

The pipeline uses the **per-χ (per comoving distance)** convention for all window functions. The Limber integral is:

$$C_\ell = \int \frac{d\chi}{\chi^2} \, W_i(\chi) \, W_j(\chi) \, P\!\left(k = \frac{\ell+\tfrac{1}{2}}{\chi},\, z\right)$$

where $d\chi = (c \cdot h / H) \, dz$ in [Mpc/h].

This differs from papers that define window functions per unit redshift (per-z). The relationship is:

$$W^{(\chi)}(\chi) = W^{(z)}(z) \times \frac{H(z)}{c \cdot h}$$

| Window | Pipeline (per-χ) | Paper (per-z, Pinetti) |
|--------|-----------------|----------------------|
| W_HI | T̄_b × b_HI × φ(z) × H/(c·h) | T̄_b × φ(z) (Eqs. 3.15–3.16; bias enters via P_cross) |
| W_γ^DM | includes 1/H factor from per-χ absorption | (σv/8π)(ρ/m_χ)²(1+z)³Δ² dN/dE e^{-τ} (Eq. 4.1; no 1/H) |
| W_γ^astro | val / (4π(1+z)²) | same (Eq. 4.3) |

**Important:** The per-z forms in the Pinetti paper do NOT include 1/H(z). The pipeline's per-χ forms absorb the H/(c·h) Jacobian from dχ/dz into the window functions for W_HI and absorb 1/H into W_DM. The astrophysical window W_astro does NOT absorb this factor (it remains in the Limber weight).

### Limber k-substitution

The pipeline uses $k = (\ell + \tfrac{1}{2}) / \chi$ (LoVerde & Afshordi 2008), which improves accuracy at low ℓ compared to the standard $k = \ell/\chi$ used in the papers.

---

## 4. Halo Model Conventions

### Peak height ν

The pipeline defines $\nu = \delta_c^2 / \sigma^2(M, z)$, which is $\nu_\text{paper}^2$ relative to the Sheth & Tormen papers where $\nu = \delta_{sc} / \sigma$.

### SMT mass function parameters

| Pipeline symbol | Paper symbol (SMT2001) | Value | Role |
|---|---|---|---|
| `SMT_Q` (= q) | a | 0.707 | Ellipsoidal collapse scale |
| `SMT_P` (= p) | q | 0.3 | Low-mass slope exponent |
| `SMT_A` | ~A (absorbs factor of 2) | 0.3222 | Normalization (paper writes 2A in formula) |

### Virial overdensity

$\Delta_\text{vir}(z)$ from Bryan & Norman (1998): $\Delta_c = 18\pi^2 + 82x - 39x^2$ where $x = \Omega_M(z) - 1$, relative to the critical density. At $z=0$ with Planck 2018 cosmology, $\Delta_c \approx 103$ (equivalently $\sim327$ relative to mean matter density). Implemented in `halo_model.Delta_vir(z)`.

### Concentration

Correa et al. (2015) Appendix B1 fitting functions for $c_{200}$, calibrated for Planck 2013 cosmology (Ω_m=0.317, h=0.67). Converted to $c_\text{vir}$ via `halo_model.c200_to_cvir()` using the Bryan & Norman $\Delta_\text{vir}(z)$. The Pinetti thesis uses different Correa coefficients from a different cosmology fit. See `pinetti2022_evidence_matrix.md` D2.

---

## 5. GLF Evolution Conventions

### LDDE inverse-sum form

Both FSRQ and BL Lac use the smooth inverse-sum evolution (Pinetti 2022 Eq. C.4):

$$e(z, L) = \left[r^{-p_1} + r^{-p_2}\right]^{-1}, \quad r = \frac{1+z}{1+z_c(L)}$$

**Exponent sign convention:** The pipeline follows Pinetti (2022) with **negative exponents** ($r^{-p_1}$). The original papers (Ajello+ 2012 Eq. 15, Ajello+ 2014 Eq. 18) use **positive exponents** ($r^{p_1}$). These produce different evolution shapes around the redshift peak $z_c$. See `pinetti2022_evidence_matrix.md` D12.

### Willott cosmology correction

The Willott (2001) RLF parameters are for **H₀=50, Ω_M=0** (Model C, Table 1). A volume correction factor η(z) converts densities to Planck 2018 cosmology:

$$\eta(z) = \left(\frac{d_C^\text{Willott}}{d_C^\text{Planck}}\right)^2 \frac{H^\text{Planck}}{H^\text{Willott}}$$

---

## 6. Instrument Conventions

### Fermi-LAT

Two modes are available:

| Parameter | Forecast (Pinetti 2020) | Data analysis (Ammazzalorso 2018) |
|---|---|---|
| Energy bins | 12 bins, 0.5–1000 GeV | 11 bins, 0.631–1000 GeV |
| Beam | Gaussian approximation `beam_fermi()` | Exact King PSF `beam_fermi_exact()` |
| Sensitivity | F_sens = 10⁻¹⁰ cm⁻²s⁻¹ (constant) | F_sens(E) scaled by PSF area |
| ℓ range | No cuts | ℓ_min = 40, ℓ_max from W_ℓ = 0.61 |
| Pixel window | Not applied | `pixel_window(ℓ, N_side)` |

### MeerKAT

| Parameter | Current (forecast) | Planned (data analysis, Cunnington 2023) |
|---|---|---|
| Beam coefficient | 1.22 (diffraction limit) | 1.16 (MeerKAT illumination) |
| Band selection | Top-hat φ(z) = 1/Δz | Frequency-dependent with RFI gaps |
| Foreground signal loss | Not modeled | Transfer function T(k) |
| Noise | Single z_mid evaluation | Per-channel T_sys(ν) |

### Brightness temperature coefficient

$$\bar{T}_b(z) = 188\,h\,\Omega_\text{HI}(z)\,\frac{(1+z)^2}{E(z)} \text{ mK}$$

The coefficient 188 is from standard 21-cm references. The Pinetti paper's Eq. 3.4 gives an equivalent formulation with coefficient ~180 mK (a ~4% difference from rounding conventions, within systematic uncertainty on Ω_HI). The Cunnington et al. (2023) data analysis uses 180. See `pinetti2020.md` for details.

---

## 7. Deliberate Deviations from Literature

The pipeline makes several deliberate choices that differ from the primary reference (Pinetti 2022 thesis). These are fully documented in `pinetti2022_evidence_matrix.md`:

| # | Deviation | Nature |
|---|-----------|--------|
| D2 | Correa concentration coefficients | Different Planck cosmology fit |
| ~~D3~~ | ~~No c₂₀₀→c_vir conversion~~ | **Resolved:** `c200_to_cvir()` now converts to virial definition |
| D4 | SF-AGN k_R2 sign | Thesis typo corrected |
| D5 | Ω_HI computed, not fixed | More physical approach |
| D6 | SMT q = 0.707, not 0.75 | Both used in literature |
| D7 | PPPC4DMID public tables | vs thesis private Pythia code |
| D8 | Limber k = (ℓ+1/2)/χ | Improved low-ℓ accuracy |
| D9 | T̄_b coefficient 188h vs 44 μK form | Equivalent, rounding difference |
| ~~D11~~ | ~~Δ_vir = 200 fixed~~ | **Resolved:** Bryan & Norman z-dependent Δ_vir(z) now implemented |
| D12 | BL Lac LDDE exponent signs | Follow Pinetti, not original paper |

---

## 8. Cross-Reference

| Convention topic | Authoritative file |
|---|---|
| Physical constants, parameters | `config.py` header + body |
| Equation-by-equation reference | `equations.md` |
| Module data flow | `architecture.md` |
| Paper-by-paper claims | `literature/*.md` |
| Literature vs pipeline comparison | `literature_evidence_matrix.md` |
| Thesis vs pipeline comparison | `pinetti2022_evidence_matrix.md` |
| Pipeline conventions (this file) | `conventions.md` |
