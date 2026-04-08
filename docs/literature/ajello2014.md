# Ajello, Romani, Gasparrini et al. (2014) — BL Lac Luminosity Function

**Authors:** M. Ajello, R. W. Romani, D. Gasparrini, M. S. Shaw, J. Bolmer, et al.
**Journal:** ApJ 780(1), 73
**arXiv:** [1310.0006](https://arxiv.org/abs/1310.0006)

## Abstract

Constructs the gamma-ray luminosity function of BL Lac objects using 211 sources from the First LAT AGN Catalog (1LAC). Compares PDE, PLE, and LDDE models. Finds LDDE provides the best fit, with overall positive evolution peaking at z ~ 1.2. HSP BL Lacs show negative evolution (density increases toward z=0), while LISP (ISP+LSP) show positive evolution.

## GLF Parameterization

### Local luminosity function (Eq. C.2, with Γ = μ★ = 2.12)

$$\frac{d\Phi}{d\log_{10}L} = \frac{A}{\left(\frac{L}{L_\star}\right)^{\gamma_1} + \left(\frac{L}{L_\star}\right)^{\gamma_2}}$$

### LDDE evolution (paper form)

$$e(z, L) = \left[\left(\frac{1+z}{1+z_c(L)}\right)^{p_1} + \left(\frac{1+z}{1+z_c(L)}\right)^{p_2}\right]^{-1}$$

where $z_c(L) = z_\star\,(L / 10^{48}\,\text{erg/s})^\beta$.

This is a smooth double power-law in redshift: rises as $(1+z)^{p_1}$ for $z \ll z_c$, peaks near $z_c$, then falls as $(1+z)^{p_2}$ for $z \gg z_c$.

### Parameters (Table 3, LDDE1)

| Parameter | Value | Unit |
|-----------|-------|------|
| $A$ | $9.20 \times 10^{-11}$ | Mpc⁻³ |
| $L_\star$ | $2.43 \times 10^{48}$ | erg/s |
| $\gamma_1$ | 1.12 | — |
| $\gamma_2$ | 3.71 | — |
| $p_1$ | 4.50 | — |
| $p_2$ | $-12.88$ | — |
| $z_\star$ | 1.67 | — |
| $\beta$ | $4.46 \times 10^{-2}$ | — |

## Key Results

- LDDE provides best fit among PDE, PLE, LDDE models
- HSP BL Lacs: negative evolution (density increases toward z=0)
- LISP (ISP+LSP): positive evolution peaking at $z \sim 1.2$
- Combined BL Lac population: peaks at $z \sim 1.2$–$1.7$ (luminosity-dependent)
- BL Lacs contribute ~10–15% of the isotropic gamma-ray background
- Spectral index: μ★ = 2.12 ± 0.03 (LDDE1, Table 3)

## Repository Use

Used by the repository as the primary source for the BL Lac luminosity-function parameters in `astro_sources.py`.
