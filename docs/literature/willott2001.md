# Willott, Rawlings, Blundell, Lacy & Eales (2001) — Radio Luminosity Function

**Authors:** C. J. Willott, S. Rawlings, K. M. Blundell, M. Lacy, S. A. Eales
**Journal:** MNRAS 322, 536–552
**arXiv:** [astro-ph/0010419](https://arxiv.org/abs/astro-ph/0010419)

## Abstract

Derives the radio luminosity function (RLF) from the combined 3CRR, 6CE, and 7CRS complete samples (356 sources). A dual-population model fits the data, with differential density evolution for low-power and high-power radio populations.

## Methodology

- 151 MHz steep-spectrum radio luminosity function
- Two-component model: low-power (FRI-like) + high-power (FRII/quasar-like)
- Assumes **H₀ = 50 km/s/Mpc, Ω_M = 0, Ω_Λ = 0** (open/empty cosmology) for the Model C parameter set later reused by [Di Mauro+ (2014)](dimauro2014.md)

## Key Results

The RLF is the sum of two populations (used via [Di Mauro+ (2014)](dimauro2014.md) Eq. C.19):

$$\rho_r(L_r, z) = \rho_l(L_r, z) + \rho_h(L_r, z)$$

where $L_r$ is the radio luminosity at 151 MHz in W/Hz.

### Low-power component

$$\rho_l = \rho_{l\star}\left(\frac{L_r}{L_{l\star}}\right)^{-\beta_l}\exp\left(-\frac{L_r}{L_{l\star}}\right)(1+z)^{k_l}$$

for $z < z_{l\star}$. For $z \ge z_{l\star}$, the evolution is frozen at $z = z_{l\star}$:

$$\rho_l(z \ge z_{l\star}) = \rho_{l\star}\left(\frac{L_r}{L_{l\star}}\right)^{-\beta_l}\exp\left(-\frac{L_r}{L_{l\star}}\right)(1+z_{l\star})^{k_l}$$

### High-power component

$$\rho_h = \rho_{h\star}\left(\frac{L_r}{L_{h\star}}\right)^{-\beta_h}\exp\left(-\frac{L_{h\star}}{L_r}\right)f_h(z)$$

with Gaussian redshift evolution:

$$f_h(z) = \exp\left\{-\frac{1}{2}\left(\frac{z - z_{h\star}}{z_{h0}}\right)^2\right\}$$

where:
- $z_{h0} = 0.568$ for $z < z_{h\star}$
- $z_{h0} = 0.956$ for $z \ge z_{h\star}$

### Parameters

| Symbol | Low-power | High-power | Unit |
|--------|-----------|------------|------|
| $\rho_\star$ | $10^{-7.523}$ | $10^{-6.757}$ | Mpc⁻³ (Willott cosmology) |
| $\beta$ | 0.586 | 2.42 | — |
| $L_\star$ | $10^{26.48}$ | $10^{27.39}$ | W/Hz (151 MHz) |
| $k$ / $z_\star$ | $k_l = 3.48$, $z_{l\star} = 0.710$ | $z_{h\star} = 2.03$ | — |
| $z_{h0}$ | — | 0.568 / 0.956 | — |

**Important:** All densities are in the Willott cosmology (H₀ = 50, Ω_M = 0). A comoving volume correction factor η(z) = (d_C^W/d_C)² × (H/H_W) is required to convert to Planck 2018 cosmology.

## Repository Use

Used by the repository as the underlying 151 MHz radio luminosity function in the mAGN source model.
