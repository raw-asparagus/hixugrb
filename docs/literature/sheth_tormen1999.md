# Sheth & Tormen (1999) — Large-Scale Halo Bias from the Peak-Background Split

**Authors:** R. K. Sheth, G. Tormen
**Journal:** MNRAS 308(1), 119–126
**arXiv:** [astro-ph/9901122](https://arxiv.org/abs/astro-ph/9901122)

## Abstract

Develops a practical relation between the halo mass function and the large-scale halo bias using the peak-background split. The key point of the paper is that knowledge of the **unconditional mass function** is sufficient to predict the large-scale bias, without requiring merger histories.

## Methodology

- Uses the GIF simulation mass function measured in SCDM, OCDM, and LCDM runs
- Applies the peak-background split directly to that mass function
- Compares the resulting bias prediction against Press-Schechter and Zeldovich-based alternatives
- Shows that the bias formula scales well with peak height across redshift

This paper does **not** present the later ellipsoidal-collapse moving-barrier derivation from [Sheth, Mo & Tormen (2001)](sheth_mo_tormen2001.md); instead it infers bias from the fitted GIF mass function itself.

## Key Results

- Massive halos are slightly **less** biased than the original Press-Schechter / Mo-White prediction
- Low-mass halos are **more** positively biased (less anti-biased) than Press-Schechter predicts
- The resulting bias relation agrees reasonably well with N-body measurements over a broad mass and redshift range

## Equation Used

**Eulerian halo bias (Eq. 12):**
$$b_\mathrm{Eul}(\nu) = 1 + \frac{a\nu - 1}{\delta_c} + \frac{2p}{\delta_c\left[1 + (a\nu)^p\right]}$$

with:

| Parameter | Value |
|-----------|-------|
| $a$ | 0.707 |
| $p$ | 0.3 |
| $\delta_c$ | 1.686 |
| $\nu$ | $\delta_c^2 / \sigma^2(M,z)$ |

The paper adopts the same $a=0.707$ and $p=0.3$ values that describe the GIF mass-function fit. Many later implementations rename the coefficient $a$ as $q$; the functional form is the same.

## Repository Use

Used by the repository as the halo-bias reference implemented in `halo_model.py`.
