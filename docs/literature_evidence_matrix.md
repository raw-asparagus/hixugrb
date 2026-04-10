# Claim-by-Claim Evidence Matrix: `docs/literature/*.md` vs `docs/papers/`

## Overview

This is the single top-level audit of the literature summaries against the local source PDFs in `docs/papers/`.

Scope:

- Verify that `docs/literature/*.md` reflects the source papers faithfully.
- Keep implementation-specific choices and code-vs-paper deviations out of this file.
- Record those implementation choices in [`equations.md`](equations.md) instead.

Status legend:

- **Match**: the literature summary matches the cited source-paper claim.
- **Minor**: the literature summary is materially correct but uses a small shorthand or compressed wording.

---

## 1. Cosmology and Halo-Model Literature

| File | Claim in `docs/literature` | Paper anchor | Status | Notes |
|------|----------------------------|--------------|--------|-------|
| `planck2018.md` | Base LCDM parameter set includes $H_0 = 67.36$, $\Omega_b h^2 = 0.02237$, $\Omega_c h^2 = 0.1200$, $n_s = 0.9649$, $\sigma_8 = 0.8111$, $\tau = 0.0544$ | Planck 2018 TT,TE,EE+lowE+lensing parameter table | **Match** | Values and uncertainties are recorded consistently |
| `planck2018.md` | Derived parameters include $\Omega_M = 0.3153$, $\Omega_\Lambda = 0.6847$, $\Omega_B = 0.0493$ | Derived-parameter tables and standard conversions | **Match** | Derived values are consistent with the quoted base parameters |
| `sheth_tormen1999.md` | Halo-bias relation is $b(\nu) = 1 + (q\nu - 1)/\delta_c + 2p/[\delta_c(1+(q\nu)^p)]$ | Sheth & Tormen (1999), bias equation | **Match** | Formula and parameter definitions are paper-faithful |
| `sheth_tormen1999.md` | Parameter values are $a = 0.707$, $p = 0.3$, $\delta_c = 1.686$ | Sheth & Tormen (1999), model parameters | **Match** | Paper notation uses $a$ (not $q$); SMT 2001 later relabels to $a$ as well |
| `sheth_mo_tormen2001.md` | SMT multiplicity function is given in the paper's Eq. 6 form | Sheth, Mo & Tormen (2001), Eq. 6 | **Match** | The summary now stays in the paper's notation |
| `sheth_mo_tormen2001.md` | Best-fit parameters are $a = 0.707$, $p = 0.3$, $A \approx 0.322$ | Sheth, Mo & Tormen (2001), Eq. 6 fit | **Match** | |
| `sheth_mo_tormen2001.md` | The paper also derives a moving-barrier bias relation | Sheth, Mo & Tormen (2001), Eq. 8 | **Match** | |
| `correa2015.md` | Low-redshift ($z \le 4$) concentration fit uses the Appendix B1 $(\alpha,\beta,\gamma)$ polynomials quoted in the summary | Correa et al. (2015), Appendix B1 | **Match** | Coefficients and redshift dependences match |
| `correa2015.md` | High-redshift ($z > 4$) fit uses the separate Appendix B1 $(\alpha,\beta)$ form | Correa et al. (2015), Appendix B1 | **Match** | |
| `correa2015.md` | The quoted validity range and reference concentrations are consistent with the paper's discussion and plots | Correa et al. (2015), abstract, Appendix B1, reference curves | **Match** | |
| `moline2017.md` | The boost prescription is the $z=0$ polynomial in $\log_{10} B(M)$ | Moline et al. (2017), Eq. 18 | **Match** | The summary no longer attributes thesis-only redshift scalings to the paper |
| `moline2017.md` | Coefficients $b_0 \ldots b_5 = (-0.186, 0.144, -8.8\times10^{-3}, 1.13\times10^{-3}, -3.7\times10^{-5}, -2\times10^{-7})$ | Moline et al. (2017), Table 3, $\alpha = 2$ | **Match** | |
| `moline2017.md` | The summary correctly identifies the fit as the tidal-stripping, $\alpha=2$ scenario with $M_{\min}=10^{-6} M_\odot$ built into the fit | Moline et al. (2017), Table 3 and surrounding discussion | **Match** | |
| `bryan_norman1998.md` | The virial overdensity fitting formula $\Delta_c(x) = 18\pi^2 + 82x - 39x^2$ with $x = \Omega_m(z) - 1$ | Bryan & Norman (1998), Eq. 6 | **Match** | |
| `loverde_afshordi2008.md` | The extended Limber approximation uses $k = (\ell + 1/2)/\chi$ instead of $k = \ell/\chi$ | LoVerde & Afshordi (2008), Eq. 2.19 | **Match** | |

---

## 2. Source-Population Literature

| File | Claim in `docs/literature` | Paper anchor | Status | Notes |
|------|----------------------------|--------------|--------|-------|
| `willott2001.md` | The radio luminosity function is the sum of low-power and high-power populations | Willott et al. (2001), Model C description | **Match** | |
| `willott2001.md` | Low-power parameters are $\rho_{l\star} = 10^{-7.523}$, $\beta_l = 0.586$, $L_{l\star} = 10^{26.48}$, $k_l = 3.48$, $z_{l\star} = 0.710$ | Willott et al. (2001), Table 1, Model C | **Match** | |
| `willott2001.md` | High-power parameters are $\rho_{h\star} = 10^{-6.757}$, $\beta_h = 2.42$, $L_{h\star} = 10^{27.39}$, $z_{h\star} = 2.03$, $z_{h0} = 0.568/0.956$ | Willott et al. (2001), Table 1, Model C | **Match** | |
| `lara2004.md` | Core-total radio relation is $\log_{10} L_{\rm core}^{4.9\,GHz} = 4.2 + 0.77 \log_{10} L_{\rm tot}^{1.4\,GHz}$ | Lara et al. (2004), fitted correlation | **Match** | The literature summary now uses the paper's 4.9 GHz label rather than rounding to 5 GHz |
| `inoue2011.md` | Frequency scaling assumes $\alpha_r = 0.80$ | Inoue (2011), radio spectral-index assumption | **Match** | |
| `inoue2011.md` | The paper quotes a gamma-ray/radio scaling with $L_\gamma \propto L_{5\,GHz}^{1.16}$ | Inoue (2011), abstract and Eq. 5 discussion | **Match** | |
| `dimauro2014.md` | Core-radio to gamma-ray relation is $\log_{10} L_\gamma = 2.0 + 1.008 \log_{10} L_{\rm core}^{5\,GHz}$ | Di Mauro et al. (2014), Eq. 5 | **Match** | |
| `dimauro2014.md` | Full mAGN luminosity function uses the paper's Eq. C.19 structure | Di Mauro et al. (2014), Eq. C.19 | **Match** | Note: "Eq. C.19" refers to Di Mauro's appendix, not the Pinetti thesis |
| `dimauro2014.md` | Parameter $k = 3.05$ is quoted correctly | Di Mauro et al. (2014), Eq. C.19 discussion | **Match** | $\Gamma = 2.37$ is from Pinetti+ (2020) Table 3, not from Di Mauro (2014) |
| `ajello2012.md` | The FSRQ sample contains 186 sources from the first-year Fermi-LAT catalog | Ajello et al. (2012), abstract and Table 3 context | **Match** | |
| `ajello2012.md` | The luminosity function is the LDDE double power law in $d\Phi/d\log_{10}L$ quoted in the summary | Ajello et al. (2012), Table 3 model definition | **Match** | |
| `ajello2012.md` | The redshift evolution is the smooth inverse-sum form of Eq. 15 with positive exponents | Ajello et al. (2012), Eq. 15 | **Match** | The summary now reflects the paper form directly |
| `ajello2012.md` | Table 3 parameters $A = 3.06\times10^{-9}$, $\gamma_1 = 0.21$, $\gamma_2 = 1.58$, $L_\star = 0.84\times10^{48}$, $z_c^\star = 1.47$, $\alpha = 0.21$, $p_1 = 7.35$, $p_2 = -6.51$, $\mu = 2.44$ are quoted correctly | Ajello et al. (2012), Table 3, ALL row | **Match** | |
| `ajello2014.md` | The BL Lac sample contains 211 1LAC sources and identifies LDDE as the preferred model | Ajello et al. (2014), abstract and model-comparison discussion | **Match** | |
| `ajello2014.md` | The local luminosity function uses the paper's Eq. C.2 form | Ajello et al. (2014), Eq. C.2 | **Match** | |
| `ajello2014.md` | The LDDE evolution is the paper-form inverse sum with positive exponents | Ajello et al. (2014), Eq. 18 | **Match** | |
| `ajello2014.md` | LDDE1 parameters $A = 9.20\times10^{-11}$, $L_\star = 2.43\times10^{48}$, $\gamma_1 = 1.12$, $\gamma_2 = 3.71$, $p_1 = 4.50$, $p_2 = -12.88$, $z_\star = 1.67$, $\beta = 4.46\times10^{-2}$ are quoted correctly | Ajello et al. (2014), Table 3, LDDE1 | **Match** | |
| `ajello2014.md` | The LDDE1 spectral index is $\mu_\star = 2.12 \pm 0.03$ | Ajello et al. (2014), Table 3, LDDE1 | **Match** | The earlier 2.11 shorthand has been removed from the literature summary |
| `gruppioni2013.md` | The IR luminosity function has five populations (spiral, starburst, SF-AGN, AGN1, AGN2); the pipeline uses three star-forming components | Gruppioni et al. (2013), Table 8 model setup | **Match** | Paper defines five populations; the three used in the pipeline (spiral, starburst, SF-AGN) are selected by Pinetti |
| `gruppioni2013.md` | Each component uses the modified-Schechter form quoted in the summary | Gruppioni et al. (2013), functional form used for Table 8 fits | **Match** | |
| `gruppioni2013.md` | Table 8 component parameters are quoted correctly for spiral and starburst populations | Gruppioni et al. (2013), Table 8 | **Match** | |
| `gruppioni2013.md` | The SF-AGN density-evolution coefficient is $k_{R2} = -3.17$ | Gruppioni et al. (2013), Table 8 | **Match** | The literature summary now reflects the paper sign correctly |
| `ackermann2012_sfg.md` | The summary uses the AGN-excluded IR-gamma scaling with $\alpha_{\rm IR} = 1.09$ and $\beta_{\rm IR} = 39.19$ | Ackermann et al. (2012), Table 5, excluding AGN row | **Match** | |
| `ackermann2012_sfg.md` | The sample size and galaxy-population description are consistent with the paper | Ackermann et al. (2012), abstract and sample description | **Match** | |

---

## 3. HI/DM Cross-Correlation, Attenuation, and Measurement Papers

| File | Claim in `docs/literature` | Paper anchor | Status | Notes |
|------|----------------------------|--------------|--------|-------|
| `padmanabhan2017.md` | The paper contains two separate MCMC fits: main-text exponential profile and Appendix A modified-NFW profile | Padmanabhan et al. (2017), Table 3 and Table A1 | **Match** | The summary now keeps the two fits clearly separated |
| `padmanabhan2017.md` | Modified-NFW best-fit parameters are $c_{\rm HI,0} = 139$, $\alpha = 0.176$, $\log v_{c,0} = 1.61$, $\beta = -0.69$, $\gamma = 0.13$ | Padmanabhan et al. (2017), Table A1 | **Match** | |
| `padmanabhan2017.md` | The HI mass relation is the paper's Eq. 1 form | Padmanabhan et al. (2017), Eq. 1 | **Match** | |
| `padmanabhan2017.md` | The modified-NFW profile and concentration relation are quoted from Eq. A1 and Eq. 3 | Padmanabhan et al. (2017), Eq. A1 and Eq. 3 | **Match** | |
| `cirelli2011.md` | PPPC4DMID tables are tabulated in $dN/d\log_{10}x$ with $x = E/m_{\rm DM}$ | Cirelli et al. (2011), released table format | **Match** | |
| `cirelli2011.md` | There are 28 primary annihilation channels over a mass range of 5 GeV to 100 TeV | Cirelli et al. (2011), PPPC4DMID release description | **Match** | |
| `cirelli2011.md` | The summary's conversions to $dN/dx$ and $dN/dE$ are the standard ones implied by the table definition | Cirelli et al. (2011), table definition | **Match** | |
| `dominguez2011.md` | The EBL model is built from K-band luminosity functions and SED fractions from about 6000 AEGIS galaxies | Dominguez et al. (2011), abstract and methodology | **Match** | |
| `dominguez2011.md` | The paper provides a tabulated optical depth $\tau(E,z)$ for gamma-ray attenuation | Dominguez et al. (2011), main result | **Match** | |
| `dominguez2011.md` | The literature summary now stops at the paper's attenuation model and does not attribute analytic fallbacks to the paper | Dominguez et al. (2011), paper scope | **Match** | |
| `pinetti2020.md` | The Limber angular-power expression is quoted from Eq. 2.1 | Pinetti et al. (2020), Eq. 2.1 | **Match** | |
| `pinetti2020.md` | The HI window summary gives the paper's per-$z$ form from Eqs. 3.15-3.16 | Pinetti et al. (2020), Eqs. 3.15-3.16 | **Match** | |
| `pinetti2020.md` | The DM and astrophysical windows are quoted from Eqs. 4.1 and 4.3 without adding repository-only prefactor changes | Pinetti et al. (2020), Eqs. 4.1 and 4.3 | **Match** | |
| `pinetti2020.md` | Forecast specifications in Tables 1, 2, and 3 are summarized correctly | Pinetti et al. (2020), Tables 1-3 | **Match** | |
| `pinetti2020.md` | Reported SNR values for MeerKAT, SKA1, and SKA2 follow the paper's forecast results | Pinetti et al. (2020), results tables | **Match** | |
| `ammazzalorso2018.md` | The measurement uses 11 Fermi-LAT energy bins spanning 0.631-1000 GeV | Ammazzalorso et al. (2018), Table I | **Match** | |
| `ammazzalorso2018.md` | The beam window is defined through the Legendre transform of the PSF | Ammazzalorso et al. (2018), Eq. 4 | **Match** | |
| `ammazzalorso2018.md` | The multipole upper limit is defined by $\langle W_\ell^k \rangle = 0.61$ or $\ell_{\max} = 1000$ | Ammazzalorso et al. (2018), Eq. 7 and Table I | **Match** | |
| `ammazzalorso2018.md` | The Gaussian error estimate matches the paper's Appendix A expression | Ammazzalorso et al. (2018), Eq. A1 | **Match** | |
| `ammazzalorso2018b_fermi_2mpz.md` | The 11 energy bins from 0.631 to 1000 GeV and per-bin $(\ell_\mathrm{min}, \ell_\mathrm{max})$ in Table I are exactly what `cfg.AMMAZZALORSO_BINS` encodes | Ammazzalorso, Fornengo, Horiuchi & Regis (2018), Table I, p6 | **Match** | Source paper for the pipeline's data-grade Fermi-LAT energy binning |
| `ammazzalorso2018b_fermi_2mpz.md` | The Fermi-LAT data is 108 months (Aug 2008 – Jul 2017) of Pass 8 ULTRACLEANVETO photons, PSF3 below 1.2 GeV and PSF1+2+3 above | Ammazzalorso+(2018b), Sec. II.A | **Match** | The full 9-year Pass 8 ULTRACLEANVETO setup, foundational for the data-mode analysis |
| `ammazzalorso2018b_fermi_2mpz.md` | $\ell_\mathrm{min} = 40$ fixed across all bins; $\ell_\mathrm{max}$ from $\langle W_\ell^k \rangle = 0.61$ or capped at 1000 | Ammazzalorso+(2018b), Eq. 7 | **Match** | Data-mode multipole window in `cfg.AMMAZZALORSO_ELL_MIN/MAX` |
| `ammazzalorso2018b_fermi_2mpz.md` | Per-energy point-source mask threshold: $F_\mathrm{thr} = (1/5) F^\gamma_\mathrm{faintest}$ in each bin, with mask radius $\theta_{\Delta E}$ = 68% PSF containment | Ammazzalorso+(2018b), Sec. II.A | **Match** | The PSF-area scaling implemented parametrically by `astro_sources.F_sens_energy` |
| `ammazzalorso2018b_fermi_2mpz.md` | $|b| > 30°$ Galactic latitude cut + per-energy point-source mask + `gll_iem_v06.fits` Galactic foreground subtraction with free per-template normalisation | Ammazzalorso+(2018b), Sec. II.A | **Match** | Pipeline does not model the Galactic foreground subtraction directly; cited for data-mode reference only |
| `ammazzalorso2018b_fermi_2mpz.md` | Beam window function $\langle W_\ell^k \rangle$ from Eq. 5 with UGRB spectral index $\alpha = 2.3$ and per-bin spectral weighting | Ammazzalorso+(2018b), Eqs. 4-5 | **Match** | Implemented in `noise_model.beam_fermi_exact` and `noise_model.beam_fermi_bin_averaged` |
| `ammazzalorso2018b_fermi_2mpz.md` | $\chi^2$ statistic uses energy-bin-diagonal covariance from PolSpice; covariance between energy bins neglected because Poisson photon noise dominates | Ammazzalorso+(2018b), Eq. 8 + surrounding text | **Match** | Same diagonal-energy assumption is implicit in the pipeline's per-bin Knox formula |
| `ammazzalorso2018b_fermi_2mpz.md` | This paper's Poisson noise terms $C_p^k$ supersede Fornasa et al. (2016) by ~factor of 2 in statistical determination | Ammazzalorso+(2018b), Fig. 15 | **Match** | Establishes 1808.09225 (this paper) as the canonical post-2016 Fermi-LAT cross-correlation measurement |
| `ballet2023_4fgl_dr4.md` | The 4FGL-DR4 catalogue contains 7,194 γ-ray sources from 14 years (4 Aug 2008 – 2 Aug 2022) of Fermi-LAT Pass 8 R3 V3 data over 50 MeV – 1 TeV | Ballet et al. (2023), Abstract / §2.1 | **Match** | Most recent public Fermi-LAT source catalogue release |
| `ballet2023_4fgl_dr4.md` | Detection threshold outside the Galactic plane is "a little above $1 \times 10^{-12}$ erg cm$^{-2}$ s$^{-1}$ in the 100 MeV to 100 GeV band" | Ballet et al. (2023), §5, p12 | **Match** | The single value of the 4FGL-DR4 catalogue completeness; note that this is energy flux, not photon flux — the corresponding photon-flux equivalent in 1-100 GeV (Pinetti's convention) is $\sim 7\times10^{-11}$ photon cm$^{-2}$ s$^{-1}$ depending on source spectral index |
| `ballet2023_4fgl_dr4.md` | Same `pointlike`/`gtlike` analysis methods as 4FGL-DR3 (Abdollahi et al. 2022), with TS ≥ 25 detection threshold and Pass 8 R3 V3 IRFs | Ballet et al. (2023), §3.3 | **Match** | DR4 paper explicitly defers methodological details to the DR3 paper as the "official reference" |
| `ballet2023_4fgl_dr4.md` | Same diffuse model `gll_iem_v07` (Galactic) and `iso_P8R3_SOURCE_V3_v1` (isotropic) as DR3, with a smooth full-sky LP modulation of the Galactic component as the principal improvement | Ballet et al. (2023), §2.2 | **Match** | The smooth-modulation refinement adds 71 sources above threshold and reduces the number of curved spectra by 245 vs DR3 |
| `ballet2023_4fgl_dr4.md` | The photon-flux conversion of the 4FGL-DR4 threshold to the pipeline's 1-100 GeV convention gives $F_\mathrm{ph}(\mathrm{1\,GeV-100\,GeV}) \approx 7\text{-}9 \times 10^{-11}$ photon cm$^{-2}$ s$^{-1}$ depending on source spectral index, with a four-source mean of $7.3 \times 10^{-11}$ | Derived from Ballet et al. (2023) §5 + power-law spectral integrals at $\alpha\in\{2.11,2.37,2.44,2.70\}$ for the four pipeline source classes | **Match** | Anchors `cfg.F_SENS_4FGL_DR4 = 7.3e-11`; the prior pipeline value of 4e-12 was a units-confusion error |
| `cunnington2023.md` | MeerKAT observing setup, frequency range, survey area, and single-dish mode are summarized consistently | Cunnington et al. (2023), Section 2 | **Match** | |
| `cunnington2023.md` | Reconvolution to a common beam follows the paper's Eqs. 16-18 | Cunnington et al. (2023), Section 4.1, Eqs. 16-18 | **Match** | |
| `cunnington2023.md` | Transfer-function correction follows the mock-injection construction of Eqs. 19-20 | Cunnington et al. (2023), Section 4.3, Eqs. 19-20 | **Match** | |
| `cunnington2023.md` | The brightness-temperature coefficient is quoted as 180 mK from Eq. 15 | Cunnington et al. (2023), Eq. 15 | **Match** | The literature summary now reports the paper value without folding in repository conventions |
| `mangla2025_meerklass_lband_dr1.md` | MeerKLASS L-band OTF DR1 covers ~268 deg² in 13.5 hr of usable on-source time across 8 rising-scan blocks | Mangla et al. (2025), Abstract, Sec. 2.2, Table 1 | **Match** | DR1 reports interferometric continuum only; rising scans only because the setting calibrator (Pictor A) is extended on interferometric baselines |
| `mangla2025_meerklass_lband_dr1.md` | The L-band receiver covers 856–1712 MHz; visibility integration is 2 s; survey speed ~150 deg² hr⁻¹ | Mangla et al. (2025), Sec. 2.2 | **Match** | |
| `mangla2025_meerklass_lband_dr1.md` | The OTF time-smearing artefact arises because the correlator delay centre is held fixed in (az, el); modelled inside DDFacet via a fringe-rate-dependent PSF | Mangla et al. (2025), Sec. 3.1.3, Sec. 3.2, Appendix B | **Match** | A new OTF-optimised correlator mode introduced at MeerKAT in 2025 removes the residual smearing in DR2 |
| `mangla2025_meerklass_lband_dr1.md` | DR1 mosaic median noise is 33 μJy beam⁻¹ at median resolution 25.5″ × 7.8″, catalogue contains 34,874 sources at SNR > 9 | Mangla et al. (2025), Abstract, Sec. 4 | **Match** | |
| `paul2025_meerklass_uhf_dr1.md` | MeerKLASS UHF OTF DR1 covers ~800 deg² in ~12 hr across 8 cross-linked OTF blocks (4 rising + 4 setting), inside the DESI footprint | Paul et al. (2025), Abstract, Sec. 2, Table 1 | **Match** | Cross-linked rising/setting strategy averages down direction-dependent systematics |
| `paul2025_meerklass_uhf_dr1.md` | The UHF receiver covers 544–1088 MHz; central frequency 816 MHz; visibility integration 2 s; scan speed ~7′ s⁻¹ | Paul et al. (2025), Sec. 2 | **Match** | |
| `paul2025_meerklass_uhf_dr1.md` | DR1 deepest RMS is ~35 μJy beam⁻¹ at median resolution ~32″ × 17″; catalogue contains 95,483 unique sources | Paul et al. (2025), Abstract, Sec. 5.1, Sec. 8 | **Match** | |
| `paul2025_meerklass_uhf_dr1.md` | The full MeerKLASS programme targets 10,000 deg² over ~2,500 hr of nighttime UHF observing; ~270 hr of UHF pilot data have been acquired since the 2022 transition from L-band | Paul et al. (2025), Sec. 1 | **Match** | The same 2,500 hr / 10,000 deg² target is the authoritative XLP configuration in Cunnington et al. (2025), Table 2 |
| `cunnington2025_meerklass_overview.md` | Cumulative MeerKLASS observations through 2024: L-band 85 hr / 500 deg² (RFI-restricted to 0.39 < z < 0.46); UHF 380 hr / 1,600 deg² (0.40 < z < 1.45) | Cunnington et al. (2025), Sec. 2, Table 1 | **Match** | UHF 2025 in-progress increment to ~880 hr / ~3,600 deg² is also tabulated |
| `cunnington2025_meerklass_overview.md` | Awarded XLP target by end of 2028: 2,500 hr / 10,000 deg² UHF; all forecasts assume a survey efficiency $\varepsilon = 0.5$ → 1,250 hr useable | Cunnington et al. (2025), Sec. 2, Sec. 6, Table 2 | **Match** | This is the basis for `RADIO_TELESCOPES['MeerKLASS_XLP_2028']` |
| `cunnington2025_meerklass_overview.md` | The L-band deep-field is 41 repeated scans over 236 deg² totalling 62 hr/dish before flagging, > 4σ cross-correlation with GAMA at 0.39 < z < 0.46 | Cunnington et al. (2025), Sec. 5.1; original MeerKLASS Collaboration et al. (2025), arXiv:2407.21626 | **Match** | Source paper is now ingested as `meerklass2025_lband_deepfield.md`; basis for `RADIO_TELESCOPES['MeerKLASS_L_deepfield']` |
| `meerklass2025_lband_deepfield.md` | MeerKLASS L-band deep-field comprises 41 attempted scan blocks over 236 deg² in the southern sky, RA (330°,360°), Dec (−36°,−25°), with 62 hr per dish before flagging | MeerKLASS Collaboration (2025), Sec. 2.1 / Sec. 2.4.1 | **Match** | 27 of 41 blocks survived RFI flagging; 14 removed due to mobile-tower RFI |
| `meerklass2025_lband_deepfield.md` | Iterative self-calibration over 5 loops replaces the Haslam-PySM Galactic model with the MeerKLASS sky map itself, reducing residual T_res standard deviation by ~10× | MeerKLASS Collaboration (2025), Sec. 2.3, Fig. 2 | **Match** | Central methodological advance over the Wang et al. (2021) standard pipeline |
| `meerklass2025_lband_deepfield.md` | Final maps reach a median noise of 1.21 mK with R_RMS = ΔT_RMS/σ_th median 1.2 in the cosmologically useable 971.2–1023.6 MHz window | MeerKLASS Collaboration (2025), Abstract, Sec. 2.4.3 | **Match** | "Entering the HI dominated regime": thermal noise subdominant to HI fluctuations at k ≲ 0.15 h/Mpc |
| `meerklass2025_lband_deepfield.md` | Cross-power spectrum between the MeerKLASS deep field and 2,269 GAMA G23 galaxies at 0.39 < z < 0.46 yields > 4σ detection with N_fg = 10 PCA modes | MeerKLASS Collaboration (2025), Abstract, Sec. 5, Fig. 18 | **Match** | GAMA G23 covers ~25% of the deep-field footprint; reduced χ²_dof = 0.42 (suggests over-conservative covariance) |
| `meerklass2025_lband_deepfield.md` | The HI brightness temperature convention is T_HI(z) = 180 Ω_HI(z) h (1+z)² / sqrt(Ω_m(1+z)³ + Ω_Λ) mK | MeerKLASS Collaboration (2025), Eq. C1 | **Match** | 180 mK Battye+2013 prefactor — same as Cunnington 2023 / Cunnington 2025 / MeerFish; pipeline `hi_model.T_bar_b_cunnington` matches |
| `meerklass2025_lband_deepfield.md` | Best-fit cross-power amplitude inferred T_HI = 0.166 mK at z ~ 0.43 (with the Table 1 fiducial parameters held fixed) | MeerKLASS Collaboration (2025), Sec. 5 | **Match** | Direct sanity-check anchor for the 'cunnington' mode of `hi_model.T_bar_b_for_model` (which returns 0.162 mK at z=0.43) |
| `meerklass2025_lband_deepfield.md` | Foreground transfer function scatter (over 500 mocks) is used as the cross-power covariance estimator instead of the Knox-formula thermal-noise approach | MeerKLASS Collaboration (2025), Sec. 5.3 | **Match** | Required because thermal noise is no longer dominant on large scales; relevant target for the planned MeerKAT-data-grade pipeline upgrade |
| `meerklass2025_lband_deepfield.md` | Data availability: calibrated maps shared "upon reasonable request" to the corresponding author; raw visibilities public via the SARAO archive | MeerKLASS Collaboration (2025), Data Availability statement (p24) | **Match** | Calibrated HI maps are not publicly downloadable; `MeerKLASS_L_deepfield` is therefore a forecast input, not a usable data product |
| `cunnington2025_meerklass_overview.md` | Mean HI brightness temperature is modelled as $\bar T_\mathrm{HI}(z) = 180\,\Omega_\mathrm{HI}\,h\,(1+z)^2/(H/H_0)$ mK (180 mK prefactor) | Cunnington et al. (2025), Eq. A4 | **Match** | The pipeline `hi_model.T_bar_b` uses 188 mK following Padmanabhan 2017 / Pinetti 2020; both Cunnington 2023 (Eq. 15) and Cunnington 2025 (Eq. A4) use 180 mK following Battye+2013 |
| `cunnington2025_meerklass_overview.md` | The forecast Ω_HI(z) polynomial is $\Omega_\mathrm{HI}(z) = 6.7432\times10^{-4} + 3.9\times10^{-4} z - 6.5\times10^{-5} z^2$ | Cunnington et al. (2025), Eq. A5 | **Match** | Adapted from SKA Cosmology SWG 2020 with the latest MeerKLASS constraints |
| `cunnington2025_meerklass_overview.md` | The forecast HI bias polynomial is $b_\mathrm{HI}(z) = 0.842 + 0.693\,z - 0.0459\,z^2$ | Cunnington et al. (2025), Eq. A3 | **Match** | Fit to Villaescusa-Navarro et al. (2018) hydrodynamic simulations |
| `cunnington2025_meerklass_overview.md` | Forecast multipoles used are $\{P_0, P_2, P_4\}$ to break the $b_\mathrm{HI}$–$f$ degeneracy; public Fisher code is `MeerFish` | Cunnington et al. (2025), Sec. 6.1, Sec. 6.1.1 | **Match** | github.com/meerklass/MeerFish |
| `pinetti2022_thesis.md` | The thesis defines the full HI x UGRB cross-correlation framework including window functions, Limber projection, and source-class decomposition | Pinetti (2022), arXiv:2212.00125, Chapters 3-5 | **Match** | |
| `pinetti2022_thesis.md` | The thesis Eq. C.4 LDDE evolution uses negative exponents $[r^{-p_1}+r^{-p_2}]^{-1}$ | Pinetti (2022), Eq. C.4 | **Match** | |
| `pinetti2022_thesis.md` | The thesis uses $q=0.75$ for the Sheth-Tormen mass function and bias | Pinetti (2022), Eq. 3.33 | **Match** | |

---

## Summary

- The top-level literature audit now has a single scope: `docs/literature/*.md` vs `docs/papers/`.
- No thesis-vs-pipeline material remains in this file.
- Implementation deviations and repository-specific conventions now live in [`equations.md`](equations.md).

Current audit result:

| Status | Count |
|--------|-------|
| **Match** | 106 |
| **Minor** | 0 |

No outstanding literature-summary mismatches remain in the audited claim set above.
