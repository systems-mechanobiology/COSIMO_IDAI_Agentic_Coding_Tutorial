from typing import Sequence, List
import numpy as np
from numpy.typing import ArrayLike

def sir_derivatives(y: Sequence[float], t: float, N: float, beta: float, gamma: float) -> List[float]:
    """
    Calculates the derivatives for the SIR model.

    Args:
        y (Sequence[float]): Current state vector [S, I, R].
        t (float): Time point (unused in autonomous system, but required by odeint).
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
