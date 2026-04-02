# Planck Collaboration (2018) — Cosmological Parameters

**Authors:** Planck Collaboration (N. Aghanim et al.)
**Journal:** A&A 641, A6 (2020)
**arXiv:** [1807.06209](https://arxiv.org/abs/1807.06209)

## Abstract

Final full-mission Planck CMB measurements providing the most precise determination of LCDM cosmological parameters from combined temperature (TT), polarization (TE, EE), and lensing power spectra.

## Methodology

- Full-mission Planck CMB anisotropy measurements
- Combined analysis: TT,TE,EE + lowE + lensing
- 6-parameter base LCDM model
- Complementary data: Type Ia SNe, BAO

## Parameters Used in This Pipeline

### Primary (from TT,TE,EE+lowE+lensing)

| Parameter | Value | Unit |
|-----------|-------|------|
| H_0 | 67.36 +/- 0.54 | km/s/Mpc |
| h | 0.6736 | — |
| Omega_b h^2 | 0.02237 +/- 0.00015 | — |
| Omega_c h^2 | 0.1200 +/- 0.0012 | — |
| n_s | 0.9649 +/- 0.0042 | — |
| sigma_8 | 0.8111 +/- 0.0060 | — |
| tau | 0.0544 +/- 0.0073 | — |
| A_s | 2.1 × 10^{-9} | — |

### Derived

| Parameter | Value |
|-----------|-------|
| Omega_M | 0.3153 |
| Omega_Lambda | 0.6847 |
| Omega_B | 0.0493 |
| Omega_CDM | 0.2660 |
| Omega_DM | Omega_M - Omega_B = 0.266 |
| T_CMB | 2.7255 K |
| rho_crit | 2.775 × 10^{11} M_sun/h / (Mpc/h)^3 |

## Key Cosmological Implications

- Flat LCDM: Omega_k consistent with zero
- H_0 tension: 3.6 sigma below local measurement (~73 km/s/Mpc)
- DM = 26%, baryons = 5%, dark energy = 68% of universe
- Power-law primordial spectrum consistent with inflation

## Implementation

**Module:** `config.py` — All Planck 2018 parameters defined as constants (`H0`, `OMEGA_M`, `SIGMA_8`, etc.). Used by `cosmology.py` for CAMB initialization, E(z), H(z), chi(z), and by `hmf_interface.py` for mass function computation.
