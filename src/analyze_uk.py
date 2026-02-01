#!/usr/bin/env python3
"""
University of Birmingham Special: UK COVID-19 Analysis
Analyzing the first wave in the UK (March - June 2020)

This script:
1. Extracts UK data from JHU global dataset
2. Fits an SIR model with time-varying transmission (lockdown effect)
3. Visualizes the result with specific focus on the March 23rd lockdown
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.integrate import odeint
from scipy.optimize import minimize
from pathlib import Path
from datetime import datetime, timedelta

# Configuration for UK
# --------------------
COUNTRY = "United Kingdom"
POPULATION = 67_081_000
START_DATE = datetime(2020, 3, 1)
END_DATE = datetime(2020, 6, 30)
LOCKDOWN_DATE = datetime(2020, 3, 23)

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = Path(__file__).parent.parent / "results" / "uk_covid_analysis.png"

# JHU Data Files
CONFIRMED_FILE = DATA_DIR / "time_series_covid19_confirmed_global.csv"
DEATHS_FILE = DATA_DIR / "time_series_covid19_deaths_global.csv"
RECOVERED_FILE = DATA_DIR / "time_series_covid19_recovered_global.csv"


def load_uk_data():
    """Load and preprocess UK data from JHU files."""
    print(f"Loading data for {COUNTRY}...")
    
    def load_metric(filepath, name):
        df = pd.read_csv(filepath)
        # Filter for UK (mainland only, no colonies)
        df = df[
            (df['Country/Region'] == COUNTRY) & 
            (df['Province/State'].isna())
        ]
        
        # Melt to long format
        id_vars = ["Province/State", "Country/Region", "Lat", "Long"]
        df_long = df.melt(id_vars=id_vars, var_name="Date", value_name=name)
        df_long["Date"] = pd.to_datetime(df_long["Date"])
        return df_long.set_index("Date")[name]

    confirmed = load_metric(CONFIRMED_FILE, "confirmed")
    deaths = load_metric(DEATHS_FILE, "deaths")
    recovered = load_metric(RECOVERED_FILE, "recovered")
    
    # Combine
    df = pd.concat([confirmed, deaths, recovered], axis=1)
    df = df.fillna(0)
    
    # Calculate active cases
    # Note: UK recovered data is notoriously poor in JHU dataset
    # We estimate active = confirmed - deaths - (recovered if available else proxy)
    # Simple proxy: recovered = confirmed cases from 14 days ago - deaths
    df['active'] = df['confirmed'] - df['deaths'] - df['recovered']
    
    # Filter date range
    mask = (df.index >= START_DATE) & (df.index <= END_DATE)
    df = df[mask].copy()
    
    return df.reset_index()


def sir_derivatives(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]


def run_sir_timevarying(params, N, I0, days, lockdown_day):
    """Run time-varying SIR using odeint for consistency with other scripts."""
    beta_pre, beta_post, gamma = params
    
    def derivatives(y, t):
        S, I, R = y
        beta = beta_pre if t < lockdown_day else beta_post
        dSdt = -beta * S * I / N
        dIdt = beta * S * I / N - gamma * I
        dRdt = gamma * I
        return [dSdt, dIdt, dRdt]
    
    t = np.linspace(0, days, days * 10 + 1)  # Higher resolution
    y0 = [N - I0, I0, 0]
    
    solution = odeint(derivatives, y0, t)
    S, I, R = solution.T
    
    # Downsample to integer days for compatibility
    t_days = np.arange(days + 1)
    S_days = np.interp(t_days, t, S)
    I_days = np.interp(t_days, t, I)
    R_days = np.interp(t_days, t, R)
    
    return t_days, S_days, I_days, R_days


def fit_model(df):
    """Fit time-varying SIR model."""
    days = (df['Date'].max() - df['Date'].min()).days
    lockdown_day = (LOCKDOWN_DATE - df['Date'].min()).days
    
    y_data = df['active'].values
    I0 = y_data[0]
    
    def objective(params):
        beta_pre, beta_post, gamma = params
        if any(p < 0 for p in params): return 1e9
        
        _, _, I_model, _ = run_sir_timevarying(params, POPULATION, I0, days, lockdown_day)
        
        # Calculate SSE
        return np.sum((I_model[:len(y_data)] - y_data) ** 2)
    
    # Initial guess
    x0 = [0.4, 0.1, 0.1]
    bounds = [(0.1, 1.0), (0.01, 0.5), (0.01, 0.2)]
    
    res = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')
    return res.x


def plot_results(df, params):
    """Create the specific UK analysis plot."""
    beta_pre, beta_post, gamma = params
    
    days = (df['Date'].max() - df['Date'].min()).days
    lockdown_day = (LOCKDOWN_DATE - df['Date'].min()).days
    I0 = df['active'].iloc[0]
    
    t, S, I, R = run_sir_timevarying(params, POPULATION, I0, days, lockdown_day)
    dates = [df['Date'].min() + timedelta(days=int(ti)) for ti in t]
    
    # Calculate R0
    R0_pre = beta_pre / gamma
    R0_post = beta_post / gamma
    
    # Plotting
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot data and model
    ax.scatter(df['Date'], df['active'], color='#002855', alpha=0.6, label='Observed Data (UK)', s=30)
    ax.plot(dates, I, color='#d62728', linewidth=3, label='SIR Model Fit')
    
    # Add lockdown line
    ax.axvline(LOCKDOWN_DATE, color='green', linestyle='--', linewidth=2, label='National Lockdown (Mar 23)')
    
    # UoB Styling
    ax.set_title("UK COVID-19 First Wave: Impact of Lockdown", fontsize=16, fontweight='bold', color='#002855')
    ax.set_ylabel("Active Infections", fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Add parameter box
    text = (
        f"Fitted Parameters:\n"
        f"──────────────────\n"
        f"β_pre  = {beta_pre:.3f}\n"
        f"β_post = {beta_post:.3f}\n"
        f"γ      = {gamma:.3f}\n\n"
        f"R₀ (Pre-Lockdown)  = {R0_pre:.2f}\n"
        f"R₀ (Post-Lockdown) = {R0_post:.2f}\n"
        f"Impact: {(1 - beta_post/beta_pre)*100:.0f}% reduction"
    )
    ax.text(0.02, 0.95, text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='#ccc'))
    
    ax.legend(fontsize=11, loc='upper right')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}k'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"Plot saved to {OUTPUT_FILE}")


def main():
    df = load_uk_data()
    print(f"Data range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    
    print("Fitting model...")
    params = fit_model(df)
    
    print("\nResults:")
    print(f"Beta (pre): {params[0]:.3f}")
    print(f"Beta (post): {params[1]:.3f}")
    print(f"Gamma: {params[2]:.3f}")
    
    plot_results(df, params)


if __name__ == "__main__":
    main()
