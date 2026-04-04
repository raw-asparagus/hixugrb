# Gruppioni, Pozzi, Rodighiero et al. (2013) — Herschel PEP/HerMES IR Luminosity Function

**Authors:** C. Gruppioni, F. Pozzi, G. Rodighiero, et al.
**Journal:** MNRAS 432(1), 23–52
**arXiv:** [1302.5209](https://arxiv.org/abs/1302.5209)

## Abstract

Derives the infrared luminosity function evolution of star-forming galaxies to z ~ 4 using deep Herschel PACS (70, 100, 160 μm) and HerMES (250, 350, 500 μm) data from the PEP survey. Identifies three sub-populations with distinct evolutionary behavior.

## Three-Component IR Luminosity Function

$$\phi_\text{IR} = \phi_\text{spiral} + \phi_\text{starburst} + \phi_\text{SF-AGN}$$

### Modified Schechter form (each component)

$$\phi_i = \phi_{0,i}(z)\left(\frac{L_\text{IR}}{L_{0,i}(z)}\right)^{1-\gamma_i}\exp\left[-\frac{1}{2\sigma_i^2}\log_{10}^2\!\left(1 + \frac{L_\text{IR}}{L_{0,i}(z)}\right)\right]$$

where $\phi_i$ returns dΦ/d log₁₀ L_IR in Mpc⁻³.

### Luminosity evolution $L_{0,i}(z)$

**Spiral** (break at $z = 1.1$, frozen above with $k_{L,2} = 0$):

$$L_{0,\text{sp}}(z) = L_{\star,\text{sp}}\left(\frac{1+z}{1.15}\right)^{k_{L}} \quad (z \le 1.1); \qquad L_{0,\text{sp}}(z > 1.1) = L_{0,\text{sp}}(1.1)$$

**Starburst and SF-AGN** (single power law, no luminosity break):

$$L_{0,j}(z) = L_{\star,j}\left(\frac{1+z}{1.15}\right)^{k_{L,j}}$$

*Note: The paper (Table 8) gives a luminosity break only for spiral ($z_{b,L} = 1.1$, $k_{L,2} = 0$). Starburst and SF-AGN have a single $k_L$ with no break. The pipeline applies the z=1.1 break to all components as a simplification; this has negligible effect since k_L values are modest and the z>1.1 contribution to the cross-correlation is small.*

*Note: The $(1+z)/1.15$ normalization (reference point at the z=0.15 bin midpoint) is a pipeline convention. The paper parameterizes evolution as $(1+z)^k$ with a reference value at each redshift bin center.*

### Density evolution $\phi_{0,i}(z)$

**Spiral** (break at $z = 0.53$):

$$\phi_{0,\text{sp}}(z) = \phi_{\star,\text{sp}}\left(\frac{1+z}{1.15}\right)^{k_{R1,\text{sp}}} \quad (z \le 0.53)$$

$$\phi_{0,\text{sp}}(z) = \phi_{\star,\text{sp}}\left(\frac{1.53}{1.15}\right)^{k_{R1,\text{sp}}}\left(\frac{1+z}{1.53}\right)^{k_{R2,\text{sp}}} \quad (z > 0.53)$$

**Starburst and SF-AGN** (break at $z = 1.1$):

$$\phi_{0,j}(z) = \phi_{\star,j}\left(\frac{1+z}{1.15}\right)^{k_{R1,j}} \quad (z \le 1.1)$$

$$\phi_{0,j}(z) = \phi_{\star,j}\left(\frac{2.1}{1.15}\right)^{k_{R1,j}}\left(\frac{1+z}{2.1}\right)^{k_{R2,j}} \quad (z > 1.1)$$

### Parameters (Table 8 in paper; labeled "Table C.2" in Pinetti 2022 thesis)

| Component | $\gamma$ | $\sigma$ | $\log_{10}(L_\star/L_\odot)$ | $\log_{10}(\phi_\star/\text{Mpc}^{-3})$ | $k_L$ | $k_{R1}$ | $k_{R2}$ |
|-----------|---------|---------|------|------|------|-------|-------|
| spiral | 1.0 | 0.50 | 9.78 | −2.12 | 4.49 | −0.54 | −7.13 |
| starburst | 1.0 | 0.35 | 11.17 | −4.46 | 1.96 | 3.79 | −1.06 |
| SF-AGN | 1.2 | 0.40 | 10.80 | −3.20 | 3.17 | 0.67 | −3.17 |

## Gamma-Ray Conversion

The IR LF is converted to a gamma-ray LF using the [Ackermann+ (2012)](ackermann2012_sfg.md) L_γ–L_IR scaling:

$$\phi_\gamma(L_\gamma, z) = \phi_\text{IR}\!\left(L_\text{IR}(L_\gamma),\, z\right)\,\frac{d\log_{10} L_\text{IR}}{d\log_{10} L_\gamma}$$

### Mass-to-luminosity for halo bias (Pinetti thesis Eq. C.29; not in this paper)

$$M(L) = \frac{10^{12}\,M_\odot}{(1+z)^{1.61}}\left(\frac{L}{6.8\times10^{39}\,\text{erg/s}}\right)^{0.92}$$

## Erratum

**MNRAS 436(3), 2875–2876 (December 2013)** — Correction to Figure 8 scaling. Does not affect luminosity function parameters.

## Implementation

**Module:** `astro_sources.py` — `_gruppioni_component()`, `_gruppioni_ir_lf()`, `_L_IR_from_Lgamma()`, `_glf_SFG()`
