#!/usr/bin/env python3
"""
Full SIR model visualization showing all compartments (S, I, R) and analysis.

This addresses the question: Does the SIR model reproduce the non-monotonic 
behavior we see in the data?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fit_sir_model import (
    fit_sir_model, run_sir_simulation, 
    DATA_FILE, N_POPULATION, SIMULATION_DAYS
)

OUTPUT_FILE = Path(__file__).parent.parent / "results" / "covid_italy_sir_full.png"
LOCKDOWN_DATE = datetime(2020, 3, 9)
DATA_START_DATE = datetime(2020, 2, 22)


def create_full_sir_figure(
    df: pd.DataFrame, 
    beta: float, 
    gamma: float, 
    R0: float
) -> plt.Figure:
    """Create comprehensive SIR visualization with all compartments."""
    
    # Run simulation with fitted parameters
    I0 = df['active'].iloc[0]
    t_sim, S_sim, I_sim, R_sim = run_sir_simulation(
        beta, gamma, N_POPULATION, I0, SIMULATION_DAYS
    )
    
    # Convert simulation days to dates
    sim_dates = [DATA_START_DATE + timedelta(days=int(d)) for d in t_sim]
    
    # Create 2x2 figure
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('SIR Model Analysis: Italy COVID-19 First Wave', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    # =========================================================================
    # Panel 1: Full SIR dynamics (absolute scale)
    # =========================================================================
    ax1 = axes[0, 0]
    ax1.plot(sim_dates, S_sim, 'b-', linewidth=2, label='S (Susceptible)')
    ax1.plot(sim_dates, I_sim, 'r-', linewidth=2, label='I (Infected)')
    ax1.plot(sim_dates, R_sim, 'g-', linewidth=2, label='R (Recovered)')
    ax1.axvline(LOCKDOWN_DATE, color='gray', linestyle='--', alpha=0.7)
    ax1.set_ylabel('Population')
    ax1.set_title('Model: All Compartments (Full Scale)', fontsize=11)
    ax1.legend(loc='right')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
    ax1.set_ylim(0, N_POPULATION * 1.05)
    
    # =========================================================================
    # Panel 2: Infected comparison (zoomed)
    # =========================================================================
    ax2 = axes[0, 1]
    ax2.scatter(df['date'], df['active'], s=30, alpha=0.7, color='red', 
                label='Data: Active Cases', zorder=3)
    ax2.plot(sim_dates, I_sim, 'b-', linewidth=2, label='Model: I(t)', zorder=2)
    ax2.axvline(LOCKDOWN_DATE, color='gray', linestyle='--', alpha=0.7, 
                label='Lockdown')
    ax2.set_ylabel('Active Infections')
    ax2.set_title('Infected Compartment: Model vs Data', fontsize=11)
    ax2.legend(loc='upper right')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
    
    # Find model peak
    peak_idx = np.argmax(I_sim)
    peak_date = sim_dates[peak_idx]
    peak_val = I_sim[peak_idx]
    ax2.annotate(f'Model peak: {peak_val/1e6:.2f}M\n({peak_date.strftime("%b %d")})',
                 xy=(peak_date, peak_val), xytext=(peak_date, peak_val*0.8),
                 fontsize=9, ha='center')
    
    # =========================================================================
    # Panel 3: Fraction infected over time
    # =========================================================================
    ax3 = axes[1, 0]
    ax3.plot(sim_dates, S_sim/N_POPULATION, 'b-', linewidth=2, label='S/N')
    ax3.plot(sim_dates, I_sim/N_POPULATION, 'r-', linewidth=2, label='I/N')
    ax3.plot(sim_dates, R_sim/N_POPULATION, 'g-', linewidth=2, label='R/N')
    ax3.scatter(df['date'], df['active']/N_POPULATION, s=20, alpha=0.5, 
                color='red', label='Data I/N', zorder=3)
    ax3.axvline(LOCKDOWN_DATE, color='gray', linestyle='--', alpha=0.7)
    ax3.set_ylabel('Fraction of Population')
    ax3.set_xlabel('Date')
    ax3.set_title('Fraction in Each Compartment', fontsize=11)
    ax3.legend(loc='right')
    ax3.set_ylim(0, 1.05)
    
    # =========================================================================
    # Panel 4: Analysis text
    # =========================================================================
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Calculate key metrics
    data_peak = df['active'].max()
    data_peak_date = df.loc[df['active'].idxmax(), 'date']
    model_peak = I_sim.max()
    model_peak_day = t_sim[np.argmax(I_sim)]
    model_peak_date = DATA_START_DATE + timedelta(days=int(model_peak_day))
    final_R = R_sim[-1]
    herd_immunity = 1 - 1/R0
    
    analysis_text = f"""
    ANALYSIS: Why the SIR Model Doesn't Match
    ══════════════════════════════════════════════════════════════
    
    FITTED PARAMETERS
    β = {beta:.4f}  (transmission rate)
    γ = {gamma:.4f}  (recovery rate)  
    R₀ = {R0:.2f}   (basic reproduction number)
    
    SCALE MISMATCH
    Data peak:     {data_peak:>12,} active cases ({data_peak/N_POPULATION:.2%} of N)
    Model peak:    {model_peak:>12,.0f} infected    ({model_peak/N_POPULATION:.1%} of N)
    
    The model predicts {model_peak/data_peak:.0f}× MORE infections than observed!
    
    TIMING MISMATCH  
    Data peaks:    {data_peak_date.strftime('%b %d, %Y')}
    Model peaks:   {model_peak_date.strftime('%b %d, %Y')} (day {model_peak_day:.0f})
    
    WHY THE MISMATCH?
    1. SIR assumes CONSTANT β — but lockdown reduced transmission
    2. With R₀ = {R0:.2f}, epidemic doesn't burn out until ~{herd_immunity:.0%} infected
    3. Real peak = {data_peak/N_POPULATION:.2%} of population (lockdown stopped it early)
    
    CONCLUSION
    The simple SIR CAN produce rise-and-fall dynamics, but only when
    herd immunity is reached. Italy's lockdown interrupted the natural
    epidemic trajectory, preventing the 33 million infections the 
    model predicts.
    """
    
    ax4.text(0.05, 0.95, analysis_text, transform=ax4.transAxes,
             fontsize=10, fontfamily='monospace', verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Format x-axes
    for ax in [axes[0,0], axes[0,1], axes[1,0]]:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig.subplots_adjust(top=0.93)
    
    return fig


def main():
    print("Loading data...")
    df = pd.read_csv(DATA_FILE, parse_dates=['date'])
    df = df[df['date'] >= '2020-02-22'].reset_index(drop=True)
    
    print("Fitting SIR model...")
    result = fit_sir_model(df)
    print(f"Fitted: β={result.beta:.4f}, γ={result.gamma:.4f}, R₀={result.R0:.2f}")
    
    print("Creating comprehensive figure...")
    fig = create_full_sir_figure(df, result.beta, result.gamma, result.R0)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nFigure saved to: {OUTPUT_FILE}")
    
    plt.close(fig)


if __name__ == "__main__":
    main()
