# Sheth & Tormen (1999) — Halo Bias

**Authors:** R. K. Sheth, G. Tormen
**Journal:** MNRAS 308(1), 119–126
**arXiv:** [astro-ph/9901122](https://arxiv.org/abs/astro-ph/9901122)

## Abstract

Develops a model relating halo abundance to large-scale spatial distribution using the peak-background split framework. Shows that knowledge of the unconditional mass function suffices to compute halo bias without merger history information.

## Methodology

- Peak-background split: long-wavelength perturbation modulates collapse threshold
- Ellipsoidal collapse framework (more realistic than spherical)
- Calibrated against N-body simulations (SCDM, OCDM, LCDM)

## Key Results

- Halos below M* are less clustered; above M* are more clustered
- Bias depends only on mass function shape, not merger history
- Excellent agreement with N-body measurements

## Equation Used

**Halo bias (peak-background split):**
$$b(\nu) = 1 + \frac{q\nu - 1}{\delta_c} + \frac{2p}{\delta_c(1 + (q\nu)^p)}$$

| Parameter | Value |
|-----------|-------|
| q | 0.707 |
| p | 0.3 |
| delta_c | 1.686 |
| nu | delta_c^2 / sigma^2(M,z) |

## Implementation

**Module:** `halo_model.py` — `bias(M, z)` and `hmf_interface.py` — `bias_ST(M, z)`. Parameters in `config.py`: `SMT_Q`, `SMT_P`, `DELTA_C`.
