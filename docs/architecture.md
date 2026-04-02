# Pipeline Architecture

## Data Flow

```
                        ┌─────────────┐
                        │  config.py  │  Planck 2018 params, instrument specs,
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
     └───┬────┘  │ LDDE GLFs (4)   │
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
               ┌─────────┼──────────┐
               ▼                    ▼
        ┌─────────────┐     ┌─────────────────────────────┐
        │validation.py│     │notebooks/                   │
        │ Phase 1-6   │     │  pipeline_validation.ipynb  │
        │ Step 5 (13  │     │  8 figures, inline plots    │
        │  checks)    │     │  SNR table, exclusion curves│
        └─────────────┘     └─────────────────────────────┘
```

**Summary:** Config → Cosmology + Tables → Halo model (via hmf) → HI / DM / Astro tracers → 3D power spectra → Limber C_ℓ → Statistics (SNR, exclusion) → Plots / Validation

## Module Descriptions

| Module | Role |
|--------|------|
| `config.py` | All physical constants, Planck 2018 cosmology, instrument specs (MeerKAT/SKA/Fermi), computational grids |
| `cosmology.py` | CAMB wrapper for P_lin(k,z); Hubble rate H(z), comoving distance χ(z), growth factor D(z) |
| `hmf_interface.py` | Thin wrapper around the `hmf` package; cached MassFunction instances, σ(M), dn/dM |
| `halo_model.py` | Virial radius R_vir, circular velocity v_c, halo bias b(M), concentration c(M), NFW Fourier transform ũ(k\|M) |
| `hi_model.py` | HI mass M_HI(M,z), altered NFW HI profile, Ω_HI, b_HI, T̄_b, HI power spectra P_HI^{1h/2h}, window W_HI |
| `dm_model.py` | NFW ρ² profile and Fourier transform ṽ(k\|M), substructure boost B(M), clumping factor Δ², DM window W_γ^DM, DM power spectra |
| `astro_sources.py` | LDDE gamma-ray luminosity functions for BL Lac, FSRQ, mAGN, SFG; astrophysical window W_γ^astro; mean UGRB intensity |
| `pppc4dmid.py` | PPPC4DMID photon yield table reader/interpolator; dN/dE for bb̄, τ⁺τ⁻, WW channels |
| `ebl.py` | EBL opacity τ(E,z) via `ebltable` package (Dominguez+2011); analytic fallback |
| `noise_model.py` | Radio noise (dish + interferometer), beam functions, Fermi-LAT noise N^γ and PSF, Fermissimo specs |
| `angular_power.py` | 3D cross-power spectra P_{HI×DM}, P_{HI×astro}; Limber integration for C_ℓ; HI auto-power C_ℓ^{HI,HI} |
| `statistics.py` | Gaussian variance ΔC_ℓ, signal-to-noise ratio, Δχ² test statistic, DM exclusion curves σ_v(m_χ) |
| `validation.py` | Automated checks against Pinetti et al. (2020): σ₈, mass function, Ω_HI, EBL, PPPC4DMID, SNR forecasts (13 checks) |
| `notebooks/pipeline_validation.ipynb` | Jupyter notebook with 8 inline figures: HI model, UGRB spectrum, EBL/PPPC, noise/beam, C_ℓ, windows, SNR table, exclusion curves |

## External Data

| Directory | Contents | Source |
|-----------|----------|--------|
| `data/pppc4dmid/` | `AtProduction_gammas.dat` (3.9 MB) | PPPC4DMID via GitHub mirror |
| `data/ebl/` | Loaded at runtime via `ebltable` | Dominguez et al. (2011) |

## Key Dependencies

- `numpy`, `scipy`, `matplotlib` — core numerics and plotting
- `camb` — Boltzmann solver for linear matter power spectrum
- `hmf` — halo mass function computation (SMT, Tinker, etc.)
- `ebltable` — EBL opacity models
- `astropy` — cosmological constants and unit conversions
