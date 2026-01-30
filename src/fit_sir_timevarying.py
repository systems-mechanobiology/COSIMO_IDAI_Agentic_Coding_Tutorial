#!/usr/bin/env python3
"""
Time-varying SIR model with piecewise transmission rate β(t).

This addresses the limitation of constant-β SIR by allowing:
- β = β_pre   for t < lockdown_day (pre-intervention)
- β = β_post  for t ≥ lockdown_day (post-intervention)

We fit THREE parameters: β_pre, β_post, and γ.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.integrate import odeint
from scipy.optimize import minimize
from scipy.interpolate import interp1d
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Tuple

# Configuration
DATA_FILE = Path(__file__).parent.parent / "data" / "covid_italy_first_wave.csv"
OUTPUT_FILE = Path(__file__).parent.parent / "results" / "covid_italy_sir_timevarying.png"
N_POPULATION = 60_360_000
SIMULATION_DAYS = 120
DATA_START_DATE = datetime(2020, 2, 22)
LOCKDOWN_DATE = datetime(2020, 3, 9)
LOCKDOWN_DAY = (LOCKDOWN_DATE - DATA_START_DATE).days  # Day 16


@dataclass
class TimeVaryingResult:
    """Results from time-varying SIR fit."""
    beta_pre: float
    beta_post: float
    gamma: float
    R0_pre: float
    R0_post: float
    sse: float
    success: bool


def sir_derivatives_timevarying(
    y: np.ndarray, 
    t: float, 
    N: int, 
    beta_pre: float, 
    beta_post: float,
    gamma: float,
    lockdown_day: float
) -> list:
    """
    SIR model with time-varying β.
    
    β(t) = β_pre   if t < lockdown_day
         = β_post  if t >= lockdown_day
    """
    S, I, R = y
    
    # Piecewise transmission rate
    beta = beta_pre if t < lockdown_day else beta_post
    
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    
    return [dSdt, dIdt, dRdt]


def run_sir_timevarying(
    beta_pre: float,
    beta_post: float,
    gamma: float, 
    N: int, 
    I0: int, 
    days: int,
    lockdown_day: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Run time-varying SIR simulation."""
    S0 = N - I0
    R0_init = 0
    y0 = [S0, I0, R0_init]
    
    t = np.linspace(0, days, days * 10 + 1)  # Higher resolution for accuracy
    
    solution = odeint(
        sir_derivatives_timevarying, y0, t, 
        args=(N, beta_pre, beta_post, gamma, lockdown_day)
    )
    S, I, R = solution.T
    
    return t, S, I, R


def fit_timevarying_sir(df: pd.DataFrame) -> TimeVaryingResult:
    """Fit time-varying SIR model with piecewise β."""
    
    df = df.copy()
    df['day'] = (df['date'] - df['date'].iloc[0]).dt.days
    data_days = df['day'].values
    data_active = df['active'].values
    I0 = data_active[0]
    
    print(f"Fitting time-varying SIR model")
    print(f"Lockdown day: {LOCKDOWN_DAY} (March 9, 2020)")
    print(f"Data points before lockdown: {(df['day'] < LOCKDOWN_DAY).sum()}")
    print(f"Data points after lockdown: {(df['day'] >= LOCKDOWN_DAY).sum()}")
    
    def objective(params):
        beta_pre, beta_post, gamma = params
        if any(p <= 0 for p in params):
            return 1e20
        
        try:
            t, S, I, R = run_sir_timevarying(
                beta_pre, beta_post, gamma, 
                N_POPULATION, I0, SIMULATION_DAYS, LOCKDOWN_DAY
            )
            I_interp = interp1d(t, I, kind='linear', fill_value='extrapolate')
            I_model = I_interp(data_days)
            sse = np.sum((I_model - data_active) ** 2)
            return sse
        except:
            return 1e20
    
    # Grid search for initial guess
    print("\nOptimizing (grid search + refinement)...")
    best_result = None
    
    for beta_pre_init in [0.3, 0.4, 0.5]:
        for beta_post_init in [0.05, 0.1, 0.15]:
            for gamma_init in [0.05, 0.07, 0.1]:
                x0 = [beta_pre_init, beta_post_init, gamma_init]
                result = minimize(
                    objective, x0,
                    method='L-BFGS-B',
                    bounds=[(0.1, 1.0), (0.01, 0.3), (0.03, 0.15)],
                    options={'maxiter': 500}
                )
                if best_result is None or result.fun < best_result.fun:
                    best_result = result
    
    beta_pre, beta_post, gamma = best_result.x
    
    return TimeVaryingResult(
        beta_pre=beta_pre,
        beta_post=beta_post,
        gamma=gamma,
        R0_pre=beta_pre / gamma,
        R0_post=beta_post / gamma,
        sse=best_result.fun,
        success=best_result.success
    )


def create_comparison_figure(
    df: pd.DataFrame,
    tv_result: TimeVaryingResult,
    const_sse: float
) -> plt.Figure:
    """Create comparison figure: constant-β vs time-varying β."""
    
    I0 = df[df['date'] >= '2020-02-22']['active'].iloc[0]
    
    # Run time-varying simulation
    t_tv, S_tv, I_tv, R_tv = run_sir_timevarying(
        tv_result.beta_pre, tv_result.beta_post, tv_result.gamma,
        N_POPULATION, I0, SIMULATION_DAYS, LOCKDOWN_DAY
    )
    sim_dates = [DATA_START_DATE + timedelta(days=d) for d in t_tv]
    
    # Create figure
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Time-Varying SIR Model: Effect of Lockdown on Transmission', 
                 fontsize=14, fontweight='bold')
    
    # =========================================================================
    # Left panel: Model fit
    # =========================================================================
    ax1 = axes[0]
    ax1.scatter(df['date'], df['active'], s=30, alpha=0.7, color='red',
                label='Observed Data', zorder=3)
    ax1.plot(sim_dates, I_tv, 'b-', linewidth=2.5, label='Time-varying β Model')
    ax1.axvline(LOCKDOWN_DATE, color='green', linestyle='--', linewidth=2,
                label='Lockdown (Mar 9)', alpha=0.8)
    
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Active Infections')
    ax1.set_title('Model Fit with Piecewise β(t)')
    ax1.legend(loc='upper right')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    
    # =========================================================================
    # Right panel: Parameters and comparison
    # =========================================================================
    ax2 = axes[1]
    ax2.axis('off')
    
    improvement = (1 - tv_result.sse / const_sse) * 100
    intervention_effect = (1 - tv_result.beta_post / tv_result.beta_pre) * 100
    
    text = f"""
    ══════════════════════════════════════════════════════════════
                    TIME-VARYING SIR RESULTS
    ══════════════════════════════════════════════════════════════
    
    FITTED PARAMETERS
    ─────────────────
    β_pre  = {tv_result.beta_pre:.4f}    (before lockdown)
    β_post = {tv_result.beta_post:.4f}    (after lockdown)
    γ      = {tv_result.gamma:.4f}
    
    REPRODUCTION NUMBERS
    ────────────────────
    R₀ (pre-lockdown)  = {tv_result.R0_pre:.2f}
    R₀ (post-lockdown) = {tv_result.R0_post:.2f}
    
    INTERPRETATION
    ──────────────
    • Lockdown reduced transmission by {intervention_effect:.0f}%
    • R₀ dropped from {tv_result.R0_pre:.2f} → {tv_result.R0_post:.2f}
    • Post-lockdown R₀ {'< 1 ✓ Epidemic controlled!' if tv_result.R0_post < 1 else '> 1 (still spreading)'}
    
    FIT QUALITY COMPARISON
    ──────────────────────
    Constant β SSE:      {const_sse:.2e}
    Time-varying β SSE:  {tv_result.sse:.2e}
    
    Improvement: {improvement:.1f}% reduction in error
    
    EPIDEMIOLOGICAL INSIGHT
    ───────────────────────
    Infectious period (1/γ): {1/tv_result.gamma:.1f} days
    Pre-lockdown doubling:   {np.log(2)/(tv_result.beta_pre - tv_result.gamma):.1f} days
    """
    
    ax2.text(0.05, 0.95, text, transform=ax2.transAxes,
             fontsize=10, fontfamily='monospace', verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    for ax in [axes[0]]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def main():
    print("=" * 60)
    print("Time-Varying SIR Model with Lockdown Intervention")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv(DATA_FILE, parse_dates=['date'])
    df = df[df['date'] >= '2020-02-22'].reset_index(drop=True)
    
    # Fit time-varying model
    tv_result = fit_timevarying_sir(df)
    
    # Get constant-β SSE for comparison (from previous fit)
    const_sse = 4.18e11  # From our constant-β fit
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"β_pre  = {tv_result.beta_pre:.4f}")
    print(f"β_post = {tv_result.beta_post:.4f}")
    print(f"γ      = {tv_result.gamma:.4f}")
    print(f"\nR₀ (pre-lockdown)  = {tv_result.R0_pre:.2f}")
    print(f"R₀ (post-lockdown) = {tv_result.R0_post:.2f}")
    print(f"\nIntervention effectiveness: {(1 - tv_result.beta_post/tv_result.beta_pre)*100:.1f}%")
    print(f"\nSSE improvement: {(1 - tv_result.sse/const_sse)*100:.1f}%")
    
    # Create figure
    print("\nCreating comparison figure...")
    fig = create_comparison_figure(df, tv_result, const_sse)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Figure saved to: {OUTPUT_FILE}")
    
    plt.close(fig)
    return tv_result


if __name__ == "__main__":
    result = main()
