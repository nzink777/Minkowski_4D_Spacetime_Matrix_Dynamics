"""
parameters.py
=============
Physical Constants, Astrochemical Observational Data, and T7->M4 Projection
Parameters for the Asymmetric Density Filter / Syntax Gate Simulation.
"""

import numpy as np

# -----------------------------------------------------------------------------
# 1. PHYSICAL & TOPOLOGICAL CONSTANTS
# -----------------------------------------------------------------------------
C_LIGHT = 2.99792458e8             # Speed of light in vacuum (m/s)
H_PLANCK = 6.62607015e-34          # Planck constant (J*s)
ORTHOGONAL_PHASE = np.pi / 2.0     # 90-degree projection angle (\sqrt{-1})

# -----------------------------------------------------------------------------
# 2. ASTROCHEMICAL OBSERVATIONAL DATA (WD 1856 b METHANE FILTER)
# -----------------------------------------------------------------------------
# Fundamental vibrational modes of CH4 (Methane)
METHANE_SPECTRUM = {
    "nu_3_asymmetric_stretch": {
        "wavelength_um": 3.32,
        "frequency_hz": 90.3e12,    # ~90.3 THz
        "description": "Primary high-density chromatic filter line"
    },
    "nu_4_bending_mode": {
        "wavelength_um": 7.66,
        "frequency_hz": 39.1e12,    # ~39.1 THz
        "description": "Secondary thermalization filter line"
    },
    "nir_overtone_1": {
        "wavelength_um": 1.60,
        "frequency_hz": 187.37e12,
        "description": "Near-Infrared transit depth marker"
    },
    "nir_overtone_2": {
        "wavelength_um": 2.20,
        "frequency_hz": 136.27e12,
        "description": "Near-Infrared overtone marker"
    }
}

# Selected target frequency for initial PyMeep run
TARGET_MODE = "nu_3_asymmetric_stretch"
TARGET_FREQ_HZ = METHANE_SPECTRUM[TARGET_MODE]["frequency_hz"]
TARGET_WAVELENGTH_UM = METHANE_SPECTRUM[TARGET_MODE]["wavelength_um"]

# -----------------------------------------------------------------------------
# 3. GLIMPSE-17775 WHITE HOLE / T7 INFLUX BOUNDARY PARAMETERS
# -----------------------------------------------------------------------------
T7_INFLUX_PARAMS = {
    "kappa_00": 1.0,               # Temporal resonance amplitude
    "coupling_constant_kappa": 0.15, # T7 -> M4 coupling factor
    "decay_length_um": {
        "lambda_x": 0.50,          # Attenuation length along x (microns)
        "lambda_y": 0.50,          # Attenuation length along y (microns)
        "lambda_z": 1.20           # Attenuation length along z (microns)
    },
    "source_bandwidth_hz": 50.0e12 # Broad-band chaotic noise bandwidth
}

# -----------------------------------------------------------------------------
# 4. PYMEEP GRID CONFIGURATION
# -----------------------------------------------------------------------------
GRID_CONFIG = {
    "resolution": 30,              # Pixels per micron
    "cell_size_um": [4.0, 4.0, 4.0], # Computational domain (x, y, z) in um
    "pml_thickness_um": 0.5,       # Perfectly Matched Layer boundary thickness
    "runtime_fs": 100.0            # Total simulation runtime in femtoseconds
}
