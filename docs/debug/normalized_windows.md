# Debug Normalized Window Functions

## Purpose

This note tracks the current implementation conventions behind
`angular_power.normalized_windows()` and records the checks needed when
comparing the repository output to Pinetti (2022) Fig. 5.1.

It intentionally reflects the **present** pipeline state in `hi_gamma_xcorr`.
Older versions of this file assumed an extra astro `(1+z)^{-2}` prefactor, an
HI window that included `b_HI`, and a DM window that already absorbed `1/H(z)`.
Those assumptions are obsolete and are not used by the current code.

---

## Current Code State

### Shared conversion used by `normalized_windows`

`normalized_windows()` constructs per-redshift kernels from per-comoving-distance
windows via

$$W^{(z)}(z) = W^{(\chi)}(z)\,\frac{d\chi}{dz}
= W^{(\chi)}(z)\,\frac{c\,h}{H(z)}.$$

This conversion is implemented once in
`hi_gamma_xcorr/angular_power.py::normalized_windows`.

### HI convention

- Survey-independent HI uses `T_bar_b(z)` directly.
- Survey-dependent HI uses `hi_model.W_HI(z, z_min, z_max)`.
- `W_HI` is defined as

$$W_{\rm HI}^{(\chi)}(z) = \bar{T}_b(z)\,\phi(z)\,\frac{H(z)}{c\,h},$$

with no `b_HI` inside the window.
- Multiplying by `c h / H` therefore cancels the built-in Jacobian and recovers
  the per-z top-hat kernel `T_bar_b(z) * phi(z)`.

This matches the current `hi_gamma_xcorr/hi_model.py::W_HI` docstring and the
current `normalized_windows()` comments.

### Astrophysical-source convention

`astro_sources.W_gamma_astro()` returns a per-chi photon-intensity window in the
pipeline's h-dependent comoving units:

$$W_\gamma^{(\chi)}(E,z)
= \frac{1}{4\pi\,h^3}\int dL\;\Phi(L,z)\,\frac{dN}{dE_{\rm em}}\Big|_{E_{\rm em}=(1+z)E}.$$

Current implementation details:

- The observed/rest-frame energy shift enters through `E_rest = (1+z) E_obs`.
- There is **no explicit extra** `(1+z)^{-2}` prefactor in `W_gamma_astro()`.
- The luminosity-function integral is first evaluated in physical `Mpc^-3`, then
  converted to `[(Mpc/h)^-3]` via the final `h^-3` factor.
- `normalized_windows()` converts this per-chi window to a per-z kernel by
  multiplying by `c h / H(z)`.

`mean_intensity()` follows the same convention:

$$\langle I_\gamma(E)\rangle = \int dz\;\frac{c\,h}{H(z)}\;W_\gamma^{(\chi)}(E,z),$$

with no extra `1/(1+z)` factor.

### DM convention

`dm_model.W_gamma_DM()` is also a per-chi window. The current code explicitly
states that it has **no baked-in `1/H(z)` factor**:

$$W_{\gamma,{\rm DM}}^{(\chi)}(E,z)
= \frac{1}{4\pi}\frac{\langle\sigma v\rangle}{2}
\left(\frac{\Omega_{\rm DM}\rho_c}{m_\chi}\right)^2
(1+z)^3\,\Delta^2(z)\,
\frac{dN}{dE'}\Big|_{E'=(1+z)E} e^{-\tau(E,z)}.$$

`normalized_windows()` therefore treats DM the same way as the other per-chi
windows and multiplies it by `c h / H(z)` to obtain the per-z kernel used for
normalization.

---

## Practical Implications For Fig. 5.1 Comparisons

When the repository plots normalized windows today:

- HI is normalized from `T_bar_b(z)` or from `W_HI * c h / H`, with no HI bias
  inside the window itself.
- BL Lac, FSRQ, mAGN, and SFG are normalized from
  `W_gamma_astro(E,z) * c h / H`.
- DM is normalized from `W_gamma_DM(E,z) * c h / H`.

So the old failure modes to keep **off** the table are:

- "astro windows are low-z because the code still multiplies by `(1+z)^{-2}`"
- "HI is being reshaped by a built-in `b_HI` factor"
- "DM gets an extra `1/H` because the window already contains one"
- "`mean_intensity()` uses a different Jacobian convention than
  `normalized_windows()`"

Those are not true for the current pipeline.

---

## Recommended Current Investigation

If the normalized windows still disagree with Pinetti Fig. 5.1, the remaining
checks should focus on choices that are still live:

1. Compare survey-independent and unresolved-only astro windows separately.
   `L_up = min(L_max, L_sens(z))` can still strongly reshape low-z behavior.

2. Check source-model assumptions rather than Jacobian conventions.
   The dominant candidates are LDDE/GLF parameter choices, source-class
   luminosity bounds, and the specific unresolved-threshold prescription.

3. Confirm the plotting grid and normalization measure.
   `normalized_windows()` assumes a uniformly spaced `z_arr` and normalizes with
   `sum(W(z)) * dz`.

4. Compare like with like against the reference figure.
   The survey-independent HI branch uses `T_bar_b(z)`, while the survey-dependent
   branch uses the top-hat-selected `W_HI`; make sure the figure being compared
   uses the corresponding convention.

---

## Code Map

- `hi_gamma_xcorr/angular_power.py::normalized_windows`
- `hi_gamma_xcorr/hi_model.py::W_HI`
- `hi_gamma_xcorr/hi_model.py::T_bar_b`
- `hi_gamma_xcorr/astro_sources.py::W_gamma_astro`
- `hi_gamma_xcorr/astro_sources.py::mean_intensity`
- `hi_gamma_xcorr/dm_model.py::W_gamma_DM`

---

## Status

This debug note is aligned with the current implementation. It is a starting
point for future comparisons against external figures, not a record of the old
superseded window-convention bugs.
