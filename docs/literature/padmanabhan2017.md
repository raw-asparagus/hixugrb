# Padmanabhan, Refregier & Amara (2017) — HI Halo Model

**Authors:** H. Padmanabhan, A. Refregier, A. Amara
**Journal:** MNRAS 469(2), 2323–2334
**arXiv:** [1611.06235](https://arxiv.org/abs/1611.06235)

## Abstract

Develops a comprehensive halo model for neutral hydrogen (HI) in the post-reionization universe (z ~ 0–5). Using MCMC methods, simultaneously fits HI abundance (ALFALFA mass function, DLA column densities, Omega_HI), clustering (ALFALFA small-scale, GBT intensity mapping), and DLA properties. The resulting M_HI(M,z) relation and HI density profile enable predictions for HI power spectra and cross-correlations.

## Methodology

- Multi-dataset MCMC fitting via CosmoHammer
- Six-parameter model: alpha, beta, v_c0, c_HI0, plus evolution
- Two profile variants tested: altered NFW (thermal core) and exponential
- Calibration data: ALFALFA (z~0), DLAs (z~2–5), GBT×WiggleZ (z~0.8)

## Key Results

| Profile | alpha | beta | v_c0 (km/s) | c_HI0 |
|---------|-------|------|-------------|-------|
| Altered NFW | 0.17 | −0.55 | 37.2 | 139 |
| Exponential | 0.09 | −0.58 | 36.3 | — |

Predicted Omega_HI: ~4e-4 at z=0, rising to ~1e-3 at z~2–3. b_HI: ~0.7 at z=0, rising to ~2.2 at z~3.

## Equations Used in This Pipeline

**M_HI–halo mass relation (Eq. 3.7):**
$$M_\text{HI}(M,z) = \alpha \, f_{H,c} \, M \left(\frac{M}{10^{11} h^{-1} M_\odot}\right)^\beta \exp\left[-\left(\frac{v_{c,0}}{v_c(M,z)}\right)^3\right]$$

where $f_{H,c} = (1 - Y_P) \Omega_B / \Omega_M$, $Y_P = 0.24$.

**Altered NFW HI profile (Eq. 3.9):**
$$\rho_\text{HI}(r) = \rho_0 \frac{r_s^3}{(r + 0.75 r_s)(r + r_s)^2}$$

**HI concentration (Eq. 3.8):**
$$c_\text{HI}(M,z) = c_{HI,0} \left(\frac{M}{10^{11} h^{-1} M_\odot}\right)^{-0.109} \frac{4}{(1+z)^{0.13}}$$

**Mean HI density (Eq. 3.2):** $\bar\rho_\text{HI}(z) = \int (dn/dM) \, M_\text{HI} \, dM$

**HI bias (Eq. 3.6):** $b_\text{HI}(z) = (1/\bar\rho_\text{HI}) \int (dn/dM) \, M_\text{HI} \, b(M) \, dM$

**HI power spectra (Eqs. 3.12–3.13):** 1-halo and 2-halo terms using u_HI Fourier transform.

## Implementation

**Module:** `hi_model.py` — `M_HI()`, `c_HI()`, `rho_HI_profile()`, `u_HI()`, `rho_HI_mean()`, `Omega_HI()`, `T_bar_b()`, `b_HI()`, `P_HI_1h/2h()`, `W_HI()`

**Parameters adopted:** Exponential profile values (alpha=0.09, beta=−0.58, v_c0=36.3) for correct Omega_HI(z) trend. Note: Pinetti et al. adopted different values (alpha=0.176, beta=−0.69, v_c0=101.61) which produce Omega_HI that decreases with z.

**Known limitation:** The halo model with SMT mass function produces Omega_HI that decreases with z even with v_c0=36.3, while observations show it increasing. This is a fundamental limitation of the analytic halo model approach at high z.
