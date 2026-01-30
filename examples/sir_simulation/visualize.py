import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from typing import List, Tuple
from config import VisualizationConfig

def setup_style(config: VisualizationConfig) -> None:
    """Sets the matplotlib style based on config preference."""
    for style in config.style_preference:
        try:
            plt.style.use(style)
            return
        except OSError:
            continue
    plt.style.use('default')

def plot_simulation_fig(t: np.ndarray, S: np.ndarray, I: np.ndarray, R: np.ndarray, 
                       beta: float, gamma: float, config: VisualizationConfig) -> Figure:
    """
    Creates the SIR simulation figure.
    """
    setup_style(config)
    fig, ax = plt.subplots(figsize=config.figsize_simulation)

    # Plot lines
    ax.plot(t, S, label='Susceptible', color=config.colors['S'], linewidth=2, alpha=0.8)
    ax.plot(t, I, label='Infected', color=config.colors['I'], linewidth=2, alpha=0.8)
    ax.plot(t, R, label='Recovered', color=config.colors['R'], linewidth=2, alpha=0.8)

    # Add labels and title
    ax.set_xlabel('Time (days)', fontsize=12)
    ax.set_ylabel('Population', fontsize=12)
    ax.set_title(f'SIR Model Simulation\n(β={beta}, γ={gamma})', fontsize=14, pad=15)

    # Customize grid and legend
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10, loc='center right', frameon=True, framealpha=0.9)

    # Clean styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig

def plot_sensitivity_fig(betas: List[float], peak_infections: List[float], 
                        peak_times: List[float], config: VisualizationConfig) -> Figure:
    """
    Creates the sensitivity analysis figure.
    """
    setup_style(config)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=config.figsize_sensitivity)

    # Panel 1: Peak Infection vs Beta
    ax1.plot(betas, peak_infections, 'o-', color=config.colors['peak'], linewidth=2)
    ax1.set_xlabel('Transmission Rate (β)', fontsize=12)
    ax1.set_ylabel('Peak Infection Count', fontsize=12)
    ax1.set_title('Impact of β on Peak Infection', fontsize=14)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Panel 2: Time to Peak vs Beta
    ax2.plot(betas, peak_times, 's-', color=config.colors['time'], linewidth=2)
    ax2.set_xlabel('Transmission Rate (β)', fontsize=12)
    ax2.set_ylabel('Time to Peak (days)', fontsize=12)
    ax2.set_title('Impact of β on Peak Timing', fontsize=14)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    return fig

def save_figure(fig: Figure, filename: str, config: VisualizationConfig) -> None:
    """Saves the figure to the configured output directory."""
    config.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = config.output_dir / filename
    fig.savefig(output_path, dpi=config.dpi, bbox_inches='tight')
    print(f"Figure saved to {output_path}")
    plt.close(fig)
