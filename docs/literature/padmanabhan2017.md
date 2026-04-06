# Padmanabhan, Refregier & Amara (2017) — HI Halo Model

**Authors:** H. Padmanabhan, A. Refregier, A. Amara
**Journal:** MNRAS 469(2), 2323–2334
**arXiv:** [1611.06235](https://arxiv.org/abs/1611.06235)

## Abstract

Develops a comprehensive halo model for neutral hydrogen (HI) in the post-reionization universe (z ~ 0–5). Using MCMC methods, simultaneously fits HI abundance (ALFALFA mass function, DLA column densities, Ω_HI), clustering (ALFALFA small-scale, GBT intensity mapping), and DLA properties. Two profile variants are tested: an exponential profile (main text) and a modified NFW profile (Appendix A).

## Two Profile Fits

The paper provides **two independent MCMC fits** to the same data, each with its own best-fit parameters. Parameters from one fit must NOT be mixed with the other.

### Exponential profile (main text, Table 3)

Profile: $\rho_\text{HI}(r) = \rho_0 \exp(-r/r_s)$

| Parameter | Best-fit (1σ) |
|-----------|---------------|
| c_HI,0 | 28.65 ± 1.76 |
| α | 0.09 ± 0.01 |
| log v_c,0 | 1.56 ± 0.04 (v_c,0 = 36.3 km/s) |
| β | −0.58 ± 0.06 |
| γ | 1.45 ± 0.04 |

### Modified NFW profile (Appendix A, Table A1)

Profile: $\rho_\text{HI}(r) = \rho_0 r_s^3 / [(r + 0.75 r_s)(r + r_s)^2]$

| Parameter | Best-fit (1σ) |
|-----------|---------------|
| c_HI,0 | 139 ± 13 |
| α | 0.176 ± 0.007 |
| log v_c,0 | 1.61 ± 0.02 (v_c,0 = 40.7 km/s) |
| β | −0.69 ± 0.03 |
| γ | 0.13 ± 0.20 |

This Appendix A fit is tied to the modified-NFW profile form and should be kept with the Appendix A parameter set rather than mixed with the main-text exponential-profile fit.

## Key Equations

**M_HI–halo mass relation (Eq. 1):**
$$M_\text{HI}(M,z) = \alpha \, f_{H,c} \, M \left(\frac{M}{10^{11} h^{-1} M_\odot}\right)^\beta \exp\left[-\left(\frac{v_{c,0}}{v_c(M,z)}\right)^3\right]$$

where $f_{H,c} = (1 - Y_P) \Omega_B / \Omega_M$, $Y_P = 0.24$.

**Altered NFW HI profile (Eq. A1):**
$$\rho_\text{HI}(r) = \rho_0 \frac{r_s^3}{(r + 0.75 r_s)(r + r_s)^2}$$

**HI concentration (Eq. 3):**
$$c_\text{HI}(M,z) = c_{HI,0} \left(\frac{M}{10^{11} M_\odot}\right)^{-0.109} \frac{4}{(1+z)^\gamma}$$

**Mean HI density:** $\bar\rho_\text{HI}(z) = \int (dn/dM) \, M_\text{HI} \, dM$

**HI bias:** $b_\text{HI}(z) = (1/\bar\rho_\text{HI}) \int (dn/dM) \, M_\text{HI} \, b(M) \, dM$

## Repository Use

Used by the repository as the main HI halo-model source, with the modified-NFW profile and its Appendix A parameter set feeding `hi_model.py`.
