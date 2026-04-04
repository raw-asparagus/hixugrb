# DM Annihilation Window Function: Complete Pipeline

## Target Quantity

The DM annihilation window function enters the Limber integral for the angular cross-power spectrum (Pinetti+ 2020, Eq. 2.1):

$$C_\ell^{ij} = \int \frac{d\chi}{\chi^2}\, W_{\rm HI}(\chi)\, W_\gamma^{\rm DM}(\chi)\, P_{\rm HI \times DM}\!\left(k = \frac{\ell+1/2}{\chi},\, z\right)$$

The DM window function itself (Pinetti+ 2020 Eq. 4.1, thesis Eq. 4.1) in per-$\chi$ convention is:

$$W_\gamma^{\rm DM}(\chi) = \frac{\langle\sigma v\rangle}{8\pi}\left(\frac{\rho_{\rm DM}}{m_\chi}\right)^2 (1+z)^3 \frac{\Delta^2(z)}{H(z)} \frac{dN}{dE'}\bigg|_{E'=(1+z)E_\gamma}\; e^{-\tau(E_\gamma,z)}$$

This requires six physically non-trivial ingredients: the annihilation cross-section $\langle\sigma v\rangle$, the DM density $\rho_{\rm DM}$ and particle mass $m_\chi$, the clumping factor $\Delta^2(z)$ (which itself depends on the halo mass function, concentration, and substructure boost), the photon yield spectrum $dN/dE$, and the EBL attenuation $e^{-\tau}$.

**Key contrast with HI:** HI traces linear density ($\propto \delta$), while DM annihilation traces density-squared ($\propto \delta^2$). This fundamental difference in redshift weighting enables tomographic separation of DM and astrophysical contributions via cross-correlation.

**Parallel implementation:** `pinetti2022.py` provides thesis-faithful overrides for shared infrastructure (bias with $q=0.75$, thesis Correa coefficients, Limber $k=\ell/\chi$). No DM-specific overrides exist yet — the DM window function formula, boost factor, and clumping factor are identical between both pipelines.

---

## Layer 1: Cosmological Backbone (shared with HI)

**Source:** Planck 2018 (TT,TE,EE+lowE+lensing) parameters. Shared between pipeline and Pinetti 2022 parallel.

| Quantity | Expression | Reference |
|----------|-----------|-----------|
| $E(z)$ | $\sqrt{\Omega_M(1+z)^3 + \Omega_\Lambda}$ | Flat LCDM |
| $H(z)$ | $H_0 E(z)$, with $H_0 = 67.36$ km/s/Mpc | Planck 2018 |
| $\chi(z)$ | $\frac{c}{H_0}\int_0^z \frac{dz'}{E(z')}$ | Standard |
| $\bar\rho_m$ | $\Omega_M \rho_c = 0.3153 \times 2.775\times10^{11}\;h^2\,M_\odot\,\text{Mpc}^{-3}$ | Planck 2018 |
| $P_{\rm lin}(k,z)$ | CAMB Boltzmann solver | Planck 2018 params |
| $\sigma(M,z)$ | $\frac{1}{2\pi^2}\int k^2 P_{\rm lin} W^2(kR)\,dk$, top-hat smoothing | Perturbation theory |

Key parameters: $h=0.6736$, $\Omega_M=0.3153$, $\Omega_B=0.0493$, $\Omega_{\rm DM}=0.2660$, $\sigma_8=0.8111$, $n_s=0.9649$.

**Implementation:** `cosmology.py` (E, H, chi, P_lin, sigma_R), `config.py` (all Planck 2018 constants).

See [HI Window Function: Layer 1](hi.md#layer-1-cosmological-backbone) for full details.

---

## Layer 2: Halo Model Infrastructure (shared with HI)

### 2a. Halo mass function -- Sheth, Mo & Tormen (2001)

$$\nu f(\nu) = A\left[1 + (q\nu)^{-p}\right]\sqrt{\frac{q\nu}{2\pi}}\exp\!\left(-\frac{q\nu}{2}\right)$$

with $A=0.3222$, $q=0.707$, $p=0.3$, and $\nu = \delta_c^2/\sigma^2(M,z)$, $\delta_c=1.686$.

**Implementation:** Delegated to the `hmf` Python package via `hmf_interface.py`.
**Pinetti 2022:** Same $dn/dM$ (hmf backend uses $q=0.707$); $q=0.75$ override enters only via `pinetti2022.bias_pinetti()`.

### 2b. Halo bias -- Sheth & Tormen (1999)

$$b(\nu) = 1 + \frac{q\nu - 1}{\delta_c} + \frac{2p}{\delta_c(1 + (q\nu)^p)}$$

**Implementation:** `halo_model.py:bias(M, z)` (line 110) with $q=0.707$.
**Pinetti 2022:** `pinetti2022.bias_pinetti(M, z)` with $q=0.75$.

### 2c. Virial overdensity -- Bryan & Norman (1998)

$$\Delta_{\rm vir}(z) = 18\pi^2 + 82x - 39x^2, \qquad x = \Omega_M(z) - 1$$

relative to $\rho_c(z)$. At $z=0$ with Planck 2018: $\Delta_{\rm vir} \approx 103$ (relative to critical density), equivalently $\sim 327$ relative to mean matter density.

**Implementation:** `halo_model.py:Delta_vir(z)` (line 23), `halo_model.py:R_vir(M, z)` (line 42). Same in both pipelines.

### 2d. Concentration--mass relation -- Correa et al. (2015)

For $z \le 4$ (Appendix B1, Planck cosmology fit):

$$\log_{10} c_{200} = \alpha + \beta\,\log_{10}(M/M_\odot)\!\left[1 + \gamma\,(\log_{10} M/M_\odot)^2\right]$$

where:
- $\alpha = 1.7543 - 0.2766(1+z) + 0.02039(1+z)^2$
- $\beta = 0.2753 + 0.00351(1+z) - 0.3038(1+z)^{0.0269}$
- $\gamma = -0.01537 + 0.02102(1+z)^{-0.1475}$

**Critical for DM:** Valid down to $\sim 10^{-2}\,M_\odot$, essential for microhalo contributions to the clumping factor.

**Implementation:** `halo_model.py:concentration_correa(M, z)` (line 125). Converts $M_\odot/h \to M_\odot$ via `M * h` (line 138). **Note:** this h-factor conversion is inconsistent with `v_circ` which uses `M / h` -- see evidence matrix for analysis.

**Pinetti 2022:** `pinetti2022.concentration_correa_thesis(M, z)` uses thesis-specific coefficients (Eq. 3.36, p.99) from a different cosmology fit within the same Correa et al. (2015) paper. Same `M * h` conversion.

### DM-specific mass range

Unlike HI (negligible below $\sim 10^8\,M_\odot/h$), DM annihilation extends to the WIMP free-streaming scale. The pipeline uses $M \in [10^{-6},\, 10^{18}]\,M_\odot/h$ for DM integrals (`config.py:M_MIN_DM`, `M_MAX_DM`). Same in both pipelines.

See [HI Window Function: Layer 2](hi.md#layer-2-halo-model-infrastructure) for full details on shared infrastructure.

---

## Layer 3: NFW $\rho^2$ Profile

The DM annihilation rate scales as $\rho^2$, requiring the density-squared profile of NFW halos. Identical between pipeline and Pinetti 2022 parallel (no overrides).

### 3a. NFW scale density

$$\rho_s = \frac{M}{4\pi\, r_s^3\, f(c)}, \qquad f(c) = \ln(1+c) - \frac{c}{1+c}$$

where $r_s = R_{\rm vir}/c$ and $c = c_{200}(M,z)$ from Correa et al. (2015), converted to $c_{\rm vir}$ via `halo_model.c200_to_cvir()`.

**Implementation:** `dm_model.py:_rho_s(M, z)` (line 19). Returns $\rho_s$ in $[M_\odot/h\;({\rm Mpc}/h)^{-3}]$.

### 3b. Analytic $\rho^2$ volume integral (Pinetti Eq. 4.2, inner integral)

**Derivation from first principles:**

$$\int_0^{R_{\rm vir}} 4\pi r^2\, \rho_{\rm NFW}^2(r)\, dr = 4\pi\rho_s^2 r_s^3 \int_0^c \frac{dx}{(1+x)^4} = \frac{4\pi}{3}\, \rho_s^2\, r_s^3 \left[1 - \frac{1}{(1+c)^3}\right]$$

where the substitution $x = r/r_s$ transforms $\rho^2 = \rho_s^2/(x^2(1+x)^4)$ and $r^2\,dr = r_s^3 x^2\,dx$, yielding $\int_0^c (1+x)^{-4}dx = \frac{1}{3}[1 - (1+c)^{-3}]$.

**Implementation:** `dm_model.py:rho2_integral_analytic(M, z)` (line 33). Returns $[(M_\odot/h)^2\,({\rm Mpc}/h)^{-3}]$. **Verified correct.**

### 3c. Fourier transform of $\rho^2$ profile

$$\tilde{v}(k|M) = \frac{4\pi}{\bar\rho_m^2} \int_0^{R_{\rm vir}} r^2\, \rho_{\rm NFW}^2(r)\, \frac{\sin(kr)}{kr}\, dr$$

Normalized so that $\tilde{v}(k\to 0) = \int\rho^2\,d^3x\;/\;\bar\rho_m^2$.

This enters the two-halo cross-power spectrum (Pinetti Eqs. 5.1--5.2), where it is divided by $\Delta^2$ to normalize the DM density-squared field: $\tilde{v}/\Delta^2$ gives each halo's fractional contribution to the mean $\langle\rho^2\rangle$.

**Implementation:** `dm_model.py:v_tilde(k, M, z)` (line 54). Numerical integration via `scipy.quad` with $r_{\rm min} = 10^{-6}\,r_s$. Falls back to the analytic $k\to 0$ limit for $k < 10^{-10}$.

---

## Layer 4: Substructure Boost Factor -- Moline et al. (2017)

Dark matter halos contain subhalos that enhance the local $\rho^2$ and hence the annihilation rate. Identical between pipeline and Pinetti 2022 parallel (no overrides).

### 4a. Boost at $z=0$ (Moline Eq. 18, Table 3, $\alpha=2$, tidal stripping)

$$\log_{10} B(M, z{=}0) = \sum_{i=0}^{5} b_i \left[\log_{10}\!\left(\frac{M}{M_\odot}\right)\right]^i$$

| $i$ | $b_i$ |
|-----|--------|
| 0 | $-0.186$ |
| 1 | $+0.144$ |
| 2 | $-8.8\times10^{-3}$ |
| 3 | $+1.13\times10^{-3}$ |
| 4 | $-3.7\times10^{-5}$ |
| 5 | $-2\times10^{-7}$ |

Valid for $10^{-6} < M\,[M_\odot] < 10^{15}$.

### 4b. Redshift scaling (Moline thesis Eq. 3.48)

$$B(M, z) = \frac{B(M, z{=}0)}{1 + z}$$

### 4c. Boost scenarios

| Scenario | $M_{\rm min,sub}$ | Description |
|----------|-------------------|-------------|
| `none` | -- | $B=0$ (smooth halos only) |
| `conservative` | $10^7\,M_\odot$ | Only massive subhalos |
| `intermediate` | $10^{-6}\,M_\odot$ | Full subhalo hierarchy; **default** |
| `optimistic` | $10^{-6}\,M_\odot$ | **Not yet distinct from intermediate** (same $M_{\rm min,sub}$) |

Application: $\rho^2_{\rm eff} = (1 + B)\;\rho^2_{\rm smooth}$

**Implementation:** `dm_model.py:boost_moline(M, z, M_min_sub)` (line 98). Converts pipeline masses $M_\odot/h \to M_\odot$ via `M * h` (line 115). Clipped to $[0, 1000]$ for numerical safety.

**Parameters:** `config.py:MOLINE_BOOST_COEFFS` (line 121).

---

## Layer 5: Clumping Factor $\Delta^2(z)$ -- Pinetti Eq. 4.2

The clumping factor encodes the mean-square density contrast across all halos:

$$\Delta^2(z) = \frac{1}{\bar\rho_m^2} \int_{M_{\rm min}}^{M_{\rm max}} \frac{dn}{dM}(M,z)\;\left[1 + B(M,z)\right]\;\int_{\rm halo} \rho_{\rm NFW}^2\, d^3x\;\; dM$$

Identical between pipeline and Pinetti 2022 parallel (concentration differences propagate via shared `halo_model.concentration`, not via explicit Pinetti 2022 override).

### Computational method

1. Set up log-spaced mass grid: $M \in [\max(M_{\rm min}, 10^{-4}),\, \min(M_{\rm max}, 10^{17})]\,M_\odot/h$, 200 points
2. For each mass $M_i$:
   - Evaluate $dn/dM(M_i, z)$ from SMT mass function
   - Compute $\int \rho^2\,d^3x$ analytically (Layer 3b)
   - Compute boost $B(M_i, z)$ from Moline polynomial (Layer 4)
   - Accumulate: $f_i = (dn/dM) \times (1+B) \times (\int\rho^2\,d^3x) \times M$
3. Integrate via rectangle rule on $d\ln M$: $\Delta^2 = \sum_i f_i \times \Delta\ln M \;/\; \bar\rho_m^2$

**Simplification:** The code clamps the mass range to $[10^{-4}, 10^{17}]$ regardless of the config values $[10^{-6}, 10^{18}]$. This truncates 2 decades of microhalo contributions at low mass (few-percent effect on $\Delta^2$).

**Caching:** Results cached by $(\text{round}(z, 4),\; \text{boost\_scenario})$.

**Implementation:** `dm_model.py:clumping_factor(z, boost_scenario)` (line 149).

---

## Layer 6: Photon Yield $dN/dE$ -- PPPC4DMID (Cirelli et al. 2011)

Identical between pipeline and Pinetti 2022 parallel. The thesis used a private Pythia code (unavailable); both pipelines use the public PPPC4DMID tables (percent-level difference, irreducible).

### 6a. Data source

PPPC4DMID tables providing $dN/d(\log_{10} x)$ where $x = E/m_\chi$, for 28 annihilation channels. Mass range: 5 GeV -- 100 TeV.

**File:** `hi_gamma_xcorr/data/pppc4dmid/AtProduction_gammas.dat`

### 6b. Conversion chain

$$\frac{dN}{dx} = \frac{dN}{d(\log_{10}x)} \cdot \frac{1}{x\,\ln 10}, \qquad \frac{dN}{dE} = \frac{dN}{dx} \cdot \frac{1}{m_\chi}$$

### 6c. Energy convention

Evaluated at **rest-frame (emitted) energy**: $E' = (1+z)\,E_\gamma$

### 6d. Interpolation

2D `RectBivariateSpline` in $(\log_{10} m_\chi,\; \log_{10} x)$ space, cubic in both dimensions. Interpolation in $\log_{10}(dN/d\log_{10}x)$ space for accuracy across many orders of magnitude.

**Implementation:** `pppc4dmid.py:dNdE(E_GeV, m_chi_GeV, channel)` (line 226), via `dNdx` (line 183) and `_dNdlog10x_table` (line 111). Analytic fallbacks for `bb`, `tautau`, `WW` when tables unavailable.

---

## Layer 7: EBL Attenuation $e^{-\tau}$ -- Dominguez et al. (2011)

High-energy gamma rays absorbed by pair production on EBL photons: $\gamma_{\rm HE} + \gamma_{\rm EBL} \to e^+e^-$. Identical between pipeline and Pinetti 2022 parallel (no overrides).

### 7a. Key regimes

| Regime | $\tau$ | Effect |
|--------|--------|--------|
| $E < 10$ GeV, any $z < 1$ | $\ll 1$ | Transparent |
| $E \sim 30$ GeV, $z \sim 0.5$ | $\sim 1$ | Onset of absorption |
| $E > 100$ GeV, $z > 0.5$ | $\gg 1$ | Opaque |

### 7b. Energy convention

$\tau(E_\gamma, z)$ is evaluated at the **observed** energy $E_\gamma$ (energy measured at Earth). The `ebltable` package takes energy in TeV internally.

### 7c. Analytic fallback

$$\tau(E,z) \approx 2.5 \left(\frac{E}{100\,{\rm GeV}}\right)^{1.0} \left(\frac{z}{1.0}\right)^{1.3} \times \left[1 + \left(\frac{20\,{\rm GeV}}{E}\right)^4\right]^{-1}$$

Calibrated to Dominguez et al. anchor points. Not derived from the paper -- a pipeline convenience approximation.

**Implementation:** `ebl.py:attenuation(E_GeV, z)` (line 70), `ebl.py:tau(E_GeV, z)` (line 37).

---

## Layer 8: Window Function Assembly -- Pinetti Eq. 4.1

### 8a. Literature equation (per-z form)

Pinetti+ (2020) Eq. 4.1:

$$W_\gamma^{\rm DM}(z) = \frac{(\Omega_{\rm DM}\rho_c)^2}{4\pi} \cdot \frac{\langle\sigma v\rangle}{2m_\chi^2} \cdot (1+z)^3 \cdot \Delta^2(z) \cdot \frac{dN}{dE'} \cdot e^{-\tau}$$

### 8b. Pipeline equation (per-$\chi$ form)

The pipeline absorbs the $1/H(z)$ Jacobian from $d\chi/dz = c/H(z)$:

$$W_\gamma^{\rm DM}(\chi) = \frac{\langle\sigma v\rangle}{8\pi}\left(\frac{\rho_{\rm DM}}{m_\chi}\right)^2 (1+z)^3 \frac{1}{H(z)} \Delta^2(z) \frac{dN}{dE'} e^{-\tau}$$

Note: $1/(4\pi) \times 1/2 = 1/(8\pi)$. The factor of $1/2$ accounts for identical (Majorana) particles.

**Pinetti 2022:** No separate `W_gamma_DM` override exists in `pinetti2022.py` yet. The DM window function formula is identical; differences enter only through the shared halo model infrastructure (concentration, bias) used in $\Delta^2(z)$ and $P_{\rm HI\times DM}^{2h}$.

### 8c. Unit conversion chain

**DM density:** $\rho_{\rm DM}$ from pipeline units to GeV/cm$^3$:

$$\rho_{\rm DM}^{\rm GeV/cm^3} = \rho_{\rm DM}^{\rm code} \times M_{\odot,\rm GeV} \times \frac{h^2}{{\rm Mpc}_{\rm cm}^3}$$

where:
- $\rho_{\rm DM}^{\rm code} = \Omega_{\rm DM} \times \rho_c = 0.2660 \times 2.775\times10^{11}$ $[M_\odot/h\;({\rm Mpc}/h)^{-3}]$
- $M_{\odot,\rm GeV} = 1.116\times10^{57}$ (solar mass in GeV)
- ${\rm Mpc}_{\rm cm} = 3.086\times10^{24}$ (Mpc in cm)
- The $h^2$ arises because $[M_\odot/h\,({\rm Mpc}/h)^{-3}] = h^2\,[M_\odot\,{\rm Mpc}^{-3}]$

**Numerically:** $\rho_{\rm DM} \approx 1.27 \times 10^{-6}$ GeV/cm$^3$ (verified).

**Hubble rate:** $H(z)$ converted from km/s/Mpc to s$^{-1}$: $H_{\rm SI} = H \times 10^3 / {\rm Mpc}_{\rm m}$

**Final conversion:** Result in CGS $[{\rm cm}^{-3}\,{\rm GeV}^{-1}]$ converted to $({\rm Mpc}/h)^{-3}\,{\rm GeV}^{-1}$ by multiplying by $({\rm Mpc}/h)^3_{\rm cm}$.

### 8d. Parameters

| Parameter | Symbol | Default | Source |
|-----------|--------|---------|--------|
| Observed energy | $E_\gamma$ | -- | Input [GeV] |
| DM mass | $m_\chi$ | -- | Input [GeV] |
| Cross-section | $\langle\sigma v\rangle$ | $3\times10^{-26}\,{\rm cm}^3/{\rm s}$ | Thermal relic |
| Channel | -- | `bb` | $b\bar{b}$ annihilation |
| Boost scenario | -- | `intermediate` | Full subhalo hierarchy |

**Implementation:** `dm_model.py:W_gamma_DM(E_GeV, z, m_chi_GeV, sigma_v, channel, boost_scenario)` (line 200).

---

## Cross-Power Spectrum: HI $\times$ DM

### Two-halo cross-power (Pinetti Eqs. 5.1--5.2)

$$P_{\rm HI\times DM}^{2h}(k,z) = \left[\int \frac{dn}{dM}\, b(M)\, \frac{\tilde{v}(k|M)}{\Delta^2}\, dM\right] \times \left[\int \frac{dn}{dM}\, b(M)\, \frac{\tilde{u}_{\rm HI}(k|M)\, M_{\rm HI}(M)}{\bar\rho_{\rm HI}}\, dM\right] \times P_{\rm lin}(k,z)$$

The $\tilde{v}/\Delta^2$ normalization ensures the DM integral approaches $\sim 1$ at $k\to 0$ (analogous to how $M_{\rm HI}/\bar\rho_{\rm HI}$ normalizes the HI integral). This is correct: $\Delta^2 = \int (dn/dM)\,\tilde{v}(0|M)\,dM$, so dividing by $\Delta^2$ yields a mean-field-normalized weighting.

**Mass range:** Uses HI-relevant range $[10^8, 10^{16}]\,M_\odot/h$ (cross-power vanishes where $M_{\rm HI} = 0$).

**Implementation:** `angular_power.py:P_HI_DM_2h(k, z)` (line 21).

**Pinetti 2022:** The bias integral in $P_{\rm HI\times DM}^{2h}$ would use $q=0.75$ via `pinetti2022.bias_pinetti()`. No separate cross-power override exists yet.

### Full Limber integral

$$C_\ell = \int_{z_{\rm min}}^{z_{\rm max}} \frac{c\,h}{H(z)\,\chi^2(z)}\; W_{\rm HI}(\chi)\; W_\gamma^{\rm DM}(\chi)\; P_{\rm HI\times DM}^{2h}\!\left(k=\frac{\ell+1/2}{\chi},\, z\right)\; dz$$

**Implementation:** `angular_power.py:C_ell_HI_gamma(ell, E_GeV, z_min, z_max, ...)` (line 101).

**Pinetti 2022:** Would use $k = \ell/\chi$ via `pinetti2022.limber_k()`.

---

## Dependency Graph

```
config.py [Planck 2018, SIGMA_V_THERMAL, MOLINE_BOOST_COEFFS, M_MIN/MAX_DM]
    |
    +---> cosmology.py [H(z), chi(z), rho_crit, P_lin(k,z)]
    |       |
    |       +---> hmf_interface.py [sigma(M,z), dn/dM -- SMT mass function]
    |               |
    |               +---> halo_model.py [Delta_vir, R_vir, concentration_correa, bias, u_nfw]
    |               |       \__ pinetti2022.py overrides: bias_pinetti (q=0.75),
    |               |                                     concentration_correa_thesis
    |
    +---> dm_model.py
          |
          +-- _rho_s(M, z)                    <-- NFW scale density
          +-- rho2_integral_analytic(M, z)     <-- int rho^2 d^3x (analytic)
          +-- v_tilde(k, M, z)                 <-- FT of rho^2 (for cross-power)
          +-- boost_moline(M, z, M_min_sub)    <-- Moline substructure boost
          +-- clumping_factor(z, scenario)      <-- Delta^2(z)
          |
          +-- W_gamma_DM(E, z, m_chi, sv, ch)  <-- Final window function
                  |
                  +-- pppc4dmid.dNdE(E', m_chi, ch)  <-- Photon yield at E'=(1+z)E
                  +-- ebl.attenuation(E, z)           <-- exp(-tau) at observed E
```

---

## Simplifications and Theoretical Choices

| Simplification | Nature | Pipeline (Pinetti 2022) | Effect |
|----------------|--------|------------------------|--------|
| Two-halo term only (no one-halo) | Theoretical | Same | One-halo subdominant at $\ell < 1000$; conservative |
| Rectangle rule for mass integration | Numerical | Same | Adequate for 200 points over smooth integrand |
| Single NFW profile (no profile variations) | Theoretical | Same | Standard; scatter in $c(M)$ is $\sim 0.15$ dex |
| Majorana DM assumed ($1/2$ factor) | Theoretical | Same | Dirac DM would remove the $1/2$, doubling the signal |
| Correa c(M) extrapolated below $10^{-2}\,M_\odot$ | Theoretical | Same | Smooth extrapolation but unvalidated; affects microhalo $\Delta^2$ |
| EBL from Dominguez (2011) only | Theoretical | Same | Saldana-Lopez (2021) is more modern; <20% difference |
| Mass limits clamped to $[10^{-4}, 10^{17}]$ | Numerical | Same | Truncates 2 decades of microhalos; few-% on $\Delta^2$ |
| `optimistic` boost = `intermediate` | Incomplete | Same | Not yet implemented as a distinct scenario |
| PPPC4DMID public tables vs thesis Pythia | Data source | Same (public; thesis Pythia unavailable) | Percent-level, irreducible |
