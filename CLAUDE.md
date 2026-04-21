# CLAUDE.md

## Documentation Tier Authority

Correctness flows **top-down** — when a discrepancy is found, fix the lower-tier artifact:

```
Tier 0  papers/*.pdf          — sole source of truth (never edit)
Tier 1  literature/*.md       — faithful summaries of Tier 0
Tier 2  equations.md          — equation catalog + deviation definitions
        conventions.md        — units, frames, deviation registry
Tier 3  hi_gamma_xcorr/*.py   — implementation (realises Tiers 1–2)
Tier 4  architecture.md       — descriptive; regenerated to match Tier 3
Tier 5  window-functions/*.md — audit docs; verify Tier 3 vs Tiers 1–2
Tier 6  literature_evidence_matrix.md — master audit of all Tier 1
```

Code-location metadata in Tier 2 (function names, line refs) is **descriptive**, not authoritative — update it after code changes, not before.

## Unit Convention

All internal calculations use **h-dependent comoving units**: distances Mpc/h, masses M☉/h, wavenumbers h/Mpc, power spectra (Mpc/h)³. Physical units (CGS, mK, GeV) appear only at module boundaries with explicit conversion.

## Deviation Registry

Active deviations (D2, D4–D8, D12, D14–D17) are documented in `docs/conventions.md` §7 and `docs/equations.md`. Resolved deviations (D3, D9, D11, D13) must not appear as active. Any new deliberate deviation from literature must be assigned a Dx number and recorded in both files before merging.

## Audit Plan

Full audit plan (Phases 0–8 + Physics Tasks 6.1–6.6): `docs/audit_plan.md`
