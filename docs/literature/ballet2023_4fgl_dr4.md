# Ballet, Bruel, Burnett & Lott (2023) — Fermi LAT Fourth Source Catalog Data Release 4 (4FGL-DR4)

**Authors:** J. Ballet, P. Bruel, T. H. Burnett, B. Lott (Fermi-LAT Collaboration)
**Status:** arXiv preprint (Draft v4 dated 25 July 2024)
**arXiv:** [2307.12546](https://arxiv.org/abs/2307.12546) (v4)

## Abstract

The fourth incremental release of the Fermi-LAT Fourth Source Catalog, **4FGL-DR4**, based on **14 years of Pass 8 R3 science data** (4 August 2008 – 2 August 2022) over the energy range **50 MeV – 1 TeV**. Contains **7,194 γ-ray sources** — adds 546 point sources, modifies 4 extended sources, and adds 4 new ones over the 12-year DR3 release. Uses the same `pointlike`/`gtlike` analysis methods, the same diffuse model (`gll_iem_v07` for the Galactic interstellar emission, `iso_P8R3_SOURCE_V3_v1` for isotropic), and the same TS ≥ 25 detection threshold as DR3, with only minor improvements (smooth Galactic-diffuse modulation, priors on curvature). **The detection threshold outside the Galactic plane is reported as "a little above 1 × 10⁻¹² erg cm⁻² s⁻¹ in the 100 MeV to 100 GeV band"** (§5, p12). This is the canonical 4FGL-DR4 high-Galactic-latitude completeness reference. For HI×UGRB cross-correlation forecasts, the relevant photon-flux equivalent (in Pinetti's 1-100 GeV convention) is **~7-9 × 10⁻¹¹ photon cm⁻² s⁻¹**, depending on source spectral index — only ~25-50% lower than Pinetti+2020's $F_\mathrm{SENS} = 10^{-10}$ assumption, *not* 25× lower as first appearances might suggest.

## Methodology

### Observation Period & Data Selection (Sec. 2.1)
- **Time range**: 4 August 2008 (15:43 UTC) → 2 August 2022 (21:53 UTC), **14 years**
- **Operation mode**: Sky-scanning survey mode (rocking ±north/south of zenith) until 8 April 2018; partial sky-scanning since
- **Solar/GRB excisions**: 54 ks excised due to bright solar flares between Jul 2021 and Jan 2022, plus ~1 ks around 3 new bright GRBs (2020-2022)
- **Instrument response**: Pass 8 R3 V3 (P8R3_V3 IRFs; Atwood et al. 2013, Bruel et al. 2018) — unchanged from DR1/2/3
- **Energy range**: 50 MeV – 1 TeV
- **Data split**: same 19 components with the same zenith-angle selections as DR3

### Diffuse Background Model (Sec. 2.2)
- **Galactic interstellar**: `gll_iem_v07` (Fermi-LAT Collaboration standard, unchanged from DR3)
- **Isotropic**: `iso_P8R3_SOURCE_V3_v1` (unchanged from DR3)
- **Improvement over DR3**: smooth full-sky LP modulation of the Galactic diffuse component, computed by smoothly interpolating per-RoI LogParabola fits across neighbouring RoI boundaries (rather than discrete RoI-by-RoI normalisations as in DR3). This avoids sharp jumps at RoI boundaries and slightly improves the source detection — adds 71 sources above threshold and reduces the number of curved spectra by 245 vs DR3.

### Detection (Sec. 3.3)
- **Method**: same as DR3 — `pointlike` detection on 14-year residual TS maps, started from the DR3 source list, relocalised over 14 years, peaks identified, refit, iterated.
- **Test Statistic**: $\mathrm{TS} = 2 \log(\mathcal{L}/\mathcal{L}_0)$ comparing the maximum likelihood with the source against without; **TS ≥ 25 detection threshold** (~5σ for one degree of freedom).
- **Seed list `uw1410`**: 11,700 seeds at TS > 10 from the iterative procedure, of which 4,846 new seeds entered the final `gtlike` characterisation pass alongside 6,569 DR3 point sources and 82 extended sources.
- **Localisation**: 95% systematic error increased to 28.5″ (was 25″ at high latitudes in DR3); systematic factor 1.075.

### Spectral Models (Sec. 3.4)
- **Power Law (PL)**: dominant for sources with TS_curv < 4
- **LogParabola (LP)**: 3,076 sources (down from 3,131 in DR3) — slight prior on the curvature parameter β added, making it slightly harder to reach the TS_curv > 4 threshold
- **PLEC4 (super-exponential cutoff)**: 276 sources (up from 258), used mostly for pulsars
- Overall fraction with curved spectral models: **47%** (down from 51% in DR3)

### Source Counts (Sec. 5)
- **Total sources**: **7,194** (up from 6,658 in DR3)
- **New sources**: 546
- **Deleted from DR3**: 14
- **New extended sources**: 4 (Cygnus Loop, Puppis A, SNR G292.2−0.5, SNR G51.3+0.1, plus 3C 58 and CTB 80 — see Table 2)
- **Sources at TS > 100 (new in DR4)**: 11, of which 8 are blazars

### Detection Threshold (Sec. 5, p12) — most relevant for the pipeline

The paper quotes (verbatim, page 12):

> *"The detection threshold outside the Galactic plane decreased but remains a little above $1 \times 10^{-12}$ erg cm⁻² s⁻¹ in the 100 MeV to 100 GeV band."*

**Important notes about this value**:
1. **Energy flux** units (erg cm⁻² s⁻¹), not photon flux
2. **Integrated over 100 MeV to 100 GeV**, not 1-100 GeV
3. **Outside the Galactic plane** (i.e., $|b| > 10°$ — and well within the $|b| > 30°$ cut used by Ammazzalorso 2018b)
4. The threshold *decreased* slightly relative to DR3 (12-year) due to the additional 2 years of data (~17% more exposure), but is still close to $10^{-12}$ erg cm⁻² s⁻¹ — i.e., the catalogue is now ~exposure-limited rather than software-limited.

### Conversion to photon-flux units (the pipeline convention)

For a power-law source $dN/dE = N_0 E^{-\alpha}$, the average photon energy in band $[E_1, E_2]$ is

$$\langle E_\mathrm{ph} \rangle = \frac{F_E}{F_\mathrm{ph}} = \frac{(E_2^{2-\alpha} - E_1^{2-\alpha})/(2-\alpha)}{(E_2^{1-\alpha} - E_1^{1-\alpha})/(1-\alpha)}$$

and the photon flux is $F_\mathrm{ph} = F_E / \langle E_\mathrm{ph} \rangle$. To convert from $F_E$ in 100 MeV - 100 GeV (as quoted by 4FGL-DR4) to $F_\mathrm{ph}$ in 1-100 GeV (Pinetti's convention), additionally apply the photon-band fraction.

For each source class in the pipeline:

| Source class | $\alpha$ | $\langle E_\mathrm{ph} \rangle$ in 0.1-100 GeV | $F_\mathrm{ph}$ in 0.1-100 GeV [cm⁻² s⁻¹] | $F_\mathrm{ph}$ in **1-100 GeV** [cm⁻² s⁻¹] |
|---|---|---|---|---|
| BL Lac | 2.11 | 0.537 GeV | $1.16 \times 10^{-9}$ | $\mathbf{8.97 \times 10^{-11}}$ |
| FSRQ | 2.44 | 0.312 GeV | $2.00 \times 10^{-9}$ | $\mathbf{7.26 \times 10^{-11}}$ |
| mAGN | 2.37 | 0.342 GeV | $1.83 \times 10^{-9}$ | $\mathbf{7.78 \times 10^{-11}}$ |
| SFG | 2.70 | 0.241 GeV | $2.59 \times 10^{-9}$ | $\mathbf{5.17 \times 10^{-11}}$ |
| UGRB-average | 2.30 | 0.379 GeV | $1.65 \times 10^{-9}$ | $8.24 \times 10^{-11}$ |

**Mean over the four source classes: $7.3 \times 10^{-11}$ photon cm⁻² s⁻¹**.

This is the value adopted as `cfg.F_SENS_4FGL_DR4`. For comparison, Pinetti+2020 uses $F_\mathrm{SENS} = 10^{-10}$ photon cm⁻² s⁻¹ in the same band, so the 4FGL-DR4 threshold is about **0.73× Pinetti** — a modest ~25% improvement, *not* the factor-of-25 improvement that a naive comparison of "$10^{-12}$ erg" vs "$10^{-10}$ photon" might suggest. The previous pipeline value of $4 \times 10^{-12}$ photon cm⁻² s⁻¹ was a units-confusion error and has been corrected.

### Source Catalogue
- **FITS file**: `gll_psc_v32.fit` (the canonical 4FGL-DR4 source list)
- **Available from**: Fermi Science Support Center, `https://fermi.gsfc.nasa.gov/ssc/data/access/lat/14yr_catalog/`
- **Public**: yes, including per-source flux/spectrum/position/classification + per-energy-bin SEDs

## Key Results

- **7,194 γ-ray sources** in 14 years of Pass 8 R3 data (the most up-to-date public Fermi-LAT catalogue as of mid-2024 / early 2025)
- **High-Galactic-latitude completeness**: $F_\mathrm{thr} \gtrsim 1 \times 10^{-12}$ erg cm⁻² s⁻¹ in 100 MeV – 100 GeV
- **Equivalent photon flux** (1-100 GeV, source-class average): $\sim 7 \times 10^{-11}$ photon cm⁻² s⁻¹ — about 0.73× Pinetti+2020's assumption
- 191 new blazars, of which 25 BLLs, 28 FSRQs, 138 BCUs (Blazar Candidates of Uncertain type)
- 18 new pulsars (17 millisecond, 1 young)
- 4 new extended sources (3C 58, SNR G292.2−0.5, SNR G51.3+0.1, CTB 80)

## Repository Use

This is the **canonical reference for the 4FGL-DR4 detection threshold** used by the pipeline's `unresolved_mode = '4fgl_dr4_psf'` dispatch (the default for all `MeerKLASS_*` canonical-mode telescope entries). It is the authoritative source for:

1. **`cfg.F_SENS_4FGL_DR4`** = $7.3 \times 10^{-11}$ photon cm⁻² s⁻¹ (1-100 GeV, source-class average)
2. **`cfg.F_SENS_4FGL_DR4_ERG_CGS`** = $1 \times 10^{-12}$ erg cm⁻² s⁻¹ (100 MeV – 100 GeV) — the directly-quoted value from §5/p12 of this paper, kept as a per-source-class conversion anchor
3. **The fact that the 4FGL-DR4 threshold is roughly comparable to Pinetti's** rather than orders of magnitude lower — important for understanding why switching from the Pinetti to the 4FGL-DR4 mode produces only a ~5–10% SNR shift, not a ~50% shift
4. **The 14-year integration period** (Aug 2008 – Aug 2022), which is contemporaneous with the underlying Pass 8 dataset used by Ammazzalorso, Fornengo, Horiuchi & Regis 2018 (`docs/literature/ammazzalorso2018b_fermi_2mpz.md`, 108 months / 9 years up to Jul 2017) — making it a clean upgrade rather than a contradicting independent measurement
5. **The Pass 8 R3 V3 IRF** as the canonical Fermi-LAT instrument response from which the per-energy PSF (used by `noise_model.beam_fermi_exact`) is derived

### Convention used in `astro_sources.F_sens_energy`

The pipeline does *not* directly tabulate per-energy 4FGL-DR4 thresholds. Instead, it uses the Ammazzalorso, Fornengo, Horiuchi & Regis (2018) PSF-area scaling

$$F_\mathrm{sens}(E) = F_\mathrm{baseline} \cdot \left(\frac{\sigma_0(E)}{\sigma_0(E_\mathrm{ref})}\right)^2$$

with $E_\mathrm{ref} = 5$ GeV and $F_\mathrm{baseline} = $ `cfg.F_SENS_4FGL_DR4` $= 7.3 \times 10^{-11}$ photon cm⁻² s⁻¹. This emulates the energy dependence (poor PSF at low E → higher confusion threshold; good PSF at high E → lower threshold) that the actual catalogue completeness curve exhibits, anchored to the 4FGL-DR4 broad-band value reported here. A more rigorous treatment would use a per-energy completeness curve extracted directly from the 4FGL-DR4 catalogue file `gll_psc_v32.fit`; that's a future refinement once the FITS catalogue is loaded into the pipeline.

### Foundational reference chain

For citation completeness, the 4FGL-DR4 release is the latest in a sequence of 4FGL data releases:

| Catalogue | Reference | arXiv | Integration |
|---|---|---|---|
| 4FGL (DR1) | Abdollahi et al. 2020, ApJS 247, 33 | [1902.10045](https://arxiv.org/abs/1902.10045) | 8 years |
| 4FGL-DR2 | Ballet et al. 2020 | [2005.11208](https://arxiv.org/abs/2005.11208) | 10 years |
| 4FGL-DR3 | Abdollahi et al. 2022, ApJS 260, 53 | [2201.11184](https://arxiv.org/abs/2201.11184) | 12 years |
| **4FGL-DR4** | **Ballet et al. 2023** (this paper) | **[2307.12546](https://arxiv.org/abs/2307.12546)** | **14 years** |

The DR4 paper explicitly says (§1, p1): *"The reader is referred to the 4FGL and DR3 papers for the detailed methodology, and the official reference remains the DR3 paper."* So when citing both the methodology and the specific data release, cite **Abdollahi et al. 2020 (DR1)** for the analysis approach + **Ballet et al. 2023 (DR4)** for the 14-year data product. For the pipeline's purposes (just the threshold value), citing Ballet et al. 2023 alone is sufficient.
