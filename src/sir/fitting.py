"""
SIR model fitting utilities.

Provides shared objective function creation and result containers.
"""

import numpy as np
from scipy.interpolate import interp1d
from dataclasses import dataclass
from typing import Callable, Tuple
import logging


@dataclass
class FittingResult:
    """Container for optimization results."""
    beta: float
    gamma: float
    R0: float
    sse: float
    success: bool
    message: str = ""


@dataclass
class TimeVaryingResult:
    """Container for time-varying SIR fit results."""
    beta_pre: float
    beta_post: float
    gamma: float
    R0_pre: float
    R0_post: float
    sse: float
    success: bool
    delay: float = 0
    transition: float = 0


def create_sse_objective(
    data_days: np.ndarray, 
    data_active: np.ndarray,
    N: int,
    I0: int,
    sim_days: int,
    run_simulation: Callable,
    weights: np.ndarray = None
) -> Callable:
    """
    Create an SSE objective function for optimization.
    
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
        Days to simulate (must cover data range)
    run_simulation : callable
        Function that takes params and returns (t, S, I, R)
    weights : np.ndarray, optional
        Weights for each data point
        
    Returns
    -------
    callable
        Objective function that takes params array and returns SSE
        
    Raises
    ------
    ValueError
        If sim_days doesn't cover data range
    """
    # Validate simulation covers data range
    max_data_day = data_days.max()
    if sim_days < max_data_day:
        raise ValueError(
            f"sim_days ({sim_days}) must cover data range ({max_data_day}). "
            "Increase sim_days to avoid extrapolation errors."
        )
    
    if weights is None:
        weights = np.ones_like(data_active, dtype=float)
    
    def objective(params: np.ndarray) -> float:
        # Check for non-positive parameters
        if any(p <= 0 for p in params[:3]):  # Assume first params are rates
            return 1e20
        
        try:
            t, S, I, R = run_simulation(params, N, I0, sim_days)
            
            # Interpolate model to data time points (no extrapolation needed)
            I_interp = interp1d(t, I, kind='linear', bounds_error=True)
            I_model = I_interp(data_days)
            
            # Weighted Sum of Squared Errors
            sse = np.sum(weights * (I_model - data_active) ** 2)
            return sse
            
        except (ValueError, RuntimeError, FloatingPointError) as e:
            logging.debug(f"Optimization step failed: {e}")
            return 1e20
    
    return objective
