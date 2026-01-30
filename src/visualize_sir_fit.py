#!/usr/bin/env python3
"""
Create publication-quality figure showing SIR model fit to COVID-19 data.

This script:
1. Loads the Italy COVID-19 data
2. Runs the SIR model optimization
3. Creates a figure with data points, model curve, and annotations
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta

# Import from our fitting module
import sys
sys.path.insert(0, str(Path(__file__).parent))
from fit_sir_model import (
    fit_sir_model, run_sir_simulation, 
    DATA_FILE, N_POPULATION, SIMULATION_DAYS
)

# Configuration
OUTPUT_FILE = Path(__file__).parent.parent / "results" / "covid_italy_sir_fit.png"
LOCKDOWN_DATE = datetime(2020, 3, 9)
DATA_START_DATE = datetime(2020, 2, 22)


def create_fit_figure(
    df: pd.DataFrame, 
    beta: float, 
    gamma: float, 
    R0: float
) -> plt.Figure:
    """
    Create publication-quality figure showing model fit.
    
    Parameters
    ----------
    df : pd.DataFrame
        COVID data with columns: date, active
    beta, gamma, R0 : float
        Fitted model parameters
        
    Returns
    -------
    plt.Figure
        Matplotlib figure object
    """
    # Run simulation with fitted parameters
    I0 = df['active'].iloc[0]
    t_sim, S_sim, I_sim, R_sim = run_sir_simulation(
        beta, gamma, N_POPULATION, I0, SIMULATION_DAYS
    )
    
    # Convert simulation days to dates
    sim_dates = [DATA_START_DATE + timedelta(days=int(d)) for d in t_sim]
    
    # Create figure
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot real data as scatter points
    ax.scatter(
        df['date'], df['active'], 
        s=40, alpha=0.7, color='#d62728', 
        edgecolors='white', linewidth=0.5,
        label='Observed Active Cases', zorder=3
    )
    
    # Plot model curve
    ax.plot(
        sim_dates, I_sim,
        linewidth=2.5, color='#1f77b4',
        label='SIR Model Fit', zorder=2
    )
    
    # Add lockdown line
    ax.axvline(
        LOCKDOWN_DATE, 
        color='#2ca02c', linestyle='--', linewidth=2,
        label='National Lockdown (Mar 9)', zorder=1
    )
    
    # Add parameter text box
    textstr = '\n'.join([
        r'$\bf{Fitted\ Parameters}$',
        f'β = {beta:.4f}',
        f'γ = {gamma:.4f}',
        f'R₀ = β/γ = {R0:.2f}',
        f'1/γ = {1/gamma:.1f} days'
    ])
    props = dict(boxstyle='round,pad=0.5', facecolor='white', 
                 edgecolor='gray', alpha=0.9)
    ax.text(
        0.02, 0.97, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', fontfamily='monospace',
        bbox=props
    )
    
    # Formatting
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Active Infections', fontsize=12)
    ax.set_title(
        'SIR Model Fit to Italy COVID-19 First Wave',
        fontsize=14, fontweight='bold', pad=15
    )
    
    # Format y-axis with thousands
    ax.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k')
    )
    
    # Format x-axis dates
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    
    # Set axis limits
    ax.set_xlim(df['date'].min() - timedelta(days=3), 
                df['date'].max() + timedelta(days=3))
    ax.set_ylim(0, max(df['active'].max(), I_sim.max()) * 1.1)
    
    # Legend
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    
    # Remove top/right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Grid
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def main():
    """Load data, fit model, and create visualization."""
    print("Loading data...")
    df = pd.read_csv(DATA_FILE, parse_dates=['date'])
    df = df[df['date'] >= '2020-02-22'].reset_index(drop=True)
    
    print("Fitting SIR model...")
    result = fit_sir_model(df)
    
    print(f"\nFitted: β={result.beta:.4f}, γ={result.gamma:.4f}, R₀={result.R0:.2f}")
    
    print("Creating figure...")
    fig = create_fit_figure(df, result.beta, result.gamma, result.R0)
    
    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Save figure
    fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nFigure saved to: {OUTPUT_FILE}")
    
    plt.close(fig)


if __name__ == "__main__":
    main()
