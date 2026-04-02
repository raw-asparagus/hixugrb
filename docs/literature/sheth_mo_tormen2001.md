# Sheth, Mo & Tormen (2001) — Halo Mass Function

**Authors:** R. K. Sheth, H. J. Mo, G. Tormen
**Journal:** MNRAS 323(1), 1–12
**arXiv:** [astro-ph/9907024](https://arxiv.org/abs/astro-ph/9907024)

## Abstract

Improves Press-Schechter predictions by accounting for ellipsoidal (rather than spherical) collapse. Develops the SMT multiplicity function widely used in modern halo models.

## Methodology

- Excursion set formalism with ellipsoidal collapse criterion
- Three free parameters fitted to N-body simulations
- Universal in peak height nu = delta_c^2 / sigma^2(M)

## Key Results

- Significantly reduced discrepancy vs Press-Schechter
- Parameters calibrated across SCDM, OCDM, LCDM cosmologies
- Foundation for modern halo model codes (including hmf Python package)

## Equation Used

**SMT multiplicity function:**
$$\nu f(\nu) = A \left[1 + (q\nu)^{-p}\right] \sqrt{\frac{q\nu}{2\pi}} \exp\left(-\frac{q\nu}{2}\right)$$

| Parameter | Value |
|-----------|-------|
| A | 0.3222 |
| q | 0.707 |
| p | 0.3 |

The mass function: $dn/dM = (\bar\rho/M^2) \, f(\sigma) \, |d\ln\sigma/d\ln M|$ where $f(\sigma) = 2 \nu f(\nu)$.

## Implementation

**Module:** `hmf_interface.py` — delegates to `hmf.MassFunction` with `hmf_model='SMT'`. Parameters in `config.py`: `SMT_A`, `SMT_Q`, `SMT_P`.
