# Gruppioni, Pozzi, Rodighiero et al. (2013) — The Herschel PEP/HerMES Luminosity Function - I: Probing the Evolution of PACS Selected Galaxies to z ≃ 4

**Authors:** C. Gruppioni, F. Pozzi, G. Rodighiero, et al.
**Journal:** MNRAS 432(1), 23–52
**arXiv:** [1302.5209](https://arxiv.org/abs/1302.5209)

## Abstract

Derives the infrared luminosity function evolution of Herschel-selected galaxies out to $z \sim 4$ using PEP and HerMES data. The paper does **not** model only three star-forming populations: it fits the total IR LF and then decomposes it into **five main SED classes**: spiral, starburst, SF-AGN, AGN2, and AGN1. For interpretation, SF-AGN is further divided into SF-AGN(SB) and SF-AGN(Spiral).

## Data and Scope

- PEP + HerMES coverage in GOODS-S, GOODS-N, ECDFS, and COSMOS
- PACS-selected samples at 70, 100, and 160 $\mu$m, supported by SPIRE data at 250, 350, and 500 $\mu$m
- Rest-frame luminosity functions at 35, 60, and 90 $\mu$m
- Total IR luminosity function integrated over $8$–$1000\,\mu$m
- Redshift coverage from the local Universe to $z \sim 4$

## Luminosity-Function Form

For both the total IR LF and the individual SED populations, the paper uses a modified Schechter form:

$$
\phi(L) = \phi^\star \left(\frac{L}{L^\star}\right)^{1-\alpha}
\exp\!\left[
-\frac{1}{2\sigma^2}
\log_{10}^2\!\left(1+\frac{L}{L^\star}\right)
\right]
$$

where $\phi(L)$ is $d\Phi/d\log_{10}L$.

## Five Main SED Populations

The paper classifies sources into the following five main populations:

- `spiral`
- `starburst`
- `SF-AGN`
- `AGN2`
- `AGN1`

For interpretation of the star-forming / AGN-mixed class, `SF-AGN` is also split into:

- `SF-AGN(SB)`
- `SF-AGN(Spiral)`

### Local LF parameters from Table 8

| Population | $\alpha$ | $\sigma$ | $\log_{10}(L^\star/L_\odot)$ | $\log_{10}(\Phi^\star/\mathrm{Mpc}^{-3}\,\mathrm{dex}^{-1})$ |
|-----------|---------|---------|-------------------------------|--------------------------------------------------------------|
| spiral | $1.00 \pm 0.05$ | $0.50 \pm 0.01$ | $9.78 \pm 0.04$ | $-2.12 \pm 0.01$ |
| starburst | $1.00 \pm 0.20$ | $0.35 \pm 0.10$ | $11.17 \pm 0.16$ | $-4.46 \pm 0.06$ |
| SF-AGN | $1.20 \pm 0.02$ | $0.40 \pm 0.10$ | $10.80 \pm 0.02$ | $-3.20 \pm 0.01$ |
| AGN2 | $1.20 \pm 0.20$ | $0.70 \pm 0.20$ | $10.80 \pm 0.20$ | $-5.14 \pm 0.17$ |
| AGN1 | $1.40 \pm 0.30$ | $0.70 \pm 0.20$ | $10.50 \pm 0.20$ | $-5.21 \pm 0.11$ |

Table 8 also gives the redshift evolution parameters for each class. In particular, the spiral population has explicit breaks at $z_{b,L}=1.1$ and $z_{b,\rho}=0.53$, while the starburst and SF-AGN fits use breaks at $z=1.1$.

## Key Results

- The total IR LF shows strong luminosity evolution:
  - $L^\star \propto (1+z)^{3.55 \pm 0.10}$ up to $z \sim 1.85$
  - $L^\star \propto (1+z)^{1.62 \pm 0.51}$ from $z \sim 1.85$ to $z \sim 4$
- The total LF density evolution is negative:
  - $\Phi^\star \propto (1+z)^{-0.57 \pm 0.22}$ up to $z \sim 1.1$
  - $\Phi^\star \propto (1+z)^{-3.92 \pm 0.34}$ above $z \sim 1.1$
- The total IR luminosity density rises as $(1+z)^{3.0 \pm 0.2}$ to $z \sim 1.1$, is nearly flat to $z \sim 2.8$, and then declines
- The population mix changes with redshift:
  - `spiral` dominates $\rho_\mathrm{IR}$ only at low redshift ($z \lesssim 0.5$–$0.6$)
  - `SF-AGN` dominates up to $z \sim 2.5$
  - `AGN1` and `AGN2` become important only at the highest redshifts in the sample

## Erratum

**MNRAS 436(3), 2875–2876 (December 2013)** corrects the scaling in one figure and does not alter the fitted luminosity-function parameters used here.
