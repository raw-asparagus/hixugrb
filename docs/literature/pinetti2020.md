# Pinetti, Camera, Fornengo & Regis (2020) — HI Intensity Mapping Meets Gamma Rays

**Authors:** E. Pinetti, S. Camera, N. Fornengo, M. Regis
**Journal:** JCAP 2020(07), 044
**arXiv:** [1911.04989](https://arxiv.org/abs/1911.04989)

## Abstract

Derives the first theoretical prediction for the angular cross-correlation between the unresolved gamma-ray background (UGRB) and neutral-hydrogen 21-cm intensity mapping. The paper combines halo-model source terms for annihilating dark matter and for astrophysical gamma-ray emitters with forecasts for Fermi-LAT, MeerKAT, and SKA.

## Methodology

- Limber projection of 3D one-halo and two-halo power spectra into angular power spectra
- Halo-model treatment of HI, dark matter annihilation, and astrophysical gamma-ray source classes
- HI modeled with [Padmanabhan et al. (2017)](padmanabhan2017.md)
- Gamma-ray source classes: BL Lacs, FSRQs, mAGN, and SFG
- Forecasts for MeerKAT, SKA1, and SKA2 combined with Fermi-LAT and a next-generation gamma-ray instrument

## Key Equations

**Angular cross-power spectrum (Eq. 2.1):**
$$C_\ell^{ij} = \int \frac{d\chi}{\chi^2} W_i(\chi) W_j(\chi) P_{ij}\!\left(k = \frac{\ell}{\chi}, z\right)$$

**HI brightness temperature (Eq. 3.4):**
$$\bar{T}_b(z) = 44\,\mu\mathrm{K} \, \frac{\Omega_\mathrm{HI}(z)\,h}{2.45\times10^{-4}} \frac{(1+z)^2}{E(z)}$$

equivalently,
$$\bar{T}_b(z) \approx 180\,\Omega_\mathrm{HI}(z)\,h\,\frac{(1+z)^2}{E(z)}\,\mathrm{mK}$$

**DM window function (Eq. 4.1):**
$$W_\gamma^\mathrm{DM} = \frac{(\Omega_\mathrm{DM}\rho_c)^2}{4\pi} \frac{\langle\sigma v\rangle}{2m_\chi^2} (1+z)^3 \Delta^2(z) \frac{dN_\gamma}{dE'} e^{-\tau}$$

**Astrophysical gamma-ray window function (Eq. 4.3):**
$$W_\gamma^\mathrm{astro} = \frac{d_L^2}{(1+z)^2} \int_0^{L_\mathrm{thr}} \Phi(L,z) \frac{dF}{dE} \, dL$$

**Full Gaussian variance (Eq. 2.7):**
$$
\left(\Delta C_\ell^{ij}\right)^2 =
\frac{1}{(2\ell+1)f_\mathrm{sky}}
\left[
\left(C_\ell^{ij}\right)^2 +
\left(C_\ell^{ii} + \frac{N_i}{(B_\ell^i)^2}\right)
\left(C_\ell^{jj} + \frac{N_j}{(B_\ell^j)^2}\right)
\right]
$$

**Noise-dominated approximation used later for HI×γ forecasts (Eq. 5.5):**
$$
\left(\Delta C_\ell^{\mathrm{HI}\gamma}\right)^2 \simeq
\frac{1}{(2\ell+1)f_\mathrm{sky}}
\left[
\frac{N^\gamma}{(B_\ell^\gamma)^2}
\left(
C_\ell^{\mathrm{HI-HI}} + \frac{N^\mathrm{HI}}{(B_\ell^\mathrm{HI})^2}
\right)
\right]
$$

The important distinction is that Eq. 2.7 is the general variance expression, while Eq. 5.5 is the paper's later approximation after noting that gamma-ray noise dominates the error budget.

## Forecast Results

- MeerKAT + Fermi-LAT: astrophysical cross-correlation forecast at **SNR ≈ 3.6–3.7**
- SKA1 + Fermi-LAT: **SNR > 5** in Band 2
- SKA2 + Fermi-LAT: **SNR ≈ 6.7–8.2**
- With Fermi-LAT-class gamma-ray data, SKA1 can probe thermal WIMPs up to about **130 GeV**, and SKA2 up to about **200 GeV**
- With a next-generation gamma-ray instrument plus SKA2, sensitivity extends toward the **TeV scale**

## Instrument Specifications

**Radio (Table 1):**

- MeerKAT: 64 dishes, 13.5 m, UHF and L band
- SKA1: 133 SKA dishes + 64 MeerKAT dishes, 14.5 m
- SKA2: 2000 dishes

**Fermi-LAT (Table 2):**

- 12 energy bins from 0.5 to 1000 GeV
- Per-bin inputs include photon counts, sky fraction, and angular resolution

**Source spectral indices (Table 3):**

- BL Lac: $\alpha = 2.11$
- FSRQ: $\alpha = 2.44$
- mAGN: $\alpha = 2.37$
- SFG: $\alpha = 2.7$

## Repository Use

Primary theoretical reference for the repository's HI×UGRB forecast formalism, instrument setup, and validation targets.
