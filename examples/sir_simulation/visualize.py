import matplotlib.pyplot as plt
import numpy as np
from typing import List

def plot_simulation(t: np.ndarray, S: np.ndarray, I: np.ndarray, R: np.ndarray, beta: float, gamma: float) -> None:
    """
    Plots the SIR simulation results.

    Args:
        t (np.ndarray): Time points.
        S (np.ndarray): Susceptible population over time.
        I (np.ndarray): Infected population over time.
        R (np.ndarray): Recovered population over time.
        beta (float): Transmission rate used in simulation.
        gamma (float): Recovery rate used in simulation.
    """
    # Create results directory if it doesn't exist
    import os
    os.makedirs("results", exist_ok=True)

    # Use a clean style
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except OSError:
        # Fallback if specific style not available
        plt.style.use('ggplot')

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot lines with distinct colors and line widths
    ax.plot(t, S, label='Susceptible', color='#3498db', linewidth=2, alpha=0.8)
    ax.plot(t, I, label='Infected', color='#e74c3c', linewidth=2, alpha=0.8)
    ax.plot(t, R, label='Recovered', color='#2ecc71', linewidth=2, alpha=0.8)

    # Add labels and title
    ax.set_xlabel('Time (days)', fontsize=12)
    ax.set_ylabel('Population', fontsize=12)
    ax.set_title(f'SIR Model Simulation\n(β={beta}, γ={gamma})', fontsize=14, pad=15)

    # Customize grid and legend
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10, loc='center right', frameon=True, framealpha=0.9)

    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Tight layout and save
    plt.tight_layout()
    output_path = "results/sir_simulation.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Figure saved to {output_path}")
    plt.close()
