"""
SIR epidemic model package.

Provides shared functions for SIR simulation to avoid code duplication.
"""

from .core import (
    sir_derivatives,
    run_sir,
    sir_derivatives_timevarying,
    run_sir_timevarying,
)

from .fitting import (
    create_sse_objective,
    FittingResult,
)

__all__ = [
    'sir_derivatives',
    'run_sir',
    'sir_derivatives_timevarying', 
    'run_sir_timevarying',
    'create_sse_objective',
    'FittingResult',
]
