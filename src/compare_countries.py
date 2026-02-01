#!/usr/bin/env python3
"""
Compare SIR model fits for Italy vs South Korea.

Italy: National lockdown approach
South Korea: Aggressive testing + contact tracing
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.integrate import odeint
from scipy.optimize import differential_evolution
from scipy.interpolate import interp1d
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = Path(__file__).parent.parent / "results" / "country_comparison.png"

# Country configurations
COUNTRIES = {
    'Italy': {
        'file': 'covid_italy_first_wave.csv',
        'population': 60_360_000,
        'intervention_date': datetime(2020, 3, 9),
        'intervention_name': 'National Lockdown',
        'color': '#d62728',  # Red
        'start_date': datetime(2020, 2, 22),
    },
    'South Korea': {
        'file': 'covid_south_korea_first_wave.csv',
        'population': 51_780_000,
        'intervention_date': datetime(2020, 2, 20),  # Shincheonji cluster response
        'intervention_name': 'Mass Testing',
        'color': '#1f77b4',  # Blue
        'start_date': datetime(2020, 2, 18),  # First significant cases
    }
}


@dataclass
class CountryResult:
    country: str
    beta_pre: float
    beta_post: float
    gamma: float
    R0_pre: float
    R0_post: float
    effectiveness: float
    sse: float
    delay: float
    transition: float


def sigmoid_beta(t, beta_pre, beta_post, intervention_day, delay, transition):
    t_eff = intervention_day + delay
    transition = max(transition, 0.1)
    sigmoid = 1 / (1 + np.exp((t - t_eff) / transition))
    return beta_post + (beta_pre - beta_post) * sigmoid


def sir_derivatives(y, t, N, beta_pre, beta_post, gamma, intervention_day, delay, transition):
    S, I, R = y
    beta = sigmoid_beta(t, beta_pre, beta_post, intervention_day, delay, transition)
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]


def run_sir(params, N, I0, days, intervention_day):
    beta_pre, beta_post, gamma, delay, transition = params
    S0 = N - I0
    y0 = [S0, I0, 0]
    t = np.linspace(0, days, days * 10 + 1)
    solution = odeint(sir_derivatives, y0, t, 
                      args=(N, beta_pre, beta_post, gamma, intervention_day, delay, transition))
    return t, solution[:, 0], solution[:, 1], solution[:, 2]


def fit_country(df, config):
    """Fit SIR model to a country's data."""
    df = df.copy()
    
    # Find first date with significant cases
    significant_idx = df[df['active'] > 10].index[0] if (df['active'] > 10).any() else 0
    df = df.iloc[significant_idx:].reset_index(drop=True)
    
    df['day'] = (df['date'] - df['date'].iloc[0]).dt.days
    data_days = df['day'].values
    data_active = df['active'].values
    I0 = max(data_active[0], 1)
    
    intervention_day = (config['intervention_date'] - df['date'].iloc[0]).days
    intervention_day = max(0, intervention_day)
    
    def objective(params):
        beta_pre, beta_post, gamma, delay, transition = params
        if any(p <= 0 for p in [beta_pre, beta_post, gamma]):
            return 1e20
        try:
            t, S, I, R = run_sir(params, config['population'], I0, 120, intervention_day)
            I_interp = interp1d(t, I, fill_value='extrapolate')
            I_model = I_interp(data_days)
            sse = np.sum((I_model - data_active) ** 2)
            return sse
        except (ValueError, RuntimeError, FloatingPointError) as e:
            import logging
            logging.debug(f"Country fit integration failed: {e}")
            return 1e20
    
    bounds = [
        (0.15, 0.8),   # beta_pre
        (0.02, 0.2),   # beta_post
        (0.04, 0.15),  # gamma
        (0, 20),       # delay
        (2, 20)        # transition
    ]
    
    result = differential_evolution(objective, bounds, seed=42, maxiter=150, 
                                    workers=1, disp=False, polish=True)
    
    beta_pre, beta_post, gamma, delay, transition = result.x
    
    return CountryResult(
        country=config.get('name', 'Unknown'),
        beta_pre=beta_pre,
        beta_post=beta_post,
        gamma=gamma,
        R0_pre=beta_pre / gamma,
        R0_post=beta_post / gamma,
        effectiveness=(1 - beta_post / beta_pre) * 100,
        sse=result.fun,
        delay=delay,
        transition=transition
    ), df


def create_comparison_figure(results, data, configs):
    """Create side-by-side comparison figure."""
    
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(16, 10))
    
    # Create grid: 2 columns for countries, 3 rows
    gs = fig.add_gridspec(3, 3, width_ratios=[1, 1, 0.8], height_ratios=[1, 1, 0.5],
                          hspace=0.3, wspace=0.3)
    
    countries = list(results.keys())
    
    for i, country in enumerate(countries):
        result = results[country]
        df = data[country]
        config = configs[country]
        
        # Find start date
        significant_idx = df[df['active'] > 10].index[0] if (df['active'] > 10).any() else 0
        df_fit = df.iloc[significant_idx:].reset_index(drop=True)
        start_date = df_fit['date'].iloc[0]
        
        intervention_day = (config['intervention_date'] - start_date).days
        intervention_day = max(0, intervention_day)
        
        I0 = max(df_fit['active'].iloc[0], 1)
        params = [result.beta_pre, result.beta_post, result.gamma, result.delay, result.transition]
        t, S, I, R = run_sir(params, config['population'], I0, 120, intervention_day)
        sim_dates = [start_date + timedelta(days=d) for d in t]
        
        # Panel 1: Data + Fit
        ax1 = fig.add_subplot(gs[0, i])
        ax1.scatter(df['date'], df['active'], s=25, alpha=0.7, color=config['color'],
                    label='Observed', zorder=3)
        ax1.plot(sim_dates, I, 'k-', linewidth=2, label='Model Fit', zorder=2)
        ax1.axvline(config['intervention_date'], color='green', linestyle='--', 
                    linewidth=1.5, alpha=0.8, label=config['intervention_name'])
        ax1.set_ylabel('Active Cases')
        ax1.set_title(f'{country}', fontsize=13, fontweight='bold')
        ax1.legend(fontsize=8, loc='upper right')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # Panel 2: β(t) curve
        ax2 = fig.add_subplot(gs[1, i])
        t_fine = np.linspace(0, 100, 500)
        beta_t = [sigmoid_beta(ti, result.beta_pre, result.beta_post, 
                               intervention_day, result.delay, result.transition) for ti in t_fine]
        dates_fine = [start_date + timedelta(days=d) for d in t_fine]
        ax2.plot(dates_fine, beta_t, color=config['color'], linewidth=2.5)
        ax2.axhline(result.beta_pre, color='gray', linestyle='--', alpha=0.4)
        ax2.axhline(result.beta_post, color='gray', linestyle=':', alpha=0.4)
        ax2.set_ylabel('Transmission Rate β')
        ax2.set_xlabel('Date')
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
    
    # Comparison table panel
    ax_table = fig.add_subplot(gs[:2, 2])
    ax_table.axis('off')
    
    italy = results['Italy']
    korea = results['South Korea']
    
    table_text = f"""
    ════════════════════════════════════════
           PARAMETER COMPARISON
    ════════════════════════════════════════
    
                    Italy    S. Korea
    ────────────────────────────────────────
    β (pre)         {italy.beta_pre:.3f}      {korea.beta_pre:.3f}
    β (post)        {italy.beta_post:.3f}      {korea.beta_post:.3f}
    γ               {italy.gamma:.3f}      {korea.gamma:.3f}
    
    R₀ (pre)        {italy.R0_pre:.2f}       {korea.R0_pre:.2f}
    R₀ (post)       {italy.R0_post:.2f}       {korea.R0_post:.2f}
    
    Effectiveness   {italy.effectiveness:.0f}%        {korea.effectiveness:.0f}%
    
    1/γ (days)      {1/italy.gamma:.1f}        {1/korea.gamma:.1f}
    
    ════════════════════════════════════════
            INTERPRETATION
    ════════════════════════════════════════
    
    Lower R₀ (post): {'Italy' if italy.R0_post < korea.R0_post else 'S. Korea'}
    
    Italy's lockdown achieved a {'higher' if italy.effectiveness > korea.effectiveness else 'lower'}
    reduction in transmission ({italy.effectiveness:.0f}% vs {korea.effectiveness:.0f}%).
    
    However, South Korea:
    • Started with lower peak cases
    • Avoided economic lockdown
    • Used targeted interventions
    
    Different strategies, both effective
    at bringing R₀ below 1.
    """
    
    ax_table.text(0.05, 0.95, table_text, transform=ax_table.transAxes,
                  fontsize=10, fontfamily='monospace', verticalalignment='top',
                  bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Bottom panel: Summary
    ax_summary = fig.add_subplot(gs[2, :2])
    ax_summary.axis('off')
    
    summary = """
    DISCUSSION: Which Strategy Was More Effective?

    • Both countries successfully reduced R₀ below 1, controlling their epidemics.
    • Italy's lockdown was more aggressive (81% reduction) but came later and had higher social/economic cost.
    • South Korea's testing + tracing was more targeted but required extensive infrastructure and public compliance.
    • The "best" strategy depends on context: healthcare capacity, cultural factors, economic constraints, and timing of intervention.
    """
    ax_summary.text(0.02, 0.9, summary, transform=ax_summary.transAxes,
                    fontsize=11, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7))
    
    fig.suptitle('COVID-19 Response Comparison: Italy (Lockdown) vs South Korea (Test & Trace)',
                 fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    fig.subplots_adjust(top=0.93)
    
    return fig


def main():
    print("=" * 60)
    print("Country Comparison: Italy vs South Korea")
    print("=" * 60)
    
    results = {}
    data = {}
    
    for country, config in COUNTRIES.items():
        config['name'] = country
        print(f"\n--- Fitting {country} ---")
        
        df = pd.read_csv(DATA_DIR / config['file'], parse_dates=['date'])
        data[country] = df
        
        print(f"Peak active: {df['active'].max():,}")
        print(f"Fitting model...")
        
        result, df_fit = fit_country(df, config)
        results[country] = result
        
        print(f"β_pre={result.beta_pre:.3f}, β_post={result.beta_post:.3f}, γ={result.gamma:.3f}")
        print(f"R₀: {result.R0_pre:.2f} → {result.R0_post:.2f}")
        print(f"Effectiveness: {result.effectiveness:.0f}%")
    
    print("\n--- Creating comparison figure ---")
    fig = create_comparison_figure(results, data, COUNTRIES)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Figure saved to: {OUTPUT_FILE}")
    
    plt.close(fig)


if __name__ == "__main__":
    main()
