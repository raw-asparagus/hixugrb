# Mangla et al. (2025) — MeerKLASS L-band On-the-Fly Continuum Survey: Data Release 1

**Authors:** S. Mangla, J. J. Mohr, K. Rozgonyi, S. Chatterjee, K. Grainge, S. Paul, M. G. Santos, Y. Perrott, O. M. Smirnov, C. Tasse, L. Wolz
**Journal:** MNRAS, submitted (preprint 22 December 2025)
**arXiv:** [2512.17685](https://arxiv.org/abs/2512.17685)

## Abstract

First public data release (DR1) of the *interferometric* component of the MeerKAT Large Area Synoptic Survey (MeerKLASS) L-band programme. Eight rising-scan blocks taken between September and October 2021 cover ~268 deg² in the southern sky and total ~13.5 hours of usable on-source time. A novel On-the-Fly (OTF) interferometric imaging strategy is used to convert continuously slewing 2 s visibilities into a 67-tile mosaic at 1284 MHz, reaching a median noise of 33 μJy beam⁻¹ at a median angular resolution of ~25.5″ × 7.8″. The release contains a catalogue of 34,874 radio sources detected at SNR > 9. The survey is commensal with the MeerKLASS single-dish HI intensity mapping programme and serves as a proof of concept for OTF imaging at SKA-Mid scale.

## Methodology

### Survey Configuration
- **Instrument:** MeerKAT, 64 dishes × 13.5 m, L-band receivers (856–1712 MHz)
- **Mode:** OTF interferometric (commensal with single-dish HI intensity mapping). The slow constant-elevation slew at ~10′/s in azimuth is *driven by* the single-dish HI mode (Wang+2021; Cunnington+2023), but interferometric visibilities are recorded simultaneously.
- **Footprint:** 268 deg² centred near RA 330°–360°, Dec −26° to −36°, overlapping KiDS-DR5 and the upcoming DESI-DR11
- **Blocks used in DR1:** 8 rising-scan blocks (Table 1 of paper); rising scans only because the setting-scan calibrator (Pictor A) is extended on interferometric baselines, complicating bandpass and gain calibration. DR2 will combine 41 rising+setting blocks at end of 2026.
- **Total OTF on-source time (DR1):** ~13.5 hr (each block ≈97–105 min on science target)
- **Calibrator:** primary J1934−638; ~20 min split between block start/end
- **Survey speed:** ~150 deg² hr⁻¹ nominal
- **Time resolution:** 2 s visibility integrations
- **Frequency channels:** 4096 across 856 MHz of bandwidth, divided into 7 sub-bands for spectral analysis

### Observation Strategy
- Constant-elevation azimuth slew (~10° throw) at ~10′/s, executed at high-elevation night-time LSTs to suppress ground spill, solar/ionospheric systematics
- Each science target normally observed twice per night (rising + setting cross-link); only rising scans are used in this DR1
- The dish primary beam progressively sweeps across the sky as the Earth rotates; the same sky position is observed many times with different effective pointing centres, averaging down beam asymmetries
- 40–50% of L-band data flagged for RFI (dominated by GNSS and satellite downlink)

### OTF Phase Centre Correction (Sec. 3.1.3)
The MeerKAT correlator holds the delay centre fixed in azimuth/elevation throughout each scan, so the geometric phase centre drifts relative to the actual array pointing centre. Two effects follow:

1. **Fringe rotation** — corrected post-correlation with `CHGCENTRE` (WSClean; Offringa et al. 2014), shifting the phase centre to the mean pointing per 2 s integration.
2. **Time-smearing** — partial decoherence within each 2 s integration; *not* fully removed at the visibility level. Modelled inside `DDFacet` (Tasse et al. 2018) by constructing an effective fringe-rate-dependent PSF and applying it self-consistently during deconvolution.

The residual time-smearing produces an anisotropic synthesised beam (elongated along RA), median ~25.5″ × 7.8″ at PA ≈ −88.9° in DR1. A new OTF-optimised correlator scanning mode adopted at MeerKAT in 2025 (which slowly steps the phase centre with the scan) removes this anisotropy and will be used in DR2.

### Imaging Workflow (Sec. 3.2)
- Sky split into 67 tiles of 2.15° × 2.15° with 0.075° overlap
- For each tile, a 2° × 2° centre region is selected; all snapshot visibilities whose pointings fall inside the 10 dB primary-beam contour at 1284 MHz are jointly imaged with `DDFacet`
- Image size 10240 × 10240 px at ~1.5″/px; SSD2 deconvolution; Briggs robust = 0
- Two-pass imaging (auto-mask → external mask seeded from first pass), then `killMS` direction-independent self-calibration at 60 s solution interval, then a final imaging run with fixed CLEAN masks
- Mosaic stitched from the 67 tiles using `Montage`

### Source Extraction & Validation
- Sources extracted with `PyBDSF`
- Final catalogue: **34,874 sources** at SNR > 9
- Astrometric accuracy: < 1.5″ relative to NVSS / TGSS / RACS-low / RACS-mid / RACS-high
- Flux density scale agrees with external surveys to within ~5%
- In-band spectral indices computed from the 7 sub-bands

### Flux-Error Calibration (Appendix B)
Because the delay centre is fixed during OTF, the source PSF is convolved with a top-hat in RA (smearing) but the noise PSF is *not* (independent random phases average out). Hence the source-response solid angle exceeds the noise-PSF solid angle. The flux-density uncertainty is therefore boosted by √(Ω_source/Ω_noise) ≈ √1.5 in DR1, and the catalogue uses
$$\mathrm{SNR} = \frac{S_\mathrm{peak}}{1.5\,\sigma_\mathrm{isl}}$$
following Chatterjee et al. (2025), Sec. 6.4.

## Key Results

- 67-tile, 268 deg² Stokes I continuum mosaic at 1284 MHz with **median noise 33 μJy beam⁻¹** and median resolution **25.5″ × 7.8″**
- Catalogue of **34,874 SNR > 9 sources** with in-band spectral indices
- Astrometric precision < 1.5″, flux-scale consistency within ~5% with NVSS/TGSS/RACS
- Differential source counts agree with prior surveys, validating the entire OTF + imaging chain
- DR1 demonstrates the viability of commensal OTF interferometric imaging alongside single-dish HI intensity mapping

## Key Observational Specifications

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Receiver | L-band, 856–1712 MHz | Sec. 2.2 |
| Dish diameter | 13.5 m | Sec. 2.2 |
| Number of dishes | 64 | Sec. 2.2 |
| Survey area (DR1) | 268 deg² | Abstract, Sec. 2.2 |
| OTF on-source time (DR1) | 13.5 hr usable (8 rising-scan blocks) | Sec. 2.2, Table 1 |
| Survey speed | ~150 deg² hr⁻¹ | Sec. 2.2 |
| Visibility integration | 2 s | Sec. 2.2 |
| Tile size | 2.15° × 2.15° (67 tiles) | Sec. 3.2.1 |
| Median synthesised beam | 25.5″ × 7.8″, PA −88.9° (anisotropic, time-smeared) | Sec. 3.4 |
| Pixel scale | 1.5″ | Sec. 3.2.2 |
| Median image RMS | 33 μJy beam⁻¹ at 1284 MHz | Abstract |
| Sources catalogued | 34,874 (SNR > 9) | Abstract |
| Astrometric accuracy | < 1.5″ | Sec. 4 |
| Flux-scale consistency | within 5% | Sec. 4 |
| RFI-flagged fraction | 40–50% across L-band | Sec. 3.1.1 |
| Spectral sub-bands | 7 (Freq-NBand 7) | Sec. 3.2.2 |
| DR2 release | 41 blocks (rising + setting), end of 2026 | Sec. 6 |

## Repository Use

This paper is the *interferometric continuum* sibling release to the MeerKLASS single-dish HI intensity mapping pipeline. The corresponding HI single-dish overview is Cunnington et al. (2025), arXiv:2510.27549 (see `docs/literature/cunnington2025_meerklass_overview.md`), which reports a much larger cumulative HI integration: 62 hr/dish over 236 deg² for the L-band deep-field (MeerKLASS Collaboration 2025, arXiv:2407.21626 — see `docs/literature/meerklass2025_lband_deepfield.md`), and 380 hr / 1,600 deg² UHF as of end-2024. **This paper is *not* an HI intensity-mapping data product**, and the 13.5 hr usable on-source time refers to interferometric continuum DR1 only — it is *not* the cumulative single-dish HI integration time on the MeerKLASS L-band field.

For the HI×UGRB cross-correlation pipeline this paper is used to:

1. Anchor the MeerKLASS L-band observational footprint (~268 deg² continuum / planned ~10,000 deg² UHF) and the OTF observing strategy.
2. Document the dish/receiver parameters used in single-dish HI noise forecasts (`config.RADIO_TELESCOPES['MeerKLASS_DR1_L']`): 64 × 13.5 m dishes, L-band 856–1712 MHz, single-dish mode driven by the same OTF scans.
3. Fix the L-band frequency edges (and corresponding HI redshift range $z \in [0, 0.66]$) used for forecast SNR computations.
4. Provide the time-smearing PSF context that is relevant when reconciling single-dish vs interferometric MeerKLASS beam-treatment in the noise model.

The forecast `t_obs_hours` and `survey_area_deg2` populated in `config.py` for `MeerKLASS_DR1_L` reflect the values quoted in this DR1 paper (13.5 hr / 268 deg²). These are deliberately conservative DR1-grade values — DR2 (end of 2026) will multiply them by ~5×. For HI single-dish forecasts, prefer `MeerKLASS_L_deepfield` (62 hr / 236 deg²), `MeerKLASS_2024_HI` (380 hr / 1,600 deg² UHF), or `MeerKLASS_XLP_2028` (2,500 hr / 10,000 deg² UHF, ε = 0.5), all derived from Cunnington et al. (2025).
