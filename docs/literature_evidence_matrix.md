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
| `sheth_tormen1999.md` | Parameter values are $q = 0.707$, $p = 0.3$, $\delta_c = 1.686$ | Sheth & Tormen (1999), model parameters | **Match** | |
| `sheth_mo_tormen2001.md` | SMT multiplicity function is given in the paper's Eq. 6 form | Sheth, Mo & Tormen (2001), Eq. 6 | **Match** | The summary now stays in the paper's notation |
| `sheth_mo_tormen2001.md` | Best-fit parameters are $a = 0.707$, $p = 0.3$, $A \approx 0.322$ | Sheth, Mo & Tormen (2001), Eq. 6 fit | **Match** | |
| `sheth_mo_tormen2001.md` | The paper also derives a moving-barrier bias relation | Sheth, Mo & Tormen (2001), Eq. 8 | **Match** | |
| `correa2015.md` | Low-redshift ($z \le 4$) concentration fit uses the Appendix B1 $(\alpha,\beta,\gamma)$ polynomials quoted in the summary | Correa et al. (2015), Appendix B1 | **Match** | Coefficients and redshift dependences match |
| `correa2015.md` | High-redshift ($z > 4$) fit uses the separate Appendix B1 $(\alpha,\beta)$ form | Correa et al. (2015), Appendix B1 | **Match** | |
| `correa2015.md` | The quoted validity range and reference concentrations are consistent with the paper's discussion and plots | Correa et al. (2015), abstract, Appendix B1, reference curves | **Match** | |
| `moline2017.md` | The boost prescription is the $z=0$ polynomial in $\log_{10} B(M)$ | Moline et al. (2017), Eq. 18 | **Match** | The summary no longer attributes thesis-only redshift scalings to the paper |
| `moline2017.md` | Coefficients $b_0 \ldots b_5 = (-0.186, 0.144, -8.8\times10^{-3}, 1.13\times10^{-3}, -3.7\times10^{-5}, -2\times10^{-7})$ | Moline et al. (2017), Table 3, $\alpha = 2$ | **Match** | |
| `moline2017.md` | The summary correctly identifies the fit as the tidal-stripping, $\alpha=2$ scenario with $M_{\min}=10^{-6} M_\odot$ built into the fit | Moline et al. (2017), Table 3 and surrounding discussion | **Match** | |

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
| `dimauro2014.md` | Full mAGN luminosity function uses the paper's Eq. C.19 structure | Di Mauro et al. (2014), Eq. C.19 | **Match** | |
| `dimauro2014.md` | Parameters $k = 3.05$ and $\Gamma = 2.37$ are quoted correctly | Di Mauro et al. (2014), Eq. C.19 discussion | **Match** | |
| `ajello2012.md` | The FSRQ sample contains 186 sources from the first-year Fermi-LAT catalog | Ajello et al. (2012), abstract and Table 3 context | **Match** | |
| `ajello2012.md` | The luminosity function is the LDDE double power law in $d\Phi/d\log_{10}L$ quoted in the summary | Ajello et al. (2012), Table 3 model definition | **Match** | |
| `ajello2012.md` | The redshift evolution is the smooth inverse-sum form of Eq. 15 with positive exponents | Ajello et al. (2012), Eq. 15 | **Match** | The summary now reflects the paper form directly |
| `ajello2012.md` | Table 3 parameters $A = 3.06\times10^{-9}$, $\gamma_1 = 0.21$, $\gamma_2 = 1.58$, $L_\star = 0.84\times10^{48}$, $z_c^\star = 1.47$, $\alpha = 0.21$, $p_1 = 7.35$, $p_2 = -6.51$, $\mu = 2.44$ are quoted correctly | Ajello et al. (2012), Table 3, ALL row | **Match** | |
| `ajello2014.md` | The BL Lac sample contains 211 1LAC sources and identifies LDDE as the preferred model | Ajello et al. (2014), abstract and model-comparison discussion | **Match** | |
| `ajello2014.md` | The local luminosity function uses the paper's Eq. C.2 form | Ajello et al. (2014), Eq. C.2 | **Match** | |
| `ajello2014.md` | The LDDE evolution is the paper-form inverse sum with positive exponents | Ajello et al. (2014), Eq. 18 | **Match** | |
| `ajello2014.md` | LDDE1 parameters $A = 9.20\times10^{-11}$, $L_\star = 2.43\times10^{48}$, $\gamma_1 = 1.12$, $\gamma_2 = 3.71$, $p_1 = 4.50$, $p_2 = -12.88$, $z_\star = 1.67$, $\beta = 4.46\times10^{-2}$ are quoted correctly | Ajello et al. (2014), Table 3, LDDE1 | **Match** | |
| `ajello2014.md` | The LDDE1 spectral index is $\mu_\star = 2.12 \pm 0.03$ | Ajello et al. (2014), Table 3, LDDE1 | **Match** | The earlier 2.11 shorthand has been removed from the literature summary |
| `gruppioni2013.md` | The IR luminosity function is the sum of spiral, starburst, and SF-AGN components | Gruppioni et al. (2013), Table 8 model setup | **Match** | |
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
| `cunnington2023.md` | MeerKAT observing setup, frequency range, survey area, and single-dish mode are summarized consistently | Cunnington et al. (2023), Section 2 | **Match** | |
| `cunnington2023.md` | Reconvolution to a common beam follows the paper's Eqs. 16-18 | Cunnington et al. (2023), Section 4.1, Eqs. 16-18 | **Match** | |
| `cunnington2023.md` | Transfer-function correction follows the mock-injection construction of Eqs. 19-20 | Cunnington et al. (2023), Section 4.3, Eqs. 19-20 | **Match** | |
| `cunnington2023.md` | The brightness-temperature coefficient is quoted as 180 mK from Eq. 15 | Cunnington et al. (2023), Eq. 15 | **Match** | The literature summary now reports the paper value without folding in repository conventions |

---

## Summary

- The top-level literature audit now has a single scope: `docs/literature/*.md` vs `docs/papers/`.
- No thesis-vs-pipeline material remains in this file.
- Implementation deviations and repository-specific conventions now live in [`equations.md`](equations.md).

Current audit result:

| Status | Count |
|--------|-------|
| **Match** | 60 |
| **Minor** | 0 |

No outstanding literature-summary mismatches remain in the audited claim set above.
