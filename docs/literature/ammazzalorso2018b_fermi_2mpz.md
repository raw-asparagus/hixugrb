# Ammazzalorso, Fornengo, Horiuchi & Regis (2018) — Characterizing the local gamma-ray Universe via angular cross-correlations

**Authors:** S. Ammazzalorso, N. Fornengo, S. Horiuchi, M. Regis
**Journal:** Phys. Rev. D **98**, 103007 (2018)
**arXiv:** [1808.09225](https://arxiv.org/abs/1808.09225) (v2)

## Abstract

A 9-year (108 month) Fermi-LAT cross-correlation analysis between the unresolved gamma-ray background (UGRB) and the 2MASS Photometric Redshift catalog (2MPZ), targeting the **local** ($z < 0.2$) gamma-ray Universe — the redshift range where roughly 10% of the total UGRB intensity is produced. Identifies the dominant signal as **unresolved AGN** (blazars + misaligned AGN) with a sub-dominant star-forming-galaxy contribution, and reports model-independent best-fit Poisson cross-power amplitudes $C_p^k$ in 11 energy bins from 0.631 GeV to 1 TeV. Establishes the data-analysis-grade Fermi-LAT pipeline (per-energy point-source mask, foreground subtraction, beam-window correction, PolSpice angular power spectrum estimator) that the pipeline's `analysis_mode='data'` path is based on, and supersedes the previous Fornasa et al. (2016) Poisson-noise determination (Fig. 15 of the paper). The 11-bin energy scheme + per-bin $(\ell_\mathrm{min}, \ell_\mathrm{max})$ window in this paper's Table I are exactly what `cfg.AMMAZZALORSO_BINS` already encodes. Co-published with the better-known Ammazzalorso et al. (2018) PRL paper on Fermi×DES weak-lensing (arXiv:1812.10785), this is its 2MPZ-galaxy companion.

## Methodology

### Fermi-LAT data selection (Sec. II.A)
- **Time range**: 4 August 2008 → 13 July 2017 (Fermi MET 239,557,417 → 521,597,050 s) → **108 months ≈ 9 years**
- **Event class**: Pass 8 ULTRACLEANVETO (P8R2_ULTRACLEANVETO_V6 IRFs) — lowest cosmic-ray contamination, recommended for diffuse-emission analysis
- **PSF event-type subselection**: PSF3 only ($z=32$, best-quality quartile) below 1.2 GeV; PSF1+PSF2+PSF3 ($z=56$, three best quartiles) above 1.2 GeV. This balances good direction reconstruction at low-$E$ photon-rich energies with adequate photon counts at high-$E$.
- **Pixelisation**: HEALPix `Nside = 1024` ($N_\mathrm{pix} = 12{,}582{,}912$, mean spacing $\sim 0.06°$) — matched to the best-resolution Fermi-LAT angular accuracy.
- **Energy binning (raw)**: 100 logarithmic bins from 100 MeV to 1 TeV, then **rebinned into 11 wider analysis bins** for the cross-correlation.

### Energy bins and multipole windows (Table I)
The 11 analysis bins and their per-bin multipole ranges:

| Bin | $E_\mathrm{min}$ [GeV] | $E_\mathrm{max}$ [GeV] | $\ell_\mathrm{min}$ | $\ell_\mathrm{max}$ |
|---|---|---|---|---|
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

- $\ell_\mathrm{min} = 40$ is fixed across all bins (chosen conservatively to avoid Galactic-foreground residuals at large angular scales).
- $\ell_\mathrm{max}$ is determined per energy from the **beam window function condition** $\langle W_\ell^k \rangle = 0.61$, capped at 1000. The condition corresponds approximately to the 68% PSF containment.

### Source masking (Sec. II.A)
- **Galactic latitude cut**: $|b| > 30°$ — avoids the brightest Galactic plane emission and minimises the relative weight of Galactic foreground residuals.
- **Per-energy point-source mask**: each energy bin uses its own mask radius and source list, derived from the Fermi-LAT FL8Y/3FHL catalogues. The mask radius is the **68% containment angle** $\theta_{\Delta E}$ in that bin. The threshold flux below which a source is *not* masked is
  $$F_\mathrm{thr,\Delta E} = \frac{1}{5}\,F^\gamma_{\Delta E,\,\mathrm{faintest}}$$
  i.e. one fifth of the flux of the faintest catalogued source in the bin. This cutoff approximately matches the per-bin map RMS — sources are detected at TS ≥ 25.
- The mask is **less restrictive at high $E$** because Fermi PSF improves with energy and high-$E$ sources are rarer, so the masked sky area shrinks as energy increases. This is the same energy-dependent treatment that the pipeline's `astro_sources.F_sens_energy` function emulates parametrically via the PSF solid-angle ratio scaling.
- **Extended sources** (FL8Y/3FHL "extended" flag) are masked using their tabulated extension radius rather than $\theta_{\Delta E}$.

### Foreground removal (Sec. II.A)
- **Galactic emission template**: `gll_iem_v06.fits` (Fermi-LAT Collaboration standard).
- The template is rebinned into the same 100-bin raw scheme then projected to HEALPix $N_\mathrm{side} = 1024$.
- Each template map is assigned a **free overall normalisation** plus a free constant (representing the residual UGRB + cosmic-ray contamination), and a Poissonian likelihood fit is performed *globally on all the masked intensity maps*.
- All best-fit normalisation parameters are of order unity, supporting the foreground description.
- The normalised templates are rebinned into the 11 analysis bins and subtracted from the corresponding intensity maps to produce the final foreground-cleaned data product.

### Beam window correction (Eqs. 4–5)
The PSF response is propagated to multipole space via the Legendre transform:
$$W_\ell(E) = 2\pi \int_{-1}^{1} d\cos\theta\, P_\ell(\cos\theta)\,\mathrm{PSF}(\theta, E)$$
and then averaged within each energy bin with the UGRB spectral index ($\alpha = 2.3$, Ackermann et al. 2015):
$$\langle W_\ell^k \rangle = \frac{\int_{E_\mathrm{min},k}^{E_\mathrm{max},k} W_\ell(E)\,E^{-\alpha}\,dE}{\int_{E_\mathrm{min},k}^{E_\mathrm{max},k} E^{-\alpha}\,dE}$$
The measured per-bin angular power spectrum is corrected as $C_\ell^k = C_{\ell,\mathrm{raw}}^k / (\langle W_\ell^k \rangle W_\mathrm{pix})$ where $W_\mathrm{pix}$ is the HEALPix pixel window. This is exactly what `noise_model.beam_fermi_exact` and `beam_fermi_bin_averaged` implement in the pipeline.

### Power-spectrum estimator (Sec. III)
- `PolSpice` (Szapudi et al. 2001) for masked-sky angular power spectra, including monopole/dipole removal before the spectrum estimation.
- Multipole rebinning: 15 logarithmically-spaced bins from $\ell = 10$ to $\ell = 1000$.
- Covariance matrix from PolSpice (which propagates the mask coupling self-consistently); per-bin energy covariance is treated as **diagonal between energy bins** because the dominant variance is from gamma-ray Poisson photon noise, which is uncorrelated across energies.

### $\chi^2$ statistic (Eq. 8)
The model-comparison statistic is

$$\chi^2 = \sum_{k=1}^{11} \sum_{\Delta\ell, \Delta\ell'} \left(C^{k,\mathrm{mod}}_{\Delta\ell} - C^{k,\mathrm{exp}}_{\Delta\ell}\right) \Gamma^{-1}_{\Delta\ell,\Delta\ell',k} \left(C^{k,\mathrm{mod}}_{\Delta\ell'} - C^{k,\mathrm{exp}}_{\Delta\ell'}\right)$$

with $\Gamma$ the per-energy-bin covariance from PolSpice (energy bins assumed independent). The detection significance is reported as $\sqrt{\Delta\chi^2}$ where $\Delta\chi^2 = \chi^2_\mathrm{null} - \chi^2_{C_p}$.

### Catalogue
- **2MPZ** (~10⁶ galaxies, mean $z = 0.07$, photometric redshifts from a NN cross-match of 2MASS XSC + WISE + SuperCOSMOS)
- Subsamples used: full 2MPZ; 2MRS (spectroscopic subsample); three redshift bins ($z<0.07$, $0.07<z<0.11$, $z>0.11$); three B-luminosity bins; three K-luminosity bins; "high-K low-B" DM target subsample
- Volumetric coverage corresponds to ~10% of the total UGRB intensity

## Key Results

- **Detection significance** of the multipole-independent $C_p^k$ amplitude in each subsample (Table II): $\Delta\chi^2$ ranges from **3** (low-$z$ subsample) to **29** (high-K subsample).
- **AGN dominance**: the cross-correlation signal in 2MPZ is dominated by **unresolved blazars + misaligned AGN**. Star-forming galaxies provide a sub-dominant contribution.
- **Best-fit Poisson noise terms** $C_p^k$ are tabulated per galaxy subsample in Table V (in units of $10^{-x}$ photons² cm⁻⁴ s⁻² sr⁻¹ depending on the bin).
- **Comparison to Fornasa et al. 2016**: Fig. 15 shows the new $C_p^k$ values agree with the previous Fornasa+2016 measurement and **improve the statistical determination by a factor ~2**, due to the longer integration (108 vs 81 months) and the Pass 8 ULTRACLEANVETO event class. **This paper supersedes Fornasa+2016 as the canonical Fermi-LAT data-grade UGRB measurement.**
- **DM bounds**: 95% CL upper limits on the DM annihilation rate $\langle\sigma v\rangle$ approach the thermal-relic value for masses $\sim 100$ GeV in the $b\bar b$ channel (Sec. IV.C).

## Key Observational / Pipeline-Relevant Specifications

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Fermi-LAT integration time | 108 months (~9 years), Aug 2008 → Jul 2017 | Sec. II.A |
| Fermi-LAT event class | Pass 8 ULTRACLEANVETO (P8R2_ULTRACLEANVETO_V6 IRFs) | Sec. II.A |
| PSF subselection | PSF3 below 1.2 GeV; PSF1+PSF2+PSF3 above 1.2 GeV | Sec. II.A |
| HEALPix Nside | 1024 (0.06° spacing) | Sec. II.A |
| Energy bins | **11**, 0.631–1000 GeV | Table I |
| Multipole window | $\ell_\mathrm{min} = 40$ (fixed); $\ell_\mathrm{max}$ from $\langle W_\ell^k \rangle = 0.61$ or $\le 1000$ | Sec. III, Eq. 7 |
| Galactic latitude cut | $|b| > 30°$ | Sec. II.A |
| Source mask radius | 68% PSF containment $\theta_{\Delta E}$ per energy bin | Sec. II.A |
| Source mask threshold | $F_\mathrm{thr,\Delta E} = (1/5)\,F^\gamma_{\Delta E, \mathrm{faintest}}$ | Sec. II.A |
| Source catalogue | FL8Y / 3FHL (the precursor to 4FGL-DR1) | Sec. II.A |
| Foreground template | `gll_iem_v06.fits` (Fermi-LAT Collaboration) | Sec. II.A |
| Foreground fitting | Free normalisation + free constant per template; global Poisson likelihood | Sec. II.A |
| Spectral weighting (beam) | $\alpha = 2.3$ (Ackermann et al. 2015) | Eq. 5 |
| Pixel window correction | HEALPix $W_\mathrm{pix}$ at $N_\mathrm{side} = 1024$ | Eq. 6 |
| Estimator | PolSpice (Szapudi et al. 2001) | Sec. III |
| Multipole rebinning | 15 log bins, $10 \le \ell \le 1000$ | Sec. III |
| Covariance | PolSpice per-bin, diagonal between energy bins | Sec. III |
| Galaxy catalogue | 2MPZ ($\sim 10^6$ gal, $\bar z = 0.07$) + 2MRS subsample | Sec. II.B |

## Repository Use

This is the **canonical Fermi-LAT data-analysis-grade reference** for the pipeline's `analysis_mode='data'` path. The 11-bin energy scheme + per-bin $(\ell_\mathrm{min}, \ell_\mathrm{max})$ window + PSF beam treatment + foreground subtraction approach are all encoded in:

- `cfg.AMMAZZALORSO_BINS` — the exact 11 bins from Table I
- `cfg.AMMAZZALORSO_ELL_MIN` / `cfg.AMMAZZALORSO_ELL_MAX` — the per-bin $\ell$ window
- `noise_model.beam_fermi_exact` — Eq. 4 Legendre transform of the King PSF
- `noise_model.beam_fermi_bin_averaged` — Eq. 5 spectral weighting with $\alpha = 2.3$

This paper is the primary reference for the **gamma-ray side of the data-grade SNR forecasts**:

1. **Energy binning**: every entry that uses the 11-bin scheme (the `analysis_mode='data'` path in `compute_SNR`, used by the new MeerKLASS canonical mode) implicitly inherits this paper's Table I.
2. **Beam window function**: the Knox variance computed for the canonical MeerKLASS forecasts uses $\langle W_\ell^k \rangle$ from this paper's Eq. 5 via `beam_fermi_exact`.
3. **Source mask threshold**: the data-mode F_sens parametrisation in `astro_sources.F_sens_energy` follows this paper's PSF-area scaling, anchored to a baseline value (`cfg.F_SENS`).
4. **Foreground subtraction**: the pipeline does not directly model foregrounds (it works at the C_ell level), but this paper's `gll_iem_v06.fits` template + free-normalisation approach is what the data-mode noise / sky-fraction values implicitly assume.
5. **Comparison to Fornasa+2016**: this paper supersedes Fornasa+2016 as the canonical Fermi-LAT cross-correlation measurement; any data-mode comparison should anchor to the values reported here, not the older Fornasa values.

### How the user splits this between forecast and canonical modes

Per the instruction to use "Pinetti 2022 + 1808.09225 for the forecast, 4FGL-DR4 + 1808.09225 for the canonical (MeerKAT) mode":

| Pipeline mode | Telescope entries | $T_\mathrm{sys}$ | $\Omega_\mathrm{HI}$ | Energy binning | $F_\mathrm{sens}$ | Beam | Source: |
|---|---|---|---|---|---|---|---|
| **Pinetti 2022 forecast** | `MeerKAT`, `SKA1`, `SKA2` | Pinetti 2020 Eq. 3.18 ($\sim 32$–$35$ K) | $2.45\times10^{-4}$ fixed (Battye+2013) | Pinetti 2020 Table 2 (12 bins) **OR** 1808.09225 Table I (11 bins) | $1\times10^{-10}$ cm⁻² s⁻¹ constant (Pinetti 2020) | Pinetti Gaussian or 1808.09225 King-PSF | Pinetti+2020/2022 + this paper |
| **MeerKAT canonical** | All `MeerKLASS_*` | MeerKLASS Collab. 2025 Eqs. 21–22 ($\sim 16$–$17$ K) | Cunnington+2025 Eq. A5 polynomial | 1808.09225 Table I (11 bins) | 4FGL-DR4 baseline ($\sim 4\times10^{-12}$ cm⁻² s⁻¹) with this paper's PSF-area scaling (`F_sens_energy`) | 1808.09225 King-PSF (`beam_fermi_exact`) | 4FGL-DR4 + this paper |

The 11-bin energy scheme + the King-PSF beam window function from 1808.09225 are the **shared** Fermi-LAT data products in both modes; only the source-completeness threshold (and the radio-side conventions, set in earlier turns) differs. This makes the canonical MeerKAT mode internally consistent with what an actual MeerKLASS-style data analysis would produce.
