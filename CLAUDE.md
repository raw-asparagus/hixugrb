# CLAUDE.md

## Audit Plan: docs/ Self-Consistency & docs/ vs hi_gamma_xcorr/ Consistency

### Documentation Structure & Dependency Tiers

The documentation forms a tiered DAG. Updates must flow **top-down** through the tiers; a file is stale when any of its dependencies is newer.

```
Tier 0 — Sources of truth (never generated, always authoritative):
  papers/*.pdf  (22 PDFs)
  hi_gamma_xcorr/*.py  (implementation)

Tier 1 — Leaf docs (depend only on papers, no inter-doc dependencies):
  literature/*.md  (22 reviews — one per paper)

Tier 2 — Synthesis docs (depend on Tier 1 + code):
  equations.md      ← literature/*.md + code (equation↔function mapping)
  conventions.md    ← literature/*.md + code (units, frames, deviations)
  architecture.md   ← code (import graph, module descriptions)

Tier 3 — Per-source audit docs (depend on Tier 1 + Tier 2 + code):
  window-functions/*.md narratives         ← literature + conventions
  window-functions/*_evidence_matrix.md    ← literature + equations + code

Tier 4 — Master audit (depends on all Tier 1):
  literature_evidence_matrix.md  ← all 22 literature/*.md
```

**Evidence matrix → code coupling** (which matrices audit which code):

| Evidence matrix | Code modules |
|----------------|--------------|
| `hi_evidence_matrix.md` | `hi_model.py`, `halo_model.py`, `hmf_interface.py`, `cosmology.py`, `config.py` |
| `dm_annihilation_evidence_matrix.md` | `dm_model.py`, `pppc4dmid.py`, `ebl.py`, `halo_model.py`, `config.py` |
| `bl_lac_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| `fsrq_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| `magn_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| `sfg_evidence_matrix.md` | `astro_sources.py`, `config.py` |

### Phase 0: Staleness Check (3 tasks, all parallel)

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 0.1 | `literature_evidence_matrix.md` git date vs all `literature/*.md` dates | matrix + 22 lit files | Matrix newer than all lit files |
| 0.2 | Each `window-functions/*_evidence_matrix.md` git date vs its narrative + code modules | 6 matrices + 6 narratives + code | Each matrix newer than sources |
| 0.3 | `equations.md` / `conventions.md` git dates vs `hi_gamma_xcorr/*.py` | 2 docs + all code | Docs at least as recent as code |

**Method:** `git log -1 --format="%aI" -- <file>` for each file.

### Phase 1: Internal Doc-to-Doc Cross-Consistency (6 tasks; 1.1-1.3 parallel, then 1.4-1.6 parallel)

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 1.1 | **Deviation registry completeness:** every Dx in `equations.md` has entry in `conventions.md` S7 and vice versa. Resolved D3/D9/D11 not referenced as active. | equations.md, conventions.md | Bijective mapping, no orphans |
| 1.2 | **equations.md source links:** ~60 equation entries link to valid `literature/*.md` files; cited eq/table exists in that file. Spot-check 15-20. | equations.md, literature/*.md | All sampled links resolve |
| 1.3 | **Formula consistency:** 10 key equations (M_HI, T_bar, W_DM, LDDE, W_astro, mAGN_GLF, Gruppioni, PSF, Limber, variance) match between equations.md and their literature source, modulo documented Dx. | equations.md, literature/*.md | Match or deviation documented |
| 1.4 | **Window-function forms:** per-chi conventions in conventions.md S3 agree with equations.md entries 3.12, 4.6, 5.5 (what's baked in: bias, Jacobian, EBL). | conventions.md, equations.md | Consistent prefactors and notes |
| 1.5 | **Parameter values:** Planck params, LDDE tables, spectral indices stated in both equations.md and conventions.md agree numerically. | conventions.md, equations.md | No numerical discrepancies |
| 1.6 | **Module attribution:** function-to-module mapping in equations.md consistent with architecture.md module descriptions. | architecture.md, equations.md | No misattributions |

### Phase 2: Docs-to-Code Structure (5 tasks; 2.1-2.3 parallel, then 2.4-2.5 parallel)

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 2.1 | **Function existence:** every function name in equations.md "Function" column exists as `def` in attributed module (~40 functions). | equations.md, all code | All resolve |
| 2.2 | **Import graph vs architecture.md:** dependency arrows match actual `import` statements. | architecture.md, all code | Graph matches |
| 2.3 | **Module docstrings vs architecture.md:** one-line descriptions semantically consistent. | architecture.md, all code | Consistent |
| 2.4 | **config.py parameter audit:** every numerical value in equations.md (Planck, HI, SMT, Moline, LDDE tables, mAGN chain, Gruppioni, Ackermann, spectral indices, Fermi bins) matches config.py. | equations.md, config.py | All match to stated precision |
| 2.5 | **Unit convention comments:** 10 boundary conversions from conventions.md S1 reflected in code comments/docstrings. | conventions.md, code | Consistent |

### Phase 3: Equations-to-Code Math Audit (7 tasks; 3.1-3.4 parallel, then 3.5-3.6 parallel, then 3.7)

| ID  | Check | Code module | Key attention points |
|-----|-------|-------------|---------------------|
| 3.1 | Cosmology (Eqs 1.1-1.11) | cosmology.py | E(z), H(z), chi(z), growth, sigma |
| 3.2 | Halo model (Eqs 2.1-2.8) | halo_model.py | Bryan-Norman Delta_vir, Correa coefficients (D2), NFW FT, units |
| 3.3 | HI model (Eqs 3.1-3.12) | hi_model.py | Modified NFW (r+0.75r_s), T_bar_b=188h, W_HI Jacobian, Omega_HI computed (D5) |
| 3.4 | DM model (Eqs 4.1-4.8) | dm_model.py, pppc4dmid.py, ebl.py | rho^2 integral, Moline boost, (1+z)^3, E_rest=E(1+z), EBL at E_obs |
| 3.5 | Astro sources (Eqs 5.1-5.15) | astro_sources.py | LDDE sign (D12), Willott eta(z), mAGN 4-step chain, Gruppioni k_R2 (D4), EBL on astro (D14) |
| 3.6 | Noise/beams (Eqs 8.1-8.16) | noise_model.py | T_sys, beam models, PSF, ell_max, bin averaging |
| 3.7 | Angular power + statistics (Eqs 9.1-10.4) | angular_power.py, statistics.py | Limber k=(ell+0.5)/chi (D8), variance N^gamma unit conversion, SNR |

### Phase 4: Cross-Cutting Checks (4 tasks; 4.1-4.3 parallel, then 4.4)

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 4.1 | **Active deviations in code:** D2,D4,D5,D6,D7,D8,D12,D13,D14 confirmed present. Resolved D3,D9,D11 confirmed absent. | conventions.md S7, code | Each deviation verified |
| 4.2 | **Window evidence matrix spot-check:** pick 3 of 6 matrices, 5 claims each, verify vs current code. Focus near known deviations. | window-functions/*_evidence_matrix.md, code | 15 sampled claims hold |
| 4.3 | **pinetti2022.py parallel implementation:** thesis-faithful functions differ from main pipeline in exactly the documented ways (concentration coefficients, q=0.75, ell/chi, T_bar=180). | pinetti2022.py, evidence matrices | Differences match documentation |
| 4.4 | **Ammazzalorso bin audit:** config bins match conventions.md S6 and equations.md S8; noise_model.py uses them correctly in data-analysis mode. | config.py, conventions.md, noise_model.py | Consistent |

### Phase 5: Reconciliation & Fix (2 tasks, sequential)

| ID  | Check |
|-----|-------|
| 5.1 | Aggregate all discrepancies. Classify as: (a) doc error, (b) code error, (c) stale audit, (d) cosmetic. Prioritize by impact. |
| 5.2 | Apply fixes for (a) doc errors and (b) code errors found in 5.1. |

### Phase 5.5: Documentation Regeneration (8 tasks; respects dependency tiers)

After Phase 5 applies fixes, all stale documentation must be re-audited **in dependency order** (see Documentation Structure above). A file is stale when any of its Tier 0 dependencies (code) or same-tier dependencies (other docs) have been modified more recently.

**Wave 1 — Tier 2 synthesis docs (1 task, reviews code changes):**

| ID  | Task | Dependencies | Files |
|-----|------|-------------|-------|
| 5.5.1 | Review `conventions.md` against recent code commits; update if any convention, unit, frame, or deviation has changed | Code (Tier 0) | `conventions.md`, all `hi_gamma_xcorr/*.py` |

**Wave 2 — Tier 3 evidence matrices (6 tasks, all parallel; depend on Wave 1):**

| ID  | Task | Code dependencies |
|-----|------|-------------------|
| 5.5.2 | Re-audit `hi_evidence_matrix.md` | `hi_model.py`, `halo_model.py`, `hmf_interface.py`, `cosmology.py`, `config.py` |
| 5.5.3 | Re-audit `dm_annihilation_evidence_matrix.md` | `dm_model.py`, `pppc4dmid.py`, `ebl.py`, `halo_model.py`, `config.py` |
| 5.5.4 | Re-audit `bl_lac_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| 5.5.5 | Re-audit `fsrq_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| 5.5.6 | Re-audit `magn_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| 5.5.7 | Re-audit `sfg_evidence_matrix.md` | `astro_sources.py`, `config.py` |

For each evidence matrix: read the current matrix, read the code modules it audits, verify every claim (equation match, parameter value, line number, status). Update any stale line numbers, changed formulas, or shifted logic. Preserve the matrix format.

**Wave 3 — Tier 4 master matrix (1 task, sequential; depends on Tier 1 being stable):**

| ID  | Task | Dependencies |
|-----|------|-------------|
| 5.5.8 | Regenerate `literature_evidence_matrix.md` | All 22 `literature/*.md` files |

### Execution Summary

| Phase | Tasks | Parallelism | Depends on |
|-------|-------|-------------|------------|
| 0 | 0.1-0.3 | 3 parallel | -- |
| 1 | 1.1-1.3 then 1.4-1.6 | 3+3 | Phase 0 |
| 2 | 2.1-2.3 then 2.4-2.5 | 3+2 | Phase 1 |
| 3 | 3.1-3.4 then 3.5-3.6 then 3.7 | 4+2+1 | Phase 2 |
| 4 | 4.1-4.3 then 4.4 | 3+1 | Phase 3 |
| 5 | 5.1-5.2 | sequential | Phase 4 |
| 5.5 | 5.5.1 then 5.5.2-5.5.7 then 5.5.8 | 1+6+1 | Phase 5 |

### Highest-Risk Areas

1. **Task 2.4** -- config.py has hundreds of parameter values to cross-check
2. **Task 3.5** -- astro_sources.py is the most complex module (4 GLF chains, multiple deviations)
3. **Task 3.7** -- Limber/variance h-factor unit conversions are historically error-prone
4. **Task 4.1** -- 9 active deviations each require understanding both literature default and deliberate choice

### Verification

After all phases, run `notebooks/pipeline_validation.ipynb` end-to-end to confirm no regressions from any fixes applied.

---

## Physics Consistency Audit: Cosmology, Frames, Units, and Density Conventions

This audit checks **physics-level consistency** across module boundaries — whether cosmologies, reference frames, density conventions, and unit dimensions remain self-consistent as quantities flow through the full pipeline. This is complementary to the structural audit above (Phases 0–5), which checks doc-to-doc and doc-to-code consistency.

### Context

- `cosmology.py` and `hmf_interface.py` run **two independent CAMB instances** with the same Planck 2018 params
- Only `_willott_volume_correction(z)` applies a cosmology correction (mAGN only); other GLFs use original-paper cosmology parameters without correction
- Energy is passed as E_obs to all window functions; rest-frame conversion `E_rest = E_obs*(1+z)` happens inside each
- The `(1+z)³` factor coupling between `clumping_factor` and `W_gamma_DM` is non-trivial bookkeeping
- `variance_Cl` converts N^γ from cm⁻⁴ to (Mpc/h)⁻⁴; cross-power C_ℓ must have matching units
- Literature fits (Ajello, Gruppioni, Ackermann, Moliné, Willott, Padmanabhan) were derived under various cosmologies — these **cannot be corrected** without re-fitting to original data; only volume/luminosity scaling corrections are possible

### Task 6.1: Cosmology Parameter Propagation

Verify identical Planck 2018 parameters reach every consumer.

| Consumer | Parameters used | How set |
|----------|----------------|---------|
| `cosmology.py` CAMB call | H0, ombh2, omch2, ns, As, tau, T_CMB | From `config.py` + hardcoded tau=0.0544 |
| `hmf_interface.py` MassFunction | H0, Om0, Ob0, sigma_8, n_s | From `config.py` |
| `halo_model.py` Delta_vir, R_vir | OMEGA_M, RHO_CRIT | From `config.py` |
| `hi_model.py` f_Hc | OMEGA_B, OMEGA_M, Y_P | From `config.py` |

**Key checks:**
- Does `hmf_interface.py` pass `Ob0 = OMEGA_B` consistently? (must match OMEGA_B_H2 / h²)
- Does `hmf` receive the same `tau_reio` that cosmology.py uses?
- Are σ₈ and A_s consistent? (CAMB computes σ₈ from A_s; hmf takes σ₈ directly)

**Files:** `config.py`, `cosmology.py`, `hmf_interface.py`

### Task 6.2: Literature Cosmology Mismatch Registry

For each external fit, identify the assumed cosmology and assess the mismatch. Document in `conventions.md` §8.

| Fit | Paper cosmology | Correction applied? | Residual |
|-----|----------------|---------------------|----------|
| Correa c(M) | Planck 2013 (Ω_m=0.317, h=0.67) | D2: re-fit coefficients | Negligible |
| Ajello 2012 FSRQ LDDE | WMAP-era | None | Small (~1-2% in d_L) |
| Ajello 2014 BL Lac LDDE | Planck 2013-era | None | Negligible |
| Willott 2001 RLF | H0=50, empty universe | η(z) volume correction | Volume corrected; fit shape not re-derived |
| Gruppioni 2013 IR LF | ΛCDM (unspecified) | None | Small |
| Ackermann 2012 L_γ–L_IR | WMAP-era | None | Cosmology enters only through d_L |
| Moliné 2017 boost | Planck 2015 | None | Negligible (N-body; weak dependence) |
| Padmanabhan 2017 HI | Planck 2015-era | None | Weak cosmology dependence |

**Action:** Read each `docs/literature/*.md` to extract stated cosmology. Check whether volume/luminosity corrections should be applied but aren't.

**Files:** All `docs/literature/*.md`, `astro_sources.py`, `config.py`

### Task 6.3: Energy Frame Consistency Across Boundaries

Trace E_GeV from top-level call through every module boundary:

```
C_ell_HI_gamma(ell, E_GeV, ...)          # E_GeV = observed
  → W_gamma_DM(E_GeV, z, ...)            # receives E_obs
      → E_emit = E_GeV * (1+z)           # converts to rest
      → dNdE(E_emit, m_chi, ch)          # spectrum at rest-frame
      → ebl.attenuation(E_GeV, z)        # EBL at observed
  → W_gamma_astro(E_GeV, z, ...)         # receives E_obs
      → E_rest = E_GeV * (1+z)           # converts to rest
      → L * E_rest^{-alpha} / I_alpha    # spectrum at rest-frame
      → ebl.attenuation(E_GeV, z)        # EBL at observed
  → noise_model functions(E_GeV)         # PSF, beam at observed
```

**Check each boundary:**
1. `angular_power.py` → `dm_model.W_gamma_DM` and `astro_sources.W_gamma_astro`: E_GeV passed as observed
2. `astro_sources.L_sens(z, alpha, E_GeV)`: K-correction uses E_GeV correctly
3. `pppc4dmid.dNdE(E_emit, ...)`: verify E_emit is rest-frame
4. `ebl.tau(E, z)`: verify ebltable expects observed energy (not rest-frame)

**Files:** `angular_power.py`, `dm_model.py`, `astro_sources.py`, `pppc4dmid.py`, `ebl.py`, `noise_model.py`

### Task 6.4: Comoving vs Physical Density Convention

Trace density convention through DM and HI chains:

**DM chain:**
1. `rho2_integral_analytic`: `_rho_s = M / (4π r_s³ f(c))` — M in M_sun/h, r_s in Mpc/h (comoving)
2. `clumping_factor`: divides by `RHO_BAR²` and `(1+z)³` → physical-frame Δ²
3. `W_gamma_DM`: multiplies by `(1+z)³` → re-inserts physical density factor
4. Net: verify `(1+z)³` factors cancel correctly

**HI chain:**
1. `rho_HI_mean`: `∫ dn/dM × M_HI dM` — comoving density
2. `Omega_HI = rho_HI_mean / RHO_CRIT` — both comoving
3. `T_bar_b = 188 h Omega_HI (1+z)² / E(z)` — (1+z)² converts comoving Ω_HI to physical brightness temperature

**Files:** `dm_model.py`, `hi_model.py`, `halo_model.py`, `config.py`

### Task 6.5: End-to-End Dimensional Analysis of C_ℓ

Trace units through the Limber integral and verify consistency with variance formula:

| Factor | Units |
|--------|-------|
| dχ/dz | [Mpc/h] |
| 1/χ² | [(Mpc/h)⁻²] |
| W_HI | [mK × (Mpc/h)⁻¹] (from T_bar × H/(c·h)) |
| W_γ | [(Mpc/h)⁻³ × gamma-ray intensity dims] |
| P_cross | [(Mpc/h)³] |
| dz | [dimensionless] |

Then verify variance `(ΔC_ℓ)² = N^γ_eff × (C_HI + N^HI_eff) / ((2ℓ+1)f_sky)` has consistent dimensions with C_ℓ.

**Files:** `angular_power.py`, `hi_model.py`, `dm_model.py`, `astro_sources.py`, `statistics.py`, `noise_model.py`

### Task 6.6: Willott Cosmology Correction Verification

Deep-dive into mAGN chain:
1. Verify Milne-universe volume element formula in `_willott_volume_correction(z)`
2. Check if η(z) corrects *density* only or also *luminosity* (Willott fit L_151 in H0=50 cosmology — should L_151 be rescaled via d_L²?)
3. Check Willott RLF parameters (ρ*, L*, slopes) for luminosity correction need
4. Verify `_glf_mAGN` calls `_willott_volume_correction` and multiplies by result

**Files:** `astro_sources.py` (lines 142–289), `docs/literature/willott2001.md`, `docs/literature/dimauro2014.md`

### Execution Summary

| Task | Focus | Parallelism |
|------|-------|-------------|
| 6.1 | Cosmology parameter propagation | All 6 tasks independent; run in parallel |
| 6.2 | Literature cosmology registry | |
| 6.3 | Energy frame consistency | |
| 6.4 | Comoving vs physical density | |
| 6.5 | Dimensional analysis of C_ℓ | |
| 6.6 | Willott correction completeness | |

After completion: fix any fixable issues; document unfixable cosmology mismatches in `docs/conventions.md` §8.

### Highest-Risk Areas

1. **Task 6.1** — Two independent CAMB instances could silently disagree on σ(M,z)
2. **Task 6.5** — Cross-power C_ℓ mixes mK (HI) with photon-intensity units (gamma)
3. **Task 6.6** — Willott luminosity correction may be missing (only volume corrected)

### Verification

After all tasks, run `notebooks/pipeline_validation.ipynb` end-to-end to confirm no regressions.