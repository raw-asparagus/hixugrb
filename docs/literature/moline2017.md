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

## Equations Used in This Pipeline

### Polynomial boost at z=0 (Eq. 18 / Thesis Eq. 3.47)

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

### Redshift evolution (Thesis Eq. 3.48)

$$B(M, z) = \frac{B(M, z{=}0)}{1 + z}$$

This approximation follows from the concentration scaling c ∝ (1+z)⁻¹ at fixed mass, giving the boost luminosity ∝ c³ ∝ (1+z)⁻³ while the smooth halo luminosity scales similarly, so the ratio B scales as (1+z)⁻¹. Equivalently, this is $(H/H_0)^{-2/3}$ in the matter-dominated regime.

### Boost scenarios

| Scenario | Description | Notes |
|----------|------------|-------|
| None | B = 0 | No substructure |
| Conservative | B = 0 for M < 10⁷ M☉ | Only resolved subhalos |
| Intermediate | Full polynomial, M_min = 10⁻⁶ M☉ | Standard WIMP scenario |

## Implementation

**Module:** `dm_model.py` — `boost_moline(M, z, M_min_sub)`. Applied multiplicatively to ρ² integral in `clumping_factor()`: $\rho^2_\text{eff} = (1 + B) \times \rho^2_\text{smooth}$.
