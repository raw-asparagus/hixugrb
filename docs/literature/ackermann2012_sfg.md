# Ackermann et al. / Fermi-LAT Collaboration (2012) — GeV Observations of Star-Forming Galaxies

**Authors:** M. Ackermann, M. Ajello, A. Allafort, L. Baldini, J. Ballet, et al. (Fermi-LAT Collaboration)
**Journal:** ApJ 755, 164
**arXiv:** [1206.1346](https://arxiv.org/abs/1206.1346)

## Abstract

Examines 69 dwarf, spiral, and luminous/ultraluminous infrared galaxies using three years of Fermi-LAT data. Establishes scaling relations between gamma-ray luminosity and both radio continuum and total infrared luminosity, demonstrating that gamma-ray emission is a reliable tracer of star formation.

## Key Result

### L_γ – L_IR scaling relation

$$\log_{10}\left(\frac{L_{0.1\text{–}100\,\text{GeV}}}{\text{erg s}^{-1}}\right) = \alpha_\text{IR}\,\log_{10}\left(\frac{L_{8\text{–}1000\,\mu\text{m}}}{10^{10}\,L_\odot}\right) + \beta_\text{IR}$$

with $\alpha_\text{IR} = 1.09$ and $\beta_\text{IR} = 39.19$ (Table 5, EM method, excluding galaxies hosting Swift-BAT AGN). The full sample gives $\alpha = 1.17 \pm 0.07$, $\beta = 39.28 \pm 0.08$; the AGN-excluded subsample is used for cleaner SFG-only calibration.

This quasi-linear scaling converts the [Gruppioni+ (2013)](gruppioni2013.md) infrared luminosity function into a gamma-ray luminosity function via:

$$\phi_\gamma(L_\gamma, z) = \phi_\text{IR}(L_\text{IR}(L_\gamma), z)\,\frac{d\log_{10} L_\text{IR}}{d\log_{10} L_\gamma}$$

where $d\log_{10} L_\text{IR} / d\log_{10} L_\gamma = 1/\alpha_\text{IR} \approx 0.917$.

## Assumed Cosmology

WMAP-era: Ω_m ≈ 0.27, Ω_Λ ≈ 0.73, h ≈ 0.71. The paper does not explicitly state cosmological parameters. Cosmology enters only through d_L in converting fluxes to luminosities; the L_γ–L_IR scaling is a correlation between two luminosities, so d_L effects largely cancel.

## Repository Use

Used by the repository to convert the Gruppioni infrared luminosity function into the SFG gamma-ray luminosity function in `astro_sources.py`.
