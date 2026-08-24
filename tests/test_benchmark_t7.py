"""
test_benchmark_t7.py
====================
Performance benchmarks for the T7 -> M4 coupling decay tensor generation.
"""

import pytest
import numpy as np
from src.fdtd_simulation import construct_coupling_decay_tensor

def test_coupling_decay_tensor_benchmark(benchmark):
    """
    Measures execution time for generating the 4x4 complex 
    coupling decay tensor kappa_mu_nu(r).
    """
    sample_r = (0.1, 0.1, 0.5)
    
    # Benchmark the tensor generation function
    result = benchmark(construct_coupling_decay_tensor, sample_r)
    
    # Assert correctness alongside performance
    assert result.shape == (4, 4)
    assert np.iscomplexobj(result)
  
