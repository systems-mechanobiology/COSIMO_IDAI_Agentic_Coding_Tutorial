# Part 3: SIR Real Data Analysis

These prompts extend the simulation by comparing it to "real" outbreak data.

---

## Prompt 3.1: Create/Load Real Data

```
Create a synthetic dataset representing "Real World Statistics" for an outbreak.
- Weeks: 0 to 8
- Cases: [15, 60, 250, 900, 2800, 4500, 3000, 900, 100]
- Total Population: 10,000

Load this into a pandas DataFrame and plot it as scatter points with error bars (assume sqrt(N) error).
```

**What to highlight:** Mixing manual data entry with pandas operations.

### Prompt 3.1a: Explain the Data
```
Look at the scatter plot.
- Describe the trend. Does it look exponential at first?
- When does it peak?
- Are the error bars realistic for these counts?
```

---

## Prompt 3.2: Fit Simulation to Data

```
We want to fit our SIR model to this data.
Create a function that:
1. Takes (beta, gamma) as inputs.
2. Runs the simulation for 60 days.
3. Interpolates the simulation results to match the "Weekly" data points.
4. Returns the Sum of Squared Errors (SSE) between model and data.

Then, use `scipy.optimize.minimize` to find the best beta and gamma.
```

**What to highlight:** Complex multi-step reasoning. Bridging "simulation time" (continuous) and "data time" (discrete).

### Prompt 3.2a: Interpret the Parameters
```
Based on the optimized `beta` and `gamma`:
1. Calculate the Basic Reproduction Number (R0 = beta/gamma).
2. Is this R0 characteristic of a highly infectious disease (like Measles) or a moderate one (like Flu)?
3. What is the expected duration of infection (1/gamma)?
```

---

## Prompt 3.3: Final Visualization

```
Create a final plot showing:
1. The "Real Data" as scatter points with error bars.
2. The "Best Fit Simulation" as a smooth curve.
3. Display the optimized R0 value (beta/gamma) in the title.
4. Save as `results/fitted_model.png`.
```

**What to highlight:** The grand finale — combining data and theory.

### Prompt 3.3a: Critical Critique
```
Critically evaluate the fit shown in `results/fitted_model.png`.
- Does the model capture the peak correctly?
- Does it capture the tail?
- The SIR model assumes a constant population/mixing. Where does this assumption fail for real epidemics?
```

---

## Debugging

If the optimizer fails:
```
The optimizer is not converging.
Try:
- Providing better initial guesses (beta=0.5, gamma=0.1)
- Bounding the parameters (0 < beta < 2, 0 < gamma < 1)
```
