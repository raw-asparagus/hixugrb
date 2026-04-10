# Paul et al. (2025) — MeerKLASS UHF On-the-Fly Continuum Survey: Data Release I

**Authors:** S. Paul, K. Grainge, M. G. Santos, S. Chatterjee, S. Mangla, L. Wolz, J. J. Mohr, O. Smirnov, C. Tasse, K. Rozgonyi, M. Hoeft, Y. Perrott
**Journal:** MNRAS, submitted (preprint 16 December 2025)
**arXiv:** [2512.11964](https://arxiv.org/abs/2512.11964)

## Abstract

First public data release (DR1) from the *interferometric* component of the MeerKLASS UHF survey, demonstrating the on-the-fly (OTF) mapping technique at large scale. Eight OTF scan blocks taken between February and July 2023 (four rising + four setting) cover ~800 deg² in the southern sky inside the DESI footprint and total ~12 hr of usable on-source time. Visibility-domain mosaicking with `DDFacet` produces an 89-tile mosaic at the UHF band centre (816 MHz), reaching an RMS sensitivity of ~35 μJy beam⁻¹ in the deepest overlap regions and a typical resolution of ~32″ × 17″. The release contains a catalogue of **95,483 radio sources**. The paper validates astrometry, flux scale, and differential source counts against RACS / NVSS / FIRST. The full MeerKLASS programme is targeting 10,000 deg² over ~2,500 hr of nighttime observing in the UHF band; ~270 hr of UHF pilot data have been acquired since the transition from L-band in 2022.

## Methodology

### Survey Configuration
- **Instrument:** MeerKAT, 64 dishes × 13.5 m, UHF receivers (544–1088 MHz)
- **Mode:** OTF interferometric, commensal with single-dish HI intensity mapping (e.g. Cunnington+2023; Cunnington+2025, arXiv:2510.27549). Constant-elevation slewing at ~7′ s⁻¹ in azimuth, driven by the single-dish HI mode.
- **Footprint (DR1):** ~800 deg² inside the DESI survey area, with maximally overlapping cross-hatch where rising × setting tracks intersect
- **Blocks used in DR1:** 8 OTF scan blocks (4 rising + 4 setting), each ~1.5 hr (Table 1 of paper); 4 rising blocks share three-way overlap; 4 setting blocks cross-link.
- **Total OTF on-source time (DR1):** ~12 hr
- **Calibrators:** primary J0408−6545 or J1331+3030 (bandpass + flux); secondary J1051−2023 or J1058+0133 (gain)
- **Survey speed:** ~150 deg² hr⁻¹ nominal; one-hour UHF pass images ~300 deg² to ~100 μJy beam⁻¹
- **Time resolution:** 2 s visibility integrations
- **Frequency channels:** 4096 across 544 MHz of bandwidth

### Cross-Linked OTF Strategy
"Rising" and "setting" passes use the same constant-elevation azimuth track, so Earth rotation projects them at orthogonal angles in equatorial coordinates, producing a cross-hatched pattern. This reduces direction-dependent systematics and striping artefacts versus single-direction scans, and is key to averaging primary-beam asymmetries.

### Calibration Pipeline
- RFI flagging via `Tricolour` (Hugo et al. 2022) integrated in `CARACal` (Józsa et al. 2020), implementing a MeerKAT-tuned SumThreshold algorithm. Flagging fractions modest near band centre, increasing toward edges.
- Custom "rogue antenna" detector flags antennas whose pointing deviates by more than ~0.1° from the array median during the slew.
- Calibration uses the standard `KGBAKGB` sequence (delays K, gains G, bandpass B, leakage A) on the primary, then `KGAKF` on the secondary applying the primary B solution to anchor the absolute flux scale. Most terms solved at solint=inf; final gains at 60 s.

### OTF Phase Centre Correction (Sec. 3.3)
Same physical effect as in the L-band DR1: the correlator delay centre is held at fixed (az, el) while the antennas slew, producing two artefacts:

1. **Fringe rotation** at the visibility level — corrected with `CHGCENTRE` (WSClean; Offringa et al. 2014) at the native 2 s cadence using the reference antenna metadata.
2. **Intra-2 s decoherence (time-smearing)** — addressed inside the customised `DDFacet` imaging by constructing an effective fringe-rate-dependent PSF that explicitly models the smearing in both minor and major deconvolution cycles. This broadens the synthesised beam but preserves flux accuracy.

A companion methodology paper (Chatterjee et al. 2025) provides the full derivation.

### Imaging Workflow (Sec. 4)
- Sky split into 89 tiles of 3.2° × 3.2° with 0.1° overlap
- Each tile selects all measurement sets within a 4° × 4° region (Fig. 3 schematic)
- Imaging with `DDFacet` (Tasse et al. 2018) at 8400 × 8400 px / 3″ pixels → ~7° image size, with a 36 × 36 facet grid (1296 facets, ~0.19° each)
- Briggs robust = 0; SSD2 deconvolution
- Two-pass scheme (auto-mask → external mask via `MakeMask.py` at 5σ → re-image with `--Predict-InitDicoModel`)
- `killMS` direction-independent self-cal at 60 s, smoothed in time/frequency
- Final imaging pass with fixed CLEAN masks
- Frequency-dependent UHF primary-beam restoration

### Source Extraction (Sec. 6)
- Source finding with `PyBDSF`
- Cross-tile de-duplication at 3″
- Catalogue: **~95,483 unique sources**
- Cross-validated against RACS-low/-mid, NVSS, FIRST: sub-arcsecond astrometric systematic; flux scale agrees with external surveys
- Differential source counts agree with literature, validating the pipeline end-to-end

### Flux-Error Treatment (Appendix B)
Same OTF-induced asymmetry as in the L-band DR1: the source PSF is broadened by an RA-direction top-hat smearing kernel while the noise PSF is not. The catalogue's flux-density uncertainties therefore include the geometric boost factor √(Ω_source/Ω_noise), with the working SNR definition following the L-band release.

## Key Results

- 89-tile, ~800 deg² UHF Stokes I continuum mosaic at 816 MHz with **deepest RMS ~35 μJy beam⁻¹** and median resolution **~32″ × 17″**
- Catalogue of **95,483 unique sources** (≈100k post-de-duplication)
- Sub-arcsecond astrometric systematic; differential source counts validated against RACS, NVSS, FIRST
- Demonstrates that ~12 hr of OTF UHF observing time, distributed across 8 cross-linked blocks, is sufficient to deliver a science-ready wide-area continuum survey
- Establishes a path to the full MeerKLASS programme: 10,000 deg² over ~2,500 hr of nighttime observing in the UHF band

## Key Observational Specifications

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Receiver | UHF, 544–1088 MHz | Sec. 1, Sec. 2 |
| Central frequency | 816 MHz | Abstract |
| Dish diameter | 13.5 m | Sec. 1 |
| Number of dishes | 64 | Sec. 1 |
| Survey area (DR1) | ~800 deg² (DESI footprint) | Abstract, Sec. 2 |
| OTF on-source time (DR1) | ~12 hr (4 rising + 4 setting blocks) | Sec. 2, Table 1 |
| Total UHF pilot acquired since 2022 | ~270 hr (single-dish + interferometric) | Sec. 1 |
| Full MeerKLASS programme goal | 10,000 deg² in ~2,500 hr night-time, UHF | Sec. 1 |
| Survey speed | ~150 deg² hr⁻¹ | Sec. 2 |
| Scan speed | 7 arcmin s⁻¹ | Sec. 2 |
| Scan stripe | ~18° in azimuth over ~200 s | Sec. 2 |
| Visibility integration | 2 s | Sec. 2 |
| Tile size | 3.2° × 3.2° (89 tiles) | Sec. 4 |
| Median synthesised beam | ~32″ × 17″ | Abstract |
| Pixel scale | 3″ | Sec. 4 |
| Field of view (UHF) | ~2.8° at low band edge → ~1.4° at high band edge | Sec. 2 |
| Deepest RMS | ~35 μJy beam⁻¹ at 816 MHz | Abstract, Sec. 5.1 |
| Median dynamic range | ~542 (16th–84th: 306–718) | Sec. 5.2 |
| Sources catalogued | 95,483 unique | Abstract, Sec. 8 |
| Astrometric systematic | < 1″ | Abstract |

## Repository Use

This paper is the **interferometric continuum** DR1 of the MeerKLASS UHF programme; it is *not* an HI intensity-mapping data release. The corresponding HI single-dish overview is Cunnington et al. (2025), arXiv:2510.27549 (see `docs/literature/cunnington2025_meerklass_overview.md`), which reports cumulative UHF totals of 110 hr / 500 deg² (end 2023), 380 hr / 1,600 deg² (end 2024), and the awarded XLP target of 2,500 hr / 10,000 deg² by end of 2028.

For the HI×UGRB cross-correlation pipeline this paper is used to:

1. Anchor the MeerKLASS UHF observational footprint and OTF observing strategy.
2. Populate the dish/receiver parameters in `config.RADIO_TELESCOPES['MeerKLASS_DR1_UHF']` — 64 × 13.5 m dishes, UHF 544–1088 MHz, OTF cross-linked scans.
3. Fix the UHF frequency edges and the corresponding HI redshift range $z \in [0.31, 1.61]$ used for forecast SNR computations.
4. Provide the planned-survey scaling (10,000 deg² / 2,500 hr) used in `MeerKLASS_full` projection forecasts.

As with the L-band DR1, the `t_obs_hours = 12` and `survey_area_deg2 = 800` populated in `config.py` for `MeerKLASS_DR1_UHF` reflect the **DR1-grade interferometric** values quoted in this paper, **not** the cumulative single-dish HI integration time on the same field. They are the most conservative published values. For HI single-dish forecasts use the Cunnington+2025-derived entries `MeerKLASS_2024_HI` (380 hr / 1,600 deg² UHF, current state) or `MeerKLASS_XLP_2028` (2,500 hr / 10,000 deg² UHF nominal with ε = 0.5, the awarded XLP target).
