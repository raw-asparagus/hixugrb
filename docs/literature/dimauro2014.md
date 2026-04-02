# Di Mauro et al. (2014) — mAGN Gamma-Ray Emission

**Authors:** M. Di Mauro, F. Calore, F. Donato, M. Ajello, L. Latronico
**Journal:** ApJ 780(2), 161
**arXiv:** [1305.4200](https://arxiv.org/abs/1305.4200)

## Abstract

Calculates diffuse gamma-ray emission from unresolved misaligned AGN (radio galaxies). Establishes a physical L_gamma–L_radio correlation validated by statistical tests and Fermi-LAT source counts.

## Methodology

- L_gamma–L_radio correlation from radio-loud AGN sample
- Gamma-ray luminosity function derived from radio galaxy population
- Constrained by Fermi-LAT source-count distribution
- Mean photon index: Gamma = 2.37 +/- 0.32

## Key Results

- IGRB contribution: 10–83% (wide range from theoretical uncertainties)
- Radio-to-gamma correlation is physical and robust
- ~500–1000× more numerous than blazars (geometric factor)
- Significant intensity contribution but negligible anisotropy (many faint sources)

## Parameters Used in This Pipeline (calibrated)

| Parameter | Value | Notes |
|-----------|-------|-------|
| A | 3.0 × 10⁻⁸ | Mpc⁻³ (calibrated to ~25% IGRB) |
| L_c | 5 × 10⁴⁴ | erg/s |
| gamma_1 | 0.60 | faint-end |
| gamma_2 | 2.00 | bright-end |
| z_c* | 0.8 | tracks radio AGN evolution |
| p_1 | 3.5 | moderate positive evolution |
| p_2 | −2.0 | negative at high z |
| Spectral index | 2.37 | from Pinetti Table 3 |

**Note:** These are calibrated approximations, not directly from the paper's tables. The original work derives the GLF indirectly from radio LF via L_gamma–L_radio correlation.

## Implementation

**Module:** `astro_sources.py` — `_MAGN_PARAMS`, `_glf_mAGN()`, piecewise LDDE.
