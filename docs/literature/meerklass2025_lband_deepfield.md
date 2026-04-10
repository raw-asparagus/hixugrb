# MeerKLASS Collaboration (2025) — L-band deep-field intensity maps: entering the HI dominated regime

**Authors:** MeerKLASS Collaboration: M. Barberi-Squarotti, J. L. Bernal, P. Bull, S. Camera, I. P. Carucci, Z. Chen, S. Cunnington†, B. N. Engelbrecht, J. Fonseca, K. Grainge, M. O. Irfan, Y. Li, A. Mazumder, S. Paul, A. Pourtsidou, M. G. Santos, M. Spinelli, J. Wang‡, A. Witzemann, L. Wolz
**Journal:** MNRAS, accepted (preprint dated 30 January 2025)
**arXiv:** [2407.21626](https://arxiv.org/abs/2407.21626) (v2)

## Abstract

Presents MeerKAT single-dish HI intensity maps from the **MeerKLASS L-band deep-field** — the final L-band observations of the MeerKLASS campaign and the deepest single-dish HI intensity maps to date. 41 repeated scans over a 236 deg² southern field, providing 62 hours per dish before flagging (3,968 cumulative dish-hours; 27 of 41 blocks survived RFI flagging). An iterative self-calibration process limits the reconstructed-map thermal noise to **1.21 mK** (1.2× the radiometer-equation theoretical level). Crucially, on large scales ($k \lesssim 0.15\,h\,\mathrm{Mpc}^{-1}$) the thermal noise is now **subdominant** to the cosmological HI fluctuations — the maps "enter the HI-dominated regime" of the title — which forces a corresponding upgrade to the covariance-estimation pipeline. Cross-correlating with **2,269 spectroscopic galaxies** from the GAMA G23 region (covering only ~25% of the deep-field footprint, narrow $0.39 < z < 0.46$), the paper reports a **> 4σ detection of the HI×galaxy cross-power spectrum**. Also presents the first stacking-based evidence of HI emission from MeerKAT single-dish maps onto GAMA galaxy positions, and a brief discussion of the HI auto-power spectrum (the full auto-power detection deferred to follow-up work). This is the underlying observational paper for `MeerKLASS_L_deepfield` in `hi_gamma_xcorr/config.py`.

## Methodology

### Observation Configuration (Sec. 2.1)
- **Instrument:** MeerKAT, 64 dishes × 13.5 m, **L-band** receivers
- **Mode:** single-dish auto-correlation (the same scan strategy as the Wang et al. 2021 pilot)
- **Field:** 236 deg² in the southern sky, RA $\in (330°, 360°)$, Dec $\in (-36°, -25°)$
- **Observing period:** 1 September – 29 December 2021
- **Scan strategy:** constant-elevation azimuth slew at 5 / cos(el) arcmin s⁻¹ (projected sky speed 5 arcmin s⁻¹), 10° throw per stripe (~120 s per stripe), 48 stripes per ~100 min observation block
- **Time resolution:** 2 s integrations
- **Noise diodes:** fired for 0.585 s every 19.5 s
- **Bandpass / flux calibration:** ~8 minutes on a nearby celestial point source bracketing each scan block
- **Block count:** 41 attempted scan blocks; **27 blocks** survived after RFI flagging (14 blocks fully removed due to non-linear gain effects from a mobile-phone tower ~54 km away that enters through sidelobes)
- **Total integration:** **62 hours per dish before flagging** → 3,968 cumulative dish-hours
- **Frequency channels:** 0.209 MHz wide, full L-band 900–1670 MHz; cosmologically usable RFI-quiet window **971.2 < ν < 1023.6 MHz** corresponding to $0.39 < z < 0.46$ for redshifted 21cm

### Standard MeerKAT Calibration (Sec. 2.2)
- Pipeline: `KATcali` (Wang et al. 2021)
- Two-stage: (a) bandpass/absolute-flux calibration on tracking observations of a strong point source, (b) noise-diode-based time-varying gain calibration on the constant-elevation scans
- Signal model:
  $$T_\mathrm{model}(t,\nu) = T_\mathrm{diffuse}(t,\nu) + T_\mathrm{el}(t,\nu) + T_\mathrm{diode}(t,\nu) + T_\mathrm{rec}(t,\nu)$$
  with $T_\mathrm{diffuse} = T_\mathrm{Gal} + T_\mathrm{CMB}$, $T_\mathrm{CMB} = 2.725$ K, $T_\mathrm{Gal}$ from PySM (Haslam 408 MHz extrapolation)
- 4th-order polynomial fit for the per-(pol, channel, dish, scan) gain $g(t, \nu)$

### Iterative Self-Calibration (Sec. 2.3) — key methodological advance
- **Problem:** the standard pipeline assumes the residual $T_\mathrm{res} = T_\mathrm{cal} - T_\mathrm{model}$ is noise-dominated, ignoring point sources in the target field. This was a fair assumption at pilot-survey noise levels but breaks down at deep-field sensitivity.
- **Method:** five iterative loops in which the input diffuse model is replaced by the previously-calibrated MeerKLASS sky map itself ($T_\mathrm{sky}$ from Level-6 of the previous loop, where Level-6 pixels with hit-count > 40 contribute), so that point sources, Galactic substructure, and the actual sky topology are all baked into the input model.
- **Time-order weights** are uniformly set to 1 (instead of up-weighting noise-diode samples).
- **Convergence:** the standard deviation of $T_\mathrm{res}$ in 971–1023 MHz drops monotonically over the five loops and plateaus by Loop 5.
- **Improvement on the line-of-sight rms:** average pixel variance reduces marginally (from 984.3 mK² standard → 977.2 mK² self-calibrated).
- **Final pixel size:** 0.3 deg.

### Final Map Characteristics (Sec. 2.4)
- **Median map noise** ($\Delta T_\mathrm{RMS}$): **1.21 mK** in 971–1023 MHz
- **$R_\mathrm{RMS} = \Delta T_\mathrm{RMS}/\sigma_\mathrm{th}$:** median 1.2, max 1.5 (so the maps are within ~20% of the radiometer-equation theoretical noise floor)
- Noise estimated via the four-channel ABBA pattern, weighted by $\sigma_\mathrm{th}^{-2}$
- 14 blocks removed entirely due to RFI from a mobile-phone tower; flagging strategy under active development to recover them in future analyses

### GAMA Galaxy Cross-Sample (Sec. 2.5)
- **Catalogue:** GAMA DR4 G23 region (the 23-hour field), which fully overlaps the MeerKLASS deep field's RA range
- **G23 footprint:** 339° < RA < 351°, −35° < Dec < −30° → covers only ~25% of the MeerKLASS deep-field footprint
- **Redshift completion:** 94.2% in G23 (Liske et al. 2015)
- **Magnitude limit:** $i$-band 19.2 (reduced from the 19.8 $r$-band plan due to limited time)
- **Galaxies in the cross-correlation:** **2,269** in the narrow $0.39 < z < 0.46$ window (caught near the end of the GAMA optimal range due to the aggressive RFI flagging on the MeerKLASS side)
- **Volume number density:** $\bar n_g = 4.8 \times 10^{-4}\,h^3\,\mathrm{Mpc}^{-3}$
- No GAMA G23 randoms available → uniform selection function across the G23 footprint assumed

### Mock Pipeline (Sec. 3)
- **500 lognormal mocks** generated with `powerbox`, used for: pipeline validation, signal-loss correction (foreground transfer function), and covariance estimation.
- Lognormal HI temperature fields convolved with the resmoothed beam; Poisson sampling of GAMA-equivalent galaxies on the same density field.
- Mock galaxy positions matched to GAMA-G23 redshift distribution.

### Foreground Cleaning (Sec. 4)
- **Method:** PCA on the frequency-frequency covariance, removing the first $N_\mathrm{fg}$ eigenmodes
- **Headline result:** $N_\mathrm{fg} = 10$ PCA modes
- **Reconvolution:** maps reconvolved to a common Gaussian resolution (similar to Cunnington et al. 2023 §4.1) before PCA — slightly improves PCA performance and suppresses systematics
- **Foreground transfer function $T(k)$:** built from the 500 mocks via signal injection. The **scatter** in the reconstructed mocks is used to estimate the cross-power covariance, replacing the previous Knox-formula approach. This transfer function correction is applied as a single power $T(k)$ (not $T(k)^2$) to both auto- and cross-power.

### Power Spectrum Estimation (Sec. 5)
- **Cartesian regridding:** spherical sky maps regridded to Cartesian volumes for Fourier analysis using the Cunnington & Wolz (2024) bias-mitigated scheme.
- **Cylindrical analysis** ($k_\perp$, $k_\parallel$) presented in Fig. 13: cross-power, transfer function, signal-to-noise, and mode count.
- **$k$-cuts:** orange contours mark the regions excluded due to low signal-to-noise.
- **Detection significance** computed as $\sqrt{\Delta\chi^2} = \sqrt{\chi^2 - \chi^2_\mathrm{null}}$ with full covariance.

### Theoretical Model & Brightness Temperature Convention (Sec. 5, Appendix C)
- **HI brightness temperature** (Eq. C1):
  $$T_\mathrm{HI}(z) = 180\,\Omega_\mathrm{HI}(z)\,h\,\frac{(1+z)^2}{\sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}}\;\mathrm{mK}$$
  i.e. the **180 mK** Battye+2013 / Cunnington+2023 / Cunnington+2025 / MeerFish convention — *not* the 188 mK Padmanabhan+2017 / Pinetti+2020 form.
- **MCMC-fitted parameters** (Appendix C, demonstration only): $\boldsymbol{\varphi} = \{\Omega_\mathrm{HI}, b_\mathrm{HI}, b_g, \sigma_v\}$, with flat priors $0 < 10^3\Omega_\mathrm{HI} < 2$, $0.5 < b_\mathrm{HI} < 2.0$, $1.8 < b_g < 2.0$, $0 < \sigma_v < 600\,\mathrm{km\,s^{-1}}$.
- **Best-fit single-amplitude inferred** $T_\mathrm{HI} = 0.166$ mK at $z \sim 0.43$ (with all other Table 1 parameters fixed).

## Key Results

- **Deepest single-dish HI intensity maps to date** (in observation hours per square degree, in the MeerKLASS programme): 62 hr/dish over 236 deg², median noise 1.21 mK.
- **Iterative self-calibration** is the central methodological advance over Wang et al. 2021 — drives $T_\mathrm{res}$ down by an order of magnitude over five loops.
- **HI dominated regime entered** at $k \lesssim 0.15\,h\,\mathrm{Mpc}^{-1}$ — thermal noise no longer dominates the variance budget; covariance must be estimated from mock injection rather than from the Knox formula. (This is the "entering the HI dominated regime" of the title.)
- **> 4σ detection** of the cross-power spectrum between the MeerKLASS deep field and 2,269 GAMA G23 galaxies at $0.39 < z < 0.46$, despite only ~25% footprint overlap and a conservative covariance approach.
- **Best-fit cross-power amplitude** equivalent to $T_\mathrm{HI} = 0.166$ mK with the Table 1 fiducial parameters held fixed (Sec. 5).
- **Reduced $\chi^2_\mathrm{dof} = 0.42$** — the conservative transfer-function-scatter error estimate appears to over-predict the uncertainty (the data scatter around the model is tighter than the error bars suggest).
- **First evidence of HI emission from stacking** the MeerKLASS maps onto the positions of GAMA galaxies (Sec. 6) — though contaminated by source double-counting and PCA-induced systematics that are explored in Appendix D.
- **HI auto-power spectrum**: briefly shown in Fig. 14, marked as the focus of follow-up work. The auto-power detection over the foreground-clean noise floor is now the main outstanding result.
- The 14 RFI-removed blocks are still potentially recoverable via a non-linear gain correction under active development.

## Key Observational Specifications

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Instrument | MeerKAT, 64 × 13.5 m dishes | Sec. 2.1 |
| Receiver | L-band, 900–1420 MHz | Sec. 2.1 |
| Cosmologically useable window | 971.2–1023.6 MHz, $0.39 < z < 0.46$ | Sec. 2.4.1 |
| Field area | 236 deg² | Sec. 2.1 |
| Field RA / Dec | (330°, 360°) / (−36°, −25°) | Sec. 2.1 |
| Total scan blocks attempted | 41 | Sec. 2.4.1 |
| Scan blocks surviving | **27** | Sec. 2.4.1 |
| Hours per dish (before flagging) | **62 hr** | Sec. 2.1 |
| Cumulative dish-hours | 3,968 hr | Sec. 2.1 |
| Time resolution | 2 s | Sec. 2.1 |
| Noise diode period | 19.5 s (firing 0.585 s) | Sec. 2.1 |
| Scan speed | 5 / cos(el) arcmin s⁻¹ | Sec. 2.1 |
| Strip throw | ~10° in azimuth | Sec. 2.1 |
| Stripes per scan block | ~48 | Sec. 2.1 |
| Pixel size | 0.3 deg | Sec. 2.4.1 |
| Channel width $\delta\nu$ | 0.209 MHz | Sec. 2.4.3, Eq. 11 |
| Self-calibration loops | 5 | Sec. 2.3 |
| Median map RMS $\Delta T_\mathrm{RMS}$ | **1.21 mK** | Abstract / Sec. 2.4.3 |
| Median $R_\mathrm{RMS} = \Delta T_\mathrm{RMS}/\sigma_\mathrm{th}$ | 1.2 | Sec. 2.4.3 |
| HI-dominated scale | $k \lesssim 0.15\,h\,\mathrm{Mpc}^{-1}$ | Abstract |
| GAMA galaxies in cross-corr | **2,269** | Sec. 2.5 |
| GAMA G23 footprint overlap | ~25% of deep field | Abstract / Sec. 2.5 |
| Galaxy number density $\bar n_g$ | $4.8 \times 10^{-4}\,h^3\,\mathrm{Mpc}^{-3}$ | Sec. 2.5 |
| PCA modes ($N_\mathrm{fg}$) | 10 (headline) | Sec. 5 |
| Mock count | 500 lognormal | Sec. 3 |
| Cross-power detection significance | **> 4σ** | Abstract / Sec. 5 |
| Best-fit $T_\mathrm{HI}$ inferred | 0.166 mK at $z \sim 0.43$ | Sec. 5 |
| Reduced $\chi^2_\mathrm{dof}$ | 0.42 | Sec. 5 |
| $T_\mathrm{HI}$ prefactor convention | **180 mK** (Battye+2013) | Eq. C1 |

## Data Availability

From the paper's Data Availability statement (Sec. 5 / p24):
> "The data underlying this article will be shared upon reasonable request to the corresponding author. Access to the raw data used in the analysis is public (for access information please contact archive@ska.ac.za)."

In practice this means:
- **Calibrated HI intensity maps**: not publicly downloadable; available **on request** to the corresponding author (Steven Cunnington, manchester.ac.uk).
- **Raw visibilities (TOD)**: publicly accessible via the SARAO archive (`archive@ska.ac.za`) — but processing them through `KATcali` + the iterative self-cal pipeline is non-trivial.
- **No DOI for a public derived-product release** is mentioned.

This is a stricter regime than e.g. Cunnington+2023 (whose pilot maps are publicly distributed). For the HI×UGRB cross-correlation pipeline, the deep-field maps cannot be downloaded and ingested directly today; they are usable only via collaboration access. The `MeerKLASS_L_deepfield` config entry encodes the *forecast input* — what the SNR forecast looks like assuming MeerKLASS-grade processing of these specific observations.

## Repository Use

This is the **observational source paper** for the `MeerKLASS_L_deepfield` entry in `hi_gamma_xcorr/config.RADIO_TELESCOPES`:

| Config field | Value | Source in paper |
|---|---|---|
| `survey_area_deg2` | 236.0 | Sec. 2.1 |
| `t_obs_hours` | 62.0 | Sec. 2.1 (per dish, before flagging) |
| `n_dishes` | 64 | Sec. 2.1 |
| `d_dish_m` | 13.5 | implicit (MeerKAT) |
| `eta` (= $\varepsilon$, the survey efficiency factor) | 0.5 | Cunnington+2025 Table 2 convention; here 27/41 = 66% of blocks survived RFI, then further flagging within blocks gives ~50% — so 0.5 is a reasonable lower bound for the deep-field RFI loss budget |
| `bands.L.z_min` | 0.39 | Sec. 2.4 / Sec. 2.5 (RFI-quiet window) |
| `bands.L.z_max` | 0.46 | Sec. 2.4 / Sec. 2.5 |

In addition, this paper provides:

1. The **180 mK** $\bar T_\mathrm{HI}$ prefactor convention used by the entire MeerKLASS data-analysis chain (Eq. C1) — consistent with `hi_model.T_bar_b_cunnington` (the `'cunnington'` mode of `hi_model.T_bar_b_for_model`) and at odds with the 188 mK pipeline default `T_bar_b`. Documented as a tracked discrepancy in `docs/literature/cunnington2025_meerklass_overview.md`.
2. A concrete **best-fit $T_\mathrm{HI}$ measurement** ($T_\mathrm{HI} = 0.166$ mK at $z\sim 0.43$) which is a direct sanity-check anchor for any future "Cunnington-mode" cross-correlation forecast: at $z=0.43$, the pipeline's `hi.T_bar_b_cunnington(0.43)` returns 0.162 mK — consistent with the measured value to ~3%, and well within the systematic uncertainty.
3. A working **foreground-transfer-function-as-covariance** estimator pattern (Sec. 5.3) that is the most relevant data-analysis-grade upgrade for the pipeline's noise model. Currently the pipeline uses the Gaussian Knox formula (`statistics.variance_Cl`) — the planned MeerKAT-data-grade upgrade in `memory/project_meerkat_upgrade.md` (item 1) explicitly cites the same covariance approach.
4. Confirmation that the iterative self-calibration plus Cunnington & Wolz (2024) Cartesian regridding plus the 500-mock transfer function are all on the critical path for any MeerKLASS data analysis — these are the upgrade items for any future "data-analysis grade" mode of the pipeline.
5. The cosmologically useable RFI window for L-band MeerKAT cosmology: **0.39 < z < 0.46**, much narrower than the full receiver bandpass. This is exactly the band already populated in `MeerKLASS_L_deepfield.bands.L`.

This is the underlying paper that the Cunnington et al. (2025) review (`docs/literature/cunnington2025_meerklass_overview.md`, Sec. 5.1) summarises as the "L-band deep-field × GAMA detection". The two should be cross-referenced when consulting for HI×galaxy benchmarks.
