# Moliné, Sánchez-Conde, Palomares-Ruiz & Prada (2017) — Substructure Boost Factor

**Authors:** A. Moliné, M. A. Sánchez-Conde, S. Palomares-Ruiz, F. Prada
**Journal:** MNRAS 466(4), 4974–4990
**arXiv:** [1603.04057](https://arxiv.org/abs/1603.04057)

## Abstract

Refines predictions for substructure enhancement of dark matter annihilation signals using Via Lactea II and ELVIS N-body simulations. Characterizes subhalo concentration parameters including position-dependent tidal effects and provides improved parameterizations for the boost factor B(M,z).

## Key Results

- Boost factors 2–3× higher than Sánchez-Conde & Prada (2014) estimates
- Tidal stripping reduces boost for satellite populations by 20–30%
- B(M) ~ 10–20 for Milky Way-scale halos with M_min = 10⁻⁶ M☉
- Valid for 10⁻⁶ < M₂₀₀ [M☉] < 10¹⁵, accuracy < 5%

## Assumed Cosmology

The boost factor polynomial is calibrated from two N-body simulations run under WMAP-era cosmologies:
- **Via Lactea II** (Diemand+ 2008): Ω_m = 0.238, Ω_Λ = 0.762, h = 0.73, σ₈ = 0.74, n_s = 0.951
- **ELVIS** (Garrison-Kimmel+ 2014): Ω_m = 0.266, Ω_Λ = 0.734, h = 0.71, σ₈ = 0.801, n_s = 0.963

The boost factor has weak dependence on the exact cosmological parameters (it is driven by the concentration–mass relation and subhalo mass function slope, not the background expansion).

## Key Equations

### Polynomial boost at z=0 (Eq. 18)

$$\log_{10} B(M, z{=}0) = \sum_{i=0}^{5} b_i \left[\log_{10}\left(\frac{M}{M_\odot}\right)\right]^i$$

### Polynomial coefficients (Table 3, α=2, with tidal stripping)

| i | $b_i$ |
|---|-------|
| 0 | −0.186 |
| 1 | 0.144 |
| 2 | −8.8 × 10⁻³ |
| 3 | 1.13 × 10⁻³ |
| 4 | −3.7 × 10⁻⁵ |
| 5 | −2 × 10⁻⁷ |

These coefficients use the c₂₀₀(m₂₀₀, x_sub) concentration-mass relation with tidal stripping. Subhalo mass function slope α = 2, normalization A = 0.012. M_min = 10⁻⁶ M☉ is built into the fit.

## Repository Use

Used by the repository as the source for the substructure boost prescription in `dm_model.py`.
