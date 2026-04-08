# Ajello et al. (2012) — The Luminosity Function of Fermi-detected Flat-Spectrum Radio Quasars

**Authors:** M. Ajello, M. S. Shaw, R. W. Romani, C. D. Dermer, L. Costamante, et al.
**Journal:** ApJ 751(2), 108
**arXiv:** [1110.3787](https://arxiv.org/abs/1110.3787)

## Abstract

Determines the gamma-ray luminosity function of flat-spectrum radio quasars (FSRQs) using 186 sources from the first-year Fermi-LAT catalog. Finds luminosity-dependent density evolution (LDDE) where more luminous FSRQs peak at earlier cosmic times.

## Methodology

- Maximum-likelihood fitting of space density vs rest-frame 0.1–100 GeV luminosity, redshift, and photon index
- Flux-limited sample: F_100 >= 10^{-8} ph/cm^2/s, ~4-5% incompleteness
- All sources spectroscopically confirmed
- Gaussian photon index distribution incorporated

## Key Results

- FSRQ density peaks at z ~ 0.5–2.0 (luminosity-dependent)
- Contribute ~9.3% of Fermi isotropic gamma-ray background
- Intrinsic unbeamed population: Lorentz factor gamma ~ 11.7
- Strong cosmological evolution similar to radio-quiet AGN

## Equations and Parameters Used (Table 3, LDDE model)

**LDDE double power-law:**
$$\frac{d\Phi}{d\log_{10} L} = \frac{A}{(L/L_c)^{\gamma_1} + (L/L_c)^{\gamma_2}}$$

**Smooth inverse-sum evolution (Eq. 15):**
$$e(z,L) = \left[\left(\frac{1+z}{1+z_c}\right)^{p_1} + \left(\frac{1+z}{1+z_c}\right)^{p_2}\right]^{-1}$$

*Note: The paper explicitly states this parametrization is "continuous around the redshift peak" (unlike a piecewise form). This is the same functional form as Ajello+(2014) for BL Lacs.*

**Luminosity-dependent peak:** $z_c(L) = z_c^* (L/10^{48})^\alpha$

| Parameter | Value | Unit |
|-----------|-------|------|
| A | 3.06 × 10⁴ | 10⁻¹³ Mpc⁻³ erg⁻¹ s |
| gamma_1 | 0.21 ± 0.12 | — |
| gamma_2 | 1.58 ± 0.27 | — |
| L* | 0.84 × 10⁴⁸ | erg/s |
| z_c* | 1.47 ± 0.16 | — |
| alpha | 0.21 ± 0.03 | — |
| p_1 | 7.35 ± 1.74 | — |
| p_2 | −6.51 ± 1.97 | — |
| mu (photon index) | 2.44 ± 0.01 | — |
