import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from boundary_conditions import dynamic_kappa, calculate_velocity_dispersion

def test_dynamic_kappa_decay():
    # Kappa should be mathematically higher closer to the pinch (r=0.1) than further away (r=10.0)
    kappa_close = dynamic_kappa(r=0.1, kappa_m4=1.0, phi_7d=10.0, sigma_scatter=0.8)
    kappa_far = dynamic_kappa(r=10.0, kappa_m4=1.0, phi_7d=10.0, sigma_scatter=0.8)
    assert kappa_close > kappa_far

def test_velocity_dispersion():
    # Simple sanity check for the Doppler broadening formula
    v = calculate_velocity_dispersion(lambda_center=2.955, delta_lambda=0.04)
    assert v > 0
  
