import numpy as np
from scipy.integrate import odeint
from model import sir_derivatives
from visualize import plot_simulation
from typing import Final, List, Tuple

def run_simulation():
    """
    Sets up and runs the SIR epidemic simulation.
    """
    # Parameters
    N: Final[float] = 1000.0
    I0: float = 1.0
    R0: float = 0.0
    S0: float = N - I0 - R0
    
    beta: float = 0.3
    gamma: float = 0.1
    
    # Time grid (in days)
    t = np.linspace(0, 160, 160)
    
    # Initial conditions vector
    y0 = [S0, I0, R0]
    
    # Integrate the SIR equations over the time grid
    ret = odeint(sir_derivatives, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    
    # Calculate statistics
    peak_infection_idx = np.argmax(I)
    peak_infection = I[peak_infection_idx]
    peak_day = t[peak_infection_idx]
    final_recovered = R[-1]
    
    print(f"Simulation Summary:")
    print(f"Peak Infection: {peak_infection:.2f} people")
    print(f"Time to Peak:   {peak_day:.2f} days")
    print(f"Final Recovered: {final_recovered:.2f} people")
    
    # Visualize results
    plot_simulation(t, S, I, R, beta, gamma)


if __name__ == "__main__":
    run_simulation()
