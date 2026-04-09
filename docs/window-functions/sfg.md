# SFG Window Function: Complete Pipeline

## Target Quantity

The star-forming galaxy (SFG) window function shares the generic astrophysical gamma-ray source form (Pinetti+ 2020, Eq. 4.3). The implemented per-chi window makes the final comoving-unit conversion explicit:

$$W_\gamma^{\rm SFG}(\chi) = \frac{1}{4\pi h^3}\int_{L_{\min}}^{L_{\rm up}}\Phi_\gamma^{\rm SFG}(L,z)\;\frac{L}{E_{\rm GeV\to erg}\,I_\alpha}\;E_{\rm rest}^{-\alpha}\;dL$$

with $\alpha = 2.7$ (Pinetti+ 2020 Table 3 SFG photon index — the softest UGRB component, reflecting pion-decay dominated emission), $E_{\rm rest}=(1+z)E_{\rm obs}$, $I_\alpha=\int_{0.1}^{100}E^{1-\alpha}\,dE$, and $L_{\rm up}=\min(L_{\max}, L_{\rm thr}(z))$ with Fermi-LAT sensitivity threshold $L_{\rm thr}(z)=4\pi d_L^2(z)\,F_{\rm sens}$. Relative to the paper form, the implementation makes the physical-Mpc$^{-3}$ to $(\mathrm{Mpc}/h)^{-3}$ conversion explicit and keeps no separate external $(1+z)^{-2}$ prefactor.

Unlike blazars (direct gamma-ray LDDE), SFGs derive their GLF from the well-constrained **infrared** luminosity function via an empirical calorimetric scaling: cosmic rays accelerated in supernova remnants lose energy primarily through pion production (gamma rays) and IR re-radiation of dust-reprocessed UV (thermal IR). Both scale with star formation rate, hence the near-linearity $L_\gamma\propto L_{\rm IR}^{1.09}$.

---

## Layer 1: Cosmological Backbone

Standard Planck 2018. Same as HI and mAGN.

**Implementation:** `cosmology.py`.

---

## Layer 2: Gruppioni et al. (2013) Three-Component IR Luminosity Function

Foundation: the sum of three distinct populations fit to deep Herschel PEP/HerMES data to $z\sim 4$:

$$\Phi_{\rm IR}(L_{\rm IR},z) = \Phi_{\rm spiral} + \Phi_{\rm starburst} + \Phi_{\rm SF\text{-}AGN}$$

Each component follows a **modified Schechter form** (Gruppioni Eq. 8 / Pinetti thesis Eq. C.23):

$$\Phi_i(L_{\rm IR},z) = \Phi_{0,i}(z)\left(\frac{L_{\rm IR}}{L_{0,i}(z)}\right)^{1-\gamma_i}\exp\!\left[-\frac{1}{2\sigma_i^2}\log_{10}^2\!\left(1+\frac{L_{\rm IR}}{L_{0,i}(z)}\right)\right]$$

Returns $d\Phi/d\log_{10}L_{\rm IR}$ in Mpc⁻³, with $L_{\rm IR}$ in $L_\odot$ (8-1000 μm total infrared).

### Parameters (Gruppioni Table 8 / Pinetti Table C.2)

| Component | $\gamma$ | $\sigma$ | $\log_{10}(L_\star/L_\odot)$ | $\log_{10}(\phi_\star/{\rm Mpc}^{-3})$ | $k_L$ | $k_{R1}$ | $k_{R2}$ |
|-----------|----------|----------|------------------------------|----------------------------------------|-------|----------|----------|
| spiral | 1.0 | 0.50 | 9.78 | −2.12 | 4.49 | −0.54 | −7.13 |
| starburst | 1.0 | 0.35 | 11.17 | −4.46 | 1.96 | 3.79 | −1.06 |
| SF-AGN | 1.2 | 0.40 | 10.80 | −3.20 | 3.17 | 0.67 | **−3.17** |

**Note on SF-AGN $k_{R2}$**: The Pinetti (2022) thesis Table C.2 has a typo showing $+3.17$; the pipeline uses the correct $-3.17$ from Gruppioni's original paper. A positive $k_{R2}$ would cause unphysical density growth at $z>1.1$.

**Implementation:** `astro_sources.py:_gruppioni_component()`, `_gruppioni_ir_lf()`; parameters in `config.py:GRUPPIONI_PARAMS`.

---

## Layer 3: Redshift Evolution (Luminosity + Density)

### Luminosity evolution $L_{0,i}(z)$ (Pinetti Eq. C.24)

$$L_{0,i}(z) = L_{\star,i}\left(\frac{1+z}{1.15}\right)^{k_{L,i}}$$

**Pipeline convention**: break at $z=1.1$ applied uniformly to all components (frozen above):

$$L_{0,i}(z>1.1) = L_{\star,i}\left(\frac{2.1}{1.15}\right)^{k_{L,i}}$$

*Deviation note*: Gruppioni Table 8 only specifies a $z=1.1$ break for the spiral component ($z_{b,L}=1.1$, $k_{L,2}=0$). Starburst and SF-AGN in the paper have single power laws with no break. The pipeline applies the freeze uniformly as a deliberate simplification — the effect is small relative to the larger GLF-evolution, spectral, and unresolved-threshold changes across the same redshift range.

### Density evolution $\Phi_{0,i}(z)$ (Pinetti Eqs. C.25-C.26)

**Spiral** (break at $z=0.53$):

$$\Phi_{0,{\rm sp}}(z)=\Phi_{\star,{\rm sp}}\times\begin{cases}((1+z)/1.15)^{k_{R1}} & z\le 0.53\\(1.53/1.15)^{k_{R1}}\,((1+z)/1.53)^{k_{R2}} & z>0.53\end{cases}$$

**Starburst & SF-AGN** (break at $z=1.1$):

$$\Phi_{0,j}(z)=\Phi_{\star,j}\times\begin{cases}((1+z)/1.15)^{k_{R1}} & z\le 1.1\\(2.1/1.15)^{k_{R1}}\,((1+z)/2.1)^{k_{R2}} & z>1.1\end{cases}$$

The reference $(1+z)/1.15$ normalization corresponds to the $z=0.15$ midpoint of Gruppioni's first redshift bin (a pipeline convention; the paper parameterizes evolution bin-by-bin).

**Implementation:** embedded in `astro_sources.py::_gruppioni_component()`.

---

## Layer 4: Ackermann et al. (2012) $L_\gamma$-$L_{\rm IR}$ Scaling

The cornerstone empirical relation: gamma-ray luminosity traces IR luminosity quasi-linearly (Ackermann+ 2012 Table 5, EM method, AGN-excluded):

$$\log_{10}\!\left(\frac{L_{0.1\text{-}100\,\rm GeV}}{\rm erg/s}\right) = \alpha_{\rm IR}\,\log_{10}\!\left(\frac{L_{8\text{-}1000\,\mu{\rm m}}}{10^{10}\,L_\odot}\right) + \beta_{\rm IR}$$

with $\alpha_{\rm IR}=1.09$ and $\beta_{\rm IR}=39.19$.

**Physical basis**: cosmic rays accelerated in supernova remnants deposit energy calorimetrically — pion production makes gamma rays while UV from young stars is dust-reprocessed to IR. Both track star formation rate, giving near-linearity $\alpha\approx 1$.

The pipeline **inverts** this to obtain $L_{\rm IR}$ from $L_\gamma$:

$$L_{\rm IR}(L_\gamma) = 10^{10}\,L_\odot \times 10^{(\log_{10}L_\gamma - \beta_{\rm IR})/\alpha_{\rm IR}}$$

with Jacobian:

$$\frac{d\log_{10}L_{\rm IR}}{d\log_{10}L_\gamma} = \frac{1}{\alpha_{\rm IR}} = \frac{1}{1.09} \approx 0.917$$

**Implementation:** `astro_sources.py:_L_IR_from_Lgamma()`; constants in `config.py` (`ACKERMANN_ALPHA_IR=1.09`, `ACKERMANN_BETA_IR=39.19`).

---

## Layer 5: SFG Gamma-Ray Luminosity Function (Pinetti Eq. C.28)

Combining the Gruppioni IR LF with the Ackermann scaling:

$$\boxed{\Phi_\gamma^{\rm SFG}(L_\gamma,z) = \Phi_{\rm IR}\!\left(L_{\rm IR}(L_\gamma),z\right)\;\left|\frac{d\log_{10}L_{\rm IR}}{d\log_{10}L_\gamma}\right|\;\frac{1}{L_\gamma\ln 10}}$$

The $1/(L_\gamma\ln 10)$ converts from $d\Phi/d\log_{10}L$ (Gruppioni's native form) to $d\Phi/dL$ (Pinetti window function's required form).

**Implementation:** `astro_sources.py:_glf_SFG()`.

---

## Layer 6: Window Function Assembly (Pinetti+ Eq. 4.3)

Same generic form as all astrophysical sources, with the implementation's final
unit conversion made explicit:

$$W_\gamma^{\rm SFG}(z) = \frac{1}{4\pi h^3}\int_{L_{\min}}^{L_{\rm up}} \Phi_\gamma^{\rm SFG}(L,z)\;\frac{L}{E_{\rm GeV\to erg}\,I_\alpha}\;E_{\rm rest}^{-\alpha}\;dL$$

with:
- $L_{\min}=10^{37}$ erg/s, $L_{\max}=10^{42}$ erg/s (Pinetti thesis Table 3.1)
- $\alpha=2.7$ (softest spectrum among UGRB sources)
- $I_\alpha=\int_{0.1}^{100}E^{1-\alpha}\,dE$ (energy normalization, 0.1-100 GeV band)
- $L_{\rm sens}(z) = F_{\rm sens}\,4\pi d_L^2\,G_{\rm eV\to erg}\,I_\alpha / [(1+z)^{2-\alpha}\,J_\alpha^{\rm EBL}(z)]$ (Fermi sensitivity cut with K-correction and EBL; Pinetti 2022 Eqs. 3.75–3.76)

The low $L_{\max}=10^{42}$ erg/s reflects that individual SFGs are much fainter than blazars (compared to $10^{50}$ erg/s for mAGN or $10^{52}$ erg/s for blazars).

**Implementation:** `astro_sources.py::W_gamma_astro(..., source_class='SFG', ...)`.

---

## Layer 7: Effective Bias (Pinetti Eq. C.29)

For HI × SFG 2-halo cross-power, SFG effective halo bias uses a direct mass-luminosity relation:

$$M_{\rm halo}(L_\gamma,z) = \frac{10^{12}\,M_\odot}{(1+z)^{1.61}}\left(\frac{L_\gamma}{6.8\times10^{39}\,{\rm erg/s}}\right)^{0.92}$$

Evaluated at a characteristic luminosity $L_\gamma^{\rm char}=10^{39}$ erg/s, then $b_{\rm SFG}(z) = b_{\rm ST}(M_{\rm halo}(z), z)$ using Sheth-Tormen bias.

The strong redshift dependence $(1+z)^{-1.61}$ encodes **downsizing**: SFGs at higher redshifts live in lower-mass halos (less biased environments). This gives SFG the lowest effective bias among UGRB components.

**Implementation:** `astro_sources.py::bias_astro(z, 'SFG')`; parameters in `config.py` (SFG_*).

---

## Complete Dependency Graph

```text
W_gamma^SFG(E_GeV, z)                               [astro_sources.py::W_gamma_astro]
├── Phi_gamma^SFG(L, z)                             [astro_sources.py::_glf_SFG]
│   ├── _L_IR_from_Lgamma(L_gamma)                  [astro_sources.py::_L_IR_from_Lgamma]
│   │   ├── log_x = (log L_gamma - beta)/alpha
│   │   ├── ACKERMANN_ALPHA_IR = 1.09               [config.py]
│   │   └── ACKERMANN_BETA_IR = 39.19               [config.py]
│   ├── _gruppioni_ir_lf(L_IR, z)                   [astro_sources.py::_gruppioni_ir_lf]
│   │   ├── spiral:    gamma=1.0, sigma=0.50, log_L*=9.78, log_phi*=-2.12
│   │   │   └── k_L=4.49, k_R1=-0.54, k_R2=-7.13   [break phi at z=0.53]
│   │   ├── starburst: gamma=1.0, sigma=0.35, log_L*=11.17, log_phi*=-4.46
│   │   │   └── k_L=1.96, k_R1=3.79, k_R2=-1.06    [break phi at z=1.1]
│   │   └── SF-AGN:    gamma=1.2, sigma=0.40, log_L*=10.80, log_phi*=-3.20
│   │       └── k_L=3.17, k_R1=0.67, k_R2=-3.17    [break phi at z=1.1]
│   └── Jacobian |dlog L_IR/dlog L_gamma| = 1/1.09 = 0.917
├── alpha = 2.7                                     [config.py]
├── L_min=1e37, L_max=1e42 erg/s                    [config.py]
├── L_sens(z) = F_sens*4pi*d_L^2*GeV2erg*I_a/[K*J_a^EBL]  [astro_sources.py::L_sens]
├── E_rest = E_obs * (1+z)                          [rest-frame energy]
├── I_alpha = integral E^{1-alpha} dE [0.1,100 GeV]
└── final return = emissivity / (4*pi*h^3)          [physical Mpc^-3 -> (Mpc/h)^-3]

bias_SFG(z)                                         [astro_sources.py::bias_astro]
├── L_char = 1e39 erg/s                             [characteristic SFG L_gamma]
├── M_halo = 1e12 / (1+z)^1.61 * (L/6.8e39)^0.92   [Pinetti Eq. C.29]
└── b_ST(M_halo, z)                                 [Sheth-Tormen bias]
```

---

## Literature Sources per Component

| Component | Primary Source | Supporting Sources |
|-----------|---------------|-------------------|
| IR LF three-component model | Gruppioni+ (2013) Table 8 | Herschel PEP (70-160 μm) + HerMES (250-500 μm) |
| Modified Schechter form | Gruppioni+ (2013) Eq. 8 | Saunders+ (1990) original form |
| $L_\gamma$-$L_{\rm IR}$ scaling | Ackermann+ (2012) Table 5 | 69 Fermi-LAT SFG observations |
| SFG GLF assembly | Pinetti (2022) thesis Eq. C.28 | |
| Window function formula | Pinetti+ (2020) Eq. 4.3 | Generic astro window |
| Mass-luminosity for bias | Pinetti (2022) thesis Eq. C.29 | |
| Spectral index $\alpha=2.7$ | Pinetti+ (2020) Table 3 | Fermi-LAT stacked SFG spectrum |

---

## Physical Intuition

The SFG window function has distinctive features:

1. **Calorimetric origin**: Unlike AGN (beaming-dominated), SFG gamma-rays come from cosmic-ray calorimetry — pion decay from CRs interacting with ISM gas. This gives $\alpha=2.7$ (softest UGRB component, reflecting the pion-bump spectrum).

2. **Multi-component IR LF**: The three Gruppioni components have very different evolution:
   - **Spiral** dominates at low $z$, declines steeply ($k_{R2}=-7.13$)
   - **Starburst** grows at low $z$ ($k_{R1}=3.79$), mild decline afterward
   - **SF-AGN** peaks at $z\sim 1-2$, declines at higher $z$

3. **Window function shape**: The combination peaks at $z\sim 1$, extending smoothly to $z\sim 3$ — broader redshift coverage than blazars but similar to mAGN.

4. **Downsizing signature**: The bias relation $M_{\rm halo}\propto(1+z)^{-1.61}$ encodes the well-known trend that star formation shifts from massive halos at $z=0$ to lower-mass halos at high $z$. This gives SFG the lowest effective bias of all UGRB components.

5. **Contribution to UGRB**: ~5-20% depending on luminosity integration range; SFGs are individually faint ($L_\gamma\lesssim 10^{42}$ erg/s) but vastly numerous — a truly "diffuse" component.
