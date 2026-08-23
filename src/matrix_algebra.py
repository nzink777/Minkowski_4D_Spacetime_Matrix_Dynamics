import numpy as np
from scipy.linalg import expm

def get_gell_mann_matrices():
    """
    Returns the standard set of 8 SU(3) Gell-Mann matrices.
    These act as the fundamental generators T^a for internal voxel collection symmetries.
    """
    l1 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
    l2 = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
    l3 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
    l4 = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
    l5 = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
    l6 = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
    l7 = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
    l8 = (1 / np.sqrt(3)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex)
    return [l1, l2, l3, l4, l5, l6, l7, l8]

def calculate_voxel_swap(V_A: np.ndarray, theta: float, a_index: int) -> np.ndarray:
    """
    Transforms voxel Collection A to Collection B across a single Planck tick
    using a specific SU(3) generator component T^a.
    
    Args:
        V_A: Initial Minkowski 4D voxel state matrix.
        theta: The phase angle (topological stress scalar).
        a_index: Index of the generator (0 to 7).
        
    Returns:
        V_B: The resulting voxel state matrix after the continuous symmetry swap.
    """
    generators = get_gell_mann_matrices()
    if not (0 <= a_index < len(generators)):
        raise ValueError("Generator index must be between 0 and 7 for SU(3).")
    
    T_a = generators[a_index]
    # Lie algebra transformation: |V_B> = exp(i * theta_a * T^a) |V_A>
    operator_matrix = expm(1j * theta * T_a)
    V_B = np.dot(operator_matrix, V_A)
    return V_B
    
