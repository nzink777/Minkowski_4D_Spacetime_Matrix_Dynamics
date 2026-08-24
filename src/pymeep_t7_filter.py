"""
pymeep_t7_filter.py
===================
FDTD Simulation engine for the Asymmetric Density Filter.
Loads real-world parameters from parameters.py and executes the T7->M4
coupling decay tensor kappa_mu_nu mapping.
"""

import numpy as np
import meep as mp
import parameters as p

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

def run_pymeep_simulation():
    """Configures and runs the PyMeep FDTD grid using parameters.py inputs."""
    cell = mp.Vector3(*p.GRID_CONFIG["cell_size_um"])
    pml = [mp.PML(p.GRID_CONFIG["pml_thickness_um"])]
    res = p.GRID_CONFIG["resolution"]

    # Convert CH4 target wavelength (um) to Meep internal frequency units (1/um)
    meep_freq = 1.0 / p.TARGET_WAVELENGTH_UM
    meep_fwidth = (p.T7_INFLUX_PARAMS["source_bandwidth_hz"] / p.C_LIGHT) * 1e-6

    # Model the T7 chaotic white hole flux as an orthogonal complex source
    sources = [
        mp.Source(
            src=mp.GaussianSource(frequency=meep_freq, fwidth=meep_fwidth),
            component=mp.Ex,
            center=mp.Vector3(0, 0, -1.5),
            amplitude=1.0 + 1j * p.T7_INFLUX_PARAMS["coupling_constant_kappa"]
        )
    ]

    # Material properties containing anisotropic susceptibility from kappa_mu_nu
    # Methane molecular syntax filter medium
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

    # Geometry: Molecular filter layer in central M4 domain
    geometry = [
        mp.Block(
            center=mp.Vector3(0, 0, 0),
            size=mp.Vector3(2.0, 2.0, 0.5),
            material=ch4_medium
        )
    ]

    sim = mp.Simulation(
        cell_size=cell,
        boundary_layers=pml,
        geometry=geometry,
        sources=sources,
        resolution=res
    )

    print(f"[INFO] Initializing T7->M4 Grid Simulation.")
    print(f"[INFO] Target Mode: {p.TARGET_MODE} ({p.TARGET_WAVELENGTH_UM} um)")
    print(f"[INFO] Coupling Constant (kappa): {p.T7_INFLUX_PARAMS['coupling_constant_kappa']}")

    sim.run(until=p.GRID_CONFIG["runtime_fs"])
    return sim

if __name__ == "__main__":
    # Test tensor generation
    sample_r = (0.1, 0.1, 0.5)
    tensor = construct_coupling_decay_tensor(sample_r)
    print("Coupling Decay Tensor kappa_mu_nu at r=(0.1, 0.1, 0.5):")
    print(np.round(tensor, 4))
    
    # Run PyMeep FDTD execution
    # sim_instance = run_pymeep_simulation()
  
