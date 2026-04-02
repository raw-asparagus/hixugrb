# Munoz-Cuartas et al. (2011) — Concentration-Mass Relation (Alternative)

**Authors:** J. C. Munoz-Cuartas, A. V. Maccio, S. Gottlober, A. A. Dutton
**Journal:** MNRAS 411(1), 584–594
**arXiv:** [1012.1299](https://arxiv.org/abs/1012.1299)

## Abstract

Presents fitting formulae for the concentration-mass relation and its redshift evolution (z=0 to z=2) from N-body simulations spanning M = 10^{10}–10^{15} h^{-1} M_sun.

## Methodology

- Millennium simulation suite (LCDM N-body)
- ~10,000 halos across wide mass range
- Spherical overdensity halo identification
- NFW profile fitting for concentration extraction

## Equation Used

**Polynomial fit:**
$$\log_{10}(c_\text{vir}) = a(z) + b(z) \log_{10}(M_{14})$$

where $M_{14} = M / (10^{14} h^{-1} M_\odot)$.

$$a(z) = 0.537 + (1.025 - 0.537) \exp(-0.718 \, z^{1.08})$$
$$b(z) = -0.097 + 0.024 \, z$$

**Bullock et al. (2001) extrapolation for M < 10^{10}:**
$$c(M) \propto (M/M_*)^{-0.13} (1+z)^{-1}$$

Anchored at M = 10^{10} from the polynomial fit.

## Implementation

**Module:** `halo_model.py` — `concentration_munoz_cuartas(M, z)`. Available as alternative to Dutton & Maccio (2014). Not the default; referenced in design spec for DM concentration in Fornengo & Regis (2014) formalism.
