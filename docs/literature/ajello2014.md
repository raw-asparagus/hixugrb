# Ajello et al. (2014) — BL Lac Luminosity Function

**Authors:** M. Ajello, R. W. Romani, R. D'Abrusco, et al.
**Journal:** MNRAS 441(2), 1760–1768
**arXiv:** [1310.0006](https://arxiv.org/abs/1310.0006)

## Abstract

Constructs the gamma-ray luminosity function of BL Lac objects using 211 sources from the Second LAT AGN Catalog (1LAC). Compares PDE, PLE, and LDDE models. Finds LDDE provides the best fit, with overall positive evolution peaking at z ~ 1.2.

## Methodology

- MCMC parameter fitting for three evolution models
- 211 BL Lac objects from 1LAC catalog
- Subclass stratification: HSP, ISP, LSP
- Analysis of spectral properties with luminosity

## Key Results

- LDDE model provides best fit
- HSP BL Lacs show negative evolution (density increases toward z=0)
- LISP (ISP+LSP) show positive evolution peaking at z ~ 1.2
- Overall BL Lac contribute ~1–5% of extragalactic gamma-ray background

## Parameters Used in This Pipeline

We adopt a single-component LDDE with piecewise evolution, capturing the overall positive evolution:

| Parameter | Value | Notes |
|-----------|-------|-------|
| A | 5.0 × 10⁻⁹ | Mpc⁻³ (combined population) |
| L_c | 1.0 × 10⁴⁶ | erg/s |
| gamma_1 | 0.60 | faint-end |
| gamma_2 | 1.80 | bright-end |
| z_c* | 1.2 | peak redshift |
| alpha | 0.15 | luminosity dependence |
| p_1 | 4.0 | positive evolution |
| p_2 | −2.0 | negative evolution above z_c |

**Note:** An alternative parameterization from Di Mauro et al. (2013) splits into HSP (p_1=−1.64, negative) and LISP (p_1=4.4, positive) components with a "sum" evolution form. This was previously used but concentrates too much emission at z~0.

## Implementation

**Module:** `astro_sources.py` — `_BL_LAC_PARAMS`, `_glf_BL_Lac()`, piecewise evolution form.
