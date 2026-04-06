# Pipeline Architecture

## Data Flow

```
                        ┌─────────────┐
                        │  config.py  │  [Planck 2018](literature/planck2018.md) params, instrument specs,
                        │             │  Fermi bins, mass/k/z grids
                        └──────┬──────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
          ┌────────────┐ ┌──────────┐ ┌──────────────┐
          │cosmology.py│ │  ebl.py  │ │ pppc4dmid.py │
          │ CAMB P(k,z)│ │ebltable  │ │ table reader │
          │ H,χ,D,E(z) │ │ τ(E,z)  │ │ dN/dE(E,m,ch)│
          └─────┬──────┘ └────┬─────┘ └──────┬───────┘
                │             │              │
                ▼             │              │
       ┌────────────────┐    │              │
       │hmf_interface.py│    │              │
       │ hmf.MassFunction│    │              │
       │ σ(M), dn/dM    │    │              │
       └───────┬────────┘    │              │
               ▼             │              │
        ┌─────────────┐      │              │
        │halo_model.py│      │              │
        │ R_vir, v_c  │      │              │
        │ bias, c(M)  │      │              │
        │ ũ_NFW(k|M)  │      │              │
        └──┬───────┬──┘      │              │
           │       │         │              │
     ┌─────▼──┐ ┌──▼─────────▼──────────────▼──┐
     │hi_model│ │         dm_model.py           │
     │ M_HI   │ │ ρ², ṽ(k|M), Δ², boost       │
     │ ũ_HI   │ │ W_γ^DM(E,z,m_χ,σv)          │
     │ ρ_HI   │ └──────────┬───────────────────┘
     │ b_HI   │            │
     │ P_HI   │  ┌─────────────────┐
     │ W_HI   │  │astro_sources.py │
     └───┬────┘  │ GLFs (4 sources)│
         │       │ W_γ^astro(E,z)  │
         │       │ mean_intensity  │
         │       └────────┬────────┘
         │                │
         ▼                ▼
    ┌───────────────────────────┐     ┌───────────────┐
    │    angular_power.py       │     │noise_model.py │
    │ P_HI×DM, P_HI×astro (3D) │     │ T_sys, N^HI   │
    │ C_ℓ Limber integration    │     │ N^γ, B_ℓ, PSF │
    │ C_ℓ^{HI,HI} auto-power   │     └───────┬───────┘
    └────────────┬──────────────┘             │
                 │                            │
                 ▼                            ▼
          ┌──────────────────────────────────────┐
          │          statistics.py                │
          │  variance_Cl  →  compute_SNR         │
          │  delta_chi2   →  exclusion_curve     │
          └──────────────┬───────────────────────┘
                         │
               │
               ▼
        ┌─────────────────────────────┐
        │notebooks/                   │
        │  pipeline_validation.ipynb  │
        │  validation plots           │
        │  SNR table, exclusion curves│
        └─────────────────────────────┘
```

**Summary:** Config → Cosmology + Tables → Halo model (via hmf) → HI / DM / Astro tracers → 3D power spectra → Limber C_ℓ → Statistics (SNR, exclusion) → Plots / Validation

For the equation-level implementation reference, see [`equations.md`](equations.md). For paper summaries and source-specific provenance, see [`literature/`](literature/).

## Module Descriptions

| Module | Role |
|--------|------|
| `config.py` | All physical constants, [Planck 2018](literature/planck2018.md) cosmology, instrument specs (MeerKAT/SKA/Fermi), computational grids |
| `cosmology.py` | CAMB wrapper for P_lin(k,z); Hubble rate H(z), comoving distance χ(z), growth factor D(z) |
| `hmf_interface.py` | Thin wrapper around the `hmf` package; cached MassFunction instances, σ(M), dn/dM |
| `halo_model.py` | Virial radius R_vir, circular velocity v_c, halo bias b(M), concentration c(M), NFW Fourier transform ũ(k, M) |
| `hi_model.py` | HI mass M_HI(M,z), altered NFW HI profile, Ω_HI, b_HI, T̄_b, HI power spectra P_HI^{1h/2h}, window W_HI |
| `dm_model.py` | NFW ρ² profile and Fourier transform ṽ(k, M), substructure boost B(M), clumping factor Δ², DM window W_γ^DM, DM power spectra |
| `astro_sources.py` | Gamma-ray luminosity functions: LDDE for FSRQ/BL Lac, radio→gamma chain for mAGN, IR→gamma chain for SFG; astrophysical window W_γ^astro; mean UGRB intensity |
| `pppc4dmid.py` | PPPC4DMID photon yield table reader/interpolator; dN/dE for bb̄, τ⁺τ⁻, WW channels |
| `ebl.py` | EBL opacity τ(E,z) via `ebltable` package (Dominguez+2011); analytic fallback |
| `noise_model.py` | Radio noise (dish + interferometer), beam functions (Gaussian + exact King PSF), Fermi-LAT noise N^γ and PSF, pixel window, Fermissimo specs |
| `angular_power.py` | 3D cross-power spectra P_{HI×DM}, P_{HI×astro}; Limber integration for C_ℓ; HI auto-power C_ℓ^{HI,HI} |
| `statistics.py` | Gaussian variance ΔC_ℓ, signal-to-noise ratio, Δχ² test statistic, DM exclusion curves σ_v(m_χ) |
| `notebooks/pipeline_validation.ipynb` | Jupyter notebook with validation plots, window-function comparisons, SNR tables, and exclusion-curve outputs |

## Window Function Pipeline

Six window functions feed into the Limber integral. All are returned in the **per-comoving-distance** convention (per χ), used with Limber weight `(dχ/dz)/χ² × dz`.

### W_HI — HI 21-cm brightness temperature

```
config.py (Planck params, HI params)
    │
cosmology.py: H(z), E(z)
    │
halo_model.py: dndM(M,z), bias(M,z), R_vir(M,z), v_circ(M,z)
    │
hi_model.py:
    ├─ M_HI(M,z)      ← [Padmanabhan+ (2017)](literature/padmanabhan2017.md) Eq. 3.7
    ├─ rho_HI_mean(z)  ← ∫ dndM × M_HI dM
    ├─ Omega_HI(z)     ← rho_HI / rho_crit
    ├─ T_bar_b(z)      ← Pinetti Eq. 3.4
    ├─ b_HI(z)         ← mass-weighted bias, Eq. 3.6
    └─ W_HI(z)         ← T_bar_b × φ(z) × H/(ch)  [pipeline form]
                           └─ φ(z) = 1/Δz (top-hat from radio band)
```

**Survey-dependent:** φ(z) set by telescope band (MeerKAT UHF: z=0.4–1.45, L: z=0–0.58, etc.). The HI bias is computed separately and enters the 3D HI power spectra, not `W_HI()` itself.

### W_γ^BL_Lac, W_γ^FSRQ, W_γ^mAGN, W_γ^SFG — Astrophysical gamma-ray sources

```
config.py (spectral indices α, L_min, L_max, F_sens)
    │
cosmology.py: d_L(z)
    │
astro_sources.py:
    ├─ L_sens(z)           ← 4π d_L² F_sens
    ├─ glf(L, z, source)   ← dispatches to source-specific GLF
    │   ├─ _FSRQ_PARAMS    ← LDDE, [Ajello+ (2012)](literature/ajello2012.md) Table 3
    │   ├─ _BL_LAC_PARAMS  ← LDDE inverse-sum, [Ajello+ (2014)](literature/ajello2014.md) Table 3 (LDDE1)
    │   ├─ _glf_mAGN       ← Radio→Gamma chain (Eq. 5.11):
    │   │   [Willott (2001)](literature/willott2001.md) RLF
    │   │   → [Inoue (2011)](literature/inoue2011.md) freq scaling
    │   │   → [Lara (2004)](literature/lara2004.md) core-total
    │   │   → [Di Mauro (2014)](literature/dimauro2014.md) L_γ-L_r
    │   └─ _glf_SFG        ← IR→Gamma chain (Eq. 5.15):
    │       [Gruppioni (2013)](literature/gruppioni2013.md) 3-component IR LF
    │       → [Ackermann (2012)](literature/ackermann2012_sfg.md) L_γ-L_IR
    │
    └─ W_gamma_astro(E, z) ← 1/(4π h³) × ∫ Φ(L,z) × L/I_α × E_rest^{-α} dL
                               [pipeline photon-emissivity form in (Mpc/h)^-3]
```

**Survey-dependent element:** Integration upper limit `min(L_max, L_sens(z))` uses Fermi-LAT sensitivity. Two modes:
- `unresolved_mode='forecast'`: constant F_sens = 10⁻¹⁰ cm⁻²s⁻¹ ([Pinetti+ 2020](literature/pinetti2020.md))
- `unresolved_mode='data'`: energy-dependent F_sens(E) scaled by PSF area ([Ammazzalorso+ 2018](literature/ammazzalorso2018.md))
- `unresolved_only=False`: survey-independent total emission

### W_γ^DM — Dark matter annihilation

```
config.py (Ω_DM, σ_v, m_χ)
    │
    ├─ pppc4dmid.py: dN/dE(E_rest, m_χ, channel)  ← [Cirelli+ (2011)](literature/cirelli2011.md) tables
    ├─ ebl.py: exp(-τ(E,z))                         ← Dominguez+ (2011)
    │
halo_model.py: dndM, bias, R_vir, concentration
    │
dm_model.py:
    ├─ rho2_integral(M,z)    ← analytic ∫ ρ_NFW² d³x
    ├─ boost_moline(M,z)     ← [Moliné+ (2017)](literature/moline2017.md)
    ├─ clumping_factor(z)    ← Δ²(z) = ∫ dndM × (1+B) × ∫ρ² d³x dM / ρ̄²
    │                           [Pinetti Eq. 4.2]
    └─ W_gamma_DM(E, z)     ← (σv/8π)(ρ_DM/m_χ)²(1+z)³ × Δ² × dN/dE × e^{-τ}
                                [pipeline per-χ form; no baked-in 1/H]
```

**Survey-independent:** No instrument parameters. Depends only on DM physics (m_χ, σv, channel) and cosmology.

### How windows combine in the Limber integral

```
angular_power.py: C_ℓ^{HI×γ}
    │
    ├─ weight = (dχ/dz) / χ² × dz     ← standard Limber
    ├─ W_HI(χ) × W_γ(χ)               ← window product
    ├─ P_cross(k=(ℓ+½)/χ, z)          ← halo model 3D power spectrum
    │   ├─ P_HI_DM_2h (for DM)        ← Eqs. 5.1–5.2
    │   └─ P_HI_astro_2h (for astro)  ← Eqs. 5.3–5.4
    │
    └─ C_ℓ = Σ_z weight × W_HI × W_γ × P_cross
```

## External Data

| Directory | Contents | Source |
|-----------|----------|--------|
| `data/pppc4dmid/` | `AtProduction_gammas.dat` (3.9 MB) | PPPC4DMID via GitHub mirror |
| `data/ebl/` | Loaded at runtime via `ebltable` | [Dominguez et al. (2011)](literature/dominguez2011.md) |

## Key Dependencies

- `numpy`, `scipy`, `matplotlib` — core numerics and plotting
- `camb` — Boltzmann solver for linear matter power spectrum
- `hmf` — halo mass function computation (SMT, Tinker, etc.)
- `ebltable` — EBL opacity models
- `astropy` — cosmological constants and unit conversions
