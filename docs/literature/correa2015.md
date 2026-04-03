# Correa, Wyithe, Schaye & Duffy (2015) — Concentration-Mass Relation

**Authors:** C. A. Correa, J. S. B. Wyithe, J. Schaye, A. R. Duffy
**Journal:** MNRAS 452(2), 1217–1232
**arXiv:** [1502.00391](https://arxiv.org/abs/1502.00391)

## Abstract

Presents a semi-analytic, physically motivated model for dark matter halo concentration as a function of halo mass and redshift. Combines an analytic model for the halo mass accretion history (MAH), based on extended Press-Schechter theory, with an empirical relation between concentration and formation time from N-body simulations. Valid for log₁₀(M/M☉) ∈ [−2, 16] and z ∈ [0, 20].

## Key Advantages

- Physically motivated from MAH (not just empirical power-law fit)
- Valid down to microhalo masses (10⁻² M☉) — critical for DM annihilation boost
- Predicts slope change at ~10¹¹ M☉ from MAH transition (exponential → power-law growth)
- No artificial upturn at high masses (only relaxed halos)
- Explicit Planck cosmology fitting functions (Appendix B1)

## Equations Used in This Pipeline (Appendix B1, Planck cosmology)

### Low-redshift regime (z ≤ 4, all halo masses)

$$\log_{10} c = \alpha + \beta\,\log_{10}(M/M_\odot)\left[1 + \gamma\,(\log_{10}(M/M_\odot))^2\right]$$

$$\alpha = 1.7543 - 0.2766(1+z) + 0.02039(1+z)^2$$
$$\beta = 0.2753 + 0.00351(1+z) - 0.3038(1+z)^{0.0269}$$
$$\gamma = -0.01537 + 0.02102(1+z)^{-0.1475}$$

### High-redshift regime (z > 4, all halo masses)

$$\log_{10} c = \alpha + \beta\,\log_{10}(M/M_\odot)$$

$$\alpha = 1.3081 - 0.1078(1+z) + 0.00398(1+z)^2$$
$$\beta = 0.0223 - 0.0944(1+z)^{-0.3907}$$

### Reference values (Planck cosmology)

| M [M☉] | c(z=0) | c(z=1) | c(z=2) |
|---------|--------|--------|--------|
| 10⁶ | ~40 | ~15 | ~8 |
| 10¹² | ~8 | ~5 | ~4 |
| 10¹⁵ | ~4 | ~3 | ~2.5 |

## Implementation

**Module:** `halo_model.py` — `concentration_correa(M, z)`. Default (and only) concentration for DM halos (`halo_model.concentration`).

**Software:** Authors provide the `commah` Python package (pip installable) for computing concentrations and MAHs at any cosmology. This pipeline uses the Appendix B1 fitting functions directly for performance.
