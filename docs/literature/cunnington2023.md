# Cunnington, Li et al. (2023) — MeerKAT HI Intensity Mapping × WiggleZ Cross-Correlation

**Authors:** S. Cunnington, Y. Li, M. G. Santos, J. Wang, I. P. Carucci, M. O. Irfan, A. Pourtsidou, M. Spinelli, L. Wolz, P. S. Soares, C. Blake, P. Bull, B. Engelbrecht, J. Fonseca, K. Grainge, Y.-Z. Ma
**Journal:** MNRAS 518(4), 6262–6272 (2023)
**arXiv:** [2206.01579](https://arxiv.org/abs/2206.01579)

## Abstract

First practical demonstration of the multi-dish auto-correlation intensity mapping technique for cosmology, using the MeerKAT array in single-dish mode. Cross-correlates 10.5 hours of MeerKAT L-band pilot survey data (973–1015 MHz, z = 0.400–0.459) with WiggleZ Dark Energy Survey galaxies. Achieves a 7.7-sigma detection, constraining Omega_HI b_HI r = [0.86 +/- 0.10 (stat) +/- 0.12 (sys)] x 10^{-3} at k_eff ~ 0.13 h/Mpc. This is the first practical demonstration of multi-dish auto-correlation intensity mapping for cosmology and a key milestone for the SKAO roadmap.

## Methodology

### MeerKAT Instrument & Observation
- **Array:** 64 dishes, 13.5 m diameter each, L-band receivers (900–1670 MHz)
- **Survey:** ~200 deg^2 in WiggleZ 11hr field (153 < RA < 172 deg, -1 < Dec < 8 deg); 4031 overlapping WiggleZ galaxies
- **Observation:** 10.5 hours total across 6 nights (Feb–Jul 2019), 7 time blocks of ~1.5 hr scans
- **Usable frequency range:** 973.2–1014.6 MHz (199 channels, of which 167 survive RFI flagging)
- **Redshift range:** z = 0.400–0.459
- **Mode:** Single-dish auto-correlation (NOT interferometric)
- **Beam:** theta_FWHM = 1.16 c/(nu D_dish) = 1.48 deg at mean frequency (Matshawule et al. 2021)

### Calibration
- Noise diodes fired every 20 s remove 1/f noise from receiver gain variations
- Bandpass and absolute calibration via bright source observations (3C 273, 3C 237, Pictor A)
- Average signal subtracted every 220 s in TOD to suppress residual long-timescale gain changes
- Three levels of RFI flagging: SEEK package on raw data, per-channel TOD outlier removal, post-map residual RFI

### Map-Making (Eq. 1–2)
Optimal map estimator (Tegmark 1997):

$$\hat{m} = (A^T N^{-1} A)^{-1} A^T N^{-1} d$$

where A is the pointing matrix, N is the diagonal noise covariance (constant variance per dish, variable between dishes), and d is the time-ordered data. Pixel noise variance:

$$\hat{n} = (A^T N^{-1} A)^{-1}$$

Maps gridded to flat-sky 0.25 deg square pixels. Final maps averaged over all dishes and time blocks per frequency channel.

### Foreground Cleaning — PCA (Sec. 4.2)
- Foregrounds (synchrotron, free-free) are 10^3–10^5x brighter than HI signal
- Blind PCA on the frequency-frequency covariance matrix C = (wX)^T(wX)/(N_theta - 1)
- Remove first N_fg eigenmodes (optimal: N_fg = 30 for this dataset)
- Signal loss primarily at small k_parallel (large radial scales)
- Residual foregrounds remain; cross-correlation mitigates their additive bias

### Reconvolution (Sec. 4.1, Eqs. 16–18)
Frequency-dependent beam causes foreground leakage into more spectral modes. Before PCA cleaning, maps are resmoothed to a common resolution:

$$K(\Delta\theta, \nu) = \exp\left[-\frac{\Delta\theta^2}{2(\gamma^2 \sigma_{\max}^2 - \sigma^2(\nu))}\right]$$

where sigma(nu) = theta_FWHM(nu) / (2 sqrt(2 ln 2)), sigma_max is the maximum across the band, and gamma = 1.2 is the resmoothing factor. Effective resolution after reconvolution: gamma * theta_FWHM(nu_min) = 1.82 deg.

The weighted reconvolution (Eq. 17) and updated weight field (Eq. 18) preserve inverse-variance weighting:

$$\delta T(\theta, \nu) = \frac{(\delta T' \cdot w'_{\rm HI}) * K}{w'_{\rm HI} * K}$$

$$w_{\rm HI}(\theta, \nu) = \frac{(w'_{\rm HI} * K)^2}{w'_{\rm HI} * K^2}$$

### Foreground Transfer Function (Sec. 4.3, Eqs. 19–20)
Compensates signal loss from PCA cleaning by injecting mock HI signal into real data:

$$M_c = [M_{\rm HI} + X_{\rm obs}]_{\rm PCA} - [X_{\rm obs}]_{\rm PCA}$$

$$T(k) = \left\langle \frac{P(M_c, M_g)}{P(M_{\rm HI}, M_g)} \right\rangle$$

Averaged over 100 lognormal mock realisations. Key features (Fig. 3):
- T(k) ~ 1 at high k (minimal signal loss)
- T(k) << 1 at low k_parallel (severe signal loss from PCA removing smooth radial modes)
- For N_fg = 30: ~80% signal loss at smallest k, ~10% at k ~ 0.1 h/Mpc

Cross-power spectrum corrected: P_obs / T(k). Auto-power corrected by 1/T(k) (NOT 1/T^2).

### Power Spectrum Estimation (Sec. 3.1, Eqs. 3–10)
Feldman–Kaiser–Peacock (FKP) optimal weighting estimator:

$$\hat{P}_{\rm HI,g}(k) = \frac{V_{\rm cell}}{\sum_x w_{\rm HI} w_g W_g} \operatorname{Re}\left\{\tilde{F}_{\rm HI}(k) \cdot \tilde{F}_g^*(k)\right\} \frac{1}{N_g}$$

with galaxy weights w_g = 1/(1 + W_g N_g P_0 / V_cell) and errors (Eq. 11):

$$\hat{\sigma}_{\rm HI,g}(k) = \frac{1}{\sqrt{2 N_m(k)}} \sqrt{\hat{P}^2_{\rm HI,g}(k) + \hat{P}_{\rm HI}(k)\left(\hat{P}_g(k) + \frac{1}{\bar{n}_g}\right)}$$

### Theoretical Model (Sec. 3.2, Eqs. 12–15)
Cross-power spectrum model:

$$P_{\rm HI,g}(k) = T_{\rm HI} b_{\rm HI} b_g r (1 + f\mu^2)^2 P_m(k) \exp\left[-\frac{(1-\mu^2) k^2 R_{\rm beam}^2}{2}\right]$$

where R_beam = 13.3 Mpc/h (Gaussian beam in comoving units after reconvolution), f = 0.737 (growth rate), b_g = 0.911 (WiggleZ galaxy bias at z_eff = 0.43).

Brightness temperature (Eq. 15):

$$T_{\rm HI}(z) = 180 \, \Omega_{\rm HI}(z) \, h \, \frac{(1+z)^2}{\sqrt{\Omega_m(1+z)^3 + \Omega_\Lambda}} \text{ mK}$$

Model convolved with survey window functions (Eq. 14) and corrected by transfer function T(k).

## Key Results

- **7.7-sigma detection** of MeerKAT HI × WiggleZ cross-correlation
- **Omega_HI b_HI r = [0.86 +/- 0.10 (stat) +/- 0.12 (sys)] x 10^{-3}** at z = 0.43, k_eff ~ 0.13 h/Mpc
- **Omega_HI = [0.83 +/- 0.15 (stat) +/- 0.11 (sys)] x 10^{-3}** (assuming b_HI = 1.13 +/- 0.10, r = 0.9 +/- 0.1)
- Good model agreement across 0.05 < k < 0.28 h/Mpc: chi^2_dof ~ 1 (dof = 24)
- Results robust to N_fg choice (6-sigma detection for N_fg = 26–34)
- Null tests (redshift shuffling, random mocks) consistent with zero
- Detection achieved even WITHOUT transfer function correction (> 4 sigma)

## Key Specifications for Pipeline Implementation

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Dish diameter | 13.5 m | Sec. 2 |
| Number of dishes | 64 (avg ~60 usable per time block) | Sec. 2 |
| L-band frequency range | 900–1670 MHz (full); 973–1015 MHz (used) | Sec. 2 |
| UHF-band frequency range | 580–1015 MHz | Sec. 2 |
| Beam FWHM | 1.16 c/(nu D_dish) | Sec. 2; cf. pipeline's 1.22 coefficient |
| Beam after reconvolution | 1.82 deg (= 1.2 * theta_FWHM(nu_min)) | Sec. 4.1 |
| R_beam (comoving) | 13.3 Mpc/h | Sec. 3.2 |
| Survey area | ~200 deg^2 | Sec. 2 |
| Integration time | 10.5 hrs (7 x 1.5 hr scans) | Sec. 2 |
| Pixel size | 0.25 deg | Sec. 2 |
| Frequency channels | 199 selected, 167 after RFI flagging | Sec. 2 |
| Channel width | ~0.188 MHz (4096 channels over 770 MHz L-band) | Sec. 2 |
| PCA modes removed | N_fg = 30 (optimal) | Sec. 5.2 |
| Transfer function | T(k) from 100 lognormal mocks | Sec. 4.3 |
| Resmoothing parameter | gamma = 1.2 | Sec. 4.1 |
| T_HI coefficient | 180 mK (cf. pipeline's 188 mK) | Eq. 15 |
| Scan speed | 5 arcmin/s along azimuth | Sec. 2 |
| Noise diode period | 20 s | Sec. 2 |

## Beam Coefficient: 1.16 vs 1.22

The paper uses theta_FWHM = 1.16 c/(nu D_dish) (Matshawule et al. 2021) rather than the standard diffraction limit 1.22 lambda/D. The 1.16 coefficient is specific to the MeerKAT dish illumination pattern. The pipeline currently uses 1.22 — this should be updated for MeerKAT-specific analysis.

## Brightness Temperature Coefficient: 180 vs 188

Eq. 15 uses 180 mK while the pipeline uses 188 h mK. The difference arises from rounding conventions: 180 Omega_HI h = 180 * h * Omega_HI = 121.2 * Omega_HI, while 188 h * Omega_HI = 126.6 * Omega_HI. This ~4% difference is within the ~15% systematic uncertainty on Omega_HI. The pipeline's 188h value follows Pinetti+(2020) and standard 21-cm references.

## Pipeline Implications — Data-Analysis-Grade HI Treatment

This paper is the primary reference for upgrading the pipeline's MeerKAT treatment from forecasting to data-analysis grade. Key upgrades identified:

1. **Reconvolution**: Frequency-dependent beam must be homogenised before foreground cleaning. Implement Eqs. 16–18 for weighted reconvolution to common resolution.

2. **Foreground transfer function**: PCA cleaning causes scale-dependent signal loss T(k). Implement Eqs. 19–20 for mock-injection-based transfer function estimation.

3. **Beam coefficient**: Update from 1.22 to 1.16 for MeerKAT illumination pattern.

4. **RFI flagging**: Model frequency channels lost to RFI (32/199 channels = 16% loss in this dataset). This modifies the effective band selection function phi(z).

5. **Survey window convolution**: Model must be convolved with survey window functions (Eq. 14) before comparison to data.

6. **1/f noise**: Noise diode calibration removes long-timescale gain variations; residual 1/f noise is subdominant to thermal noise for scan times < 20 s.

7. **Single-dish vs interferometer**: This paper uses single-dish mode only (no baselines). The pipeline's interferometer noise model (Eq. 8.4) does not apply; only the single-dish noise formula is relevant.

## Implementation

**Primary use:** Reference for data-analysis-grade MeerKAT HI intensity mapping treatment. Defines the foreground cleaning, transfer function, reconvolution, and power spectrum estimation methodology that the pipeline must implement for actual MeerKAT data.

**Modules affected:** `noise_model.py` (beam coefficient, reconvolution), `hi_model.py` (transfer function, band selection with RFI gaps), `angular_power.py` (survey window convolution), `config.py` (MeerKAT beam coefficient)

**Upstream references:**
- Wang et al. (2021) — MeerKAT calibration and first sky maps
- Matshawule et al. (2021) — MeerKAT beam characterisation (1.16 coefficient)
- Wolz et al. (2022) — HI intensity mapping cross-correlation formalism
