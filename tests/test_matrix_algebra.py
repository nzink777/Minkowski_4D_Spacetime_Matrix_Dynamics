import numpy as np
import sys
import os
# Ensure pytest can find our src module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from matrix_algebra import get_gell_mann_matrices, calculate_voxel_swap

def test_gell_mann_matrices_count():
    matrices = get_gell_mann_matrices()
    assert len(matrices) == 8
    assert matrices[0].shape == (3, 3)

def test_voxel_swap_identity():
    # A zero phase angle (theta=0, no topological stress) should result in no change.
    V_A = np.array([1, 0, 0])
    V_B = calculate_voxel_swap(V_A, theta=0.0, a_index=0)
    np.testing.assert_array_almost_equal(V_A, V_B)
  
