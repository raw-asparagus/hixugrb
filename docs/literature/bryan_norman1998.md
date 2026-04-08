# Bryan & Norman (1998) — Virial Overdensity from Cluster Scaling Relations

**Authors:** G. L. Bryan, M. L. Norman
**Journal:** ApJ 495, 80–99
**arXiv:** [astro-ph/9710107](https://arxiv.org/abs/astro-ph/9710107)

## Abstract

Compares Eulerian hydrodynamic simulations of X-ray cluster formation against virial scaling relations between cluster mass, dark matter velocity dispersion, gas temperature, and X-ray luminosity. Calibrates the Press-Schechter prescription with simulations across three cosmological models (CDM, CHDM, OCDM) at multiple redshifts, establishing scaling normalizations and scatter for use of clusters as cosmological probes.

## Key Result for This Repository

The paper provides a fitting formula for the virial overdensity $\Delta_c$ relative to the critical density, derived from the spherical top-hat collapse solution (Eq. 6):

$$\Delta_c = 18\pi^2 + 82x - 39x^2 \qquad (\Omega_R = 0, \text{ i.e. flat } \Lambda\text{CDM})$$

$$\Delta_c = 18\pi^2 + 60x - 32x^2 \qquad (\Omega_\Lambda = 0, \text{ i.e. open})$$

where $x = \Omega(z) - 1$ and $\Omega(z) = \Omega_0(1+z)^3 / E(z)^2$. These fits are accurate to 1% for $\Omega(z) \in [0.1, 1]$.

For Planck 2018 cosmology at $z=0$: $\Delta_c \approx 103$ (relative to critical density), equivalently $\sim 327$ relative to the mean matter density.

## Other Key Equations

- **M–$\sigma$ relation** (Eq. 4): virial mass vs 1D velocity dispersion, normalization $f_\sigma \approx 0.9$
- **M–T relation** (Eq. 9): virial mass vs gas temperature, normalization $f_T \approx 0.8$
- **Press-Schechter mass function** (Eq. 18): calibrated $\delta_c \approx 1.7$–$1.8$ across models

## Repository Use

Used by the repository for the redshift-dependent virial overdensity $\Delta_\text{vir}(z)$ implemented in `halo_model.py`. The flat-$\Lambda$CDM formula ($\Omega_R = 0$ case) is the one adopted.
