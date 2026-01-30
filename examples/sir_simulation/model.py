import numpy as np
from typing import Tuple, List

def sir_derivatives(y: List[float], t: float, N: float, beta: float, gamma: float) -> List[float]:
    """
    Calculates the derivatives for the SIR model.

    Args:
        y (List[float]): Current state vector [S, I, R].
        t (float): Time point.
        N (float): Total population.
        beta (float): Transmission rate.
        gamma (float): Recovery rate.

    Returns:
        List[float]: Derivatives [dS/dt, dI/dt, dR/dt].
    """
    S, I, R = y
    
    dSdt = -beta * S * I / N
    dIdt = (beta * S * I / N) - (gamma * I)
    dRdt = gamma * I
    
    return [dSdt, dIdt, dRdt]
