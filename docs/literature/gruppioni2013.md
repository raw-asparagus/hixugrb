# Gruppioni et al. (2013) — IR Luminosity Function (SFG)

**Authors:** C. Gruppioni, F. Pozzi, G. Rodighiero, et al.
**Journal:** MNRAS 432(1), 23–52
**arXiv:** [1302.5209](https://arxiv.org/abs/1302.5209)

## Abstract

Derives the infrared luminosity function evolution of star-forming galaxies to z ~ 4 using deep Herschel PACS (70, 100, 160 um) and HerMES (250, 350, 500 um) data from the PEP survey. Covers rest-frame 35, 60, 90 um and total IR luminosity functions.

## Methodology

- Herschel PEP/HerMES deep far-IR photometry
- Bayesian SED fitting to galaxy spectral energy distributions
- Modified Schechter function fits with redshift-dependent parameters
- Population decomposition: main sequence vs starburst

## Key Results

**IR luminosity evolution:**
- z < 2: $L_\text{IR} \propto (1+z)^{3.55 \pm 0.10}$
- z > 2: $L_\text{IR} \propto (1+z)^{1.62 \pm 0.51}$

**IR density evolution:**
- z < 1: $\Phi \propto (1+z)^{-0.57 \pm 0.22}$
- z > 1: $\Phi \propto (1+z)^{-3.92 \pm 0.34}$

IR luminosity density tracks cosmic star formation rate history: steep increase to z~1, plateau z~1–3, decline for z > 3.

## Equations and Parameters Used

**Gamma-ray conversion (from literature):**
$$L_\gamma \propto L_\text{IR}^{1.17 \pm 0.07}$$

This combined with Gruppioni's (1+z)^{3.55} gives effective gamma-ray evolution (1+z)^{~4.15} for z < 2.

**Parameters adopted (calibrated LDDE approximation):**

| Parameter | Value | Notes |
|-----------|-------|-------|
| A | 1 × 10⁻⁸ | Mpc⁻³ (calibrated to ~10–30% IGRB) |
| L_c | 5 × 10⁴⁰ | erg/s (L* for gamma-ray SFGs) |
| gamma_1 | 0.4 | faint-end |
| gamma_2 | 2.5 | bright-end |
| z_c* | 2.0 | cosmic SFR peak |
| p_1 | 3.55 | **directly from Gruppioni** |
| p_2 | −4.0 | rapid decline after z~2 |
| Spectral index | 2.7 | from Pinetti Table 3 |

## Implementation

**Module:** `astro_sources.py` — `_SFG_PARAMS`, `_glf_SFG()`, piecewise LDDE. The p_1=3.55 evolution index is the primary quantitative result adopted from this paper.
