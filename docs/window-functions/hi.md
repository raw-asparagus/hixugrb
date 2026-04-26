# HI Window Function: Complete Pipeline

## Target Quantity

The HI window function enters the Limber integral for the angular cross-power spectrum (Pinetti+ 2020, Eq. 2.1):

$$C_\ell^{ij} = \int \frac{d\chi}{\chi^2}\, W_{\rm HI}(\chi)\, W_j(\chi)\, P_{ij}\!\left(k = \frac{\ell+1/2}{\chi},\, z\right)$$

The window function itself (Eqs. 3.15–3.16) is:

$$W_{\rm HI}(\chi) = \bar{T}_b(z)\; \phi(z)\; \frac{H(z)}{c\,h}$$

where $\phi(z) = 1/(z_{\max} - z_{\min})$ is a top-hat redshift selection function for the radio survey band. In the current implementation, `W_HI()` contains the mean brightness temperature and the per-$\chi$ Jacobian; the effective HI bias is computed separately and enters the HI power spectra.

---

## Layer 1: Cosmological Backbone

**Source:** Planck 2018 (TT,TE,EE+lowE+lensing) parameters.

| Quantity | Expression | Reference |
|----------|-----------|-----------|
| $E(z)$ | $\sqrt{\Omega_M(1+z)^3 + \Omega_\Lambda}$ | Flat LCDM |
| $H(z)$ | $H_0 E(z)$, with $H_0 = 67.36$ km/s/Mpc | Planck 2018 |
| $\chi(z)$ | $\frac{c}{H_0}\int_0^z \frac{dz'}{E(z')}$ | Standard |
| $\bar\rho_m$ | $\Omega_M \rho_c = 0.3153 \times 2.775\times10^{11}\;h^2\,M_\odot\,\text{Mpc}^{-3}$ | Planck 2018 |
| $P_{\rm lin}(k,z)$ | CAMB Boltzmann solver | Planck 2018 params |
| $\sigma(M,z)$ | $\frac{1}{2\pi^2}\int k^2 P_{\rm lin} W^2(kR)\,dk$, top-hat smoothing | Perturbation theory |

Key parameters: $h=0.6736$, $\Omega_M=0.3153$, $\Omega_B=0.0493$, $\sigma_8=0.8111$, $n_s=0.9649$.

**Implementation:** `cosmology.py` (E, H, chi, P_lin, sigma_R, sigma_M, growth_factor), `config.py` (all Planck 2018 constants).

---

## Layer 2: Halo Model Infrastructure

### 2a. Halo mass function — Sheth, Mo & Tormen (2001)

$$\nu f(\nu) = A\left[1 + (q\nu)^{-p}\right]\sqrt{\frac{q\nu}{2\pi}}\exp\!\left(-\frac{q\nu}{2}\right)$$

with $A=0.3222$, $q=0.707$, $p=0.3$, and $\nu = \delta_c^2/\sigma^2(M,z)$, $\delta_c=1.686$. Converts to:

$$\frac{dn}{dM} = \frac{\bar\rho_m}{M^2}\,f(\sigma)\,\left|\frac{d\ln\sigma}{d\ln M}\right|$$

**Implementation:** Delegated to the `hmf` Python package with `hmf_model='SMT'` via `hmf_interface.py`.

### 2b. Halo bias — Sheth & Tormen (1999)

Peak-background split:

$$b(\nu) = 1 + \frac{q\nu - 1}{\delta_c} + \frac{2p}{\delta_c(1 + (q\nu)^p)}$$

Same $q=0.707$, $p=0.3$, $\delta_c=1.686$.

**Implementation:** `halo_model.py:bias(M, z)`.

### 2c. Virial quantities

Using the Bryan & Norman (1998) redshift-dependent virial overdensity:

$$R_{\rm vir} = \left(\frac{3M}{4\pi \cdot \Delta_{\rm vir}(z) \cdot \rho_c(z)}\right)^{1/3}, \qquad v_c = \sqrt{\frac{GM}{R_{\rm vir}}}$$

The circular velocity $v_c(M,z)$ is critical because it enters the M_HI exponential cutoff.

**Implementation:** `halo_model.py:R_vir(M, z)`, `halo_model.py:v_circ(M, z)`.

---

## Layer 3: HI Halo Model — Padmanabhan, Refregier & Amara (2017)

All parameters from the **modified NFW profile fit** (Table A1), not the exponential profile fit (Table 3).

### 3a. HI mass–halo mass relation (Padmanabhan+ 2017 Eq. 1 / Pinetti+ Eq. 3.7)

$$M_{\rm HI}(M,z) = \alpha\, f_{H,c}\, M \left(\frac{M}{10^{11}h^{-1}M_\odot}\right)^\beta \exp\!\left[-\left(\frac{v_{c,0}}{v_c(M,z)}\right)^3\right]$$

| Parameter | Value | Meaning |
|-----------|-------|---------|
| $\alpha$ | 0.176 | HI fraction normalization |
| $\beta$ | −0.69 | Mass slope (negative: HI fraction drops for massive halos) |
| $v_{c,0}$ | 40.7 km/s | Low-mass cutoff velocity |
| $f_{H,c}$ | $(1-Y_P)\Omega_B/\Omega_M$ | Cosmic hydrogen fraction; $Y_P=0.24$ |

The exponential cutoff at low $v_c$ (low mass) models suppression of HI in halos too small to retain gas against photoionization. The power-law slope $\beta < 0$ means very massive halos are inefficient at hosting HI (AGN feedback, hot gas).

**Implementation:** `hi_model.py:M_HI(M, z)`, parameters in `config.py`.

### 3b. HI concentration (Padmanabhan+ 2017 Eq. 3 / Pinetti+ Eq. 3.8)

$$c_{\rm HI}(M,z) = c_{HI,0} \left(\frac{M}{10^{11}M_\odot}\right)^{-0.109} \frac{4}{(1+z)^\gamma}$$

with $c_{HI,0}=139$, $\gamma=0.13$ (Table A1).

**Implementation:** `hi_model.py:c_HI(M, z)`.

### 3c. Modified NFW HI density profile (Pinetti+ Eq. 3.9)

$$\rho_{\rm HI}(r) = \rho_0 \frac{r_s^3}{(r + 0.75\,r_s)(r + r_s)^2}$$

where $r_s = R_{\rm vir}/c_{\rm HI}$ and $\rho_0$ is fixed by normalization: $\int_0^{R_{\rm vir}} 4\pi r^2 \rho_{\rm HI}\,dr = M_{\rm HI}$.

The normalization integral is computed analytically via partial fraction decomposition:

$$\int_0^{c} \frac{x^2}{(x+0.75)(x+1)^2}\,dx = 9\ln\!\left(\frac{c+0.75}{0.75}\right) - 8\ln(c+1) + 4\left(\frac{1}{c+1}-1\right)$$

**Implementation:** `hi_model.py:_hi_profile_norm_integral(c_hi)`, `hi_model.py:rho0_HI(M, z)`.

### 3d. Fourier transform of HI profile (Pinetti+ Eq. 3.14)

$$\tilde{u}_{\rm HI}(k|M) = \frac{4\pi}{M_{\rm HI}} \int_0^{R_{\rm vir}} r^2 \rho_{\rm HI}(r) \frac{\sin(kr)}{kr}\,dr$$

Normalized so $\tilde{u}_{\rm HI}(k\to 0) = 1$. No closed-form exists for the modified NFW profile; computed via numerical quadrature (`scipy.integrate.quad`, epsrel=1e-6).

**Implementation:** `hi_model.py:u_HI(k, M, z)`.

### 3e. Mean comoving HI density (Pinetti+ Eq. 3.2)

$$\bar\rho_{\rm HI}(z) = \int_{M_{\min}}^{M_{\max}} \frac{dn}{dM}\, M_{\rm HI}(M,z)\, dM$$

Integration limits: $M_{\min}=10^8\,M_\odot/h$, $M_{\max}=10^{16}\,M_\odot/h$. The integrand is exponentially suppressed at both limits by the M_HI cutoff and the mass function falloff.

**Implementation:** `hi_model.py:rho_HI_mean(z)`, via `scipy.quad` in log-mass.

### 3f. HI density parameter (Pinetti+ Eq. 3.3)

$$\Omega_{\rm HI}(z) = \frac{\bar\rho_{\rm HI}^\mathrm{com}(z)}{\rho_c}$$

The pipeline computes this from the halo integral (z-dependent, **D5**), rather than using a fixed value. Both $\bar\rho_{\rm HI}$ and $\rho_c$ are comoving (z=0) quantities — no $(1+z)^3$ factor.

**Implementation:** `hi_model.py:Omega_HI(z)`.

### 3g. Mean brightness temperature (Pinetti+ Eq. 3.4)

$$\bar{T}_b(z) = 188\,h\;\Omega_{\rm HI}(z)\;\frac{(1+z)^2}{E(z)} \quad [\text{mK}]$$

Converts the HI density into an observable 21-cm signal strength. The 188$h$ prefactor comes from fundamental 21-cm radiation physics (spin temperature >> CMB temperature in the post-reionization regime). Typical values: $\bar{T}_b \sim 0.05$–$0.3$ mK over $z \sim 0$–$4$.

**Implementation:** `hi_model.py:T_bar_b(z)`.

### 3h. Effective HI bias (Pinetti+ Eq. 3.6)

$$b_{\rm HI}(z) = \frac{1}{\bar\rho_{\rm HI}(z)} \int \frac{dn}{dM}\, M_{\rm HI}(M,z)\, b(M,z)\, dM$$

HI-mass-weighted average of the Sheth-Tormen halo bias. Since HI lives preferentially in $\sim10^{10}$–$10^{12}\,M_\odot$ halos (moderate mass, moderate bias), $b_{\rm HI}$ is typically $\sim1$–$2$.

**Implementation:** `hi_model.py:b_HI(z)`, via `scipy.quad` in log-mass.

---

## Layer 4: Assembly into the Window Function

Combining everything (Pinetti+ Eqs. 3.15–3.16):

$$W_{\rm HI}(z) = \underbrace{188\,h\;\Omega_{\rm HI}(z)\;\frac{(1+z)^2}{E(z)}}_{\bar{T}_b(z)} \;\times\; \underbrace{\frac{1}{z_{\max}-z_{\min}}}_{\phi(z)} \;\times\; \underbrace{\frac{H(z)}{c\,h}}_{\text{Jacobian}}$$

The $\phi(z)$ factor is a top-hat in redshift determined by the radio survey band (e.g., MeerKAT UHF band $\to$ $z \in [0.4, 1.45]$). The $H(z)/(c\,h)$ factor is the geometric Jacobian converting the paper's per-$z$ form into the repository's per-$\chi$ convention. The HI bias is applied in the HI power spectra, not inside `W_HI()`.

**Implementation:** `hi_model.py:W_HI(z, z_min, z_max)`.

---

## Layer 5: HI Power Spectra (for Limber integrand)

### One-halo (Pinetti+ Eq. 3.12)

$$P_{\rm HI}^{\rm 1h}(k,z) = \frac{1}{\bar\rho_{\rm HI}^2} \int \frac{dn}{dM}\, M_{\rm HI}^2\, \tilde{u}_{\rm HI}^2\, dM$$

### Two-halo (Pinetti+ Eq. 3.13)

$$P_{\rm HI}^{\rm 2h}(k,z) = \left[\frac{1}{\bar\rho_{\rm HI}} \int \frac{dn}{dM}\, b(M)\, M_{\rm HI}\, \tilde{u}_{\rm HI}\, dM\right]^2 P_{\rm lin}(k,z)$$

Both computed via summation over a log-spaced mass grid (n_M=160 points, $10^8$–$10^{16}\,M_\odot/h$).

**Implementation:** `hi_model.py:P_HI_1h(k, z)`, `hi_model.py:P_HI_2h(k, z)`.

---

## Complete Dependency Graph

```
W_HI(z, z_min, z_max)                           [hi_model.py:408]
├── T_bar_b(z)                                   [hi_model.py:206]  Pinetti+ Eq. 3.4
│   ├── Omega_HI(z)                              [hi_model.py:192]  Pinetti+ Eq. 3.3
│   │   ├── rho_HI_mean(z)                       [hi_model.py:178]  Pinetti+ Eq. 3.2
│   │   │   ├── dn/dM(M,z)                       [hmf_interface.py] SMT 2001 via hmf
│   │   │   │   ├── sigma(M,z)                    [hmf_interface.py] from CAMB-backed hmf transfer
│   │   │   │   └── delta_c = 1.686               [config.py:160]   spherical collapse
│   │   │   └── M_HI(M,z)                        [hi_model.py:33]   Padmanabhan+ 2017 Eq. 1
│   │   │       ├── alpha=0.176, beta=-0.69       [config.py:170-171] Table A1
│   │   │       ├── v_c0=40.7 km/s                [config.py:172]    Table A1
│   │   │       ├── f_Hc = (1-Y_P)*Omega_B/Omega_M [config.py:177]
│   │   │       └── v_circ(M,z)                   [halo_model.py:73] from R_vir, Delta_vir(z)
│   │   └── rho_crit                              [config.py:149]    Planck 2018
│   ├── h = 0.6736                                [config.py:133]    Planck 2018
│   └── E(z)                                      [cosmology.py:161] flat LCDM
├── b_HI(z)                                       [hi_model.py:295]  used by P_HI(k,z), not by W_HI()
│   ├── rho_HI_mean(z)                            (same as above)
│   ├── dn/dM(M,z)                                (same as above)
│   ├── M_HI(M,z)                                 (same as above)
│   └── b(M,z)                                    [halo_model.py:111] Sheth & Tormen 1999
│       ├── q=0.707, p=0.3                        [config.py:161-162]
│       └── nu = delta_c^2/sigma^2(M,z)           [hmf_interface.py]
├── phi(z) = 1/(z_max - z_min)                    top-hat selection
└── H(z)/c                                        [cosmology.py:167] cosmological Jacobian
```

---

## Literature Sources per Component

| Component | Primary Source | Supporting Sources |
|-----------|---------------|-------------------|
| Window function formula | Pinetti+ (2020) Eqs. 3.15–3.16 | Pinetti (2022) thesis Ch. 3 |
| $M_{\rm HI}(M,z)$ relation | Padmanabhan+ (2017) Table A1 | MCMC fit to ALFALFA, DLA, GBT data |
| $\bar{T}_b$ formula | Pinetti+ (2020) Eq. 3.4 | Standard 21-cm cosmology (Battye+ 2013, Bull+ 2015) |
| $b_{\rm HI}$ integral | Pinetti+ (2020) Eq. 3.6 | Padmanabhan+ (2017) |
| Halo mass function | Sheth, Mo & Tormen (2001) | Calibrated to N-body across cosmologies |
| Halo bias | Sheth & Tormen (1999) | Peak-background split, ellipsoidal collapse |
| Cosmological parameters | Planck 2018 (Aghanim+ 2020) | TT,TE,EE+lowE+lensing |

---

## Physical Intuition

The HI window function is a **weighted tracer of linear density**. Unlike the DM annihilation window (which traces $\rho^2$ and is sensitive to halo profiles/substructure), $W_{\rm HI}$ depends on:

1. **How much HI exists** ($\Omega_{\rm HI}$ via $M_{\rm HI}$ summed over the halo mass function) — peaks at intermediate-mass halos ($\sim10^{11}\,M_\odot$) where gas cooling is efficient but AGN feedback hasn't expelled it
2. **How biased that HI is** ($b_{\rm HI}$) — an HI-mass-weighted average bias, typically $\sim1$–$2$
3. **The survey geometry** ($\phi$) — which redshift slice the radio telescope observes

The redshift evolution of $W_{\rm HI}$ is primarily governed by $\bar{T}_b(z) \propto \Omega_{\rm HI}(z)(1+z)^2/E(z)$, which rises with redshift (more HI at higher $z$) but is modulated by the expansion rate.
