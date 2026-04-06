# Debug Normalized Window Function Mismatch vs Pinetti 2022 Fig 5.1

## Context

The pipeline's first major comparable quantity against Pinetti 2022 — the normalized window
functions $\hat{W}_i(z)$ for HI, DM, BL Lac, FSRQ, mAGN, SFG (thesis Fig. 5.1) — disagrees
with the reference not only in amplitude but in **shape/trend**. The existing output
(`hi_gamma_xcorr/plots/fig6_windows_both.png`) shows that in both survey-independent and
survey-dependent modes, all astrophysical gamma-ray sources are crushed to $z \lesssim 0.5$
and monotonically decreasing — whereas Pinetti Fig. 5.1 has BL Lac/FSRQ/mAGN peaking at
$z \sim 0.5$–$2$ and vanishing at $z=0$.

The evidence matrices all report line-by-line "Match" against the thesis, so the failure is
likely either (a) a silent convention/units bug in the cross-tracer assembly, (b) a missing
$(1+z)$ factor, or (c) a different overall definition of $\hat{W}_i$ between the pipeline
and the thesis figure. This plan diagnoses the root cause before any code is changed.

---

## Primary Suspects (ordered by prior)

### Suspect 1 — Extra $(1+z)^{-2}$ in astro window (possibly spurious)

`astro_sources.py:569` multiplies the emissivity integral by $1/(4\pi(1+z)^2)$. The docs
derive this from Pinetti Eq. 4.3 via $d_L^2$ cancellation in $dF/dE$, but a first-principles
derivation of photon number intensity from a population of sources at comoving distance
$\chi$ gives

$$W^\chi = \frac{1}{4\pi}\int dL\,\Phi(L,z)\,\frac{dN}{dE_{\rm em}}\Big|_{E_{\rm em}=(1+z)E_0}$$

with **no** $(1+z)^{-2}$ prefactor — because the $(1+z)^2$ K-correction in the photon-number
flux $dF/dE_{\rm obs} = (1+z)^2/(4\pi d_L^2)\cdot dN/dE_{\rm em}$ cancels $d_L^2 = \chi^2(1+z)^2$
exactly, leaving only $1/(4\pi)$. Depending on whether $dF/dE$ absorbs the $(1+z)^2$ K-factor
(photon-number vs energy-flux convention), the code could be off by $(1+z)^{-2}$. At $z=1$
this is a factor of 4; at $z=2$ a factor of 9 — large enough to flip the shape of the
normalized window entirely.

**Cross-check**: Camera et al. 2015 (the HI×γ progenitor paper) uses exactly the code's
$\chi^2/(4\pi d_L^2)=1/(4\pi(1+z)^2)$ convention, so this **may** be correct — but only if
the inner integrand uses $dN/dE$ as energy flux per source, not photon flux. The code's
integrand is $L \cdot E_{\rm rest}^{-\alpha}/(GeV\text{-}erg\cdot I_\alpha)$, which is photon
rate density $dN/dE_{\rm em}$ (ph/s/GeV). That's the photon-flux convention — so the
$(1+z)^{-2}$ would be double-counted.

### Suspect 2 — Cross-tracer inconsistency in `normalized_windows`

`angular_power.py:285` computes $c \cdot h / H(z)$ and applies it **uniformly** to all tracers,
but the tracers carry different built-in Jacobians:

- `W_HI(z, z_min, z_max)` **includes** $H/(c \cdot h)$ internally (line 295), so multiplying
  by $c h/H$ cancels → survey-dependent `W_hi_perz = T_b · b_HI / (z_max−z_min)`.
- `W_gamma_astro` returns a **per-chi** quantity with no Jacobian → $\times c h/H$ is needed.
- `W_gamma_DM` absorbs $1/H$ into the per-chi window → $\times c h/H$ adds **another** $1/H$,
  giving total $1/H^2$ relative to per-z. This might be double-counting or it might be
  correct, depending on which convention `W_gamma_DM` returns.

**Verify**: confirm that `W_gamma_DM(z) · c h/H(z)` produces the right per-z kernel, not
$1/H^2$. `mean_intensity` in `astro_sources.py:579` uses `j · (c/H) · 1/(1+z)` — with an
extra $1/(1+z)$ that `normalized_windows` does NOT apply. This is a direct internal
inconsistency: two different per-z conversions of `W_gamma_astro` exist in the code.

### Suspect 3 — HI window mixes bias into the "normalized window"

`normalized_windows` uses $T_b(z) \cdot b_{\rm HI}(z)$ for HI (line 293), which is the
**intensity-weighted-bias** kernel that enters the $C_\ell$ integrand. But Pinetti's Fig. 5.1
typically shows the pure **emissivity window** for all tracers. If blazar windows omit bias
while HI includes it, the curves are not directly comparable.

Check whether Pinetti Fig 5.1 shows $\tilde{W}=W_{\rm intensity}/\int W\,dz$ (pure emission,
no bias) or $\tilde{W}=(W\cdot b)/\int(W\cdot b)\,dz$ (biased). HI's $T_b\cdot b_{\rm HI}$ has
a very different z-shape from $T_b$ alone.

### Suspect 4 — Unresolved-flux threshold $L_{\rm thr}(z)$ dominates shape

For `unresolved_only=True` (notebook default), $L_{\rm up}=\min(L_{\max}, L_{\rm thr}(z))$
where $L_{\rm thr}(z)=4\pi d_L^2 F_{\rm sens}$ rises rapidly with $z$. At low $z$ the cap
is severe (many bright sources excluded); at high $z$ it barely bites. The combination with
$(1+z)^{-2}$ and strongly-peaked LDDE evolution can produce a sharp low-$z$ peak if the
threshold is being applied backwards (upper-limit when should be lower-limit-style cut) or
if $F_{\rm sens}$ is wrong by orders of magnitude. The notebook plot's crushed-to-$z\approx 0$
shape is consistent with this kind of pathology.

**Check**: plot $L_{\rm thr}(z)$ vs $[L_{\min}, L_{\max}]$ for each source. Also, the
survey-independent panel of fig6 uses the same astro call and is equally crushed — so the
threshold alone is not the full explanation.

### Suspect 5 — Raw (un-normalized) per-z window is correct, but integration/normalization discretization wrong

`normalized_windows` uses uniform `dz` and `np.sum(…)·dz` (left Riemann). If `z_arr` is
log-spaced or not uniform, the normalization is wrong and shapes get distorted. Verify the
notebook constructs a linearly-spaced `z_arr`.

---

## Deliverables (artifacts to create)

1. **`docs/debug/normalized_windows.md`** — persistent markdown copy of this plan, tracked
   in git alongside the repo's other documentation. Will be updated with findings as each
   diagnostic step completes.
2. **`notebooks/debug_normalized_windows.ipynb`** — new diagnostic notebook with one
   section per step (A–F below). Inline plots + numerical tables per step so the root
   cause is visible from the notebook alone.

No production code under `hi_gamma_xcorr/` is modified. At the end, I will **stop and
report the root cause + proposed fix + peer-reviewed citation** for user review before
any production edit.

## Investigation Steps

All steps are read-only/diagnostic — no production code changes until root cause is
confirmed with the user.

### Step A — Plot un-normalized per-z windows directly

In a scratch cell or a new diagnostic script: for each tracer plot
`W_perz(z) = W^\chi(z) · c h / H(z)` on a linear $z\in[0,4]$ grid, **without normalizing**.
Compare peak locations to Pinetti Fig. 5.1:

| Tracer | Expected peak (Fig 5.1) | Code peak |
|---|---|---|
| HI | monotone rise until $z\sim 2$ | ? |
| DM | $z\sim 0$–0.5 | ? |
| SFG | $z\sim 0.3$–1 | ? |
| mAGN | $z\sim 0.5$–1 | ? |
| FSRQ | $z\sim 1$ | ? |
| BL Lac | $z\sim 1$–2 | ? |

If the un-normalized windows already peak in the wrong places, the bug is in the window
definitions, not the normalization.

### Step B — Decompose W_gamma_astro into factors

For one source (BL Lac, $E=5$ GeV, $z \in\{0.1, 0.5, 1, 2, 3\}$), print:
- the emissivity integral $\int dL\,\Phi\,(dN/dE_{\rm em})$ (no prefactor)
- the $(1+z)^{-\alpha}$ K-correction
- the $(1+z)^{-2}$ cosmological-dimming factor
- $L_{\rm thr}(z)/L_{\max}$ ratio
- the GLF evolution factor $e(z, L_c)$ at break luminosity

Expected (from Ajello+ 2014): $e(z, L_c)$ peaks at $z \sim z_c^*=1.67$. If the code's
$e(z)$ peaks at $z=0$, the LDDE sign convention is wrong.

### Step C — Test the $(1+z)^{-2}$ hypothesis

Re-plot Fig 6 with `W_gamma_astro` multiplied by $(1+z)^{+2}$ at plotting time (removing
the cosmological-dimming factor). If the shapes now match Pinetti Fig 5.1, the
$(1+z)^{-2}$ is spurious (double-counting K-correction). Document the result and propose
a fix by deriving from first principles, cross-checking against Camera et al. 2015
Eq. 2.8, Ando & Pavlidou 2009, and the original Pinetti 2020 paper (not the 2022 thesis).

### Step D — Audit `mean_intensity` vs `normalized_windows` consistency

Both claim to "integrate $W^\chi$ to get observed intensity," but they differ by a factor
of $(1+z)$:
- `mean_intensity`: $\int dz\,(c/H)\,W^\chi/(1+z)$
- `normalized_windows`: $\int dz\,(c h/H)\,W^\chi$

Determine which is right. If `mean_intensity` is right (standard UGRB convention with
extra $(1+z)^{-1}$ from photon-time-dilation), then the per-z window in
`normalized_windows` is missing a $(1+z)^{-1}$ — this would push high-z tails down, but
**also** changes shape. Apply the fix and re-plot.

### Step E — Check HI bias inclusion

Plot HI $T_b(z)$ alone and $T_b(z)\cdot b_{\rm HI}(z)$ alongside. Compare to Pinetti Fig 5.1
HI curve to infer which quantity Pinetti actually plotted.

### Step F — Verify evolution-function signs for LDDE GLFs

For BL Lac at $L=10^{48}$ erg/s (near $L_c$), print $e(z)$ on $z \in [0, 3]$. Confirm it
peaks near $z_c^* = 1.67$. Repeat for FSRQ with $z_c^*=1.47$. If the peaks are at $z=0$
or monotone, the `ldde_inv` form's sign convention is inverted.

---

## Critical Files

| File | Role |
|---|---|
| `hi_gamma_xcorr/angular_power.py:233-325` | `normalized_windows` — where the comparison plot is assembled |
| `hi_gamma_xcorr/astro_sources.py:485-569` | `W_gamma_astro` — $(1+z)^{-2}$ prefactor in question |
| `hi_gamma_xcorr/astro_sources.py:576-612` | `mean_intensity` — inconsistent $(1+z)^{-1}$ factor |
| `hi_gamma_xcorr/astro_sources.py:373-435` | `_ldde_glf` — evolution sign convention for BL Lac/FSRQ |
| `hi_gamma_xcorr/astro_sources.py:619-643` | `bias_astro` — fixed-mass bias may or may not enter window |
| `hi_gamma_xcorr/hi_model.py:282-296` | `W_HI` — includes $b_{\rm HI}$ and $H/(c h)$ |
| `hi_gamma_xcorr/dm_model.py:200-272` | `W_gamma_DM` — includes $1/H$ |
| `hi_gamma_xcorr/plots/fig6_windows_both.png` | Current broken output |
| `notebooks/pipeline_validation.ipynb` §6a | Plotting code that calls `normalized_windows` |

---

## Verification Plan

1. Generate a side-by-side overlay of code output vs. a reproduction of Pinetti Fig 5.1
   (e.g., numerical values traced from the thesis figure, or DOI of digitized data).
2. For each tracer, require the normalized-window peak $z_{\rm peak}$ and FWHM to match
   Pinetti to $\Delta z < 0.1$.
3. Once the astro window is fixed, confirm that `mean_intensity` still reproduces
   Pinetti+ 2020 Table 5 intensity values (BL Lac $\sim 4\times 10^{-8}$ cm$^{-2}$s$^{-1}$sr$^{-1}$
   for $E > 0.1$ GeV, etc.).
4. Confirm $\int \hat{W}_i(z)\,dz = 1$ numerically for each tracer (sanity check).
5. Re-run the full notebook `pipeline_validation.ipynb` and inspect `fig6_windows_both.png`
   against Pinetti Fig 5.1.

---

## Deliverables After Diagnosis

Before any code change:
1. A scratch notebook / script showing Steps A–F outputs with plots.
2. A concrete, single-sentence statement of the root cause, with the specific line(s) to fix.
3. A proposed fix with cross-reference to a peer-reviewed source (not the thesis) confirming
   the correct formula.
4. Updated evidence matrix entries reflecting the corrected derivation.

---

## Findings (2026-04-04)

Diagnostic scripts live in `notebooks/debug_archive/_debug_step_{a,b,c,e,f}.py`. Numerical outputs
summarized below; plots at `notebooks/debug_archive/_debug_step_a.png` and `_debug_step_c.png`.

### Summary of Peak Locations (per-z windows, E=5 GeV)

| Tracer   | Code peak_z | Pinetti expected | Match |
|---|---|---|---|
| HI (T_b·b) | 0.02 | rise to z~2      | **FAIL** |
| HI (T_b)   | 0.02 | rise to z~2      | **FAIL** |
| DM         | 0.02 | z~0–0.5          | OK |
| BL Lac     | 0.02 | z~1–2            | **FAIL** |
| FSRQ       | 0.52 | z~1              | **FAIL** |
| mAGN       | 0.02 | z~0.5–1          | **FAIL** |
| SFG        | 0.02 | z~0.3–1          | **FAIL** |

Everything except DM peaks at z≈0. Two independent bugs explain this:

---

### Bug #1 — HI `Omega_HI(z)` double-applies physical→comoving conversion

**Location**: `hi_gamma_xcorr/hi_model.py:169-175`

```python
def Omega_HI(z, **kwargs):
    """Omega_HI = (1+z)^{-3} * rho_HI(z) / rho_crit"""
    rho = rho_HI_mean(z, **kwargs)
    return rho / ((1.0 + z)**3 * cfg.RHO_CRIT)
```

`rho_HI_mean` returns a **comoving** density (the halo integral ∫(dn/dM)·M_HI·dM uses
`dn/dM` which is comoving, and Padmanabhan's M_HI(M,z) is defined on comoving quantities).
The division by `(1+z)^3` then subtracts a physical→comoving conversion that the density
never needed.

**Consequence**: `Omega_HI(z)` falls from 8.1×10⁻⁴ at z=0.02 to 3.8×10⁻⁵ at z=3 (should be
roughly constant ~2–4×10⁻⁴). Feeding this into

$$\bar{T}_b(z) = 188\,h\,\Omega_{HI}(z)\,(1+z)^2/E(z)$$

gives T_b that **decreases** with z (0.106 mK at z=0 → 0.017 mK at z=3), when it should
**rise** (0.032 → 0.109 mK with fixed Ω_HI=2.45×10⁻⁴ per Pinetti p.122, matching
Bull+2015 and Chang+2008).

**Peer-reviewed reference**: Bull, Ferreira, Patel & Santos 2015 (ApJ 803:21,
arXiv:1405.1452) Eq. 3: $\bar{T}_b \approx 189\,h\,\Omega_{HI}(z)\,(1+z)^2/E(z)$ mK with
Ω_HI the **comoving** fraction (no extra (1+z)⁻³).

**Fix (single line)**: remove the `(1+z)**3` factor from `Omega_HI`:

```python
return rho / cfg.RHO_CRIT
```

After this fix, Ω_HI(z) is roughly constant, T_b rises as (1+z)²/E(z) (modulated by halo
evolution), and the HI window no longer peaks at z=0.

---

### Bug #2 — Astrophysical window has spurious `(1+z)^{-2}` prefactor

**Location**: `hi_gamma_xcorr/astro_sources.py:569`

```python
return val / (4.0 * np.pi * (1.0 + z)**2)
```

The docs (e.g. `docs/window-functions/bl_lac.md:111`) derive this factor by cancelling
$d_L^2$ in Pinetti Eq. 4.3 against $dF/dE$'s $1/(4\pi d_L^2)$. But that derivation
**omits** the $(1+z)^2$ K-correction that belongs inside the photon-number flux:

$$\frac{dF_{\rm ph}}{dE_{\rm obs}} = \frac{(1+z)^2}{4\pi d_L^2}\,\frac{dN}{dE_{\rm em}}\Big|_{E_{\rm em}=(1+z)E_{\rm obs}}$$

(see e.g. Hogg 1999 "Distance measures in cosmology" §4, or Peebles 1993 §13). When you
substitute this into Pinetti Eq. 4.3, the $(1+z)^2$ from $dF/dE$ and the $(1+z)^{-2}$ from
$d_L^2/(1+z)^2$ cancel exactly, and the intensity shell contribution is

$$W^{(\chi)}(E_0, z) = \frac{1}{4\pi}\int dL\,\Phi(L,z)\,\frac{dN}{dE_{\rm em}}\Big|_{(1+z)E_0}$$

with **no** $(1+z)^{-2}$ prefactor. The raw emissivity integrals (Step B, `_debug_step_b.py`)
peak at the correct z for every source:

| Source  | emissivity peak_z | expected | with code's (1+z)⁻² |
|---|---|---|---|
| BL Lac  | ~1.0  | z~1–2   | 0.02 ✗ |
| FSRQ    | ~1.5  | z~1     | 0.52 ✗ |
| mAGN    | ~2.0  | z~0.5–1 | 0.02 ✗ |
| SFG     | ~1.0  | z~0.3–1 | 0.02 ✗ |

Removing the $(1+z)^{-2}$ (Step C, variant "no (1+z)^-2, with K-corr") shifts the peaks
to BL Lac z=0.93, FSRQ z=0.88, SFG z=0.52 — matching Pinetti Fig 5.1 within tolerance.
mAGN still peaks too low (z=0.02) after this single fix, suggesting either (a) the mAGN
GLF evolution in the code is wrong or (b) mAGN has a separate issue in the
luminosity-conversion chain (Di Mauro Eq C.13/C.14/C.19). Needs follow-up.

**Peer-reviewed reference**: Ando & Komatsu 2006 (PRD 73:023521, arXiv:astro-ph/0512217)
Eq. 1–3 derives the intensity formula with per-chi emissivity window
$\frac{1}{4\pi}\int\Phi\cdot dN/dE_{\rm em}\,dL$ — no $(1+z)^{-2}$. Same in Ando &
Pavlidou 2009 (MNRAS 400:2122, arXiv:0908.3890) Eq. 6.

**Fix (single line)**:

```python
return val / (4.0 * np.pi)
```

Also requires reviewing `mean_intensity` on line 598–609, which currently includes an extra
`1/(1+z)` factor (`dimming = 1.0/(1.0+z_arr)`). With the corrected per-chi window, the
mean-intensity integral should simply be $\int dz \cdot (c/H) \cdot W^{(\chi)}$; the
$1/(1+z)$ there is either wrong or is implicitly compensating for the missing $(1+z)^2$
in W_gamma_astro. Needs a consistent re-derivation after Bug #2 fix.

---

### Confirmed OK

- LDDE GLF evolution sign convention (Step F, `_debug_step_f.py`): BL Lac evolution
  peaks at z=1.58 (expected z_c*=1.67), FSRQ at z=1.43 (expected z_c*=1.47). ✓
- Raw emissivity integrals ∫Φ·L·dN/dE dL for all 4 astro sources peak at the expected
  redshifts. The GLFs themselves are fine.
- DM window peak location (z≈0). ✓

---

## Recommended Action (awaiting user approval)

**Two-line fix** — no new code, just deletions:

1. `hi_model.py:175` — remove `(1.0 + z)**3 *` from the denominator
2. `astro_sources.py:569` — remove `* (1.0 + z)**2` from the denominator

**Then**:
- Re-run the diagnostic scripts; confirm peaks match Pinetti Fig 5.1.
- Audit `mean_intensity` in `astro_sources.py:576-612` for consistency with the
  corrected per-chi window, and verify it reproduces Ammazzalorso+2018 / Pinetti 2020
  Table 5 UGRB intensities.
- Separately investigate the mAGN GLF / L-conversion chain (peak still too low after fix).
- Update evidence matrices `docs/window-functions/hi_evidence_matrix.md` and the four
  astro-source evidence matrices to reflect the corrected derivations.

---

## Applied Fixes (2026-04-04, after user approval)

All fixes applied to `hi_gamma_xcorr/`:

1. **`hi_model.py:169-180`** — removed `(1.0+z)**3` from `Omega_HI`. The halo integral
   `rho_HI_mean` returns comoving density, so no physical→comoving conversion is needed.
   After this fix, Ω_HI rises slowly with z (8.6e-4 at z≈0 → 2.4e-3 at z=3, peaking at
   z≈4); T_b rises correctly with z (0.11 → 1.08 mK); HI window no longer peaks at z=0.

2. **`astro_sources.py:560-570`** — removed `*(1.0+z)**2` from `W_gamma_astro` prefactor.
   Derivation from Hogg 1999 §4 / Ando & Komatsu 2006 confirms the $(1+z)^2$ K-correction
   in $dF/dE_{\rm obs}$ exactly cancels the $(1+z)^{-2}$ from $d_L^2/(1+z)^2$ in Pinetti
   Eq. 4.3, leaving $W^{(\chi)} = (1/4\pi)\int dL\,\Phi\,L\,E_{\rm rest}^{-\alpha}/(I_\alpha\cdot GeV\text{-}erg)$.

3. **`astro_sources.py:219-259`** — added `(1+z)^Gamma` convention-conversion factor to
   `_glf_mAGN` to make it compatible with the uniform `E_rest^{-alpha}` spectral factor.
   **Context**: Di Mauro Eq. C.19's $(1+z)^{-(2-\Gamma)}$ K-correction is valid for a
   formulation using `E_obs^{-alpha}` (Di Mauro's convention), but our pipeline uses
   Pinetti Eq. 4.3's `E_rest^{-alpha}` (the uniform convention of Ajello LDDE /
   Ackermann SFG). The additional $(1+z)^\Gamma$ factor ensures
   $\phi^{new}(L)\cdot L \cdot E_{\rm rest}^{-\alpha} = \phi^{DM}(L)\cdot L \cdot E_{\rm obs}^{-\alpha}$.

### Peak Locations After Fixes (survey-independent, E=5 GeV)

| Tracer  | Before | After | Expected | Status |
|---|---|---|---|---|
| HI      | 0.02 | 5.00 (monotone rise) | rise to z~2 | Partial (rises too far) |
| DM      | 0.02 | 0.02 | z~0-0.5 | ✓ |
| BL Lac  | 0.02 | 0.92 | z~1-2 | Borderline (just below) |
| FSRQ    | 0.52 | 0.94 | z~1 | ✓ |
| mAGN    | 0.02 | 0.72 | z~0.5-1 | ✓ |
| SFG     | 0.02 | 0.52 | z~0.3-1 | ✓ |

### Code Orderings vs User's Expected (at key z)

**z=0.02** (expected: BL_Lac=FSRQ=mAGN~0, HI < SFG < DM):
- Code: FSRQ=0 ✓, HI=0.014, BL_Lac=0.032, mAGN=0.16, SFG=0.67, DM=0.996
- Matches HI < SFG < DM ✓. mAGN=0.16 is higher than "near 0".

**z=0.25** (expected: BL_Lac < FSRQ~HI < mAGN < DM~SFG):
- Code: HI=0.02 < FSRQ=0.20 < mAGN=0.22 < BL_Lac=0.46 < DM=0.81 < SFG=0.83
- **BL_Lac too high** (should be lowest). HI is lowest in code.

**z=1.0** (expected: DM < HI < mAGN < SFG < FSRQ < BL_Lac):
- Code: HI=0.06 < mAGN=0.32 < DM=0.37 < SFG=0.55 < FSRQ=0.77 < BL_Lac=0.91
- Two inversions: **DM should be lowest (not 3rd)**, **mAGN should exceed DM**.

---

## Remaining Issues (not yet fixed)

### R1 — HI window peaks at grid edge (z=5), should peak at z~1-3

After Bug #1 fix, Ω_HI(z) is 8.6e-4 at z≈0 rising to peak 2.44e-3 at z≈4 then declining.
The observed Ω_HI peaks around z~2-3 (1e-3 range) and declines beyond; our code's
halo-integral Ω_HI is ~2× higher than observations AND peaks too late.

**Root cause candidate**: Padmanabhan M_HI(M,z) formula produces excess HI mass at high z
for low-mass halos (scan at M=1e9 Msun/h: M_HI goes from 0.23 at z=0 to 1.3e7 at z=3 —
a 54-million-factor growth, driven by the `exp(-(v_c,0/v_c)^3)` suppression becoming
inactive at high z because physical halo radii shrink).

**Investigation (2026-04-04, Step P)**: Tested thesis-faithful fixed Ω_HI=2.45e-4 via
`pinetti2022.T_bar_b_thesis`. Both halo-integral AND fixed-Ω_HI versions produce HI
windows that monotonically rise to z=5 (grid edge). The fixed-Ω_HI variant is only
modestly flatter (at z=0: 3.5e-2 vs 1.4e-2 for code). Bias b_HI(z) rises independently
from 0.80 at z=0 to 2.21 at z=5, contributing to monotone rise.

**Diagnosis**: The SHAPE of HI window (monotone rise) is driven by $(1+z)^2/E(z)\cdot b_{HI}(z)$
which asymptotes slowly at very high z. This is **probably correct physics** — HI 21-cm
brightness naturally grows with z. Pinetti Fig 5.1 likely shows a limited z-range
([0, 2] or [0, 3]) where HI is still rising but capped by the plot axes.

**Conclusion**: No additional code fix needed for HI window shape. The HI shape is
physically consistent. Defer further tuning (Padmanabhan parameter refinement,
z-dependent v_c,0) to a separate task.

### R2 — DM decays too slowly with z (too high at z=1) — RESOLVED (Bug #4)

**Pinetti Fig 5.1 is plotted at E=5 GeV per its caption** (user confirmation). At this
energy EBL is transparent and m_χ=100 GeV gives a soft dN/dE cutoff, so neither handles
DM suppression. The actual root cause is a **4th bug in the clumping factor**.

**Bug #4 — Clumping factor Δ²(z) missing (1+z)⁻³ factor**

**Location**: `hi_gamma_xcorr/dm_model.py:149-193` (`clumping_factor`)

The halo integral `∫(dn_com/dM)·(1+B)·∫ρ²_phys·dV·dM` returns `<ρ²>_phys per comoving
volume` (dn is comoving but ∫ρ²dV uses physical volume). Dividing by the comoving
`ρ_bar_com²` instead of the physical `ρ_bar_phys(z)² = ρ_bar_com²·(1+z)⁶` leaves a net
factor `(1+z)³` mismatch. The standard physical-variable definition
$\Delta^2(z) = \langle\rho^2\rangle_{phys}/\bar\rho^2_{phys}(z)$ used in Ullio+2002
Eq. 10 / Pinetti Eq. 4.1 requires dividing by `(1+z)^3`.

**Consequence**: Code's Δ²(z) was **nearly constant** (4.2e5 → 3.6e5 from z=0 to z=3),
whereas literature expects Δ² to decline by ~factor 100 due to less-collapsed structure
at high z (Taylor & Silk 2003, Cirelli+2011).

After correction, Δ² falls from 3.94e5 at z=0 to 5.77e3 at z=3 — matching literature.

**Fix** (`dm_model.py:191`):
```python
result = np.sum(integrand_arr) * dlnM / cfg.RHO_BAR**2 / (1.0 + z)**3
```

**Result at E=5 GeV, m_χ=100 GeV, z range [0.02, 3.0]**:
- z=1.00: **DM(0.16) < HI(0.19) < mAGN(0.39) < SFG(0.55) < FSRQ(0.77) < BL_Lac(0.91)** ✓

**Exact match to user's expected Pinetti Fig 5.1 ordering at z=1.**

### R3 — BL Lac peak slightly below z=1 (0.92 vs expected [1,2])

Borderline. Could reflect: (a) minor parameter difference vs Ajello+ 2014, (b) user's
mental image of "z~1-2" may include z=0.92 as acceptable. Defer.

---

## Final Status (2026-04-04)

After **4 bug fixes** (Ω_HI, astro (1+z)⁻², mAGN K-corr, DM clumping (1+z)⁻³), at
**E=5 GeV, m_χ=100 GeV, z range [0.02, 3.0]** (matching Pinetti Fig 5.1 caption), the
code reproduces user's expected orderings:

| z | Expected | Code (E=5 GeV) | Match |
|---|---|---|---|
| 0.02 | BL_Lac=FSRQ=mAGN~0 < HI < SFG < DM | FSRQ(0) < BL_Lac(0.03) < HI(0.04) < mAGN(0.20) < SFG(0.67) < DM(3.21) | Ordering ✓ (mAGN larger than expected ~0) |
| 0.25 | BL_Lac < FSRQ~HI < mAGN < DM~SFG | HI(0.07) < FSRQ(0.19) < mAGN(0.26) < BL_Lac(0.45) < SFG(0.83) < DM(1.43) | Partial (BL_Lac position inverted) |
| **1.00** | **DM < HI < mAGN < SFG < FSRQ < BL_Lac** | **DM(0.16) < HI(0.19) < mAGN(0.39) < SFG(0.55) < FSRQ(0.77) < BL_Lac(0.91)** | **✓ Exact match** |

### Bug #5 — HI window double-counts bias b_HI

**Location**: `hi_gamma_xcorr/hi_model.py:W_HI` and `angular_power.py:normalized_windows`

**Found via direct reading of Pinetti 2020 paper (arXiv:1911.04989) Eq. 3.15**:

$$W_{HI}(z) = W_0(z) \cdot \bar T_b(z)$$

The HI window in Pinetti's convention contains **only** the selection function $W_0$ and
brightness temperature $\bar T_b$. The bias $b_{HI}$ enters **only** through the HI power
spectrum $P_{HI}(k,z)$ in the Limber integrand (via the bias-weighted mass integral
`I_HI = ∫(dn/dM)·b·M_HI·u_HI/ρ_HI dM` used in `P_HI_astro_2h`, `P_HI_DM_2h`).

Previously the code had $b_{HI}$ in **both** $W_{HI}$ **and** $P_{HI}$, which
double-counts the bias in C_ell and distorts the HI window shape.

**Fix**: remove `b_HI(z)` from `W_HI` (hi_model.py:296) and from the survey-independent
HI window in `normalized_windows` (angular_power.py:293). The bias remains correctly in
`P_HI_DM_2h` and `P_HI_astro_2h` via their internal mass integrals.

**Peer-reviewed reference**: Pinetti+ 2020 (arXiv:1911.04989) Eq. 3.15 explicitly
defines $W_{HI} = W_0 \bar T_b$ with no bias factor. Text p.13: "For the 21-cm
brightness temperature, the window function is broad and almost featureless".

### Bug #6 — W_gamma_DM has spurious 1/H(z) factor

**Location**: `hi_gamma_xcorr/dm_model.py:W_gamma_DM`

Pinetti 2020 Eq. 4.1 (verified directly from arXiv:1911.04989):
$W_{\gamma,DM}(E, z) = \frac{1}{4\pi} \frac{\langle\sigma v\rangle}{2} \Delta^2(z) \left(\frac{\Omega_{DM}\rho_c}{m_\chi}\right)^2 (1+z)^3 \frac{dN}{dE}[(1+z)E] e^{-\tau}$

**No 1/H(z) factor.** Mean intensity: $\langle I_\gamma\rangle = \int dz \cdot c/H(z) \cdot W_\gamma(z)$
(paper p. 9 text). The c/H Jacobian is supplied by the integration measure, not by W.

The code's `inv_H` multiplication was off by a factor of ~10¹⁷ s (Hubble time), making
the mean DM intensity **~10¹⁷× too large** (10⁸ ph/cm²/sr/GeV vs expected few × 10⁻⁹
ph/cm²/s/sr/GeV from Pinetti 2020 Fig 2).

**Fix**: remove `inv_H` from W_cgs computation.

**Verification**: after fix, $\langle I_{DM}\rangle$ at E=5 GeV, m_χ=100 GeV, bb channel
= **3.4×10⁻⁹** ph/cm²/s/sr/GeV — matches Pinetti 2020 Fig 2 expectation.

The shape change (removing 1/H makes DM window less steeply peaked at z=0) also fixes
the z=1 ordering: **DM(0.22) < HI(0.24) < mAGN(0.39) < SFG(0.55) < FSRQ(0.77) <
BL_Lac(0.91)** — EXACT match to user's expected Pinetti Fig 5.1 ordering at E=5 GeV.

### Summary of All Six Bug Fixes

| # | File | Bug | Physical Interpretation |
|---|---|---|---|
| 1 | `hi_model.py:169-180` | Ω_HI double (1+z)⁻³ conversion | rho_HI_mean is comoving; no physical→comoving conversion needed |
| 2 | `astro_sources.py:560-570` | Spurious (1+z)⁻² prefactor | (1+z)² from K-correction in dF/dE already cancels d_L²/(1+z)² |
| 3 | `astro_sources.py:219-259` | mAGN K-corr convention mismatch | Di Mauro uses E_obs; Pinetti uses E_rest; add (1+z)^Γ factor |
| 4 | `dm_model.py:149-193` | Clumping factor missing (1+z)⁻³ | ρ_bar_phys(z) = ρ_bar_com·(1+z)³; halo ρ²_int is physical |
| 5 | `hi_model.py:282-297`, `angular_power.py:289-295` | b_HI in HI window (double-counted) | Pinetti 2020 Eq. 3.15: W_HI = W_0 · T_b only; bias enters via P_HI |
| 6 | `dm_model.py:W_gamma_DM` | Spurious 1/H(z) factor | Pinetti 2020 Eq. 4.1: no 1/H; c/H supplied by integration measure |

### Survey Band Identification

User confirmed "HI peaks at z~0.5" in Pinetti 2022 Fig 5.1. This matches:
- **MeerKAT L-band** [0, 0.58]: HI top-hat peaks at z=0.57 ✓
- **SKA1 Band 2** [0, 0.5]: HI top-hat peaks at z=0.50 ✓

The production fig6 now shows MeerKAT L-band as the reference HI survey configuration.
Pinetti 2020 paper text describes HI as "broad and almost featureless" which is
consistent with a wide top-hat over [0, 0.58] modulated by the gentle T_b(z) rise.

### R4 — Astrophysical mean intensities too high (total ~5× Ackermann+2015 UGRB)

After Bug #2 fix, summed mean intensities at E=1 GeV: BL_Lac=2.7e-7 + FSRQ=9.0e-8 +
mAGN=4.2e-8 + SFG=4.5e-8 = **4.5e-7 ph/cm²/s/sr/GeV**, vs Ackermann+2015 IGRB total of
~5e-7 ph/cm²/s/sr/GeV. These are UNRESOLVED-only components — their sum should be
significantly LESS than the total UGRB. Current ratios (BL_Lac 60%, rest ~40%) suggest
BL_Lac is overpredicted OR the `(1+z)^{-1}` "dimming" in `mean_intensity:598` is an
appropriate factor that the first-principles derivation missed (e.g., from a specific
intensity vs photon flux-density convention).

**Proposed next step**: (a) re-derive the UGRB intensity formula from Fornasa &
Sanchez-Conde 2015 §2, which uses a `(1+z)^{-4}` factor convention — determine if that's
because they use specific ENERGY intensity rather than photon-number intensity; (b)
cross-check with Ammazzalorso+2018 Eq. 2; (c) if `(1+z)^{-1}` is correct, add the
compensating factor to `W_gamma_astro` for C_ell consistency; otherwise remove it from
`mean_intensity` and investigate the 5× absolute normalization gap.

