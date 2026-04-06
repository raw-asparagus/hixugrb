# Dominguez et al. (2011) — EBL Opacity Model

**Authors:** A. Dominguez, J. R. Primack, D. J. Rosario, et al.
**Journal:** MNRAS 410(4), 2556–2578
**arXiv:** [1007.1459](https://arxiv.org/abs/1007.1459)

## Abstract

Determines the evolving extragalactic background light (EBL) spectrum from z=0 to z~4 based on observed K-band galaxy luminosity functions and SED type fractions from ~6000 AEGIS galaxies. Computes gamma-ray pair-production optical depth tau(E,z).

## Methodology

- K-band galaxy LF evolution to z=4
- SED type fractions from Spitzer SWIRE template fitting
- ~6000 galaxies from AEGIS survey (z = 0.2–1.0)
- Calculates UV-to-IR luminosity densities and cosmic SFR density
- Derives pair-production optical depth for gamma-ray propagation

## Key Results

- Complete EBL spectrum UV (0.1 um) to IR (~1000 um)
- tau(E,z) parameterization for gamma-ray astronomy
- Well-constrained in UV to mid-IR; less precise in far-IR
- Standard reference for Fermi-LAT and CTA analyses

## Physical Process

Gamma-ray pair production on EBL photons: $\gamma_\text{HE} + \gamma_\text{EBL} \to e^+e^-$

- Threshold: ~30 GeV at z~0.5; ~10 GeV at z~2
- tau > 1 (opaque): E > 100 GeV at z > 0.5
- tau << 1 (transparent): E < 10 GeV at any z < 1

## Equation Used

**Attenuation factor:** $A(E,z) = e^{-\tau(E,z)}$

tau(E,z) provided as 2D tabulated grid (energy vs redshift) via the `ebltable` Python package.

## Repository Use

Used by `ebl.py` as the default tabulated EBL attenuation model.
