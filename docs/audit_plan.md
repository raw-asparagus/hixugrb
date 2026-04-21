# CLAUDE.md

## Audit Plan: docs/ Self-Consistency & docs/ vs hi_gamma_xcorr/ Consistency

### Documentation Structure & Dependency Tiers

The documentation and code form a tiered DAG. Correctness flows **top-down**: each tier must be consistent with the tiers above it. When a discrepancy is found, the **higher-tier artifact is authoritative** — fix the lower-tier one.

```
Tier 0 — Sole source of truth (never generated, always authoritative):
  papers/*.pdf  (28 PDFs)

Tier 1 — Leaf docs (faithful summaries of Tier 0):
  literature/*.md  (28 reviews — one per paper)

Tier 2 — Synthesis docs (depend on Tier 1; define deviations):
  equations.md      ← literature/*.md (equation catalog + deviation definitions)
  conventions.md    ← literature/*.md (units, frames, deviations)
  NOTE: These docs have a dual role — authoritative for what the math
  should be, but descriptive for where code implements it (function names,
  module attributions, line refs). The code-location metadata is not a
  dependency; it is updated after code changes, not before.

Tier 3 — Implementation (realization of Tier 1 + Tier 2 with documented deviations):
  hi_gamma_xcorr/*.py

Tier 4 — Descriptive docs (depend on Tier 3):
  architecture.md   ← code (import graph, module descriptions)

Tier 5 — Audit docs (verify Tier 3 against Tier 1 + Tier 2):
  window-functions/*.md narratives         ← literature + conventions
  window-functions/*_evidence_matrix.md    ← literature + equations + code

Tier 6 — Master audit (depends on all Tier 1):
  literature_evidence_matrix.md  ← all 28 literature/*.md
```

**Correctness authority flows top-down:** if code (Tier 3) disagrees with literature + equations (Tiers 1–2) and no deviation is documented, the code is suspect. Evidence matrices (Tier 5) and architecture (Tier 4) are regenerated to match code, but code itself is corrected to match the literature.

**Evidence matrix → code coupling** (which matrices audit which code):

| Evidence matrix | Code modules |
|----------------|--------------|
| `hi_evidence_matrix.md` | `hi_model.py`, `halo_model.py`, `hmf_interface.py`, `cosmology.py`, `config.py` |
| `dm_annihilation_evidence_matrix.md` | `dm_model.py`, `pppc4dmid.py`, `ebl.py`, `halo_model.py`, `config.py` |
| `bl_lac_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| `fsrq_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| `magn_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| `sfg_evidence_matrix.md` | `astro_sources.py`, `config.py` |

### Phase 0: Literature Review Verification (28 tasks, all parallel)

Verify each `literature/*.md` review faithfully summarizes its corresponding `docs/papers/*.pdf`. This is the foundational check — everything downstream depends on the reviews being accurate.

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 0.x | For each of the 28 papers: read the PDF and the corresponding `.md`; verify key equations, parameter values, and qualitative claims in the review match the paper. Flag any inaccuracies or missing content. | `docs/papers/*.pdf`, `docs/literature/*.md` (pairwise) | Review accurately represents the paper |

**Method:** Read each PDF alongside its review. Focus on: (1) equations reproduced correctly, (2) parameter values transcribed accurately, (3) no claims in the review that aren't in the paper, (4) no material omissions relevant to this pipeline.

**The 6 most-recently-added digests** (added during the MeerKLASS / 4FGL-DR4 plumbing work; never previously audited):

| Digest | Paper |
|---|---|
| `literature/mangla2025_meerklass_lband_dr1.md` | `papers/2512.17685v1.pdf` |
| `literature/paul2025_meerklass_uhf_dr1.md` | `papers/2512.11964v1.pdf` |
| `literature/cunnington2025_meerklass_overview.md` | `papers/2510.27549v2.pdf` |
| `literature/meerklass2025_lband_deepfield.md` | `papers/2407.21626v2.pdf` |
| `literature/ammazzalorso2018b_fermi_2mpz.md` | `papers/1808.09225v2.pdf` |
| `literature/ballet2023_4fgl_dr4.md` | `papers/2307.12546v4.pdf` |

### Phase 1: Internal Doc-to-Doc Cross-Consistency (6 tasks; 1.1-1.3 parallel, then 1.4-1.6 parallel)

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 1.1 | **Deviation registry completeness:** every Dx in `equations.md` has entry in `conventions.md` S7 and vice versa. Resolved D3/D9/D11 not referenced as active. **NEW: must include the three new convention divergences** — (a) Cunnington brightness mode (180 mK + Cunnington+2025 Eqs A3/A5 polynomials, dispatch via per-telescope `default_hi_brightness`); (b) MeerKAT canonical T_sys (`T_sys_meerkat`: T_rx + T_spl + T_CMB + T_gal, MeerKLASS Collab. 2025 Eqs 21–22) vs Pinetti generic (`T_sys_pinetti`), dispatched via `T_sys_model`; (c) 4FGL-DR4 F_sens dispatch (`'4fgl_dr4_psf'` mode → `F_SENS_4FGL_DR4 = 7.3e-11` from Ballet+2023, vs `'pinetti_constant'` → `F_SENS_PINETTI = 1e-10`), dispatched via `default_unresolved_mode`. | equations.md, conventions.md | Bijective mapping, no orphans; new dispatch axes documented |
| 1.2 | **equations.md source links:** ~60 equation entries link to valid `literature/*.md` files; cited eq/table exists in that file. Spot-check 15-20. | equations.md, literature/*.md | All sampled links resolve |
| 1.3 | **Formula consistency:** 10 key equations (M_HI, T_bar, W_DM, LDDE, W_astro, mAGN_GLF, Gruppioni, PSF, Limber, variance) match between equations.md and their literature source, modulo documented Dx. | equations.md, literature/*.md | Match or deviation documented |
| 1.4 | **Window-function forms:** per-chi conventions in conventions.md S3 agree with equations.md entries 3.12, 4.6, 5.5 (what's baked in: bias, Jacobian, EBL). | conventions.md, equations.md | Consistent prefactors and notes |
| 1.5 | **Parameter values:** Planck params, LDDE tables, spectral indices stated in both equations.md and conventions.md agree numerically. | conventions.md, equations.md | No numerical discrepancies |
| 1.6 | **Module attribution:** function-to-module mapping in equations.md consistent with architecture.md module descriptions. (Cross-check between Tier 2 descriptive metadata and Tier 4; neither is authoritative over the other — resolve against actual code.) | architecture.md, equations.md | No misattributions |

### Phase 2: Docs-to-Code Structure (5 tasks; 2.1-2.3 parallel, then 2.4-2.5 parallel)

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 2.1 | **Function existence:** every function name in equations.md "Function" column exists as `def` in attributed module (~40 functions). **NEW functions added this session that must appear in equations.md and resolve in code:** `hi_model.Omega_HI_cunnington`, `hi_model.b_HI_cunnington`, `hi_model.T_bar_b_cunnington`; extended `hi_model.b_HI(..., hi_brightness)`, `hi_model.T_bar_b_for_model(..., 'cunnington')`, `hi_model.P_HI_2h(..., hi_brightness)`; `noise_model.T_sys_pinetti`, `noise_model.T_sys_meerkat`, `noise_model.T_sys(..., model)`; `astro_sources.L_sens(..., F_sens_baseline)`, `astro_sources.F_sens_energy(..., F_sens_baseline)`; `angular_power.C_ell_HI_gamma_multi_E`; `cosmology._chi_interp`, `cosmology._growth_interp`, `cosmology._cosmo_fingerprint`. | equations.md, all code | All resolve, including new symbols |
| 2.2 | **Import graph vs architecture.md:** dependency arrows match actual `import` statements. | architecture.md, all code | Graph matches |
| 2.3 | **Module docstrings vs architecture.md:** one-line descriptions semantically consistent. | architecture.md, all code | Consistent |
| 2.4 | **config.py parameter audit:** every numerical value in equations.md (Planck, HI, SMT, Moline, LDDE tables, mAGN chain, Gruppioni, Ackermann, spectral indices, Fermi bins) matches config.py. **NEW constants to verify**: `F_SENS_PINETTI = 1e-10`, `F_SENS_4FGL_DR4 = 7.3e-11` (corrected from prior 4e-12 units error), `F_SENS_4FGL_DR4_ERG_CGS = 1.0e-12`, `T_SPL_MEERKAT_K = 3.0`, `T_CMB_K = 2.725`. **NEW RADIO_TELESCOPES entries** (each with η=0.5 and per-entry `T_sys_model='meerkat'`, `default_hi_brightness='cunnington'`, `default_unresolved_mode='4fgl_dr4_psf'`): `MeerKLASS_L_pilot` (renamed from `MeerKLASS_DR0`), `MeerKLASS_L_deepfield`, `MeerKLASS_DR1_L`, `MeerKLASS_DR1_UHF`, `MeerKLASS_2024_HI`, `MeerKLASS_XLP_2028`. **Per-telescope dispatch fields** must exist on every entry (legacy entries default to `'pinetti'`, `'fixed_omega'`, `'pinetti_constant'`). **Corrected legacy Pinetti targets**: MeerKAT L = 3.6 (was 2.0), SKA1 Band1 = 4.6, SKA2 Band2 = 7.0. | equations.md, config.py | All match to stated precision |
| 2.5 | **Unit convention comments:** 10 boundary conversions from conventions.md S1 reflected in code comments/docstrings. | conventions.md, code | Consistent |

### Phase 3: Equations-to-Code Math Audit (7 tasks; 3.1-3.4 parallel, then 3.5-3.6 parallel, then 3.7)

| ID  | Check | Code module | Key attention points |
|-----|-------|-------------|---------------------|
| 3.1 | Cosmology (Eqs 1.1-1.11) | cosmology.py | E(z), H(z), chi(z), growth, sigma. **NEW**: verify `_chi_interp` and `_growth_interp` cumulative-trapezoid splines reproduce original `quad`-based path to rel-tol 1e-9 over [0, Z_MAX]; verify `_cosmo_fingerprint` mutation guard re-initialises CAMB if any cosmology constant changes. |
| 3.2 | Halo model (Eqs 2.1-2.8) | halo_model.py | Bryan-Norman Delta_vir, Correa coefficients (D2), NFW FT, units |
| 3.3 | HI model (Eqs 3.1-3.12) | hi_model.py | Modified NFW (r+0.75r_s), T_bar_b=188h, W_HI Jacobian, Omega_HI computed (D5). **NEW**: verify Cunnington-mode dispatch — `Omega_HI_cunnington(z)`, `b_HI_cunnington(z)`, `T_bar_b_cunnington(z)` polynomials match Cunnington+2025 Eqs A3/A5 with 180 mK prefactor; `T_bar_b_for_model(..., 'cunnington')` and `b_HI(..., 'cunnington')` route correctly; `P_HI_2h` collapses to `b² P_lin` in cunnington mode (no halo-model integral); bias plumbing self-consistent across `P_HI_DM_2h`, `P_HI_astro_2h`. |
| 3.4 | DM model (Eqs 4.1-4.8) | dm_model.py, pppc4dmid.py, ebl.py | rho^2 integral, Moline boost, (1+z)^3, E_rest=E(1+z), EBL at E_obs |
| 3.5 | Astro sources (Eqs 5.1-5.15) | astro_sources.py | LDDE sign (D12), Willott eta(z), mAGN 4-step chain, Gruppioni k_R2 (D4), EBL on astro (D14). **NEW**: verify `F_sens_baseline` plumbing through `L_sens` and `F_sens_energy`; verify `_W_gamma_astro_impl` dispatch arms — `'4fgl_dr4_psf'`/`'data'` → `cfg.F_SENS_4FGL_DR4`, `'pinetti_constant'`/`'forecast'` → `cfg.F_SENS_PINETTI`; verify all `_W_gamma_astro_impl` arguments are hashable (`@lru_cache(maxsize=16384)`). |
| 3.6 | Noise/beams (Eqs 8.1-8.16) | noise_model.py | T_sys, beam models, PSF, ell_max, bin averaging. **NEW**: verify `T_sys_meerkat(nu_MHz)` formula = T_rx + T_spl + T_CMB + T_gal matches MeerKLASS Collab. 2025 Eqs 21–22; `T_sys_pinetti` is just the renamed legacy `T_sys`; `T_sys(model=...)` dispatcher honours both keys; `noise_dish` and `noise_interf` consult `tel.get('T_sys_model', 'pinetti')`. |
| 3.7 | Angular power + statistics (Eqs 9.1-10.4) | angular_power.py, statistics.py | Limber k=(ell+0.5)/chi (D8), variance N^gamma unit conversion, SNR. **NEW**: verify `C_ell_HI_gamma_multi_E` returns results bit-equivalent (rel-tol 1e-10) to a per-energy loop over the legacy `C_ell_HI_gamma`; verify `compute_SNR`, `delta_chi2`, and `exclusion_curve` all read per-telescope `default_hi_brightness` and `default_unresolved_mode` and pass them through to the angular-power layer. |

### Phase 4: Cross-Cutting Checks (4 tasks; 4.1-4.3 parallel, then 4.4)

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 4.1 | **Active deviations in code:** D2,D4,D5,D6,D7,D8,D12,D13,D14 confirmed present. Resolved D3,D9,D11 confirmed absent. **NEW deviations to verify present (after Phase 1.1 assigns Dx numbers)**: Cunnington brightness mode, MeerKAT canonical T_sys, 4FGL-DR4 F_sens dispatch — each must be reachable via at least one config entry and exercised by `compute_SNR` for at least one telescope. | conventions.md S7, code | Each deviation verified |
| 4.2 | **Window evidence matrix spot-check:** pick 3 of 6 matrices, 5 claims each, verify vs current code. Focus near known deviations. | window-functions/*_evidence_matrix.md, code | 15 sampled claims hold |
| 4.3 | **pinetti2022.py parallel implementation:** thesis-faithful functions differ from main pipeline in exactly the documented ways (concentration coefficients, q=0.75, ell/chi, T_bar=180). | pinetti2022.py, evidence matrices | Differences match documentation |
| 4.4 | **Ammazzalorso bin audit:** config bins match conventions.md S6 and equations.md S8; noise_model.py uses them correctly in data-analysis mode. | config.py, conventions.md, noise_model.py | Consistent |

### Phase 5: Reconciliation & Fix (2 tasks, sequential)

| ID  | Check |
|-----|-------|
| 5.1 | Aggregate all discrepancies. Classify as: (a) doc error, (b) code error, (c) stale audit, (d) cosmetic. Prioritize by impact. |
| 5.2 | Apply fixes for (a) doc errors and (b) code errors found in 5.1. |

### Phase 5.5: Documentation Regeneration (9 tasks; respects dependency tiers)

After Phase 5 applies fixes, all affected documentation must be re-audited **in dependency order** (see Documentation Structure above). Re-audit any doc whose upstream content was changed by Phase 5 fixes.

**Wave 1 — Tier 2 synthesis docs (1 task, reviews literature changes):**

| ID  | Task | Dependencies | Files |
|-----|------|-------------|-------|
| 5.5.1 | Review `conventions.md` and `equations.md` against literature reviews (Tier 1); update math, deviations, and conventions to match authoritative literature. Then update code-location metadata (function names, module attributions, line refs) to reflect any code fixes from Phase 5. **KNOWN STALE — must run**: `conventions.md` and `equations.md` currently contain **zero** references to `cunnington`, `MeerKLASS`, `F_SENS_4FGL`, `T_sys_meerkat`, `4FGL-DR4`, `Ballet`, or `multi_E`. Wave 1 must (a) absorb the 6 new digests, (b) document the 3 new convention divergences from Phase 1.1, (c) record the 5 new constants from Phase 2.4, (d) catalogue the 8 new functions from Phase 2.1, and (e) update §8 cosmology mismatch table per Physics 6.2. | Literature (Tier 1) for math; code (Tier 3) for metadata only | `conventions.md`, `equations.md`, `literature/*.md`, all `hi_gamma_xcorr/*.py` |

**Wave 1.5 — Tier 4 descriptive docs (1 task; depends on Wave 1):**

| ID  | Task | Dependencies | Files |
|-----|------|-------------|-------|
| 5.5.1b | Regenerate `architecture.md` against current code: verify import graph, module descriptions, and one-line summaries reflect any code fixes from Phase 5 | Code (Tier 3) | `architecture.md`, all `hi_gamma_xcorr/*.py` |

**Wave 2 — Tier 5 evidence matrices (6 tasks, all parallel; depend on Wave 1.5):**

| ID  | Task | Code dependencies |
|-----|------|-------------------|
| 5.5.2 | Re-audit `hi_evidence_matrix.md` | `hi_model.py`, `halo_model.py`, `hmf_interface.py`, `cosmology.py`, `config.py` |
| 5.5.3 | Re-audit `dm_annihilation_evidence_matrix.md` | `dm_model.py`, `pppc4dmid.py`, `ebl.py`, `halo_model.py`, `config.py` |
| 5.5.4 | Re-audit `bl_lac_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| 5.5.5 | Re-audit `fsrq_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| 5.5.6 | Re-audit `magn_evidence_matrix.md` | `astro_sources.py`, `config.py` |
| 5.5.7 | Re-audit `sfg_evidence_matrix.md` | `astro_sources.py`, `config.py` |

For each evidence matrix: read the current matrix, read the code modules it audits, verify every claim (equation match, parameter value, line number, status). Correct any inaccurate line numbers, formulas, or logic descriptions. Preserve the matrix format.

**Wave 3 — Tier 6 master matrix (1 task, sequential; depends on Tier 1 being stable):**

| ID  | Task | Dependencies |
|-----|------|-------------|
| 5.5.8 | Regenerate `literature_evidence_matrix.md` | All 28 `literature/*.md` files |

### Phase 7: Stale Documentation Sweep (4 tasks, all parallel; depends on Phase 2)

Catches references in `docs/` that no longer point to anything real after the session's renames, additions, and dispatch refactor.

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 7.1 | **Dead function/symbol references**: every `function_name`, `module.symbol`, `cfg.CONSTANT`, line number, and file path mentioned in the synthesis and audit docs resolves to an actual symbol in current code. Particular attention to renames (e.g. `T_sys` → `T_sys_pinetti`, `MeerKLASS_DR0` → `MeerKLASS_L_pilot`). | `docs/equations.md`, `docs/conventions.md`, `docs/architecture.md`, `docs/window-functions/*.md`, all `hi_gamma_xcorr/*.py` | All sampled refs resolve |
| 7.2 | **Stale parameter values**: every numerical constant cited in docs (Planck params, Ω_HI, T_sys formula coefficients, F_sens, telescope area/time/η, spectral indices, mAGN chain values, Gruppioni params, Fermi bins) matches current `config.py`. Flag any drift. | All `docs/*.md`, `config.py` | All match to stated precision |
| 7.3 | **Orphan literature digests**: every `literature/*.md` is referenced from at least one of `equations.md`, `conventions.md`, `literature_evidence_matrix.md`, or a `window-functions/*.md`. Flag orphans (digests added but never wired into the synthesis layer — currently expected for the 6 new MeerKLASS/4FGL-DR4 digests). Reverse: synthesis docs citing a digest that does not exist. | All `docs/literature/*.md`, all `docs/*.md` | No orphans, no dangling cites |
| 7.4 | **Stale prose claims**: scan `architecture.md`, `conventions.md`, and `window-functions/*.md` narratives for outdated phrasing — e.g. "the pipeline uses Pinetti T_sys throughout" (no longer true after dispatch), "F_sens is a fixed constant" (no longer true), "188 mK is the only brightness convention" (no longer true after Cunnington mode), "MeerKLASS_DR0" (renamed), claims about energy-loop being a bottleneck (no longer true after `C_ell_HI_gamma_multi_E` hoist). | `docs/architecture.md`, `docs/conventions.md`, `docs/window-functions/*.md` | All prose reflects current state |

### Phase 8: Stale Code Sweep (5 tasks, all parallel; depends on Phase 3)

Catches dead code, unreachable branches, and stale comments in `hi_gamma_xcorr/` left over from the dispatch refactor and earlier session work.

| ID  | Check | Files | Pass |
|-----|-------|-------|------|
| 8.1 | **Dead functions / unused exports**: identify functions, classes, and module-level symbols in `hi_gamma_xcorr/*.py` that have no callers anywhere in the package, in `notebooks/`, or in `pinetti2022.py`. Distinguish (a) genuinely dead, (b) public API kept for users, (c) tests-only. Recommend removal for (a). | All `hi_gamma_xcorr/*.py`, `notebooks/*.ipynb`, `pinetti2022.py` | List of dead symbols + recommendation |
| 8.2 | **Dead dispatch branches**: every string literal compared in dispatch logic (`unresolved_mode`, `hi_brightness`, `T_sys_model`, `analysis_mode`) is reachable from at least one config entry or documented default. Flag dispatch arms whose key never appears in any caller. | `hi_model.py`, `noise_model.py`, `astro_sources.py`, `angular_power.py`, `statistics.py`, `config.py` | All dispatch arms reachable |
| 8.3 | **Dead imports and unused parameters**: per-module unused-import audit and unused-parameter audit on functions whose signatures grew during the dispatch refactor (e.g. `hi_brightness`, `unresolved_mode`, `F_sens_baseline` plumbing). | All `hi_gamma_xcorr/*.py` | No unused imports/params |
| 8.4 | **Stale comments / docstrings**: comments or docstrings that reference removed code, old names, or old behaviour (e.g. docstring still says "uses Pinetti T_sys" on a now-dispatched function, "F_sens = 1e-10" in `L_sens` docstring, references to `MeerKLASS_DR0`, comments claiming `T_sys` is the only T_sys function). | All `hi_gamma_xcorr/*.py` | All docstrings/comments current |
| 8.5 | **Cache hygiene**: every `@_cache_stable` and `@lru_cache` target is genuinely deterministic in its declared arguments (no hidden module-state dependence that would cause stale returns after `cfg` mutation). Re-audit the decorated set after this session's additions, including the new `lru_cache` on `_W_gamma_astro_impl`, `noise_radio_combined`, `beam_fermi_exact`, and the new `@_cache_stable` on `_b_HI_default`. Confirm no decorated function reads a `cfg` value not in its argument list. | `cache.py`, all decorated functions | All caches sound; stale-cache risks documented |

### Execution Summary

| Phase | Tasks | Parallelism | Depends on |
|-------|-------|-------------|------------|
| 0 | 0.x (28 tasks) | 28 parallel | -- |
| 1 | 1.1-1.3 then 1.4-1.6 | 3+3 | Phase 0 |
| 2 | 2.1-2.3 then 2.4-2.5 | 3+2 | Phase 1 |
| 3 | 3.1-3.4 then 3.5-3.6 then 3.7 | 4+2+1 | Phase 2 |
| 4 | 4.1-4.3 then 4.4 | 3+1 | Phase 3 |
| 7 | 7.1-7.4 (NEW) | 4 parallel | Phase 2 |
| 8 | 8.1-8.5 (NEW) | 5 parallel | Phase 3 |
| 5 | 5.1-5.2 | sequential | Phases 4, 7, 8 |
| 5.5 | 5.5.1 then 5.5.1b then 5.5.2-5.5.7 then 5.5.8 | 1+1+6+1 | Phase 5 |

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
| Ajello 2014 BL Lac LDDE | WMAP-era (H₀=71, Ω_M=0.27) | None | Small (~1-2% in d_L) |
| Willott 2001 RLF | H0=50, empty universe | η(z) volume correction | Volume corrected; fit shape not re-derived |
| Gruppioni 2013 IR LF | ΛCDM (unspecified) | None | Small |
| Ackermann 2012 L_γ–L_IR | WMAP-era | None | Cosmology enters only through d_L |
| Moliné 2017 boost | Planck 2015 | None | Negligible (N-body; weak dependence) |
| Padmanabhan 2017 HI | Planck 2015-era | None | Weak cosmology dependence |
| **NEW** Cunnington 2025 brightness polynomials | Planck 2018 (native) | None needed | None |
| **NEW** Mangla 2025 MeerKLASS L DR1 | Planck 2018 (native) | None needed | None |
| **NEW** Paul 2025 MeerKLASS UHF DR1 | Planck 2018 (native) | None needed | None |
| **NEW** MeerKLASS 2025 L deepfield | Planck 2018 (native) | None needed | None |
| **NEW** Ammazzalorso 2018b 2MPZ×Fermi | Planck 2015-era | None | Negligible (data-mode forecast input only) |
| **NEW** Ballet 2023 4FGL-DR4 thresholds | Cosmology-independent (flux thresholds) | N/A | None |

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