# Window Function Discrepancy Analysis

Systematic comparison of our pipeline's normalized window functions against [Pinetti (2022, arXiv:2212.00125)](literature/pinetti2020.md) (PhD thesis; same equations as the 2020 paper) Figure 5.1.

**Date:** 2026-04-02
**Status:** Formulas verified correct; input physics models partially fixed.

### Fixes Applied
- **HI:** v_{c,0} restored to 36.3 km/s (Padmanabhan+ 2017 original); α=0.09, β=−0.58; T̄_b coefficient corrected to 188h mK
- **BL Lac:** Replaced [Di Mauro+ (2013)](literature/dimauro2014.md) HSP+LISP reparameterization with single-component [Ajello+ (2014)](literature/ajello2014.md) piecewise LDDE
- **mAGN:** L_c raised from 3×10⁴³ to 5×10⁴⁴; A and evolution adjusted
- **SFG:** L_c raised from 2×10³⁹ to 5×10⁴⁰; A adjusted

### Remaining Issues
- Ω_HI(z) still decreases with z (halo model limitation; observed: increases)
- mAGN and SFG window shapes still need calibration against published source counts
- DM steepness needs concentration model review

---

## Method

Claim-by-claim evidence matrix comparing: (A) Pinetti thesis Figure 5.1 expected shapes, (B) our code output, (C) underlying scholarly literature.

---

## 1. HI Window — Ω_HI(z) trend inverted (CRITICAL)

**Expected:** Smooth curve peaking at z~0.7–1.0 within MeerKAT UHF band.
**Ours:** Peaks at z~0.4 (band edge), monotonically declines.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| H1 | W_HI = T̄_b · b_HI · φ · H/(ch) | [Pinetti](literature/pinetti2020.md) Eq. 3.15 | Same | YES |
| H2 | T̄_b = 188 h Ω_HI (1+z)²/E(z) mK | [Pinetti](literature/pinetti2020.md) Eq. 3.4 | ~180 h mK (4% low) | YES |
| H3 | b_HI increases with z | Literature | 0.93→1.6 over z=0→2 | YES |
| H4 | **Ω_HI increases** ~4e-4 → ~1e-3 over z=0→2 | ALFALFA, DLAs; "Ω_HI ∝ (1+z)^0.6" | **DECREASES** 2e-4→1.2e-5 | **MISMATCH** |
| H5 | v_{c,0} range 36–102 km/s | [Padmanabhan+ (2017)](literature/padmanabhan2017.md) | 101.61 (upper extreme) | PARTIAL |

**Root cause:** The Padmanabhan model with v_{c,0}=101.61 km/s cuts off HI at M~5×10¹¹ M☉, leaving only massive halos. Combined with the SMT mass function (~63% normalization), this produces Ω_HI that decreases with z — opposite to observations. Since T̄_b ∝ Ω_HI, the HI window inherits this wrong trend.

---

## 2. BL Lac Window — GLF parameters concentrate emission at z~0 (HIGH)

**Expected:** Rises from 0 at z~0.2, peaks at z~1.0, declines to ~0 by z~2.
**Ours:** Peaks at z~0.1, declines from there.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| B1 | W = d_L²/(1+z)² × ∫Φ dF/dE dL | [Pinetti](literature/pinetti2020.md) Eq. 4.3 | Same (after algebraic simplification) | YES |
| B2 | LDDE from Ajello+ (2014) | 211 BL Lacs, 1LAC catalog | HSP+LISP from [Di Mauro+ (2013)](literature/dimauro2014.md) | PARTIAL |
| B3 | HSP negative evolution p₁=−1.64 | [Ajello+ (2014)](literature/ajello2014.md) | Same | YES |
| B4 | Window peaks at z~1 | Figure 5.1 | Peaks at z~0.1 | **MISMATCH** |

**Root cause:** The [Di Mauro+ (2013)](literature/dimauro2014.md) reparameterization of the [Ajello+ (2014)](literature/ajello2014.md) BL Lac GLF uses a "sum" evolution form with HSP p₁=−1.64 (negative), which makes HSP BL Lac density increase toward z=0. This overwhelms the LISP component, concentrating all BL Lac emission at very low z. The original [Ajello+ (2014)](literature/ajello2014.md) paper may use a different parameterization (e.g., PLE or LDDE with different form) that produces a peak at z~1.

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

## 4. DM Window — Not steep enough (MEDIUM)

**Expected:** Very steeply peaked near z=0, drops to ~0 by z~1.5.
**Ours:** Peaked near z=0 but extends to z~2+.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| D1 | W = (σv/8π)(ρ/m)²(1+z)³/H × Δ² × dN/dE × e^{-τ} | [Pinetti](literature/pinetti2020.md) Eq. 4.1 | Same structure | YES |
| D2 | Δ²(z) decreases steeply | Structure formation | Δ²(0)~4e5 | YES |
| D3 | Shape steeply peaked | Figure 5.1 | Extends too far | PARTIAL |

**Root cause:** The Δ²(z) evolution may not be steep enough, and the per-z conversion (multiplying by c·h/H) partially counteracts the 1/H suppression. Additionally, the concentration-mass relation affects Δ² through the ρ² integral.

---

## 5. mAGN and SFG — Rough approximations (HIGH)

**Expected:** mAGN peaks z~0.3–0.5; SFG peaks z~1–2.
**Ours:** mAGN peaks z~0.07; SFG peaks z~0.02.

| # | Claim | Reference | Our Code | Match |
|---|-------|-----------|----------|-------|
| M1 | mAGN from [Di Mauro+ (2014)](literature/dimauro2014.md) radio LF | L_γ–L_radio correlation | Hand-calibrated LDDE | **MISMATCH** |
| S1 | SFG from [Gruppioni+ (2013)](literature/gruppioni2013.md) IR LF × L_γ∝L_IR^1.17 | Herschel PEP/HerMES | Hand-calibrated LDDE | **MISMATCH** |

**Root cause:** The mAGN and SFG GLF parameters (A, L_c, evolution indices) were hand-calibrated to approximate IGRB contributions, not fitted to the original papers' source count data. The L_c values are especially suspect (mAGN: 3e43, SFG: 2e39 — both very low, concentrating emission at nearby faint sources).

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
