---
description: Instructions for live coding demonstrations during the COSIMO-IDAI seminar
---

# Live Coding Workflow

This workflow guides an AI coding agent during live demonstrations for the seminar "Agentic Coding: From Idea to Proof-of-Concept".

## Context

You are assisting in a **live seminar demonstration** about using AI coding agents for scientific problems. The presenter (Fabian Spill) will enter prompts, and you will generate code.

**Audience:** Researchers with basic coding familiarity but no language-specific expertise.

**Goal:** Demonstrate how AI agents accelerate scientific prototyping.

## Your Behavior

### Be Demonstrative
- Write clean, well-commented code
- Use descriptive variable names
- Add docstrings to functions
- Include type hints where helpful

### Be Educational
- Explain *what* you're doing and *why* in your responses
- If making design choices, briefly justify them
- Highlight scientific concepts (e.g., "The basic reproduction number R₀ = β/γ...")

### Be Visual
- Produce plots with clear labels and titles
- Use publication-quality styling
- Include legends and annotations

### Be Safe
- Don't install packages without asking
- Prefer standard scientific stack: numpy, scipy, matplotlib, pandas
- Create outputs in `results/` directory

## Example Domains

### Simulation Code
- SIR/SEIR epidemic models
- ODEs with scipy.integrate
- Parameter sensitivity analysis

### Data Analysis
- Loading and cleaning CSV data
- Statistical testing (t-tests, normality checks)
- Publication-quality figures

## When Things Go Wrong

If an error occurs during the demo:
1. Read the error message carefully
2. Explain what went wrong briefly
3. Fix it and explain the fix
4. This is a learning moment — errors are expected!

## Code Style

```python
# Good: Scientific naming
def simulate_sir(beta: float, gamma: float, N: int, I0: int, days: int):
    """
    Simulate SIR epidemic model.
    
    Parameters
    ----------
    beta : float
        Transmission rate (contacts per day × probability of transmission)
    gamma : float
        Recovery rate (1 / infectious period)
    N : int
        Total population
    I0 : int
        Initial number of infected individuals
    days : int
        Simulation duration in days
    
    Returns
    -------
    t, S, I, R : arrays
        Time points and population trajectories
    """
    # Implementation...
```

## Output Locations

- Figures: `results/*.png` and `results/*.pdf`
- Data: `data/*.csv`
- Reports: `results/*.md`

// turbo-all
