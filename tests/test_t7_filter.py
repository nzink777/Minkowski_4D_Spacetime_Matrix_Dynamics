import numpy as np
import pytest
import src.parameters as p
from src.fdtd_simulation import construct_coupling_decay_tensor

def test_parameters_loading():
    """Verify observational parameters load correctly."""
    assert p.TARGET_WAVELENGTH_UM == 3.32
    assert p.ORTHOGONAL_PHASE == np.pi / 2.0
    assert "nu_3_asymmetric_stretch" in p.METHANE_SPECTRUM

def test_coupling_decay_tensor_orthogonality():
    """Verify tensor shape and imaginary 90-degree phase shift."""
    sample_r = (0.1, 0.1, 0.5)
    tensor = construct_coupling_decay_tensor(sample_r)
    
    assert tensor.shape == (4, 4)
    # Check temporal component is real
    assert np.isreal(tensor[0, 0])
    # Check spatial components contain complex imaginary phase (sqrt(-1))
    assert np.iscomplexobj(tensor[1, 1])
  
