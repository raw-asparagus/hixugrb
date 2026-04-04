# Ammazzalorso, Fornengo, Horiuchi & Regis (2018) — Fermi-LAT × 2MPZ Cross-Correlation

**Authors:** S. Ammazzalorso, N. Fornengo, S. Horiuchi, M. Regis
**Journal:** Phys. Rev. D 98, 103007 (2018)
**arXiv:** [1808.09225](https://arxiv.org/abs/1808.09225)

## Abstract

Cross-correlates 9 years of Fermi-LAT gamma-ray data (0.631–1000 GeV, Pass 8 ULTRACLEANVETO) with the 2MPZ galaxy catalog (~10⁶ galaxies, distribution peaked at z = 0.07) to characterize the local (z < 0.2) unresolved gamma-ray background. Using a halo model with halo occupation distribution (HOD), the authors decompose the signal into contributions from misaligned AGN, star-forming galaxies, blazars, and dark matter annihilation. mAGN are identified as the dominant contributor, with 95% CL DM bounds reaching near the thermal relic cross-section for m_χ ~ 10 GeV.

## Methodology

- **APS measurement:** PolSpice for angular power spectrum with mask deconvolution; 15 logarithmic multipole bins from ℓ = 10 to 1000
- **Galaxy clustering:** Halo model + HOD formalism (Eqs. B1–B6) with parameters fitted from galaxy auto-correlation
- **Source modeling:** Three astrophysical classes (BLZ = combined BL Lac + FSRQ, mAGN, SFG) plus DM annihilation; same underlying references as Pinetti+(2020)
- **Fitting:** Two approaches — "reference" (modeled shot-noise from multi-wavelength relations) and "free C_p" (shot-noise as free power-law, Eq. 9)
- **Tomographic analysis:** Galaxy catalog split by redshift, K-luminosity, and B-luminosity bins to isolate source populations

## Key Results

- Null hypothesis (no correlation) excluded at >99.99% CL
- mAGN are the dominant contributor to the cross-correlation signal at z < 0.2
- SFG are subdominant; upper bounds ~2–3× the reference model
- Blazar contribution is highly sensitive to shot-noise modeling
- 95% CL DM bounds for b̄b channel: σv ≲ ⟨σv⟩_th for m_χ ~ 10 GeV, rising linearly with mass
- Tomographic approach increases significance of mAGN detection
- Weak DM hint in 2MRS High-K/Low-B subsample (σv ~ 4⟨σv⟩_th at m_χ = 37 GeV)

## Fermi-LAT Data Specifications

These specifications define the data-analysis-grade treatment for an actual cross-correlation measurement (as opposed to the forecasting approach in Pinetti+(2020)).

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Data period | 108 months (Aug 2008 – Jul 2017) | Sec. II.A |
| Event class | Pass 8 ULTRACLEANVETO (P8R2_ULTRACLEANVETO_V6) | Sec. II.A |
| PSF selection | PSF3 (type 32) below 1.2 GeV; PSF1+2+3 (type 56) above | Sec. II.A |
| Pixelization | HEALPix N_side = 1024 (~0.06° spacing) | Sec. II.A |
| Energy bins | 11 bins, 0.631–1000 GeV (Table I) | Sec. II.A, Table I |
| Galactic cut | $\lvert b \rvert \lt 30^\circ$ | Sec. II.A.1 |
| Point source mask | FL8Y + 3FHL (>10 GeV), energy-dependent radius (Eq. 1) | Sec. II.A.1 |
| Foreground model | gll_iem_v06.fits, Poisson likelihood normalization | Sec. II.A.1 |
| Multipole range | ℓ_min = 40, ℓ_max from W_ℓ = 0.61 condition (Table I) | Sec. III, Eq. 7 |

**Energy Bins and Multipole Range (Table I):**

| Bin | E_min [GeV] | E_max [GeV] | ℓ_min | ℓ_max |
|-----|-------------|-------------|-------|-------|
| 1 | 0.631 | 1.202 | 40 | 220 |
| 2 | 1.202 | 2.290 | 40 | 250 |
| 3 | 2.290 | 4.786 | 40 | 307 |
| 4 | 4.786 | 9.120 | 40 | 487 |
| 5 | 9.120 | 17.38 | 40 | 695 |
| 6 | 17.38 | 36.31 | 40 | 907 |
| 7 | 36.31 | 69.18 | 40 | 1000 |
| 8 | 69.18 | 131.8 | 40 | 1000 |
| 9 | 131.8 | 275.4 | 40 | 1000 |
| 10 | 275.4 | 524.8 | 40 | 1000 |
| 11 | 524.8 | 1000.0 | 40 | 1000 |

## Equations

### Beam window function (Eq. 4)

$$W_\ell(E) = 2\pi \int_{-1}^{1} d\cos\theta \, P_\ell(\cos\theta) \, \mathrm{PSF}(\theta, E)$$

where $P_\ell$ are Legendre polynomials and PSF($\theta$, E) is the Fermi-LAT point spread function for the specific IRF and energy.

### Energy-averaged beam per bin (Eq. 5)

$$\langle W_\ell^k \rangle = \frac{\int_{E_{\min,k}}^{E_{\max,k}} W_\ell(E) \, E^{-\alpha} \, dE}{\int_{E_{\min,k}}^{E_{\max,k}} E^{-\alpha} \, dE}, \quad \alpha = 2.3$$

### Corrected APS (Eq. 6)

$$C_\ell^k = \frac{C_{\ell,\mathrm{raw}}^k}{\langle W_\ell^k \rangle \, W_\mathrm{pix}}$$

where $W_\mathrm{pix}$ is the HEALPix pixel window function.

### Point source mask radius (Eq. 1)

$$F_{\Delta E}^\gamma \exp\left(-\frac{R^2}{2\theta_{\Delta E}^2}\right) > \frac{F_{\Delta E,\mathrm{faintest}}^\gamma}{5}$$

where $\theta_{\Delta E}$ is the 68% PSF containment angle in the energy bin. Every cataloged source is masked within a radius $R$ determined by this condition — brighter sources receive larger masks.

### Multipole upper limit (Eq. 7)

$$\langle W_{\ell_\max}^k \rangle = 0.61$$

or $\ell_\max = 1000$, whichever is smaller. Ensures beam correction does not amplify noise excessively.

### Chi-squared estimator (Eq. 8)

$$\chi^2 = \sum_{k=1}^{11} \sum_{\Delta\ell,\Delta\ell'} \left(C_{\Delta\ell}^{k,\mathrm{mod}} - C_{\Delta\ell}^{k,\mathrm{exp}}\right) \Gamma_{\Delta\ell,\Delta\ell',k}^{-1} \left(C_{\Delta\ell'}^{k,\mathrm{mod}} - C_{\Delta\ell'}^{k,\mathrm{exp}}\right)$$

### Shot-noise model (Eq. 9)

$$\frac{dC_p^{(j)}}{dE} = N_j \, E^{-\alpha_j}$$

Two free parameters (normalization and spectral index) per galaxy sample.

### Gaussian error estimate (Eq. A1)

$$\delta C_\ell = \sqrt{\frac{(C_\ell^{\gamma,\mathrm{gal}})^2 + C_\ell^{\gamma,\gamma} \, C_\ell^{\mathrm{gal,gal}}}{(2\ell+1) \, f_\mathrm{sky} \, \Delta\ell}}$$

### HOD parameterization (Eqs. B1–B2)

$$\langle N_\mathrm{cen}(M) \rangle = \frac{1}{2}\left[1 + \mathrm{erf}\left(\frac{\log M - \log M_\mathrm{cut}}{\sigma_{\log M}}\right)\right]$$

$$\langle N_\mathrm{sat}(M) \rangle = \left(\frac{M - M_\mathrm{cut}}{M_1}\right)^\alpha \quad \text{for } M > M_\mathrm{cut}$$

### Galaxy power spectra (Eqs. B5–B6)

$$P_{gg}^\mathrm{1h}(k, z) = \int \frac{dn}{dM} \frac{2\langle N_\mathrm{cen}\rangle \langle N_\mathrm{sat}\rangle \tilde{v}_\delta + \langle N_\mathrm{sat}\rangle^2 \tilde{v}_\delta^2}{\bar{n}_g^2} \, dM$$

$$P_{gg}^\mathrm{2h}(k, z) = \left[\int \frac{dn}{dM} b_h(M) \frac{\langle N_g \rangle}{\bar{n}_g} \tilde{v}_g(k|M) \, dM\right]^2 P_\mathrm{lin}(k)$$

## Pipeline Mapping

Comparison of the pipeline's current implementation against this paper:

| Pipeline Element | This Paper | Status | Action |
|---|---|---|---|
| Fermi PSF: σ₀(E) parametric Gaussian (`noise_model.py`) | Eq. 4: Legendre transform of actual PSF | **Upgrade needed** | Implement exact beam from King function PSF |
| Beam B_ℓ^γ: modified Gaussian (`noise_model.py`) | Eq. 5–6: energy-averaged W_ℓ per bin | **Upgrade needed** | Add `beam_fermi_exact()` |
| Energy bins: 12 bins, 0.5–1000 GeV (`config.py`) | Table I: 11 bins, 0.631–1000 GeV | **Upgrade needed** | Add alternate bin config |
| No ℓ-range cuts | ℓ_min = 40, ℓ_max from Eq. 7 per bin | **Missing** | Add energy-dependent ℓ cuts |
| No pixel window | Eq. 6: W_pix correction | **Missing** | Add `pixel_window(ℓ, N_side)` |
| f_sky tabulated per bin | Derived from actual mask | **Upgrade needed** | Add mask-based f_sky computation |
| F_sens = 10⁻¹⁰ cm⁻²s⁻¹ constant | FL8Y catalog masking (energy-dependent) | **Different approach** | Add energy-dependent threshold |
| Gaussian variance (Eq. 10.1) | Eq. A1 | **Consistent** | — |
| Limber C_ℓ (Eq. 9.1) | Eq. 2–3 (APS definition) | **Consistent** | — |
| Halo model (NFW, bias, concentration) | Appendix B (same framework) | **Consistent** | — |
| mAGN/SFG source models | Same references (Di Mauro+2014, Ackermann+2012) | **Consistent** | — |
| DM window W_γ^DM | Same formalism (Regis+2015) | **Consistent** | — |
| HI window W_HI, radio noise model | Not in paper (uses galaxy HOD, not 21-cm) | **N/A** | — |

## Key Differences from Pinetti+(2020)

1. **Observational vs forecasting:** This paper performs an actual measurement on data; Pinetti+(2020) produces SNR forecasts
2. **Galaxy tracer vs HI:** Cross-correlates with 2MPZ galaxy catalog (HOD formalism), not HI 21-cm intensity mapping
3. **Beam treatment:** Exact Legendre transform of Fermi-LAT PSF (Eq. 4) vs parametric Gaussian approximation
4. **Energy bins:** 11 bins starting at 0.631 GeV vs 12 bins starting at 0.5 GeV — lowest bin excluded due to poor angular resolution
5. **Multipole range:** Energy-dependent ℓ_max from beam window threshold (Eq. 7) vs no ℓ cut
6. **Masking:** Energy-dependent point source masking (Eq. 1) vs single flux threshold F_sens
7. **Pixel window:** Applied (Eq. 6) vs not applied
8. **Foreground:** Galactic template subtraction with free normalization vs not modeled

## Implementation

**Primary use:** Reference for upgrading the Fermi-LAT treatment from forecasting-grade to data-analysis-grade. Key upgrades: exact beam window function, energy-dependent multipole cuts, pixel window correction.

**Modules affected:** `noise_model.py` (beam), `config.py` (energy bins, PSF parameters), `astro_sources.py` (energy-dependent sensitivity), `statistics.py` (ℓ-range cuts)
