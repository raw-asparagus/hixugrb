"""HI 21-cm × Gamma-Ray Cross-Correlation Pipeline.

Computes angular cross-correlation power spectra between HI intensity maps
and Fermi-LAT gamma-ray maps, forecasts SNR, and derives WIMP DM constraints.
Validates against Pinetti, Camera, Fornengo & Regis (2020, arXiv:1911.04989).
"""

from .config import (
    HiBrightness,
    UnresolvedMode,
    AnalysisMode,
    TSysModel,
    BoostScenario,
    Channel,
    EBLModel,
)

__all__ = [
    "HiBrightness",
    "UnresolvedMode",
    "AnalysisMode",
    "TSysModel",
    "BoostScenario",
    "Channel",
    "EBLModel",
]
