# Sheth, Mo & Tormen (2001) — Ellipsoidal Collapse and an Improved Model for the Number and Spatial Distribution of Dark Matter Haloes

**Authors:** R. K. Sheth, H. J. Mo, G. Tormen
**Journal:** MNRAS 323(1), 1–12
**arXiv:** [astro-ph/9907024](https://arxiv.org/abs/astro-ph/9907024)

## Abstract

Improves Press-Schechter predictions by accounting for ellipsoidal (rather than spherical) collapse. Develops the SMT multiplicity function widely used in modern halo models.

## Methodology

- Excursion set formalism with ellipsoidal collapse criterion (moving barrier)
- Ellipsoidal barrier shape introduces mass-dependent collapse threshold (Eq. 3–4)
- GIF simulation mass function (Eq. 6) fitted with parameters $a=0.707$, $q=0.3$, and $A \approx 0.322$
- Universal in peak height ν = δ_sc / σ(M) (paper convention)

## Key Results

- Significantly reduced discrepancy vs Press-Schechter
- Parameters calibrated across SCDM, OCDM, LCDM cosmologies
- Foundation for modern halo model codes (including hmf Python package)

## Equation Used

**SMT multiplicity function (Eq. 6, GIF simulation fit):**
$$\nu f(\nu) = 2A \left[1 + \frac{1}{(a\nu^2)^q}\right] \sqrt{\frac{a\nu^2}{2\pi}} \exp\left(-\frac{a\nu^2}{2}\right)$$

where $\nu = \delta_\mathrm{sc}/\sigma$ in the paper's notation, with best-fit parameters $a = 0.707$, $q = 0.3$, and $A \approx 0.322$.

**Halo bias (Eq. 8, with barrier parameters a=0.707, b=0.5, c=0.6):**

The paper also derives the large-scale bias relation from the moving barrier.

The mass function: $dn/dM = (\bar\rho/M^2) \, f(\sigma) \, |d\ln\sigma/d\ln M|$.
