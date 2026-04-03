# Dutton & Maccio (2014) — Concentration-Mass Relation

**Authors:** A. A. Dutton, A. V. Maccio
**Journal:** MNRAS 441(4), 3359–3374
**arXiv:** [1402.7073](https://arxiv.org/abs/1402.7073)

## Abstract

Presents evolution of cold dark matter halo structural parameters across five decades in mass (10^9–10^15 M_sun/h) in Planck cosmology. Calibrated from high-resolution N-body simulations.

## Methodology

- High-resolution N-body+SPH simulations
- M_200 halo definition (rho = 200 rho_crit)
- Einasto and NFW profile fitting for relaxed halos
- Redshift range z = 0–10

## Key Results

- ~20% higher concentration at z=0 vs WMAP cosmology (Planck boost)
- Power-law c(M) relation with redshift-dependent coefficients
- Einasto profile provides better fits than NFW at small radii

## Equation Used

**Concentration-mass relation (Eqs. 10–11, Planck cosmology):**
$$\log_{10}(c) = a(z) + b(z) \log_{10}\left(\frac{M}{10^{12} M_\odot/h}\right)$$

$$a(z) = 0.520 + (0.905 - 0.520) \exp(-0.617 \, z^{1.21})$$
$$b(z) = -0.101 + 0.026 \, z$$

At z=0: a=0.905, b=−0.101 → c(10^12) ≈ 8.0.

## Implementation

**Module:** `halo_model.py` — `concentration_dutton_maccio(M, z)`. Available as an alternative concentration model. Valid for M = 10¹⁰–10¹⁵ M☉/h; extrapolated as power law below.

**Status:** Superseded by [Correa et al. (2015)](correa2015.md) as the default, which provides physically-motivated concentrations valid down to 10⁻² M☉ — essential for DM annihilation boost factor calculations.
