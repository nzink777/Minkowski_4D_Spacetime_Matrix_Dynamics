import numpy as np

def dynamic_kappa(r: float, kappa_m4: float, phi_7d: float, sigma_scatter: float, epsilon: float = 1e-5) -> float:
    r"""
    Calculates the fluid boundary condition for the topological coupling constant.
    
    Args:
        r: Radial distance from the topological pinch point.
        kappa_m4: The baseline stable coupling constant (derived from WD 1856 b).
        phi_7d: The mass-energy flux injected from the T7 manifold.
        sigma_scatter: Electron scattering cross-section (derived from GLIMPSE-17775 H-peak).
        epsilon: Regulatory parameter to prevent mathematical singularity at r=0.
        
    Returns:
        The localized coupling constant \kappa(r).
    """
    stress_decay = (phi_7d / (r**2 + epsilon**2)) * sigma_scatter
    return kappa_m4 + stress_decay

def calculate_velocity_dispersion(lambda_center: float, delta_lambda: float) -> float:
    r"""
    Extracts the velocity dispersion from the FWHM of a spectral peak.
    Uses the Doppler broadening formula: \Delta v = c * (\Delta \lambda / \lambda)
    """
    c_microns_per_sec = 2.9979e14 # Speed of light in microns/second
    return c_microns_per_sec * (delta_lambda / lambda_center)
    
