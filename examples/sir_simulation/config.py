"""
Configuration dataclasses for SIR simulation.

These define the parameters for simulation and visualization.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple, Dict, List


@dataclass
class SimulationConfig:
    """Configuration for SIR epidemic simulation."""
    
    # Population parameters
    N: int = 1000          # Total population
    I0: int = 1            # Initial infected
    
    # Model parameters
    beta: float = 0.3      # Transmission rate
    gamma: float = 0.1     # Recovery rate
    
    # Simulation settings
    duration: int = 160    # Days to simulate
    
    # Sensitivity analysis
    beta_sweep_range: Tuple[float, float, int] = (0.1, 0.5, 10)
    
    @property
    def S0(self) -> int:
        """Initial susceptible population."""
        return self.N - self.I0
    
    @property
    def R0(self) -> int:
        """Initial recovered population (always 0)."""
        return 0
    
    @property
    def R_naught(self) -> float:
        """Basic reproduction number."""
        return self.beta / self.gamma


@dataclass
class VisualizationConfig:
    """Configuration for plotting and figure output."""
    
    # Output settings
    output_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "results")
    dpi: int = 300
    
    # Figure sizes
    figsize_simulation: Tuple[int, int] = (10, 6)
    figsize_sensitivity: Tuple[int, int] = (12, 5)
    
    # File names
    simulation_plot_name: str = "sir_simulation.png"
    sensitivity_plot_name: str = "sir_sensitivity.png"
    
    # Colors
    colors: Dict[str, str] = field(default_factory=lambda: {
        'S': '#1f77b4',   # Blue for Susceptible
        'I': '#d62728',   # Red for Infected
        'R': '#2ca02c',   # Green for Recovered
        'peak': '#ff7f0e',  # Orange for peak analysis
        'time': '#9467bd',  # Purple for time analysis
    })
    
    # Style preference (tries each in order)
    style_preference: List[str] = field(default_factory=lambda: [
        'seaborn-v0_8-whitegrid',
        'seaborn-whitegrid', 
        'ggplot',
        'default'
    ])
