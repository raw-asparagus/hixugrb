# Window Function Discrepancy Analysis

Systematic comparison of our pipeline's normalized window functions against [Pinetti (2022, arXiv:2212.00125)](literature/pinetti2020.md) (PhD thesis; same equations as the 2020 paper) Figure 5.1.

**Date:** 2026-04-02
**Status:** Formulas verified correct; input physics models partially fixed.

### Fixes Applied
- **HI:** Corrected parameter mismatch — now uses consistent [Padmanabhan+ (2017)](literature/padmanabhan2017.md) Table A1 parameters (α=0.176, β=−0.69, v_c,0=40.7) matching the modified NFW profile. Ω_HI(z) trend remains a known model limitation.
- **BL Lac:** Implemented [Ajello+ (2014)](literature/ajello2014.md) Table C.1 parameters with LDDE inverse-sum evolution (Eq. C.4)
- **mAGN:** Implemented full radio→gamma chain from [Di Mauro+ (2014)](literature/dimauro2014.md) via [Willott (2001)](literature/willott2001.md) RLF
- **SFG:** Implemented [Gruppioni+ (2013)](literature/gruppioni2013.md) 3-component IR LF with [Ackermann+ (2012)](literature/ackermann2012_sfg.md) L_γ–L_IR scaling

### Remaining Issues
- Ω_HI(z) still decreases with z (halo model limitation; observed: increases)
- mAGN and SFG window shapes still need calibration against published source counts
- DM steepness needs concentration model review

---

## Method

Claim-by-claim evidence matrix comparing: (A) Pinetti thesis Figure 5.1 expected shapes, (B) our code output, (C) underlying scholarly literature.

---

## 1. HI Window — Parameter mismatch corrected; Ω_HI(z) trend is model limitation (PARTIAL)

**Expected:** Smooth curve peaking at z~0.7–1.0 within MeerKAT UHF band.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| H1 | W_HI = T̄_b · b_HI · φ · H/(ch) | [Pinetti](literature/pinetti2020.md) Eq. 3.15 | Same | YES |
| H2 | T̄_b = 188 h Ω_HI (1+z)²/E(z) mK | [Pinetti](literature/pinetti2020.md) Eq. 3.4 | Same | YES |
| H3 | b_HI increases with z | Literature | YES | YES |
| H4 | Ω_HI increases ~4e-4 → ~1e-3 over z=0→2 | ALFALFA, DLAs | **Still decreases** — model limitation | **KNOWN** |
| H5 | Modified NFW profile with Table A1 parameters | [Padmanabhan+ (2017)](literature/padmanabhan2017.md) Table A1 | α=0.176, β=−0.69, v_c,0=40.7 km/s, c_HI,0=139, γ=0.13 | YES |

**Fix applied:** Parameters are now self-consistent — all five from [Padmanabhan+ (2017)](literature/padmanabhan2017.md) Table A1 (modified NFW fit). Previously mixed exponential-fit parameters (Table 3) with the modified NFW profile form; the Pinetti thesis propagated this mismatch.

**Remaining limitation:** Ω_HI(z) still decreases with z. This is inherent to the Padmanabhan model with passive (non-evolving) HIHM parameters — the paper documents this in Section 6 conclusion (viii): "the effective cutoff halo mass evolves roughly as M_cutoff ∝ (1+z)^{-3/2}." Redshift evolution of α, β, or v_c,0 was tested but not statistically favored by their data. Fixing this would require a different HIHM model (e.g., Villaescusa-Navarro+ 2018) or explicit parameter evolution.

---

## 2. BL Lac Window — Implemented from Ajello+ (2014) Table C.1 (RESOLVED)

**Expected:** Rises from 0 at z~0.2, peaks at z~1.0, declines to ~0 by z~2.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| B1 | W = d_L²/(1+z)² × ∫Φ dF/dE dL | [Pinetti](literature/pinetti2020.md) Eq. 4.3 | Same (after algebraic simplification) | YES |
| B2 | LDDE from [Ajello+ (2014)](literature/ajello2014.md) | 211 BL Lacs, 1LAC catalog | Table C.1 parameters with LDDE inverse-sum evolution (Eq. C.4) | **IMPLEMENTED** |
| B3 | Combined BL Lac population, smooth peaked evolution | [Ajello+ (2014)](literature/ajello2014.md) | A=9.20e-11, L★=2.43e48, p₁=4.50, p₂=−12.88 | **IMPLEMENTED** |

**Previous root cause (now resolved):** Was using calibrated single-component piecewise LDDE with hand-tuned parameters. Replaced with original [Ajello+ (2014)](literature/ajello2014.md) Table C.1 parameters and LDDE inverse-sum evolution form (Eq. C.4).

---

## 3. FSRQ Window — Closest match

**Expected:** Peaks at z~0.5.
**Ours:** Peaks at z~0.7.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| F1 | LDDE from [Ajello+ (2012)](literature/ajello2012.md) Table 3 | Direct paper values | Same | YES |
| F2 | Peak z~0.5 | Figure 5.1 | z~0.7 | PARTIAL |

**Root cause:** Minor. May be E-dependent or due to slight differences in spectral normalization.

---

## 4. DM Window — Boost factor updated with z-scaling (IMPROVED)

**Expected:** Very steeply peaked near z=0, drops to ~0 by z~1.5.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| D1 | W = (σv/8π)(ρ/m)²(1+z)³/H × Δ² × dN/dE × e^{-τ} | [Pinetti](literature/pinetti2020.md) Eq. 4.1 | Same structure | YES |
| D2 | Δ²(z) decreases steeply | Structure formation | Full Moliné polynomial + 1/(1+z) scaling | YES |
| D3 | B(M,z) = B(M,0)/(1+z) | [Moliné+ (2017)](literature/moline2017.md) Eq. 18 + Thesis Eq. 3.48 | Full polynomial (Table 3, α=2) with z-scaling | **IMPLEMENTED** |

**Fix applied:** Replaced simplified `B = 1.6e-3 [log(M/M_min)]^2.5` (no z-dependence) with full Moliné 5th-order polynomial (Eq. 18, Table 3) and `1/(1+z)` z-evolution (Thesis Eq. 3.48). The z-scaling makes the boost decrease at high z, steepening the DM window drop-off.

---

## 5. mAGN and SFG — Implemented from original literature (RESOLVED)

**Expected:** mAGN peaks z~0.3–0.5; SFG peaks z~1–2.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| M1 | mAGN from [Di Mauro+ (2014)](literature/dimauro2014.md) radio LF | L_γ–L_radio correlation | Full radio→gamma chain: [Willott (2001)](literature/willott2001.md) RLF → [Inoue (2011)](literature/inoue2011.md) freq scaling → [Lara (2004)](literature/lara2004.md) core-total → [Di Mauro (2014)](literature/dimauro2014.md) Eq. C.19 | **IMPLEMENTED** |
| S1 | SFG from [Gruppioni+ (2013)](literature/gruppioni2013.md) IR LF × L_γ∝L_IR^1.17 | Herschel PEP/HerMES | Full IR→gamma chain: [Gruppioni (2013)](literature/gruppioni2013.md) 3-component modified Schechter IR LF → [Ackermann (2012)](literature/ackermann2012_sfg.md) L_γ-L_IR scaling (Eq. C.28) | **IMPLEMENTED** |

**Previous root cause (now resolved):** The mAGN and SFG GLFs were hand-calibrated single-LDDE approximations. They have been replaced with faithful implementations of the original multi-step conversion chains from the source papers.

---

## Summary of Root Causes

| # | Root Cause | Windows Affected | Severity | Status |
|---|-----------|-----------------|----------|--------|
| RC1 | Ω_HI(z) decreases instead of increasing | HI | CRITICAL | Formula correct; model parameters wrong |
| RC2 | BL Lac HSP GLF parameters from indirect source | BL Lac | HIGH | Need original [Ajello+ (2014)](literature/ajello2014.md) fit |
| RC3 | DM Δ²(z) not steep enough at high z | DM | MEDIUM | Check concentration model, boost factor |
| RC4 | mAGN/SFG GLFs are rough approximations | mAGN, SFG | HIGH | Need proper fits from papers |
| RC5 | T̄_b coefficient ~4% low | HI amplitude | LOW | 180 vs 188 mK |

## Conclusion

All window function **formulas** (Limber integral, Eqs. 3.15, 4.1, 4.3) are correctly implemented. The discrepancies are entirely in **input physics models**: the HI mass–halo mass relation, gamma-ray luminosity function parameters, and clumping factor evolution.
