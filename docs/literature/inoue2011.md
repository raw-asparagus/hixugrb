# Inoue (2011) — Gamma-Ray Loud Radio Galaxies Core Emissions

**Author:** Y. Inoue
**Journal:** ApJ 733, 66
**arXiv:** [1103.3946](https://arxiv.org/abs/1103.3946)

## Abstract

Establishes the contribution of gamma-ray loud radio galaxy core emissions to the cosmic MeV/GeV background using Fermi-LAT detections. Finds gamma-ray loud radio galaxies contribute ~25% of the unresolved extragalactic gamma-ray background above 100 MeV.

## Key Results Used in This Pipeline

### Radio spectral index for frequency scaling

$$\frac{L_r}{\nu} \propto \nu^{-\alpha_r}, \quad \alpha_r = 0.80$$

This is used to convert between radio frequencies. The [Willott+ (2001)](willott2001.md) RLF is defined at 151 MHz; the [Lara+ (2004)](lara2004.md) core-total relation uses 1.4 GHz total and 5 GHz core luminosities:

$$L_r^{1.4\,\text{GHz}} = L_r^{151\,\text{MHz}} \times \left(\frac{1400}{151}\right)^{-\alpha_r}$$

### Radio-gamma correlation

Partial correlation analysis gives $L_\gamma \propto L_{5\,\text{GHz}}^{1.16}$, consistent with the [Di Mauro+ (2014)](dimauro2014.md) relation used in this pipeline.

## Implementation

Used by: `astro_sources.py:_L151_from_Lgamma()` (frequency scaling between 151 MHz and 1.4 GHz)
