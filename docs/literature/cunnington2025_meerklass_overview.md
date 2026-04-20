# Cunnington et al. (2025) — Revealing Cosmological Fluctuations in 21 cm Intensity Maps with MeerKLASS: from Maps to Power Spectra

**Authors:** S. Cunnington, M. Barberi-Squarotti, J. L. Bernal, S. Camera, I. P. Carucci, Z. Chen, J. Fonseca, M. G. Santos, M. Spinelli, J. Wang, L. Wolz
**Journal:** preprint (arXiv v2 dated 2 February 2026)
**arXiv:** [2510.27549](https://arxiv.org/abs/2510.27549)

## Abstract

A comprehensive review of the MeerKLASS *single-dish* HI intensity-mapping programme: the observational strategy, the analysis pipeline (foreground cleaning, signal-loss reconstruction, regridding), the published cross-correlation detections, and forecasts for the full programme. Covers all single-dish results to date, namely the WiggleZ pilot (Cunnington+2023a), the L-band deep-field × GAMA result (MeerKLASS Collaboration 2025, arXiv:2407.21626), and the multiscale-PCA reanalysis (Carucci+2025, arXiv:2412.06750). Concludes with a Fisher forecast for the awarded extra-large proposal (XLP) configuration of 10,000 deg² in the UHF band, using the public `MeerFish` Fisher code (https://github.com/meerklass/MeerFish). This is the **authoritative MeerKLASS HI single-dish overview paper** as of early 2026 and the corresponding HI release for the commensal *interferometric continuum* DR1s described in Mangla et al. (2025) and Paul et al. (2025).

## Methodology

### Observing Strategy (Sec. 2)
- 64-dish MeerKAT array operated in **auto-correlation (single-dish) mode**, accessing scales below the interferometer's shortest baseline (~0.2 h Mpc⁻¹)
- Constant-elevation azimuth slew, fast-scan to suppress slow gain drifts; noise diodes fired at regular intervals for gain reference
- L-band (900–1670 MHz) initially used 2018–2021; cosmological useable range RFI-restricted to **971–1023 MHz, 0.39 < z < 0.46**
- UHF-band (580–1000 MHz, Table 2 cosmological window) used since 2023; cosmological useable range **0.40 < z < 1.45** (40× larger comoving volume than L-band)
- Interferometric visibilities are recorded commensally (basis for the Mangla+2025 L-band and Paul+2025 UHF continuum DR1s)

### Cumulative Observations (Table 1)

| Year | Added [hr] | Cumulative [hr] | Cumulative area [deg²] | Receiver | z range | Status |
|------|-----------:|----------------:|-----------------------:|----------|---------|--------|
| 2019 | +15* | 15  | 250    | L   | 0.39–0.46 | observed |
| 2021 | +70  | 85  | 500    | L   | 0.39–0.46 | observed |
| 2023 | +110 | 110 | 500    | UHF | 0.40–1.45 | observed |
| 2024 | +270 | 380 | 1,600  | UHF | 0.40–1.45 | observed |
| 2025 | +500 | 880 | 3,600  | UHF | 0.40–1.45 | observing |
| 2026 | +500 | 1,380 | 5,600 | UHF | 0.40–1.45 | XLP awarded |
| 2027 | +550 | 1,930 | 7,800 | UHF | 0.40–1.45 | XLP extension |
| 2028 | +570 | **2,500** | **10,000** | UHF | 0.40–1.45 | XLP extension |
| 2029 | +500 | 3,000 | 12,000 | UHF | 0.40–1.45 | pre-SKAO continuation |
| 2030 | +500 | 3,500 | 14,000 | UHF | 0.40–1.45 | pre-SKAO continuation |

\* of 36 hr observed in 2018/19, only 15 hr were retained, of which ~10.5 hr were ultimately used in Cunnington+2023.

The text quotes the **current state** as "over 650 hr of UHF data reaching nearly 3,000 deg²" — i.e. the 2025 row is partially observed by paper publication. All forecasts in the paper assume the 2028 XLP target.

### Foreground Cleaning (Sec. 3)
- Diffuse Galactic synchrotron + free–free dominate by 3–5 orders of magnitude over the HI signal, but are spectrally smooth
- Blind component separation, primarily **PCA** on the frequency–frequency covariance matrix; first $N_\mathrm{fg}$ eigenmodes removed
- Multiscale PCA (mPCA, Carucci+2025) is more efficient, preserving large-scale modes
- Signal loss is unavoidable, characterised by a **foreground transfer function** $T(k)$ derived from mock-injection (Switzer+2015; Cunnington+2023b)
- Power spectra and auto-power error budgets are corrected by $1/T(k)$ (not $1/T(k)^2$)

### Map Regridding (Sec. 4)
- Spherical sky maps are regridded into Cartesian volumes for Fourier analysis
- Naive regridding biases large-area surveys; the bias-mitigated regridding scheme of Cunnington & Wolz (2024) is used

### Cross-Correlation Detections (Sec. 5)

| Detection | Reference | Data | Significance | Constraint |
|-----------|-----------|------|--------------|------------|
| MeerKAT × WiggleZ pilot | Cunnington et al. 2023a (arXiv:2206.01579) | 10.5 hr L-band, ~200 deg², 0.400 < z < 0.459 | 7.7σ | $\Omega_\mathrm{HI} b_\mathrm{HI} r = (0.86 \pm 0.10_\mathrm{stat} \pm 0.12_\mathrm{sys}) \times 10^{-3}$ at $k_\mathrm{eff} \sim 0.13\,h\,\mathrm{Mpc}^{-1}$ |
| MeerKLASS L-band deep-field × GAMA | MeerKLASS Collaboration 2025 (arXiv:2407.21626; see `meerklass2025_lband_deepfield.md`) | 41 scans, 236 deg², **62 hr per dish** before flagging | > 4σ | 0.39 < z < 0.46 |
| MeerKLASS pilot × WiggleZ re-analysis | Carucci et al. 2025 (arXiv:2412.06750) | Same data as Cunnington+2023, mPCA pipeline | ~6σ (without signal-loss correction) | $\Omega_\mathrm{HI} b_\mathrm{HI} r = (0.93 \pm 0.17) \times 10^{-3}$, robust over $0.04 \lesssim k \lesssim 0.3\,h\,\mathrm{Mpc}^{-1}$ |

The L-band deep field crosses into the regime where thermal noise is no longer dominant compared to HI fluctuations, requiring more sophisticated covariance estimation.

### Fisher Forecast (Sec. 6, Appendix A) — `MeerFish`

**Forecast configuration (Table 2):**

| Parameter | MeerKLASS UHF | SKAO-Mid Band 1 |
|-----------|---------------|-----------------|
| $\nu_\mathrm{min}$ | 580 MHz | 350 MHz |
| $\nu_\mathrm{max}$ | 1,000 MHz | 1,050 MHz |
| $z_\mathrm{min}$ | 0.4 | 0.35 |
| $z_\mathrm{max}$ | 1.45 | 3 |
| $\delta\nu$ | 132.8 kHz | 10.8 kHz |
| Survey area $A_\mathrm{sur}$ | **10,000 deg²** | 20,000 deg² |
| Total time $t_\mathrm{tot}$ | **2,500 hr** | 10,000 hr |
| Survey efficiency $\varepsilon$ | **0.5** | 0.5 |
| Useable observation time $t_\mathrm{obs}$ | **1,250 hr** | 5,000 hr |
| $N_\mathrm{dish}$ | 64 | 197 |
| $D_\mathrm{dish}$ | 13.5 m | 15 m (approximate) |

A **conservative 50% RFI loss factor** is applied to the nominal 2,500 hr to obtain the effective 1,250 hr used in all forecast results.

**Pipeline-relevant equations from Appendix A:**

- HI bias (Villaescusa-Navarro et al. 2018 hydro fit, Eq. A3):
  $$b_\mathrm{HI}(z) = 0.842 + 0.693\,z - 0.0459\,z^2$$
- Mean HI brightness temperature (Eq. A4):
  $$\bar T_\mathrm{HI}(z) = 180\,\Omega_\mathrm{HI}\,h\,\frac{(1+z)^2}{H(z)/H_0}\;\mathrm{mK}$$
  Note the **180 mK** prefactor (Cunnington+2023 / Battye+2013), *not* the 188 mK form used in `hi_model.T_bar_b` (Pinetti 2020 / Padmanabhan 2017 convention).
- HI density (SKA Cosmology SWG 2020 model, adapted to MeerKLASS data, Eq. A5):
  $$\Omega_\mathrm{HI}(z) = 0.00067432 + 0.00039\,z - 0.000065\,z^2$$
- **System temperature decomposition (Eq. A19, page 35):**
  $$T_\mathrm{sys}(\nu) = T_\mathrm{rx}(\nu) + T_\mathrm{spl} + T_\mathrm{CMB} + T_\mathrm{gal}(\nu)$$
  with $T_\mathrm{spl} = 3$ K (spillover), $T_\mathrm{CMB} = 2.725$ K, $T_\mathrm{rx}(\nu)$ tuned to match measured MeerKAT receiver noise (Cunnington 2022), and the **Galactic synchrotron contribution**
  $$T_\mathrm{gal}(\nu) = 15\,\mathrm{K}\,\left(\frac{408\,\mathrm{MHz}}{\nu}\right)^{2.75}$$
  tuned to match the average sky temperature excluding $|b| < 10°$. **The 15 K coefficient is what Cunnington+2025 explicitly publishes**, *not* the 25 K coefficient sometimes used in earlier MeerKAT noise budgets. The pipeline currently uses 25 K in `noise_model.T_sys_meerkat` (lines 55, 72) — this is a discrepancy with this paper that needs reconciliation. See `docs/scratch.md` and the Phase 0 audit findings.
- Observed HI power spectrum (Eq. 19): $P_\mathrm{HI}^\mathrm{obs}(k,\mu) = P_\mathrm{HI}(k,\mu)\,B^2_\mathrm{beam}(k,\mu) + P_N$
- Multipole expansion: monopole + quadrupole + hexadecapole $\{P_0, P_2, P_4\}$ used to break the $b_\mathrm{HI}$–$f$ degeneracy

**Key forecast results (Sec. 6.1–6.4):**
- Forecast S/N on $P_0$ at $k = 0.02\,h\,\mathrm{Mpc}^{-1}$ rivals DESI DR2 LRG/ELG/QSO across the available UHF redshift range
- Wide-and-shallow strategies are preferred (Sec. 6.1.1): cosmic variance dominates over thermal noise, so spreading time over more area pays off
- Strong $f_\mathrm{NL}$ leverage from access to ultra-large modes
- Cross-correlation with Rubin/DESI provides multi-tracer gains, especially for $f_\mathrm{NL}$

## Key Observational Specifications (for forecast use)

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Receiver (current) | UHF, 580–1000 MHz cosmological window (full bandpass 544–1088 MHz) | Sec. 2, Table 2 |
| Receiver (legacy) | L-band, 971–1023 MHz cosmological window (full bandpass 900–1670 MHz) | Sec. 2 |
| Useable z (UHF) | 0.40 < z < 1.45 | Table 1, Table 2 |
| Useable z (L-band) | 0.39 < z < 0.46 (RFI-limited) | Sec. 2, Table 1 |
| Number of dishes | 64 | Table 2 |
| Dish diameter | 13.5 m | Table 2 |
| Channel width (UHF, default) | 132.8 kHz | Table 2 |
| Survey efficiency | $\varepsilon = 0.5$ (50% RFI loss) | Table 2 |
| L-band pilot (Cunnington+2023a) | 10.5 hr, ~200 deg², z ≈ 0.43 | Sec. 5.1, also Cunnington+2023 abstract |
| L-band deep-field (MeerKLASS Collab 2025) | 62 hr/dish, 236 deg², 41 scans | Sec. 5.1, also arXiv:2407.21626 |
| 2024 cumulative UHF | 380 hr / 1,600 deg² | Table 1 |
| 2025 cumulative UHF (in progress) | 880 hr / 3,600 deg² | Table 1 |
| **Forecast: 2028 XLP target** | **2,500 hr / 10,000 deg² UHF, ε = 0.5 → 1,250 hr effective** | Table 1, Table 2, Sec. 6 |
| Pre-SKAO continuation (2030) | 3,500 hr / 14,000 deg² | Table 1 |
| HI bias model | $b_\mathrm{HI}(z) = 0.842 + 0.693z - 0.0459z^2$ | Eq. A3 |
| Mean HI brightness | $\bar T_\mathrm{HI}(z) = 180 \Omega_\mathrm{HI} h (1+z)^2 H_0/H(z)$ mK | Eq. A4 |
| HI density model | $\Omega_\mathrm{HI}(z) = 6.7432\times10^{-4} + 3.9\times10^{-4} z - 6.5\times10^{-5} z^2$ | Eq. A5 |
| Forecast multipoles | $\{P_0, P_2, P_4\}$ | Sec. 6.1.1 |
| Forecast code | `MeerFish` (https://github.com/meerklass/MeerFish) | Sec. 6 |

## Repository Use

This is the *authoritative* MeerKLASS single-dish HI intensity-mapping reference for the HI×UGRB cross-correlation forecasts in `hi_gamma_xcorr/`. It supersedes the conservative DR1-grade hours quoted in the commensal interferometric-continuum papers (Mangla et al. 2025, Paul et al. 2025) for any HI single-dish noise calculation.

In `config.RADIO_TELESCOPES` it is used to populate:

1. **`MeerKLASS_L_deepfield`** — 62 hr / 236 deg² L-band deep-field HI integration (Sec. 5.1, citing MeerKLASS Collaboration 2025 = arXiv:2407.21626; the source paper is now ingested at `docs/literature/meerklass2025_lband_deepfield.md`).
2. **`MeerKLASS_2024_HI`** — 380 hr / 1,600 deg² UHF, the cumulative single-dish HI total at end of 2024 (Table 1).
3. **`MeerKLASS_XLP_2028`** — 2,500 hr / 10,000 deg² UHF nominal with $\varepsilon = 0.5$ → 1,250 hr effective, the same configuration the paper uses for all its public forecasts (Table 2, Sec. 6).

Additionally, this paper provides:

- A direct **180 mK vs 188 mK** discrepancy with `hi_model.T_bar_b`. The pipeline default `T_bar_b` uses 188 mK (Padmanabhan 2017 / Pinetti 2020 convention); Cunnington 2025 Eq. A4 — and the earlier Cunnington 2023 Eq. 15 — both use 180 mK (Battye+2013 convention). This shifts the absolute brightness amplitude by ~4% and propagates into all HI×anything cross-correlations.
- A consistent $\Omega_\mathrm{HI}(z)$ polynomial (Eq. A5) and matched $b_\mathrm{HI}(z)$ polynomial (Eq. A3, fit to Villaescusa-Navarro et al. 2018 hydro simulations).
- A reference Fisher pipeline (`MeerFish`) the package can be cross-validated against.

These are all now exposed in the pipeline as a third HI brightness mode, **`'cunnington'`** (aliases: `'meerfish'`, `'cunnington2025'`):

- `hi_model.Omega_HI_cunnington(z)` — Eq. A5 polynomial
- `hi_model.b_HI_cunnington(z)` — Eq. A3 polynomial
- `hi_model.T_bar_b_cunnington(z)` — Eq. A4, 180 mK + Eq. A5 polynomial Ω_HI
- `hi_model.T_bar_b_for_model(z, 'cunnington')` — dispatch entry

All HI-touching plotting cells in `notebooks/pipeline_validation.ipynb` (HI model properties, cross-power spectrum, normalised window functions, SNR forecast bar chart, DM exclusion curves) have been updated to overlay the Cunnington 2025 result as a **dash-dotted** line/bar alongside the Padmanabhan (solid) and fixed-$\Omega_\mathrm{HI}$ (dashed) variants.
