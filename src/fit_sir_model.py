#!/usr/bin/env python3
"""
Fit SIR epidemic model to real COVID-19 data for Italy.

This script:
1. Loads the preprocessed Italy COVID-19 data
2. Defines the SIR model differential equations
3. Creates an objective function (Sum of Squared Errors)
4. Uses scipy.optimize.minimize to find best (beta, gamma)
5. Reports the optimized parameters and R0

Key assumptions:
- Population N = 60,360,000 (Italy)
- Initial infected I0 from data on Feb 22, 2020
- Recovery rate gamma and transmission rate beta are constant
"""

import numpy as np
import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import minimize
from scipy.interpolate import interp1d
from pathlib import Path
from dataclasses import dataclass
from typing import Tuple, Callable

# Configuration
DATA_FILE = Path(__file__).parent.parent / "data" / "covid_italy_first_wave.csv"
N_POPULATION = 60_360_000  # Italy's population
SIMULATION_DAYS = 120


@dataclass
class FittingResult:
    """Container for optimization results."""
    beta: float
    gamma: float
    R0: float
    sse: float
    success: bool
    message: str


def sir_derivatives(y: np.ndarray, t: float, N: int, beta: float, gamma: float) -> list:
    """
    SIR model differential equations.
    
    dS/dt = -beta * S * I / N
    dI/dt = beta * S * I / N - gamma * I
    dR/dt = gamma * I
    
    Parameters
    ----------
    y : array-like
        Current state [S, I, R]
    t : float
        Current time (unused, but required by odeint)
    N : int
        Total population
    beta : float
        Transmission rate
    gamma : float
        Recovery rate
        
    Returns
    -------
    list
        Derivatives [dS/dt, dI/dt, dR/dt]
    """
    S, I, R = y
    
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    
    return [dSdt, dIdt, dRdt]


def run_sir_simulation(
    beta: float, 
    gamma: float, 
    N: int, 
    I0: int, 
    days: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Run SIR simulation with given parameters.
    
    Parameters
    ----------
    beta : float
        Transmission rate
    gamma : float
        Recovery rate
    N : int
        Total population
    I0 : int
        Initial infected count
    days : int
        Duration to simulate
        
    Returns
    -------
    tuple
        (t, S, I, R) arrays
    """
    # Initial conditions
    S0 = N - I0
    R0_init = 0
    y0 = [S0, I0, R0_init]
    
    # Time points
    t = np.linspace(0, days, days + 1)
    
    # Solve ODEs
    solution = odeint(sir_derivatives, y0, t, args=(N, beta, gamma))
    S, I, R = solution.T
    
    return t, S, I, R


def create_objective_function(
    data_days: np.ndarray, 
    data_active: np.ndarray,
    N: int,
    I0: int,
    sim_days: int
) -> Callable:
    """
    Create an objective function for optimization.
    
    The objective is the Sum of Squared Errors (SSE) between
    the model's I(t) and the observed active cases.
    
    Parameters
    ----------
    data_days : np.ndarray
        Days since start (from data)
    data_active : np.ndarray
        Observed active cases
    N : int
        Total population
    I0 : int
        Initial infected count
    sim_days : int
        Days to simulate
        
    Returns
    -------
    Callable
        Objective function that takes [beta, gamma] and returns SSE
    """
    def objective(params: np.ndarray) -> float:
        beta, gamma = params
        
        # Ensure parameters are positive
        if beta <= 0 or gamma <= 0:
            return 1e20
        
        try:
            # Run simulation
            t, S, I, R = run_sir_simulation(beta, gamma, N, I0, sim_days)
            
            # Create interpolation function for model I(t)
            I_interp = interp1d(t, I, kind='linear', fill_value='extrapolate')
            
            # Interpolate to data time points
            I_model = I_interp(data_days)
            
            # Sum of Squared Errors
            sse = np.sum((I_model - data_active) ** 2)
            
            return sse
            
        except (ValueError, RuntimeError, FloatingPointError) as e:
            # Log integration failures for debugging
            import logging
            logging.debug(f"SIR integration failed: {e}")
            return 1e20
    
    return objective


def fit_sir_model(df: pd.DataFrame) -> FittingResult:
    """
    Fit SIR model to COVID-19 data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Data with columns: date, active
        
    Returns
    -------
    FittingResult
        Optimized parameters and diagnostics
    """
    # Convert dates to days since first date
    df = df.copy()
    df['day'] = (df['date'] - df['date'].iloc[0]).dt.days
    
    # Get data arrays
    data_days = df['day'].values
    data_active = df['active'].values
    
    # Initial infected from first data point
    I0 = data_active[0]
    
    print(f"Fitting SIR model to {len(df)} data points")
    print(f"Initial infected (I0): {I0:,}")
    print(f"Population (N): {N_POPULATION:,}")
    print(f"Simulation duration: {SIMULATION_DAYS} days")
    
    # Create objective function
    objective = create_objective_function(
        data_days, data_active, N_POPULATION, I0, SIMULATION_DAYS
    )
    
    # Initial guess for [beta, gamma]
    # Typical COVID-19: R0 ~ 2.5, gamma ~ 0.07 (14-day recovery)
    # So beta ~ 0.175
    x0 = [0.2, 0.07]
    
    # Parameter bounds: realistic for COVID-19
    # gamma: 0.05-0.15 corresponds to 7-20 day infectious period
    # beta: allow wide range
    bounds = [(0.01, 0.5), (0.05, 0.15)]
    
    print("\nOptimizing...")
    
    # Run optimization with multiple restarts for robustness
    best_result = None
    for gamma_init in [0.05, 0.07, 0.1, 0.12]:
        for beta_init in [0.15, 0.2, 0.3]:
            x0_trial = [beta_init, gamma_init]
            result = minimize(
                objective,
                x0_trial,
                method='L-BFGS-B',
                bounds=bounds,
                options={'maxiter': 1000}
            )
            if best_result is None or result.fun < best_result.fun:
                best_result = result
    
    result = best_result
    
    beta_opt, gamma_opt = result.x
    R0_opt = beta_opt / gamma_opt
    
    return FittingResult(
        beta=beta_opt,
        gamma=gamma_opt,
        R0=R0_opt,
        sse=result.fun,
        success=result.success,
        message=result.message
    )


def main():
    """Main function to load data and fit model."""
    print("=" * 60)
    print("SIR Model Fitting to Italy COVID-19 Data")
    print("=" * 60)
    
    # Load data
    print(f"\nLoading data from: {DATA_FILE}")
    df = pd.read_csv(DATA_FILE, parse_dates=['date'])
    
    # Start from Feb 22 when cases become meaningful
    df = df[df['date'] >= '2020-02-22'].reset_index(drop=True)
    
    print(f"Data range: {df['date'].iloc[0].date()} to {df['date'].iloc[-1].date()}")
    print(f"Total days: {len(df)}")
    
    # Fit model
    result = fit_sir_model(df)
    
    # Print results
    print("\n" + "=" * 60)
    print("OPTIMIZATION RESULTS")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    print()
    print(f"Optimized Parameters:")
    print(f"  β (transmission rate):  {result.beta:.6f}")
    print(f"  γ (recovery rate):      {result.gamma:.6f}")
    print()
    print(f"Derived Quantities:")
    print(f"  R₀ = β/γ:               {result.R0:.2f}")
    print(f"  Infectious period 1/γ:  {1/result.gamma:.1f} days")
    # Guard against β ≈ γ which causes division by zero
    if abs(result.beta - result.gamma) > 0.001:
        print(f"  Doubling time:          {np.log(2) / (result.beta - result.gamma):.1f} days")
    else:
        print(f"  Doubling time:          N/A (β ≈ γ)")
    print()
    print(f"Fit Quality:")
    print(f"  Sum of Squared Errors:  {result.sse:.2e}")
    print(f"  RMSE:                   {np.sqrt(result.sse / len(df)):.0f} cases")
    
    return result


if __name__ == "__main__":
    result = main()
