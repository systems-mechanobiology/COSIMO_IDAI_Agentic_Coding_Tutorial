import numpy as np
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import Tuple, List, Final
import sys
import os

# Ensure we can import from local modules if running as script
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from model import sir_derivatives
# Note: updating imports to match new visualize.py API
from visualize import plot_simulation_fig, plot_sensitivity_fig, save_figure
from config import SimulationConfig, VisualizationConfig

@dataclass
class SimulationStats:
    peak_infection: float
    peak_day: float
    final_recovered: float

def simulate_sir(config: SimulationConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Runs the SIR simulation based on the provided configuration.
    
    Returns:
        Tuple[t, S, I, R] arrays.
    """
    t = np.linspace(0, config.duration, config.duration)
    y0 = [config.S0, config.I0, config.R0]
    
    ret = odeint(sir_derivatives, y0, t, args=(config.N, config.beta, config.gamma))
    S, I, R = ret.T
    return t, S, I, R

def compute_stats(t: np.ndarray, I: np.ndarray, R: np.ndarray) -> SimulationStats:
    """Computes summary statistics from simulation results."""
    peak_idx = np.argmax(I)
    return SimulationStats(
        peak_infection=I[peak_idx],
        peak_day=t[peak_idx],
        final_recovered=R[-1]
    )

def run_simulation() -> None:
    """Sets up and runs the SIR epidemic simulation."""
    sim_config = SimulationConfig()
    viz_config = VisualizationConfig()
    
    # Run Simulation
    t, S, I, R = simulate_sir(sim_config)
    stats = compute_stats(t, I, R)
    
    # Print Summary
    print(f"Simulation Summary:")
    print(f"Peak Infection: {stats.peak_infection:.2f} people")
    print(f"Time to Peak:   {stats.peak_day:.2f} days")
    print(f"Final Recovered: {stats.final_recovered:.2f} people")
    
    # Visualize
    fig = plot_simulation_fig(t, S, I, R, sim_config.beta, sim_config.gamma, viz_config)
    save_figure(fig, viz_config.simulation_plot_name, viz_config)

def run_sensitivity_analysis() -> None:
    """Runs the SIR model for a range of beta values and plots sensitivity."""
    print("\nRunning Sensitivity Analysis...")
    config = SimulationConfig()
    viz_config = VisualizationConfig()
    
    start, stop, count = config.beta_sweep_range
    betas = np.linspace(start, stop, count)
    peak_infections = []
    peak_times = []
    
    for beta in betas:
        # Create temp config for this run
        temp_config = SimulationConfig(beta=beta)
        t, S, I, R = simulate_sir(temp_config)
        stats = compute_stats(t, I, R)
        
        peak_infections.append(stats.peak_infection)
        peak_times.append(stats.peak_day)
        
    # Visualize
    fig = plot_sensitivity_fig(betas, peak_infections, peak_times, viz_config)
    save_figure(fig, viz_config.sensitivity_plot_name, viz_config)

if __name__ == "__main__":
    run_simulation()
    run_sensitivity_analysis()
