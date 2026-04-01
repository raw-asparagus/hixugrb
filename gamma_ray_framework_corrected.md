# Gamma-ray framework for HI 21-cm cross-correlation studies

**The gamma-ray side of HI × γ-ray cross-correlation measurements provides a powerful, multi-spectral probe of both astrophysical source populations and dark matter annihilation in large-scale structure.** Following the formalism of Pinetti, Camera, Fornengo & Regis (2020), the observable cross-power spectrum between neutral hydrogen intensity maps and Fermi-LAT gamma-ray maps decomposes into distinct astrophysical and dark matter contributions, each with characteristic energy spectra, redshift kernels, and angular scale dependences. This framework exploits these differences tomographically and spectrally to separate a potential WIMP annihilation signal from astrophysical backgrounds — projecting sensitivity to the thermal relic cross-section for DM masses up to ~130 GeV with SKA × Fermi-LAT. Since the paper's publication, the Fermi-LAT dataset has nearly doubled to **~17.7 years**, the 4FGL catalog has grown to over **7,000 sources**, and several gamma-ray luminosity functions have been updated — but no measurement has fundamentally altered the framework's assumptions. The most pressing update needs involve the flux sensitivity threshold, EBL absorption models, and the absence of a confirmed "Fermissimo"-class successor mission.

---

## Part 1 — The unresolved gamma-ray background encodes the cosmos

The **Unresolved Gamma-Ray Background (UGRB)** — operationally identical to the Isotropic Diffuse Gamma-Ray Background (IGRB) — is the residual all-sky emission after subtracting resolved point sources and modeled Galactic diffuse emission. It comprises cumulative flux from sub-threshold extragalactic sources (blazars, misaligned AGN, star-forming galaxies), truly diffuse processes (intergalactic cosmic-ray interactions, structure-formation shocks), and potentially exotic contributions such as dark matter annihilation or decay. The UGRB is approximately isotropic but contains angular anisotropies: Poisson fluctuations from discrete unresolved sources dominate at small angular scales (high multipoles ℓ), while clustering of sources tracing large-scale structure contributes a 2-halo term at larger scales. Crucially, the UGRB is observation-time dependent — as Fermi-LAT accumulates data, fainter sources are resolved and removed, reducing the UGRB intensity.

The definitive spectral measurement by Ackermann et al. (2015) used 50 months of Fermi-LAT survey data, covering **100 MeV to 820 GeV** — nearly four decades in energy. The spectrum is well-described by a power law with exponential cutoff: spectral index **Γ = 2.32 ± 0.02** and break energy **E_break = 279 ± 52 GeV**. The total integrated intensity above 100 MeV is **I(>100 MeV) = (7.2 ± 0.6) × 10⁻⁶ cm⁻² s⁻¹ sr⁻¹**, with additional systematic uncertainty of +15%/−30% from Galactic diffuse foreground modeling. The high-energy cutoff has been attributed to EBL absorption of blazar emission. This measurement, based on the 2FGL source catalog, remains the standard IGRB reference; no updated IGRB spectrum using the 4FGL catalog has been published as of early 2026.

### What fraction is explained by known sources?

The landmark decomposition by Ajello et al. (2015) established that known source classes can collectively account for the entire Extragalactic Gamma-ray Background (EGB = IGRB + resolved sources): **blazars contribute ~50% of the EGB** above 100 MeV, with star-forming galaxies at ~10–30% and misaligned AGN at ~10–50% (the latter carrying order-of-magnitude uncertainties). The picture has been refined but not overturned since 2020. Roth et al. (2021, Nature) made the provocative claim that star-forming galaxies alone could explain the entire IGRB using a physical cosmic-ray transport model, but this was challenged by Shimono, Totani & Sudoh (2024), who found substantially lower SFG contributions using an independent model calibrated against six nearby gamma-ray galaxies. The consensus remains that **blazars dominate the UGRB anisotropy** while SFGs and mAGN contribute the bulk of the intensity. Korsmeier, Pinetti, Negro, Regis & Fornengo (2022) confirmed, using the UGRB angular power spectrum jointly with 4FGL catalog data, that two blazar populations (FSRQs at low energies, BL Lacs at higher energies) are required to explain the anisotropy signal.

Given the factor-of-five uncertainty in SFG contributions and order-of-magnitude uncertainty in mAGN contributions, **meaningful parameter space remains for a subdominant DM component**, particularly below ~100 GeV. Dark matter annihilation produces gamma-rays with a distinct spectral shape (hard cutoff at the DM mass, channel-dependent spectral features) and a distinct spatial distribution (tracing the DM halo density squared, peaking at low redshift). These signatures differ qualitatively from the power-law spectra and redshift evolution of astrophysical sources, enabling separation through cross-correlation with large-scale structure tracers like HI intensity maps — the central strategy of Pinetti et al. (2020).

---

## Part 2 — Four astrophysical populations and their evolving luminosity functions

### BL Lac objects

BL Lacs are radio-loud AGN with relativistic jets pointed within ~10° of our line of sight, characterized by weak emission lines (equivalent width < 5 Å), strong variability, and high polarization. Their gamma-ray emission arises from **synchrotron self-Compton (SSC)** scattering: relativistic jet electrons upscatter their own synchrotron photons to GeV–TeV energies. The average Fermi-LAT photon index is **Γ ≈ 2.2**, harder than FSRQs; Pinetti et al. adopt **α = 2.11** in their Table 3 (a representative value for the brighter, harder-spectrum BL Lacs that dominate the unresolved contribution). BL Lacs are subdivided by synchrotron peak frequency into low- (LSP), intermediate- (ISP), and high-synchrotron-peaked (HSP) classes.

The gamma-ray luminosity function from Ajello et al. (2014) is based on 211 BL Lacs from the 1LAC catalog. The best-fit model is a **Luminosity-Dependent Density Evolution (LDDE)** parameterization, with the local luminosity function described by a double power law multiplied by a Gaussian photon-index distribution. Redshift evolution is positive for most classes (space density peaking at z ~ 1.2), **except HSP BL Lacs, which show negative evolution** — their number density increases toward z = 0 for L_γ ≤ 10⁴⁶ erg/s. This negative HSP evolution means BL Lacs have strong overlap with low-redshift HI surveys (z < 0.5), making them an important astrophysical foreground for DM searches in HI × γ cross-correlations. Qu, Zeng & Yan (2019) updated the BL Lac GLF using an enlarged Fermi-LAT sample and confirmed the LDDE preference, finding BL Lacs contribute ~20% of the EGB above 100 MeV but dominate above ~50 GeV.

### Flat-Spectrum Radio Quasars

FSRQs are the luminous, high-redshift blazar subclass with strong broad emission lines. Their gamma-ray emission is powered by **external Compton (EC)** scattering of photons from the broad-line region, dusty torus, or accretion disk, producing softer spectra (**Γ ≈ 2.4–2.5**; Pinetti et al. adopt **α = 2.44** in Table 3) and higher Compton dominance than BL Lacs. The Ajello et al. (2012) GLF, based on 186 FSRQs from the first-year catalog, is strongly LDDE with **luminosity-dependent redshift peaks** — the most luminous FSRQs peak at z ~ 2–3, lower-luminosity objects at lower z, consistent with cosmic downsizing. Singal et al. (2025) updated the FSRQ GLF using the full 4LAC sample and found broadly consistent LDDE parameters with improved constraints.

### Misaligned AGN

Misaligned AGN (mAGN) are radio-loud AGN with jets at viewing angles >14°, including FR I and FR II radio galaxies and steep-spectrum radio quasars. They share jet physics with blazars but are de-beamed, making them intrinsically fainter in gamma-rays yet **~500–1000× more numerous** (geometric factor ~2Γ²). Only ~55 mAGN appear in 4FGL-DR4. Because the detected sample is small, the GLF is derived indirectly from the well-measured **radio core luminosity function** via an L_γ–L_radio correlation (Di Mauro et al. 2014). The contribution to the IGRB ranges from 10% to nearly 100%, representing the **largest uncertainty among all source classes**. Fukazawa et al. (2022) updated the radio galaxy GLF using 4FGL-DR2 and tested eight models, but the contribution remains poorly constrained. Despite potentially dominating IGRB intensity, mAGN produce **negligible anisotropy** because they are numerous and faint — their Poisson (shot-noise) term is small.

### Star-forming galaxies

SFGs produce gamma-rays primarily through **hadronic processes**: cosmic rays accelerated in supernova remnants interact with interstellar gas via pp collisions, producing π⁰ mesons that decay to gamma-ray pairs. Only ~12 SFGs are individually detected by Fermi-LAT, so their contribution is estimated indirectly using the **infrared luminosity function** from Gruppioni et al. (2013, Herschel PEP/HerMES) combined with an empirical L_γ–L_IR scaling (L_γ ∝ L_IR^{1.17±0.07}). The IR LF shows strong luminosity evolution proportional to (1+z)^{3.55} up to z ~ 2, tracking the cosmic star formation rate history. Recent ALMA observations (A3COSMOS, 2024) confirm the Gruppioni IR LF to z ~ 3 but find higher normalization at z > 3.5, suggesting a modest increase in the high-redshift SFG gamma-ray contribution.

### Mass-luminosity relations and halo connections

Camera et al. (2015) developed the **tomographic-spectral approach** connecting gamma-ray source populations to dark matter halos via halo occupation distributions (HODs) or effective bias prescriptions. Blazars typically reside in massive halos (M ~ 10¹³–10¹⁴ M☉, effective bias b ~ 1.5–3), while SFGs occupy a broader mass range (M ~ 10¹¹–10¹³ M☉, b ~ 1.0–1.5). These mass-luminosity relations determine the 2-halo clustering term of the cross-power spectrum, which is typically where the signal-to-noise ratio is highest.

### Updates from the 4FGL catalog era

The 4FGL catalog has evolved from 5,064 sources (8 years, DR1) to **7,194 sources** (14 years, DR4, Ballet et al. 2023), roughly doubling the number of detected sources compared to the 2FGL-era samples underlying the original GLFs. An interim 16-year source list (FL16Y, 7,220 sources) was presented at ICRC 2025, with the full 5FGL catalog awaiting a new Galactic diffuse emission model. Despite these advances, the **Ajello et al. (2012, 2014) LDDE parameterizations remain broadly valid** when extrapolated below the detection threshold. The main improvements are tighter parameter constraints and confirmation of LDDE as the preferred evolutionary model.

Regarding the flux sensitivity threshold, Pinetti et al. adopt **F_sens = 10⁻¹⁰ cm⁻² s⁻¹** (>100 MeV), characteristic of the 2FGL/3FGL era. With 14 years of data, the effective sensitivity has improved to approximately **5–8 × 10⁻¹¹ cm⁻² s⁻¹** for persistent high-latitude sources. For consistency with the Ackermann et al. (2015) IGRB measurement (which used 2FGL masking), the original threshold remains appropriate. However, **future analyses using an updated IGRB measurement based on 4FGL catalogs will need to adopt a lower threshold** of ~2–5 × 10⁻¹¹ cm⁻² s⁻¹.

---

## Part 3 — Dark matter annihilation signal from WIMPs to photons

### Annihilation channels and spectral signatures

The bb̄ (bottom quark-antiquark) channel serves as the standard benchmark for WIMP indirect detection because it is kinematically accessible for m_DM > ~5 GeV, dominates in many theoretically motivated models (Higgs-mediated neutralino annihilation), and produces a conservative, soft, broadly-peaked photon spectrum peaking at E_γ ~ m_DM/20 through the hadronization chain bb̄ → jets → π⁰ → γγ. The spectrum cuts off sharply at E_γ = m_DM. The τ⁺τ⁻ channel yields a harder spectrum with fewer total photons but at higher energies (prominent peak at higher x = E_γ/m_DM), serving as a "leptophilic" benchmark. The W⁺W⁻ channel (available only for m_DM > 80.4 GeV) produces intermediate spectral hardness. At fixed DM mass, the photon multiplicity ordering is bb̄ > W⁺W⁻ > τ⁺τ⁻, while spectral hardness is reversed.

### PPPC4DMID photon yield tables

The **Poor Particle Physicist Cookbook for Dark Matter Indirect Detection** (Cirelli et al. 2011) provides tabulated energy spectra dN/dlog₁₀x of stable particles (photons, positrons, antiprotons, neutrinos) per DM annihilation as a function of x = E/m_DM, for 28 primary channels and DM masses from 5 GeV to 100 TeV. Spectra were generated using PYTHIA and HERWIG Monte Carlo generators, and critically include **electroweak corrections** (Ciafaloni et al. 2011) that modify spectra significantly when m_DM ≫ m_W through EW bremsstrahlung.

The tables are distributed as Mathematica interpolating functions (dlNdlxEW.m) and plain-text numerical files at www.marcocirelli.net/PPPC4DMID.html, with a C++ reader on GitHub (carmeloevoli/PPPC4DMID-C). Python users typically read the .dat tables and perform bilinear interpolation in log₁₀(m_DM) and log₁₀(x). The package has seen six major releases: Release 2.0 (2012) added the Higgs channel for m_h = 125 GeV; Release 5.0 (2015) added secondary radiation (bremsstrahlung, synchrotron, improved IC). Amoroso et al. (2019) assessed QCD uncertainties by comparing PYTHIA vs. HERWIG predictions, providing alternative tables on Zenodo. The website was last updated in October 2022. For m_DM < 5 GeV, supplementary analytical expressions from other works are required.

### The DM window function, factor by factor

The DM gamma-ray window function (Equation 4.1 of Pinetti et al.) encodes all particle physics and cosmological factors:

**W_DM(E_γ, z) = [⟨σv⟩ / (8π)] × [(Ω_DM ρ_c)² / m_χ²] × (1+z)³ × [dN_γ/dE′|_{E′=E_γ(1+z)}] × e^{−τ(E_γ,z)} × [c / H(z)]**

Each factor carries specific physical meaning. The **⟨σv⟩** term is the thermally averaged annihilation cross-section times relative velocity, setting the overall signal amplitude. The **(Ω_DM ρ_c)² / m_χ²** factor encodes that annihilation rate density scales as (n_DM)² × ⟨σv⟩ = (ρ_DM/m_χ)² × ⟨σv⟩, reflecting the two-body nature of the process. The factor of 1/2 in the denominator (8π = 2 × 4π) avoids double-counting particle pairs for self-conjugate Majorana fermions. The **(1+z)³** factor accounts for the cosmological evolution of the physical DM density: ρ_DM(z) = Ω_DM ρ_c (1+z)³, so ρ² ∝ (1+z)⁶, but three powers are absorbed into the comoving volume element, leaving (1+z)³. The **dN_γ/dE′** term is the differential photon yield from PPPC4DMID, evaluated at the emitted energy E′ = E_γ(1+z) to account for cosmological redshifting. The **e^{−τ}** factor is the EBL absorption opacity. Finally, **c/H(z)** is the cosmological line-of-sight element dχ/dz.

The total mean DM-induced intensity is I_DM(E_γ) = ∫ dz W_DM(E_γ, z) × Δ²(z), where Δ²(z) is the clumping/intensity multiplier from DM clustering in halos and subhalos.

### EBL absorption and model comparison

Gamma-rays undergo pair production on EBL photons (γ_HE + γ_EBL → e⁺e⁻), with peak cross-section near the kinematic threshold 2 E_γ ε_EBL (1 − cos θ) ≈ (2 m_e c²)², which for head-on collisions gives E_γ · ε_EBL ≈ (m_e c²)² ≈ 0.26 MeV². The optical depth τ exceeds unity at **E_γ > ~30 GeV for z > 0.5** and at **E_γ > ~100 GeV for z > 0.1**, while it is negligible below ~10 GeV at any relevant redshift. Pinetti et al. adopt the Razzaque, Dermer & Finke (2009) parameterization. The Domínguez et al. (2011) model, constructed from observed galaxy luminosity functions using ~6,000 AEGIS galaxies, provides public opacity tables at side.iaa.es/EBL/. Finke et al. (2022) updated the Finke, Razzaque & Dermer (2010) model with BPASS stellar spectra, metallicity/dust evolution tracking, and three self-consistent dust components fitted to gamma-ray opacity and galaxy survey data, available on Zenodo. The Python package **ebltable** provides unified access to all major EBL models.

For the HI × γ cross-correlation at z ~ 0–0.5 and E ~ 0.5–500 GeV, **all standard EBL models agree to within ~10–20%**, with differences appearing only in the highest energy bins (E > 50 GeV, z > 0.3). Updated EBL models would produce only modest changes to cross-correlation predictions, making this a low-priority update.

### The thermal relic cross-section

The canonical value **⟨σv⟩ ≈ 3 × 10⁻²⁶ cm³/s** emerges from requiring that the WIMP relic abundance matches the Planck measurement Ω_DM h² ≈ 0.12 through standard freeze-out at T_F ≈ m_DM/20. Steigman, Dasgupta & Beacom (2012) computed the precise mass dependence: for self-conjugate WIMPs above 10 GeV, the thermal value is **~2.2 × 10⁻²⁶ cm³/s** (weakly mass-dependent), rising to ~5.2 × 10⁻²⁶ at m_DM ~ 0.3 GeV. Current constraints exclude the thermal cross-section for m_DM ≲ 100 GeV (bb̄) from Fermi-LAT dwarf spheroidal galaxy observations, and for m_DM ≲ 10–30 GeV from Planck CMB energy injection limits. The Pinetti et al. projections show that **SKA × Fermi-LAT cross-correlation can probe thermal-relic WIMPs up to ~130 GeV**, offering complementary sensitivity to these established methods.

---

## Part 4 — Angular power spectra distinguish point sources from extended halos

### Astrophysical sources: shot noise plus clustering

The auto- and cross-angular power spectra of unresolved astrophysical sources decompose into a **1-halo (Poisson) term** and a **2-halo (clustering) term** (Equations 4.6–4.7 of Pinetti et al.). The 1-halo term is the shot noise from discrete unresolved sources: C_ℓ^{1h} = C_P = ∫ dz (dV/dzdΩ) ∫ dL Φ(L,z) [S(L,z)]², where Φ is the GLF and S is the flux from a source of luminosity L at redshift z. This term is **flat in multipole ℓ** because point sources contribute equally at all angular scales — a distinctive signature. The 2-halo term C_ℓ^{2h} traces large-scale clustering through the projected linear matter power spectrum P_lin, weighted by the source window function and effective bias: C_ℓ^{2h} = ∫ dz (c/H(z))/χ²(z) × [W_★(z)]² × [b_★(z)]² × P_lin(k = ℓ/χ, z). This term dominates at low ℓ (large angular scales, ℓ ≲ 100) and typically provides the highest signal-to-noise ratio in cross-correlations.

Source biases vary considerably: **blazars** reside in massive halos (b ≈ 1.5–3, increasing with z), **SFGs** in less massive systems (b ≈ 1.0–1.5), and **mAGN** similar to blazars (b ≈ 1.5–2.5). The HI bias is b_HI ≈ 0.8–1.5 at z ~ 0–0.5, increasing with redshift. The cross-correlation amplitude scales as b_HI × b_★, making blazars the dominant astrophysical cross-correlation signal despite their subdominant contribution to UGRB intensity.

### Dark matter: spatially extended emission

The DM annihilation power spectra (Equations 4.4–4.5) differ qualitatively from astrophysical sources. The 1-halo term involves the Fourier transform of ρ²_DM(r) — the squared NFW profile — rather than a delta function. This means the DM 1-halo term is **not flat in ℓ** but decreases at high multipoles, reflecting the extended spatial emission from individual halos. The halo concentration c(M,z) and the **substructure boost factor B(M,z)** critically affect predictions. The boost factor, parameterizing luminosity enhancement from sub-halos, spans from tens of percent at dwarf masses to ~10 at cluster masses (Hiroshima et al. 2018), but extrapolation across >20 mass decades makes it highly uncertain — spanning orders of magnitude. The different ℓ-dependence of DM versus astrophysical signals provides a key handle for separation in the cross-correlation analysis.

### Validation against Fermi-LAT auto-correlation measurements

The Fermi-LAT auto-correlation angular power spectrum from Ackermann et al. (2018), using 8 years of Pass 8 data in 13 energy bins (0.5–500 GeV), detected anisotropy above photon noise at **≥99.99% CL for ℓ ≥ 155**. The measurement provided ~3.7σ evidence that **two source classes are needed**: a soft component (Γ₁ = 2.55 ± 0.23, consistent with FSRQs) and a hard component (Γ₂ = 1.86 ± 0.15, consistent with BL Lacs). The Poisson term C_P was confirmed to be constant for ℓ ≥ 155. **No updated Fermi-LAT APS auto-correlation measurement has superseded this result** as of early 2026, though cross-correlations with external catalogs (DES weak lensing at 5.3σ by Ammazzalorso et al. 2025; DESI forecasts by Zhou, Bernal, Pinetti et al. 2024) provide complementary anisotropy constraints. Pinetti et al. (2025) also published CTA cross-correlation forecasts.

---

## Part 5 — Fermi-LAT after seventeen years of surveying the gamma-ray sky

### Instrument design and performance

The Fermi Large Area Telescope is a pair-conversion gamma-ray telescope consisting of a 4×4 array of identical towers, each containing a silicon strip tracker interleaved with tungsten converter foils (thin "front" and thick "back" sections), a CsI(Tl) crystal calorimeter, and a segmented plastic scintillator anti-coincidence detector. The instrument covers **20 MeV to >300 GeV** with a peak effective area of **>8,000 cm²** on-axis at ~1 GeV, a field of view of **~2.4 sr** (~20% of sky), and angular resolution improving from ~5° at 100 MeV to ~0.04° at 100 GeV (68% containment). In sky-scanning survey mode, Fermi-LAT maps the entire gamma-ray sky every ~3 hours (two orbits at ~565 km altitude, 25.6° inclination).

### Energy binning and PSF considerations

Anisotropy analyses employ **~12 logarithmic energy bins from 0.5 GeV to ~1 TeV**. Logarithmic binning is necessitated by three factors: the PSF width varies by over two orders of magnitude across this range, photon statistics fall steeply (~E^{−2.4}), and the LAT energy resolution of ~10% (0.1 in log₁₀E) makes finer binning unproductive. Equal logarithmic widths ensure comparable dynamic range per bin. The PSF is parameterized as a double King function with an energy-dependent scale factor S(E) = √(c₀² × (E/100 MeV)^{−2β} + c₁²), where the c₀ term represents multiple scattering dominance at low energies and c₁ is the high-energy tracker resolution floor. Representative 68% containment angles for P8R3 SOURCE class are: **~5° at 100 MeV, ~0.8° at 1 GeV, ~0.2° at 10 GeV, ~0.04° at 100 GeV**.

The beam window function W_beam(E,ℓ) suppresses the observed angular power spectrum at high multipoles through the Legendre transform of the PSF: W_beam(E,ℓ) = 2π ∫₀^π PSF(E,θ) P_ℓ(cos θ) sin θ dθ. Pass 8 partitions events into four PSF quartiles (PSF0 = worst to PSF3 = best); anisotropy analyses typically select **PSF2+PSF3 event types** for improved angular resolution at the cost of ~50% acceptance.

### Noise, masks, and sky coverage

For a photon-count map, the Poisson noise angular power spectrum is C_N = 4π f_sky / N_γ (in units of sr), where N_γ is the total number of detected photons in the energy bin within the unmasked region. When working with intensity maps I = counts / (A_eff T_obs ΔE Ω_pix), the noise power spectrum inherits the conversion factor and takes the form N^γ = C_N × (Ī/c̄)², where Ī and c̄ are the mean intensity and mean counts per pixel respectively. The noise values listed in Pinetti et al. Table 2 are in intensity-squared units (cm⁻⁴ s⁻² sr⁻¹), reflecting this conversion. This noise is white (flat in ℓ) and dominates at high multipoles where the true anisotropy signal is suppressed by the PSF beam function. In the cross-correlation variance (Equation 2.7 of Pinetti et al.), the noise term N^γ/(B_ℓ^γ)² grows exponentially at high multipoles due to the beam suppression — this is what ultimately limits the highest usable multipole for the cross-correlation. This creates a fundamental trade-off: low energies have good statistics but broad PSF; high energies have narrow PSF but overwhelming photon noise. The optimal energy range for the cross-correlation is typically ~1–50 GeV.

Standard sky masks combine Galactic plane exclusion (|b| > 30°) with energy-dependent point-source masking around 4FGL catalog sources. The resulting sky fraction **f_sky ranges from ~0.3 to ~0.5** depending on energy and masking strategy.

### Data infrastructure and current status

The **Fermitools v2.5.0** (released December 2025) provides the standard analysis framework, installed via conda. Data are accessed through the LAT Data Server at fermi.gsfc.nasa.gov. The current recommended IRFs are **P8R3_SOURCE_V3**, with effective area and PSF systematic uncertainties <5% between 100 MeV and 10 GeV. Diffuse emission models include gll_iem_v07.fits (Galactic) and iso_P8R3_SOURCE_V3_v1.txt (isotropic). Standard event selections for anisotropy analyses are SOURCE class (evclass=128), PSF2+PSF3 types, zenith angle < 90°, and DATA_QUAL>0 && LAT_CONFIG==1.

**Pass 8 R3 remains the current data release** — there is no Pass 9. P8R3 (2018) fixed an anisotropic residual cosmic-ray background in P8R2 related to electrons leaking through ACD ribbons and non-interacting heavy ions, with <1% acceptance loss. The P8R3_V3 IRFs incorporate in-flight PSF calibration using Vela and Earth limb data.

As of April 2026, Fermi-LAT has accumulated **~17.7 years** of science data, compared to ~8 years in many published analyses. This yields a factor of **~2.2× more photons**, reducing photon noise by the same factor and improving signal-to-noise by ~√2.2 ≈ 1.49. The catalog has grown from 5,064 sources (4FGL-DR1) to **7,194 sources** (4FGL-DR4, 14 years), with an interim FL16Y list of 7,220 sources presented at ICRC 2025. The full **5FGL catalog** awaits a new Galactic diffuse emission model under development.

---

## Part 6 — No confirmed successor matches the "Fermissimo" benchmark

Pinetti et al. define "Fermissimo" as a hypothetical next-generation Fermi-like telescope with **2× exposure, PSF 5× better (α_σ = 0.2), and f_sky = 0.8**. No approved mission currently matches these specifications in the core GeV band, creating a significant gap in the experimental landscape for HI × γ cross-correlation science.

**COSI** (NASA SMEX, launching **August 2027**) is the only confirmed upcoming gamma-ray space mission. It covers 0.2–5 MeV with germanium Compton detectors — entirely in the soft MeV band, far below the Fermi-LAT energy range. It cannot serve as a Fermi successor for GeV-band cross-correlations but enables novel MeV-band studies.

**CTAO** (Cherenkov Telescope Array Observatory) is the most advanced project, established as an ERIC in January 2025 with construction underway at both sites (La Palma and Atacama). It will achieve ~10× sensitivity improvement over current IACTs across 20 GeV–300 TeV. However, CTA is a **ground-based pointed instrument** with limited instantaneous field of view (~4–8°), making it unsuitable for the all-sky survey work central to Pinetti et al. Early CTA science is expected by ~2026–2027, with full array operations overlapping SKA Phase 1 (~2028–2029). Pinetti et al. (2025) have already published CTA cross-correlation forecasts.

**HERD** (High Energy cosmic-Radiation Detection, China) is an approved payload for China's Space Station launching ~2027 with 10-year lifetime. Its geometrical factor (>3 m²·sr) exceeds Fermi-LAT, but its angular resolution for gamma-rays is not optimized — it will not match the Fermissimo PSF requirement. HERD will be contemporaneous with SKA Phase 1 and could provide supplementary all-sky gamma-ray data.

**VLAST** (Very Large Area gamma-ray Space Telescope, China) is the concept that **most closely matches or exceeds Fermissimo specifications**: acceptance ~10 m²·sr (~4× Fermi-LAT), angular resolution better than 0.2° at 10 GeV, all-sky survey mode, and ~10× Fermi sensitivity. However, VLAST remains in early R&D with no government approval or firm launch date. If approved and launched in the mid-2030s, it would overlap with SKA Phase 2 and would be ideal for the Pinetti et al. science case.

**GAMMA-400** (Russia, ~2030) offers superb angular resolution (~0.01° at 100 GeV) but operates in **pointed mode with narrow FoV**, making it incompatible with all-sky cross-correlation requirements. **AMEGO-X** and **e-ASTROGAM** were not selected for their respective NASA MIDEX and ESA M5 mission slots and have no current path to flight. **APT** (Advanced Particle-astrophysics Telescope) is an ambitious probe-class concept exceeding Fermissimo specifications, but it remains at the early concept stage with a balloon demonstrator (ADAPT) planned for 2026–2027.

The most realistic near-term path to Fermissimo-class science is **continued Fermi-LAT operations** into the early 2030s (~22+ years of data), achieving >2× exposure improvement, combined with improved analysis techniques — though this cannot deliver the 5× PSF improvement.

---

## Part 7 — Systematic effects demand careful treatment on the gamma-ray side

### Galactic diffuse emission residuals are the dominant systematic

The Fermi-LAT Galactic diffuse model (gll_iem_v07) is **constructed from HI 21-cm and CO spectral line surveys** combined with GALPROP cosmic-ray propagation modeling. Galactic gamma-ray emission arises from π⁰ production (CR protons on HI/H₂ gas), bremsstrahlung (CR electrons on gas), and inverse Compton scattering (CR electrons on interstellar radiation fields). Because the model is fit to HI gas templates, **any subtraction residuals correlate with HI maps by construction**. The systematic uncertainty on the IGRB from Galactic foreground modeling is ~15–30%, quantified through three alternative IEMs (Models A, B, C from Ackermann et al. 2015) that yield UGRB intensities varying by ~25%. Loop I, the Fermi Bubbles, and the Cygnus cocoon create additional structured residuals requiring dedicated patch templates.

### Point-source leakage through the broad low-energy PSF

At E < 1 GeV, even masked point sources leak photons into the analysis region through the multi-degree PSF wings. Energy-dependent mask radii (scaling with both source flux and PSF size) partially mitigate this, but residual leakage introduces spurious small-scale correlations. The P8R3 PSF systematic uncertainty is <5% between 100 MeV and 10 GeV, rising to ~25% at 1 TeV. Cross-correlation studies limit ℓ_max to the multipole corresponding to the PSF containment angle in each energy bin and may restrict analysis to E > 1 GeV where the PSF is < 1°.

### Cosmic ray contamination after P8R3

P8R3 largely resolved the CR contamination issue: the ecliptic-plane anisotropy present in P8R2 (factor ~2 enhancement at 1–3 GeV) was traced to cosmic-ray electrons leaking through ACD ribbons and non-interacting heavy ions. Simple cuts removed these events with <1% acceptance loss, bringing SOURCE class residual background close to ULTRACLEANVETO levels below ~50 GeV. The isotropic spectral template explicitly absorbs remaining residual CR events. Post-P8R3, CR contamination is approximately isotropic and should not produce strong spurious cross-correlations with extragalactic tracers.

### The z ≈ 0 Galactic foreground-HI correlation

This is the **most insidious systematic** specific to HI × γ cross-correlation. Milky Way HI emits at 1420.405 MHz (z = 0) and simultaneously serves as the target material for CR interactions producing Galactic diffuse gamma-rays. This creates a strong intrinsic positive correlation between the 21-cm map and the gamma-ray map at z ≈ 0 that has nothing to do with extragalactic physics. Galactic HI has a broad velocity distribution spanning ±200 km/s (z ≈ ±0.001), with high-velocity clouds extending to z ~ 0.003 and Magellanic Stream gas to z ~ 0.003. **Conservatively, z_min > 0.03 is needed at high Galactic latitudes; z_min > 0.05–0.1 is safer.** In practice, Pinetti et al. focus on radio telescopes (SKA, MeerKAT) operating at z > 0.3, safely avoiding this contamination.

### A toolkit of mitigation strategies

Effective mitigation combines several approaches. Template fitting marginalizes over Galactic emission model normalizations, with cross-checks using alternative IEMs (Models A, B, C). Aggressive Galactic plane masking at |b| > 30° (or |b| > 40–50° as systematic cross-checks) reduces structured residuals, supplemented by masking where the Galactic template exceeds 3–4× the isotropic level. Energy-dependent point-source masking from 4FGL-DR4 and 3FHL catalogs suppresses PSF leakage. Multipole range selection (ℓ_min ~ 30–100 to exclude large-scale Galactic residuals; ℓ_max set by PSF) focuses on the signal-dominated regime. Jackknife and null tests — varying mask width, randomizing map alignments, time-based half-mission splits — verify robustness. The tomographic approach, correlating in narrow redshift bins, separates Galactic from extragalactic contributions. Recent implementations (Ammazzalorso et al. 2025; Tröster et al. 2025) demonstrate that these combined strategies enable high-significance (5.3σ) detection of UGRB × large-scale structure cross-correlations.

Additional systematics include exposure non-uniformity (~1–2% azimuthal variations), energy dispersion effects (5–15% corrections below 300 MeV, ~5% at higher energies; Fermitools energy dispersion correction recommended), and isotropic template uncertainty inherited from Galactic model errors. These are generally subdominant to the Galactic foreground-HI correlation for cross-correlation studies.

---

## Conclusions and what needs updating

The gamma-ray framework of Pinetti et al. (2020) remains fundamentally sound. The Fermi-LAT dataset has grown from ~8 to ~17.7 years, reducing photon noise by a factor of ~2.2 and expanding the source catalog to >7,000 objects. **Three aspects warrant priority updates.** First, the flux sensitivity threshold should be lowered from 10⁻¹⁰ to ~5 × 10⁻¹¹ cm⁻² s⁻¹ when paired with a new IGRB measurement using 4FGL-era catalogs — this would change the resolved/unresolved partition and modify both the UGRB intensity and the Poisson noise term. Second, the substructure boost factor remains the single largest theoretical uncertainty in DM predictions, spanning orders of magnitude; recent N-body simulations and semi-analytical models should be incorporated. Third, the absence of a confirmed Fermissimo-class mission means that the optimistic next-generation projections depend on either continued Fermi-LAT operations into the 2030s or the approval of VLAST.

Key publicly available tools and data products include: Fermitools v2.5.0 (conda-forge), Fermi-LAT data server (fermi.gsfc.nasa.gov), PPPC4DMID tables (www.marcocirelli.net/PPPC4DMID.html), the ebltable Python package for EBL opacity, 4FGL-DR4 catalog, P8R3_SOURCE_V3 IRFs, and Galactic/isotropic diffuse templates from the FSSC. The Fermi-LAT APS measurement from Ackermann et al. (2018) remains the definitive auto-correlation reference, while cross-correlations with DES, DESI, and 2MASS provide increasingly powerful complementary constraints on the composition of the unresolved gamma-ray sky.
