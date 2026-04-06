# Di Mauro, Calore, Donato, Ajello & Latronico (2014) — mAGN Gamma-Ray Emission

**Authors:** M. Di Mauro, F. Calore, F. Donato, M. Ajello, L. Latronico
**Journal:** ApJ 780(2), 161
**arXiv:** [1304.0908](https://arxiv.org/abs/1304.0908)

## Abstract

Calculates diffuse gamma-ray emission from unresolved misaligned AGN (radio galaxies). Establishes a physical L_γ–L_radio correlation validated by statistical tests and Fermi-LAT source counts. mAGN contribute 10–63% of the IGRB (depending on model assumptions), are far more numerous than blazars, and produce negligible anisotropy.

## Methodology

The gamma-ray luminosity function is derived indirectly from the radio luminosity function via a multi-step conversion chain:

1. Start with the [Willott+ (2001)](willott2001.md) two-component radio LF at 151 MHz
2. Scale to 1.4 GHz using a power-law spectrum with α_r = 0.80 ([Inoue 2011](inoue2011.md))
3. Convert total 1.4 GHz to core 5 GHz using the [Lara+ (2004)](lara2004.md) relation
4. Convert core radio to gamma-ray luminosity using the empirical correlation

## Key Equations

### Gamma-ray to radio-core correlation

$$\log_{10} L_\gamma = 2.0 + 1.008\,\log_{10} L_{r,\text{core}}^{5\,\text{GHz}}$$

where $L_\gamma$ is in erg/s and $L_{r,\text{core}}$ is in W/Hz.

### Full gamma-ray luminosity function (Eq. C.19)

$$\phi_\gamma(L, z) = \frac{k\,\eta}{(1+z)^{2-\Gamma}}\,\frac{1}{\ln(10)\,L_{151}}\,\left|\frac{dL_{151}}{dL_\gamma}\right|\,\rho_r\!\left(L_{151}(L_\gamma),\, z\right)$$

where:
- $k = 3.05$ — beaming/duty-cycle correction factor
- $\Gamma = 2.37$ — mean photon spectral index
- $(1+z)^{2-\Gamma}$ — K-correction for the observed-to-rest-frame energy shift
- $\eta(z)$ — comoving volume correction from [Willott](willott2001.md) (H₀=50) to Planck cosmology
- $\rho_r$ — [Willott+ (2001)](willott2001.md) radio LF (dΦ/d log₁₀L at 151 MHz)
- $L_{151}(L_\gamma)$ — inverted conversion chain (see below)

### Conversion chain (inverted: L_γ → L_151)

$$\log_{10} L_{r,\text{core}}^{5\,\text{GHz}} = \frac{\log_{10} L_\gamma - 2.0}{1.008}$$

$$\log_{10} L_{r,\text{tot}}^{1.4\,\text{GHz}} = \frac{\log_{10} L_{r,\text{core}}^{5\,\text{GHz}} - 4.2}{0.77}$$

$$L_{r,\text{tot}}^{151\,\text{MHz}} = L_{r,\text{tot}}^{1.4\,\text{GHz}} \times \left(\frac{1400}{151}\right)^{0.80}$$

Composite Jacobian: $dL_{151}/dL_\gamma = (L_{151}/L_\gamma) / (1.008 \times 0.77)$

### Mass-to-luminosity for halo bias (Eqs. C.20–C.21)

$$M_\star = 10^9\,M_\odot\left(\frac{L_\gamma}{10^{48}\,\text{erg/s}}\right)^{0.36}$$

$$M_\text{halo} = 10^{13}\,M_\odot\left(\frac{M_\star}{10^{8.8}\,(1+z)^{1.4}}\right)^{0.645}$$

## Repository Use

Used by the repository as the main mAGN gamma-ray luminosity-function reference in `astro_sources.py`, together with the Willott, Lara, and Inoue radio relations it builds on.
