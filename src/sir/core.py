"""
Core SIR model functions.

This module consolidates the duplicated SIR logic that was spread across
multiple scripts (fit_sir_model.py, fit_sir_timevarying.py, etc.)
"""

import numpy as np
from scipy.integrate import odeint
from typing import Tuple, Callable


def sir_derivatives(y: np.ndarray, t: float, N: int, beta: float, gamma: float) -> list:
    """
    Standard SIR model differential equations.
    
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


def run_sir(
    beta: float, 
    gamma: float, 
    N: int, 
    I0: int, 
    days: int,
    resolution: int = 1
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Run standard SIR simulation with constant parameters.
    
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
    resolution : int
        Points per day (default 1)
        
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
    t = np.linspace(0, days, days * resolution + 1)
    
    # Solve ODEs
    solution = odeint(sir_derivatives, y0, t, args=(N, beta, gamma))
    S, I, R = solution.T
    
    return t, S, I, R


def sir_derivatives_timevarying(
    y: np.ndarray, 
    t: float, 
    N: int, 
    beta_func: Callable[[float], float],
    gamma: float
) -> list:
    """
    SIR model with time-varying transmission rate beta(t).
    
    Parameters
    ----------
    y : array-like
        Current state [S, I, R]
    t : float
        Current time
    N : int
        Total population
    beta_func : callable
        Function that returns beta at time t
    gamma : float
        Recovery rate
        
    Returns
    -------
    list
        Derivatives [dS/dt, dI/dt, dR/dt]
    """
    S, I, R = y
    beta = beta_func(t)
    
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    
    return [dSdt, dIdt, dRdt]


def run_sir_timevarying(
    beta_func: Callable[[float], float],
    gamma: float, 
    N: int, 
    I0: int, 
    days: int,
    resolution: int = 10
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Run SIR simulation with time-varying beta.
    
    Parameters
    ----------
    beta_func : callable
        Function that returns beta at time t
    gamma : float
        Recovery rate
    N : int
        Total population
    I0 : int
        Initial infected count
    days : int
        Duration to simulate
    resolution : int
        Points per day for integration (default 10)
        
    Returns
    -------
    tuple
        (t, S, I, R) arrays
    """
    S0 = N - I0
    y0 = [S0, I0, 0]
    
    t = np.linspace(0, days, days * resolution + 1)
    
    solution = odeint(
        sir_derivatives_timevarying, y0, t, 
        args=(N, beta_func, gamma)
    )
    S, I, R = solution.T
    
    return t, S, I, R


def make_piecewise_beta(
    beta_pre: float, 
    beta_post: float, 
    transition_day: float
) -> Callable[[float], float]:
    """
    Create a piecewise constant beta function.
    
    Parameters
    ----------
    beta_pre : float
        Beta before transition
    beta_post : float
        Beta after transition
    transition_day : float
        Day when transition occurs
        
    Returns
    -------
    callable
        Function beta(t)
    """
    def beta_func(t: float) -> float:
        return beta_pre if t < transition_day else beta_post
    return beta_func


def make_sigmoid_beta(
    beta_pre: float,
    beta_post: float,
    transition_day: float,
    delay: float = 0,
    width: float = 3
) -> Callable[[float], float]:
    """
    Create a smooth sigmoid transition in beta.
    
    Parameters
    ----------
    beta_pre : float
        Beta before transition
    beta_post : float
        Beta after transition
    transition_day : float
        Day when transition begins
    delay : float
        Additional delay after transition_day
    width : float
        Width of sigmoid transition (days)
        
    Returns
    -------
    callable
        Function beta(t)
    """
    def beta_func(t: float) -> float:
        t_eff = transition_day + delay
        w = max(width, 0.1)  # Prevent division by zero
        sigmoid = 1 / (1 + np.exp((t - t_eff) / w))
        return beta_post + (beta_pre - beta_post) * sigmoid
    return beta_func
