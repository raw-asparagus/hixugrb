"""Central parameter store for the HI × gamma-ray cross-correlation pipeline.

All physical constants, cosmological parameters, halo model parameters,
instrument specifications, and computational grids are defined here.

Convention: internal calculations use h-dependent cosmological units
  - Distances in Mpc/h (comoving)
  - Masses in M_sun/h
  - Wavenumbers in h/Mpc
  - Densities in (M_sun/h) / (Mpc/h)^3
Physical (SI/CGS) units are used only at interfaces (e.g., instrument noise).
"""

import numpy as np

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8          # Speed of light [m/s]
C_LIGHT_KM_S = 2.99792458e5    # Speed of light [km/s]
G_NEWTON = 6.67430e-11          # Newton's constant [m^3 kg^-1 s^-2]
M_SUN = 1.98848e30              # Solar mass [kg]
MPC_TO_M = 3.0856775814913673e22  # 1 Mpc in meters
KPC_TO_M = 3.0856775814913673e19  # 1 kpc in meters
KM_TO_MPC = 1.0 / (MPC_TO_M / 1e3)  # km to Mpc
ERG_TO_GEV = 624.151            # 1 erg in GeV
GEV_TO_ERG = 1.0 / ERG_TO_GEV  # 1 GeV in erg
CM2_TO_M2 = 1e-4               # cm^2 to m^2
SR_TO_DEG2 = (180.0 / np.pi)**2  # 1 sr in deg^2

# ---------------------------------------------------------------------------
# Planck 2018 cosmological parameters (TT,TE,EE+lowE+lensing)
# ---------------------------------------------------------------------------
H0 = 67.36                     # Hubble constant [km/s/Mpc]
h = H0 / 100.0                 # Dimensionless Hubble parameter
OMEGA_B_H2 = 0.02237           # Physical baryon density
OMEGA_CDM_H2 = 0.1200          # Physical CDM density
N_S = 0.9649                   # Scalar spectral index
SIGMA_8 = 0.8111               # RMS matter fluctuations at 8 Mpc/h
A_S = 2.1e-9                   # Scalar amplitude (approximate)
OMEGA_M = 0.3153               # Total matter density parameter
OMEGA_B = OMEGA_B_H2 / h**2    # Baryon density parameter
OMEGA_CDM = OMEGA_CDM_H2 / h**2  # CDM density parameter
OMEGA_DM = OMEGA_M - OMEGA_B   # DM density parameter (CDM ≈ DM here)
OMEGA_LAMBDA = 1.0 - OMEGA_M   # Dark energy density (flat universe)
T_CMB = 2.7255                  # CMB temperature today [K]

# Derived cosmological quantities
# Critical density today: rho_c = 3 H0^2 / (8 pi G)  [kg/m^3]
RHO_CRIT_SI = 3.0 * (H0 * 1e3 / MPC_TO_M)**2 / (8.0 * np.pi * G_NEWTON)
# Convert to M_sun/h / (Mpc/h)^3:
# RHO_CRIT_SI [kg/m^3] → [M_sun/Mpc^3] via * MPC_TO_M^3 / M_SUN
# Then [M_sun/Mpc^3] → [M_sun/h / (Mpc/h)^3] via / h^2
# because 1 M_sun/Mpc^3 = h^{-2} (M_sun/h)/(Mpc/h)^3
RHO_CRIT = RHO_CRIT_SI * MPC_TO_M**3 / M_SUN / h**2  # [M_sun/h / (Mpc/h)^3]
RHO_BAR = OMEGA_M * RHO_CRIT   # Mean comoving matter density [M_sun/h / (Mpc/h)^3]

# ---------------------------------------------------------------------------
# Sheth-Mo-Tormen / Sheth-Tormen halo model parameters
# ---------------------------------------------------------------------------
DELTA_C = 1.686                 # Spherical collapse threshold
SMT_Q = 0.707                  # SMT parameter q
SMT_P = 0.3                    # SMT parameter p
SMT_A = 0.3222                 # SMT normalization A
DELTA_VIR_FIXED = 200.0        # Legacy fixed overdensity (M_200c definition)

# ---------------------------------------------------------------------------
# HI model parameters (Padmanabhan, Refregier & Amara 2017, Table A1)
# Modified NFW profile fit — all parameters from the same MCMC fit.
# ---------------------------------------------------------------------------
HI_ALPHA = 0.176               # Normalization (Table A1, modified NFW)
HI_BETA = -0.69                # Mass slope (Table A1)
HI_VC0 = 10**1.61              # Minimum circular velocity cutoff [km/s] ≈ 40.7 (Table A1)
HI_C0 = 139.0                  # HI concentration normalization (Table A1)
HI_GAMMA_CONC = 0.13           # Concentration redshift evolution exponent (Table A1)
Y_P = 0.24                     # Primordial helium mass fraction
F_HC = (1.0 - Y_P) * OMEGA_B / OMEGA_M  # Cosmic hydrogen fraction in halos

# ---------------------------------------------------------------------------
# Astrophysical gamma-ray source parameters (Pinetti et al. Table 3)
# ---------------------------------------------------------------------------
ASTRO_SOURCES = {
    'BL_Lac': {
        'alpha': 2.11,          # Spectral index
        'L_min': 7e43,          # Min luminosity [erg/s]
        'L_max': 1e52,          # Max luminosity [erg/s]
        'glf_ref': 'Ajello+2014',
    },
    'FSRQ': {
        'alpha': 2.44,
        'L_min': 1e44,
        'L_max': 1e52,
        'glf_ref': 'Ajello+2012',
    },
    'mAGN': {
        'alpha': 2.37,
        'L_min': 1e40,
        'L_max': 1e50,
        'glf_ref': 'DiMauro+2014',
    },
    'SFG': {
        'alpha': 2.7,
        'L_min': 1e37,
        'L_max': 1e42,
        'glf_ref': 'Gruppioni+2013',
    },
}

# Fermi-LAT flux sensitivity threshold [cm^{-2} s^{-1}] (1-100 GeV)
F_SENS = 1e-10

# Thermal relic cross-section [cm^3/s]
SIGMA_V_THERMAL = 3e-26

# ---------------------------------------------------------------------------
# Moliné et al. (2017) boost factor polynomial coefficients
# Eq. 18, Table 3: alpha=2, with tidal stripping, c_200 concentration
# log10 B(M, z=0) = sum_i b_i [log10(M/M_sun)]^i
# Valid for 10^{-6} < M [M_sun] < 10^{15}
# ---------------------------------------------------------------------------
MOLINE_BOOST_COEFFS = [-0.186, 0.144, -8.8e-3, 1.13e-3, -3.7e-5, -2e-7]

# Solar luminosity [erg/s]
L_SUN = 3.828e33

# ---------------------------------------------------------------------------
# mAGN: Willott et al. (2001) Radio Luminosity Function parameters
# Table 1 Model C at 151 MHz, H0=50 km/s/Mpc, Omega_M=0, Omega_Lambda=0
# ---------------------------------------------------------------------------
H0_WILLOTT = 50.0                   # km/s/Mpc
WILLOTT_RHO_L_STAR = 10**(-7.523)   # Mpc^{-3} (Willott cosmology)
WILLOTT_BETA_L = 0.586
WILLOTT_L_L_STAR = 10**26.48        # W/Hz at 151 MHz
WILLOTT_K_L = 3.48
WILLOTT_Z_L_STAR = 0.710
WILLOTT_RHO_H_STAR = 10**(-6.757)   # Mpc^{-3}
WILLOTT_BETA_H = 2.42
WILLOTT_L_H_STAR = 10**27.39        # W/Hz at 151 MHz
WILLOTT_Z_H_STAR = 2.03
WILLOTT_Z_H0_LO = 0.568             # Gaussian width z < z_h*
WILLOTT_Z_H0_HI = 0.956             # Gaussian width z >= z_h*

# ---------------------------------------------------------------------------
# mAGN: Lara et al. (2004) core-total radio luminosity relation
# log L_core^{5GHz} = LARA_A + LARA_B * log L_tot^{1.4GHz}  [W/Hz]
# ---------------------------------------------------------------------------
LARA_A = 4.2
LARA_B = 0.77

# ---------------------------------------------------------------------------
# mAGN: Di Mauro et al. (2014) gamma-radio-core correlation
# log L_gamma [erg/s] = DIMAURO_A + DIMAURO_B * log L_core [W/Hz]
# ---------------------------------------------------------------------------
DIMAURO_GAMMA_RADIO_A = 2.0
DIMAURO_GAMMA_RADIO_B = 1.008
DIMAURO_K = 3.05                     # beaming/duty-cycle factor
RADIO_ALPHA = 0.80                   # Inoue (2011) spectral index

# ---------------------------------------------------------------------------
# SFG: Gruppioni et al. (2013) modified Schechter IR LF parameters (Table C.2)
# ---------------------------------------------------------------------------
GRUPPIONI_PARAMS = {
    'spiral': {
        'gamma': 1.0, 'sigma': 0.50,
        'log_Lstar': 9.78,    # log10(L*/L_sun)
        'log_phistar': -2.12, # log10(phi*/Mpc^{-3})
        'k_L': 4.49,
        'k_R1': -0.54, 'k_R2': -7.13,
    },
    'starburst': {
        'gamma': 1.0, 'sigma': 0.35,
        'log_Lstar': 11.17,
        'log_phistar': -4.46,
        'k_L': 1.96,
        'k_R1': 3.79, 'k_R2': -1.06,
    },
    'sf_agn': {
        'gamma': 1.2, 'sigma': 0.40,
        'log_Lstar': 10.80,
        'log_phistar': -3.20,
        'k_L': 3.17,
        'k_R1': 0.67, 'k_R2': -3.17,
    },
}

# ---------------------------------------------------------------------------
# SFG: Ackermann et al. (2012) L_gamma - L_IR scaling
# log10(L_{0.1-100GeV} / erg s^-1) = alpha * log10(L_IR / 10^10 L_sun) + beta
# ---------------------------------------------------------------------------
ACKERMANN_ALPHA_IR = 1.09
ACKERMANN_BETA_IR = 39.19

# ---------------------------------------------------------------------------
# Mass-luminosity relations for halo bias
# ---------------------------------------------------------------------------
# mAGN: Di Mauro (2014) Eqs. C.20-C.21
MAGN_MSTAR_NORM = 1e9               # M_sun
MAGN_MSTAR_LNORM = 1e48             # erg/s
MAGN_MSTAR_SLOPE = 0.36
MAGN_MHALO_PIVOT = 10**8.8          # M_sun
MAGN_MHALO_SLOPE = 0.645
MAGN_MHALO_Z_EXP = 1.4
# SFG: Eq. C.29
SFG_MHALO_NORM = 1e12               # M_sun
SFG_MHALO_LNORM = 6.8e39            # erg/s
SFG_MHALO_SLOPE = 0.92
SFG_MHALO_Z_EXP = 1.61

# ---------------------------------------------------------------------------
# Fermi-LAT energy bins (Pinetti et al. Table 2)
# Columns: E_min [GeV], E_max [GeV], N^gamma [cm^{-4} s^{-2} sr^{-1}],
#           f_sky, sigma_0 [deg], E_b [GeV]
# ---------------------------------------------------------------------------
FERMI_BINS = np.array([
    #  E_min    E_max      N_gamma         f_sky   sigma_0   E_b
    [  0.5,     1.0,      1.056e-17,      0.134,   0.87,    0.71  ],
    [  1.0,     1.7,      3.548e-18,      0.184,   0.50,    1.30  ],
    [  1.7,     2.8,      1.375e-18,      0.398,   0.33,    2.18  ],
    [  2.8,     4.8,      8.324e-19,      0.482,   0.22,    3.67  ],
    [  4.8,     8.3,      3.904e-19,      0.549,   0.15,    6.31  ],
    [  8.3,    14.5,      1.768e-19,      0.574,   0.11,   11.0   ],
    [ 14.5,    22.9,      6.899e-20,      0.574,   0.09,   18.2   ],
    [ 22.9,    39.8,      3.895e-20,      0.574,   0.07,   30.2   ],
    [ 39.8,    69.2,      1.576e-20,      0.574,   0.07,   52.5   ],
    [ 69.2,   120.2,      6.205e-21,      0.574,   0.06,   91.2   ],
    [120.2,   331.1,      3.287e-21,      0.597,   0.06,  199.5   ],
    [331.1,  1000.0,      5.094e-22,      0.597,   0.06,  575.4   ],
])

FERMI_E_MIN = FERMI_BINS[:, 0]     # [GeV]
FERMI_E_MAX = FERMI_BINS[:, 1]     # [GeV]
FERMI_N_GAMMA = FERMI_BINS[:, 2]   # [cm^{-4} s^{-2} sr^{-1}]
FERMI_F_SKY = FERMI_BINS[:, 3]
FERMI_SIGMA0 = FERMI_BINS[:, 4]    # PSF 68% containment [deg]
FERMI_E_B = FERMI_BINS[:, 5]       # Geometric bin center [GeV]
FERMI_N_BINS = len(FERMI_BINS)

# Fermi-LAT PSF parameterization (Eq. 4.11)
FERMI_E_REF = 0.5                  # Reference energy [GeV]
FERMI_SIGMA0_REF = 1.20            # sigma_0 at E_ref [deg]
FERMI_PSF_FLOOR = 0.05             # PSF floor [deg]

# ---------------------------------------------------------------------------
# Fermissimo (hypothetical next-gen gamma-ray telescope)
# ---------------------------------------------------------------------------
FERMISSIMO_EXPOSURE_FACTOR = 2.0    # 2x Fermi exposure
FERMISSIMO_PSF_ALPHA = 0.2          # PSF improvement factor
FERMISSIMO_PSF_FLOOR = 0.001        # PSF floor [deg]
FERMISSIMO_F_SKY = 0.8
FERMISSIMO_LSENS_FACTOR = 1.0 / np.sqrt(2.0)  # Sensitivity improvement

# ---------------------------------------------------------------------------
# Radio telescope specifications (Pinetti et al. Table 1)
# ---------------------------------------------------------------------------
RADIO_TELESCOPES = {
    'MeerKAT': {
        'survey_area_deg2': 4000.0,
        't_obs_hours': 4000.0,
        'n_dishes': 64,
        'd_dish_m': 13.5,
        'd_interf_km': 1.0,
        'n_beams': 1,
        'n_pol': 2,
        'eta': 1.0,
        'n_u': 0.0005,         # Baseline density parameter
        'bands': {
            'UHF': {'z_min': 0.4, 'z_max': 1.45},
            'L':   {'z_min': 0.0, 'z_max': 0.58},
        },
        'f_sky': 0.097,
    },
    'SKA1': {
        'survey_area_deg2': 25000.0,
        't_obs_hours': 10000.0,
        'n_dishes': 133 + 64,  # SKA1-MID + MeerKAT
        'd_dish_m': 14.5,
        'd_interf_km': 3.0,
        'n_beams': 1,
        'n_pol': 2,
        'eta': 1.0,
        'n_u': 0.005,
        'bands': {
            'Band1': {'z_min': 0.35, 'z_max': 3.0},
            'Band2': {'z_min': 0.0,  'z_max': 0.5},
        },
        'f_sky': 0.61,
    },
    'SKA2': {
        'survey_area_deg2': 30000.0,
        't_obs_hours': 10000.0,
        'n_dishes': 2000,
        'd_dish_m': 14.5,
        'd_interf_km': 10.0,
        'n_beams': 36,
        'n_pol': 2,
        'eta': 1.0,
        'n_u': 0.005,
        'bands': {
            'Band1': {'z_min': 0.35, 'z_max': 3.0},
            'Band2': {'z_min': 0.0,  'z_max': 0.5},
        },
        'f_sky': 0.72,
    },
}

# Radio system temperature model: T_sys = T_inst + T_sky
# T_sky = 60 * (300 MHz / nu)^2.55  [K]
# T_inst ~ 30 K (hardcoded constant in noise_model.T_sys)
T_SKY_COEFF = 60.0             # [K]
T_SKY_NU_REF = 300.0           # [MHz]
T_SKY_INDEX = 2.55

# HI 21-cm rest frequency
NU_21CM = 1420.405              # [MHz]
LAMBDA_21CM = 0.211061          # [m]

# ---------------------------------------------------------------------------
# Computational grids
# ---------------------------------------------------------------------------
# Wavenumber grid [h/Mpc]
K_MIN = 1e-4
K_MAX = 1e4
N_K = 500
K_GRID = np.logspace(np.log10(K_MIN), np.log10(K_MAX), N_K)

# Redshift grid (denser at low z for better resolution of window functions)
Z_MAX = 5.0
N_Z = 50
# Non-uniform: more points at low z
Z_GRID = np.concatenate([
    np.linspace(0.0, 0.5, 15),
    np.linspace(0.55, 1.5, 15),
    np.linspace(1.6, 3.0, 10),
    np.linspace(3.2, Z_MAX, 10),
])

# Halo mass grid [M_sun/h]
M_MIN = 1e-6    # WIMP free-streaming mass
M_MAX = 1e18    # Above supercluster scales
N_M = 200
M_GRID = np.logspace(np.log10(M_MIN), np.log10(M_MAX), N_M)

# HI-relevant mass range (M_HI is negligible below ~1e8)
M_MIN_HI = 1e8
M_MAX_HI = 1e16

# DM-relevant mass range (extends to free-streaming scale)
M_MIN_DM = 1e-6
M_MAX_DM = 1e18

# Multipole grid
ELL_MIN = 10
ELL_MAX = 1000
ELL_MAX_FERMISSIMO = 2000
N_ELL_PLOT = 50  # Log-spaced for plotting
ELL_PLOT = np.unique(np.logspace(
    np.log10(ELL_MIN), np.log10(ELL_MAX), N_ELL_PLOT
).astype(int))

# ---------------------------------------------------------------------------
# Ammazzalorso et al. (2018) energy bins and multipole ranges (Table I)
# Data-analysis-grade specifications for Fermi-LAT cross-correlation.
# Columns: E_min [GeV], E_max [GeV], l_min, l_max
# ---------------------------------------------------------------------------
AMMAZZALORSO_BINS = np.array([
    [  0.631,    1.202,   40,   220],
    [  1.202,    2.290,   40,   250],
    [  2.290,    4.786,   40,   307],
    [  4.786,    9.120,   40,   487],
    [  9.120,   17.38,    40,   695],
    [ 17.38,    36.31,    40,   907],
    [ 36.31,    69.18,    40,  1000],
    [ 69.18,   131.8,     40,  1000],
    [131.8,    275.4,     40,  1000],
    [275.4,    524.8,     40,  1000],
    [524.8,   1000.0,     40,  1000],
])

AMMAZZALORSO_E_MIN = AMMAZZALORSO_BINS[:, 0]
AMMAZZALORSO_E_MAX = AMMAZZALORSO_BINS[:, 1]
AMMAZZALORSO_ELL_MIN = AMMAZZALORSO_BINS[:, 2].astype(int)
AMMAZZALORSO_ELL_MAX = AMMAZZALORSO_BINS[:, 3].astype(int)
AMMAZZALORSO_E_B = np.sqrt(AMMAZZALORSO_E_MIN * AMMAZZALORSO_E_MAX)  # geometric mean
AMMAZZALORSO_N_BINS = len(AMMAZZALORSO_BINS)

# Minimum multipole for data-analysis (Ammazzalorso Sec. III)
FERMI_ELL_MIN = 40

# ---------------------------------------------------------------------------
# Fermi-LAT PSF: King function parameters for exact beam computation
# (Ammazzalorso Eq. 4)
#
# The PSF is modeled as a single King function with tail index gamma_king.
# sigma_king is calibrated from the 68% containment angle at each energy.
# For a King function: PSF(theta) = (1-1/gamma)/(2*pi*sigma^2) *
#                      [1 + theta^2/(2*gamma*sigma^2)]^{-gamma}
# ---------------------------------------------------------------------------
FERMI_PSF_GAMMA_KING = 2.0  # King function tail index (standard for Fermi)
