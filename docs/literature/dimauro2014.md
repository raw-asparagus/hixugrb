# Di Mauro, Calore, Donato, Ajello & Latronico (2014) — Diffuse Gamma-Ray Emission from Misaligned AGN

**Authors:** M. Di Mauro, F. Calore, F. Donato, M. Ajello, L. Latronico
**Journal:** ApJ 780(2), 161
**arXiv:** [1304.0908](https://arxiv.org/abs/1304.0908)

## Abstract

Calculates the diffuse gamma-ray emission produced by unresolved misaligned active galactic nuclei (MAGN). The paper establishes an empirical correlation between 5 GHz radio-core luminosity and 0.1–100 GeV gamma-ray luminosity, tests that relation against Fermi-LAT upper limits, converts the radio luminosity function into a gamma-ray luminosity function, and predicts the MAGN contribution to the isotropic gamma-ray background (IGRB).

## Methodology

- Fits the radio-core to gamma-ray correlation using 12 Fermi-LAT detected MAGN
- Checks consistency with 95% CL upper limits for 39 radio-loud FRI/FRII galaxies not detected by Fermi-LAT
- Uses the [Willott et al. (2001)](willott2001.md) total radio luminosity function, converted to a core RLF through the [Lara et al. (2004)](lara2004.md) core-total relation
- Adopts a power-law radio spectrum with $\alpha_\mathrm{tot}=0.80$ to shift the Willott RLF from 151 MHz to 5 GHz
- Fits the source-count distribution to determine the normalization factor $k$

## Key Equations

**Radio-core to gamma-ray correlation (Eq. 5):**
$$\log_{10} L_\gamma = (2.00 \pm 0.98) + (1.008 \pm 0.025)\,\log_{10} L_{r,\mathrm{core}}^{5\,\mathrm{GHz}}$$

**Core-total radio relation adopted from Lara et al. (Eq. 13 in this paper):**
$$\log_{10} L_{\nu,\mathrm{core}}^{5\,\mathrm{GHz}} = (4.2 \pm 2.1) + (0.77 \pm 0.08)\,\log_{10} L_{\nu,\mathrm{tot}}^{1.4\,\mathrm{GHz}}$$

**Core radio luminosity function from the total RLF (Eq. 16):**
$$\rho_{r,\mathrm{core}}(L_{r,\mathrm{core}}, z) = \rho_{r,\mathrm{tot}}(L_{r,\mathrm{tot}}, z)\,\frac{d\log L_{r,\mathrm{tot}}}{d\log L_{r,\mathrm{core}}}$$

**Gamma-ray luminosity function (Eq. 20):**
$$
\rho_\gamma(L_\gamma, z) =
k\,
\rho_{r,\mathrm{tot}}\!\left(L_{r,\mathrm{tot}}\!\left(L_{r,\mathrm{core}}(L_\gamma)\right), z\right)\,
\frac{d\log L_{r,\mathrm{core}}}{d\log L_\gamma}\,
\frac{d\log L_{r,\mathrm{tot}}}{d\log L_{r,\mathrm{core}}}
$$

This is the paper's actual GLF construction. It does **not** contain an "Eq. C.19" or the later appendix-style halo-mass mappings that appeared in downstream synthesis material.

## Key Results

- The radio-core / gamma-ray correlation survives partial-correlation tests and upper-limit checks
- Best fit to the source-count distribution gives **$k = 3.05 \pm 0.20$**
- A physically interesting case with **$k = 1$** also fits the source counts reasonably well, suggesting many radio-core MAGN may emit gamma rays
- Unresolved MAGN are predicted to contribute about **10–63%** of the IGRB
- The cascade component is subdominant; in the benchmark calculation it is about **8%** of the total MAGN energy flux

## Repository Use

Used by the repository as the main MAGN gamma-ray luminosity-function reference in `astro_sources.py`, together with the [Willott](willott2001.md) and [Lara](lara2004.md) radio relations it builds on.

More repo-convenient appendix-style rewrites of these source classes appear later in [Pinetti (2022)](pinetti2022_thesis.md), but they are not part of this 2014 paper itself.
