# Ajello, Romani, Gasparrini et al. (2014) — BL Lac Luminosity Function

**Authors:** M. Ajello, R. W. Romani, D. Gasparrini, M. S. Shaw, J. Bolmer, et al.
**Journal:** ApJ 780(1), 73
**arXiv:** [1310.0006](https://arxiv.org/abs/1310.0006)

## Abstract

Constructs the gamma-ray luminosity function of BL Lac objects using 211 sources from the First LAT AGN Catalog (1LAC). Compares PDE, PLE, and LDDE models. Finds LDDE provides the best fit, with overall positive evolution peaking at z ~ 1.2. HSP BL Lacs show negative evolution (density increases toward z=0), while LISP (ISP+LSP) show positive evolution.

## Assumed Cosmology

WMAP-era: H₀ = 71 km/s/Mpc, Ω_M = 0.27, Ω_Λ = 0.73 (explicitly stated in Sec. 1: "standard concordance cosmology"). Despite being published in 2014, this paper uses WMAP-era cosmology, not Planck 2013.

## GLF Parameterization

### Local luminosity function (Eq. C.2, with Γ = μ★ = 2.12)

$$\frac{d\Phi}{d\log_{10}L} = \frac{A}{\left(\frac{L}{L_\star}\right)^{\gamma_1} + \left(\frac{L}{L_\star}\right)^{\gamma_2}}$$

### LDDE evolution (paper form)

$$e(z, L) = \left[\left(\frac{1+z}{1+z_c(L)}\right)^{p_1} + \left(\frac{1+z}{1+z_c(L)}\right)^{p_2}\right]^{-1}$$

where $z_c(L) = z_\star\,(L / 10^{48}\,\text{erg/s})^\beta$.

This is a smooth double power-law in redshift: rises as $(1+z)^{p_1}$ for $z \ll z_c$, peaks near $z_c$, then falls as $(1+z)^{p_2}$ for $z \gg z_c$.

### Parameters (Table 3, LDDE1 — τ=0 baseline variant)

**Important:** Ajello+2014 reports two LDDE variants in Table 3:
- **LDDE1** ($\tau=0$ baseline) — listed below
- **LDDE2** ($\tau$-varied) — the paper's *preferred* fit (improves on PLE3 by ~3σ via AIC)

The values tabulated below are **LDDE1**, which is what the pipeline uses (inherited from Pinetti 2022 PhD thesis Table C.1, which adopted LDDE1 to keep the BL Lac LDDE in the same simple 4-parameter $[r^{-p_1}+r^{-p_2}]^{-1}$ form as the FSRQ Ajello+2012 fit). The LDDE2 best-fit values differ materially: $A\!\approx\!3.39\times10^{-9}$, $\gamma_1\!\approx\!0.27$, $\gamma_2\!\approx\!1.86$, $L_\star\!\approx\!0.28\times10^{48}$ erg/s, $z_\star\!\approx\!1.34$, $p_1^\star\!\approx\!2.24$, $p_2\!\approx\!-7.37$, $\tau\!\approx\!4.92$, $\alpha\!\approx\!4.53\times10^{-2}$. See Ajello+2014 §5 / Table 3 for the full LDDE2 entry; not used by this pipeline.

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
- LDDE2 (τ-varied) is the paper's preferred LDDE variant; LDDE1 (τ=0) is the simpler baseline used by this pipeline via Pinetti 2022 Table C.1
- HSP BL Lacs: negative evolution (density increases toward z=0)
- LISP (ISP+LSP): positive evolution peaking at $z \sim 1.2$
- Combined BL Lac population: peaks at $z \sim 1.2$–$1.7$ (luminosity-dependent)
- BL Lacs contribute ~10–15% of the isotropic gamma-ray background
- Spectral index: μ★ = 2.12 ± 0.03 (LDDE1, Table 3)

## Repository Use

Used by the repository as the primary source for the BL Lac luminosity-function parameters in `astro_sources.py` (`_BL_LAC_PARAMS`, lines 176–186). The proximate source for the parameter values is Pinetti 2022 PhD thesis Table C.1, which adopted Ajello+2014 LDDE1 (not LDDE2). The choice of LDDE1 over LDDE2 is a tracking decision following the thesis, not a deviation from Ajello+2014 per se — both variants are reported by the paper.
