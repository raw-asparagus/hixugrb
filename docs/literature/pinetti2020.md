# Pinetti, Camera, Fornengo & Regis (2020) — Primary Reference

**Authors:** E. Pinetti, S. Camera, N. Fornengo, M. Regis
**Journal:** JCAP 2020(07), 044
**arXiv:** [1911.04989](https://arxiv.org/abs/1911.04989)

## Abstract

Derives the first theoretical prediction of the cross-correlation signal between the unresolved gamma-ray background (UGRB) and neutral hydrogen (HI) 21-cm intensity mapping. Using Fermi-LAT gamma-ray data and forecasts for MeerKAT and SKA, the authors project sensitivity for constraining dark matter annihilation. The key innovation is combining two tracers with different density weightings: HI traces linear density, while DM annihilation traces density-squared, enabling clean separation via tomographic redshift discrimination.

## Methodology

- Limber approximation to project 3D power spectra to angular cross-power spectra
- Halo model decomposition into one-halo and two-halo terms
- Padmanabhan et al. (2017) HI model for abundance and clustering
- PPPC4DMID tables for DM annihilation photon yields
- Four astrophysical gamma-ray source classes (BL Lac, FSRQ, mAGN, SFG)
- Gaussian variance for SNR forecasting

## Key Results

- MeerKAT + Fermi-LAT astrophysical SNR ~ 3.7 (UHF band)
- SKA1 + Fermi-LAT SNR ~ 5.7 (Band 2)
- SKA2 + Fermi-LAT SNR ~ 8.2 (Band 1)
- SKA2 + next-gen gamma-ray telescope can probe thermal relic cross-section to ~TeV scale
- Cross-correlation naturally suppresses uncorrelated foregrounds

## Equations Used in This Pipeline

**Limber integral (Eq. 2.1):**
$$C_\ell^{ij} = \int \frac{d\chi}{\chi^2} W_i(\chi) W_j(\chi) P_{ij}\left(k = \frac{\ell+1/2}{\chi}, z\right)$$

**HI window function (Eqs. 3.15–3.16):**
$$W_\text{HI}(\chi) = \bar{T}_b(z) \, b_\text{HI}(z) \, \phi(z) \, \frac{H(z)}{c}$$

**DM window function (Eq. 4.1):**
$$W_\gamma^\text{DM} = \frac{(\Omega_\text{DM}\rho_c)^2}{4\pi} \frac{\langle\sigma v\rangle}{2m_\chi^2} \frac{(1+z)^3}{H(z)} \Delta^2(z) \frac{dN_\gamma}{dE'} e^{-\tau}$$

**Astrophysical window function (Eq. 4.3):**
$$W_\gamma^\text{astro} = \frac{d_L^2}{(1+z)^2} \int_0^{L_\text{thr}} \Phi(L,z) \frac{dF}{dE} dL$$

**Brightness temperature (Eq. 3.4):**
$$\bar{T}_b(z) = 188 \, h \, \Omega_\text{HI}(z) \frac{(1+z)^2}{E(z)} \text{ mK}$$

**Clumping factor (Eq. 4.2):**
$$\Delta^2(z) = \frac{1}{\bar\rho^2} \int \frac{dn}{dM} \int \rho^2 d^3x \, dM$$

**HI×DM cross-power (Eqs. 5.1–5.2):**
$$P_{\text{HI}\times\text{DM}}^\text{2h} = \left[\int \frac{dn}{dM} b \frac{\tilde{v}}{\Delta^2} dM\right] \left[\int \frac{dn}{dM} b \frac{\tilde{u}_\text{HI} M_\text{HI}}{\bar\rho_\text{HI}} dM\right] P_\text{lin}$$

**Variance (Eq. 5.5):**
$$(\Delta C_\ell)^2 = \frac{1}{(2\ell+1)f_\text{sky}} \frac{N^\gamma}{(B_\ell^\gamma)^2} \left[C_\ell^\text{HI} + \frac{N^\text{HI}}{(B_\ell^\text{HI})^2}\right]$$

**SNR (Eq. 5.6):** $\text{SNR}^2 = \sum_{\ell,E} [C_\ell / \Delta C_\ell]^2$

**Delta chi-squared (Eq. 5.7):** $\Delta\chi^2 = \sum_{\ell,E} [(C_\ell^\text{tot}/\sigma)^2 - (C_\ell^\text{astro}/\sigma)^2]$

## Instrument Specifications

**Radio (Table 1):** MeerKAT (64 dishes, 13.5m, UHF/L), SKA1 (197 dishes, 14.5m), SKA2 (2000 dishes)

**Fermi-LAT (Table 2):** 12 energy bins 0.5–1000 GeV with N_gamma, f_sky, sigma_0 per bin

**Source spectral indices (Table 3):** BL Lac α=2.11, FSRQ α=2.44, mAGN α=2.37, SFG α=2.7

## Implementation

Primary reference for: `angular_power.py`, `statistics.py`, `noise_model.py`, `config.py` (instrument specs and energy bins)
