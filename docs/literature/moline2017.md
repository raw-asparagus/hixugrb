# Moline et al. (2017) — Substructure Boost Factor

**Authors:** A. Moline, M. A. Sanchez-Conde, S. Palomares-Ruiz, F. Prada
**Journal:** MNRAS 466(4), 4974–4990
**arXiv:** [1603.04057](https://arxiv.org/abs/1603.04057)

## Abstract

Refines predictions for substructure enhancement of dark matter annihilation signals using Via Lactea II and ELVIS N-body simulations. Characterizes subhalo concentration parameters and provides improved parameterizations for the boost factor B(M,z).

## Methodology

- High-resolution N-body simulations (Via Lactea II, ELVIS)
- Statistical sample of subhalos: M = 10^6–10^11 h^{-1} M_sun
- Position-dependent subhalo concentration refinements including tidal effects
- Refinement of Sanchez-Conde & Prada (2014) model

## Key Results

- Boost factors 2–3× higher than previous estimates
- Tidal stripping reduces boost for satellite populations by 20–30%
- B(M) ~ 10–20 for Milky Way-scale halos with M_min = 10^{-6} M_sun
- Dominant source of theoretical uncertainty in DM annihilation signals (up to 2 orders of magnitude)

## Equation Used (simplified parameterization)

$$B(M, M_\text{min}) = 1.6 \times 10^{-3} \left[\log_{10}\left(\frac{M}{M_\text{min}}\right)\right]^{2.5}$$

**Scenarios implemented:**
| Scenario | M_min | Typical B(10^12) |
|----------|-------|-----------------|
| None | — | 0 |
| Conservative | 10^7 M_sun | ~1 |
| Intermediate | 10^{-6} M_sun | ~15 |
| Optimistic | 10^{-6} M_sun (enhanced) | ~50 |

## Implementation

**Module:** `dm_model.py` — `boost_moline(M, z, M_min_sub)`. Applied multiplicatively to rho^2 integral in `clumping_factor()`: $\rho^2_\text{eff} = (1 + B) \times \rho^2_\text{smooth}$.
