# Cirelli et al. (2011) — PPPC4DMID Photon Yield Tables

**Authors:** M. Cirelli, G. Corcella, A. Hektor, G. Hutsi, M. Kadastik, P. Panci, M. Raidal, F. Sala, A. Strumia
**Journal:** JCAP 1103, 051 (Erratum: JCAP 1210, E01)
**arXiv:** [1012.4515](https://arxiv.org/abs/1012.4515)

## Abstract

"Poor Particle Physicist Cookbook for Dark Matter Indirect Detection." Provides energy spectra of photons, positrons, antiprotons, and neutrinos from DM annihilation across 28 channels, computed via PYTHIA and HERWIG Monte Carlo.

## Methodology

- High-statistics Monte Carlo with PYTHIA and HERWIG (cross-validated)
- 28 primary annihilation channels
- Mass range: 5 GeV to 100 TeV
- Includes electroweak corrections (Ciafaloni et al. 2011) for m_DM >> m_W
- Release history: v2.0 (2012, Higgs channel), v5.0 (2015, secondary radiation)

## Key Results

Tables of dN/d(log10 x) where x = E/m_DM for each channel. Key channels for indirect detection: bb-bar (soft, broad), tau+tau- (hard, fewer photons), WW (intermediate).

## Data Format

- File: `AtProduction_gammas.dat`
- Columns: mDM [GeV], Log10(x), then dN/dLog10(x) for 28 channels
- 62 unique masses × 179 x-points × 28 channels

## Equations Used

**Conversion from table format:**
$$\frac{dN}{dx} = \frac{dN}{d\log_{10} x} \cdot \frac{1}{x \ln 10}$$

$$\frac{dN}{dE} = \frac{dN}{dx} \cdot \frac{1}{m_\chi}$$

**Channel mapping:** bb → 'b', tautau → '\[Tau\]', WW → 'W'

## Implementation

**Module:** `pppc4dmid.py` — `dNdx()`, `dNdE()`, `total_multiplicity()`. Table loaded from `data/pppc4dmid/AtProduction_gammas.dat`. 2D `RectBivariateSpline` interpolation in (log10 m_DM, log10 x). Analytic fallback for when tables unavailable.
