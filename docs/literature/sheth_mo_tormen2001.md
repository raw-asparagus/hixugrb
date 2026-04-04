# Sheth, Mo & Tormen (2001) — Halo Mass Function

**Authors:** R. K. Sheth, H. J. Mo, G. Tormen
**Journal:** MNRAS 323(1), 1–12
**arXiv:** [astro-ph/9907024](https://arxiv.org/abs/astro-ph/9907024)

## Abstract

Improves Press-Schechter predictions by accounting for ellipsoidal (rather than spherical) collapse. Develops the SMT multiplicity function widely used in modern halo models.

## Methodology

- Excursion set formalism with ellipsoidal collapse criterion (moving barrier)
- Ellipsoidal barrier shape introduces mass-dependent collapse threshold (Eq. 3–4)
- GIF simulation mass function (Eq. 6) fitted with parameters a=0.707, q=0.3 (paper notation)
- Universal in peak height ν = δ_sc / σ(M) (paper convention; pipeline uses ν = δ_c² / σ²)

## Key Results

- Significantly reduced discrepancy vs Press-Schechter
- Parameters calibrated across SCDM, OCDM, LCDM cosmologies
- Foundation for modern halo model codes (including hmf Python package)

## Equation Used

**SMT multiplicity function (Eq. 6, GIF simulation fit):**
$$\nu f(\nu) = 2A \left[1 + \frac{1}{(a\nu^2)^p}\right] \sqrt{\frac{a\nu^2}{2\pi}} \exp\left(-\frac{a\nu^2}{2}\right)$$

where ν = δ_sc/σ (paper convention). The pipeline uses ν = δ_c²/σ² (i.e., ν_pipeline = ν_paper²), with the factor of 2 absorbed into A:

| Paper parameter | Pipeline parameter | Value |
|---|---|---|
| a | SMT_Q (= q) | 0.707 |
| q | SMT_P (= p) | 0.3 |
| 2A | — | 2 × 0.322 ≈ 0.644 |
| — | SMT_A (includes factor 2) | 0.3222 |

**Halo bias (Eq. 8, with barrier parameters a=0.707, b=0.5, c=0.6):**

The paper also derives the large-scale bias relation from the moving barrier. The pipeline uses the simpler [Sheth & Tormen (1999)](sheth_tormen1999.md) bias formula which is equivalent for practical purposes.

The mass function: $dn/dM = (\bar\rho/M^2) \, f(\sigma) \, |d\ln\sigma/d\ln M|$.

## Implementation

**Module:** `hmf_interface.py` — delegates to `hmf.MassFunction` with `hmf_model='SMT'`. Parameters in `config.py`: `SMT_A`, `SMT_Q`, `SMT_P`.
