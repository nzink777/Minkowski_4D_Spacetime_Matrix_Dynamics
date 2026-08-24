"""
fdtd_simulation.py
==================
FDTD Simulation engine modeling localized topological stress (the pinch)
and the orthogonal T7 energy influx tensor into Minkowski spacetime (M4).
"""

import numpy as np

# Robust import handling for standalone execution and pytest/CI environments
try:
    import meep as mp
except ImportError:
    mp = None

try:
    import src.parameters as p
except ModuleNotFoundError:
    import parameters as p

try:
    from src.boundary_conditions import dynamic_kappa
except ModuleNotFoundError:
    from boundary_conditions import dynamic_kappa


def construct_coupling_decay_tensor(r_coords):
    """
    Computes the complex tensor kappa_mu_nu(r) = diag(kappa_00, kappa_11*e^(-r/lx), ...)
    representing the orthogonal T7 energy influx into M4.
    """
    rx, ry, rz = r_coords
    lx = p.T7_INFLUX_PARAMS["decay_length_um"]["lambda_x"]
    ly = p.T7_INFLUX_PARAMS["decay_length_um"]["lambda_y"]
    lz = p.T7_INFLUX_PARAMS["decay_length_um"]["lambda_z"]
    
    # Real temporal resonance
    k00 = p.T7_INFLUX_PARAMS["kappa_00"]
    
    # Imaginary spatial decay components (orthogonal phase shift e^(i * pi/2) = 1j)
    k11 = np.exp(-abs(rx) / lx) * np.exp(1j * p.ORTHOGONAL_PHASE)
    k22 = np.exp(-abs(ry) / ly) * np.exp(1j * p.ORTHOGONAL_PHASE)
    k33 = np.exp(-abs(rz) / lz) * np.exp(1j * p.ORTHOGONAL_PHASE)
    
    return np.diag([k00, k11, k22, k33])


def run_topological_pinch_sim(resolution: int = 20, domain_size: float = 10.0, sigma_scatter: float = 0.8):
    """
    Initializes a Finite-Difference Time-Domain (FDTD) simulation 
    modeling localized topological stress (the pinch) in a 2D M4 slice.
    """
    if mp is None:
        print("[WARN] PyMeep (meep) is not installed. Simulation execution skipped.")
        return None

    # Convert CH4 target wavelength (um) to Meep internal frequency units (1/um)
    meep_freq = 1.0 / p.TARGET_WAVELENGTH_UM
    meep_fwidth = (p.T7_INFLUX_PARAMS["source_bandwidth_hz"] / p.C_LIGHT) * 1e-6

    cell = mp.Vector3(domain_size, domain_size, 0)
    
    # Define the T7 energy injection source (The White Hole / Pinch)
    sources = [
        mp.Source(
            src=mp.ContinuousSource(frequency=meep_freq),
            component=mp.Ez,
            center=mp.Vector3(0, 0, 0),
            amplitude=1.0 + 1j * p.T7_INFLUX_PARAMS["coupling_constant_kappa"]
        )
    ]
    
    # Methane molecular syntax filter medium susceptibility
    ch4_medium = mp.Medium(
        epsilon=1.0,
        E_susceptibilities=[
            mp.LorentzianSusceptibility(
                frequency=meep_freq,
                gamma=meep_fwidth * 0.1,
                sigma=p.T7_INFLUX_PARAMS["coupling_constant_kappa"]
            )
        ]
    )

    # Initialize the rigid voxel environment
    sim = mp.Simulation(
        cell_size=cell,
        boundary_layers=[mp.PML(1.0)],
        geometry=[],
        sources=sources,
        resolution=resolution,
    )
    
    # Run simulation for Planck ticks
    sim.run(until=200)
    print("Simulation complete. Data ready for HDF5 extraction.")
    return sim


if __name__ == '__main__':
    run_topological_pinch_sim(resolution=20, domain_size=10.0, sigma_scatter=0.8)
    
