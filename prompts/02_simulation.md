# Simulation Code Prompts

These prompts build an SIR (Susceptible-Infected-Recovered) epidemic model from scratch.

---

## Prompt 2.1: Project Initialization

```
Create a Python project structure for simulating an SIR epidemic model.
Include:
- A main simulation script
- A module for the model equations
- A visualization script
- Proper docstrings and type hints
```

**What to highlight:** Notice we describe the *scientific goal* (SIR model), not the implementation details. The agent knows what SIR means.

---

## Prompt 2.2: Implement the Model

```
Implement the SIR model differential equations in the model module.
The model should track:
- S(t): Susceptible population
- I(t): Infected population  
- R(t): Recovered population

Parameters:
- β (beta): transmission rate
- γ (gamma): recovery rate
- N: total population (constant)

Use scipy.integrate.odeint for numerical integration.
```

**What to highlight:** We use domain terminology (β, γ, SIR). We specify the tool (scipy) but not how to use it — the agent knows.

---

## Prompt 2.3: Run a Simulation

```
Update the main script to run a simulation with these parameters:
- Population N = 1000
- Initial infected I0 = 1
- Transmission rate β = 0.3
- Recovery rate γ = 0.1
- Simulate for 160 days

Print summary statistics at the end (peak infection, time to peak, final recovered).
```

**What to highlight:** Concrete parameters let the agent produce runnable code immediately.

---

## Prompt 2.4: Visualization

```
Create a visualization that shows S, I, R curves over time.
Requirements:
- Clear axis labels with units (days, population)
- Legend identifying each curve
- Title including the key parameters (β, γ)
- Use a clean, publication-ready style (not default matplotlib)
- Save the figure to results/sir_simulation.png at 300 DPI
```

**What to highlight:** Specifying "publication-ready" communicates intent better than listing specific style parameters.

---

## Prompt 2.5: Explain the Results

```
Look at the plot `results/sir_simulation.png` (or the code used to generate it).
Explain what is happening in the simulation.
- What is the peak number of infected people?
- When does it occur?
- Why does the epidemic end?
```

**What to highlight:** Multimodal capabilities (if using an agent that sees images) or code reasoning. It turns the agent into a tutor.

---

## Prompt 2.6: Parameter Sensitivity

```
Create a function that runs the SIR model for a range of β values (0.1 to 0.5).
For each β, record the peak infection count and time to peak.
Plot these as a function of β in a two-panel figure.
```

**What to highlight:** Building on previous code — the agent remembers context.

---

### Prompt 2.6a: Explain the Change
```
Look at the new results.
- How did changing beta to 0.5 affect the peak parameters?
- Is the relationship linear?
```

---

## Prompt 2.7: Agent Code Reviewer (Best Practice)

*Best Practice: In a multi-agent workflow, one agent codes, another reviews. Here, we ask the model to switch personas.*

```
Act as a Senior Python Engineer Code Reviewer.
Review the current codebase (model.py, main.py, visualize.py).
Identify issues in:
1. **Hardcoded values** (should be constants/config)
2. **Type Hints** and Documentation
3. **Modularity**

Provide specific refactoring instructions but DO NOT apply them yet.
```

**What to highlight:** Agents are excellent linting tools. This reinforces "Trust but Verify".

---

## Prompt 2.8: Apply the Fixes

*Copy the list of issues provided by the Reviewer Agent and paste them here.*

```
Here is the code review feedback:
[PASTE REVIEW FEEDBACK HERE]

Please apply these changes to the codebase. Ensure the simulation still produces the same results after refactoring.
```

**What to highlight:** Closing the loop. The "Coder" agent follows the "Reviewer" agent's instructions.

---

## Prompt 2.9: Scientific Report Generation

*Now we switch personas again: from Coder to Author.*

```
Write a brief "Scientific Report" (markdown) summarizing the work:
1. **Methods:** Description of the SIR model and parameters used.
2. **Results:** Summary of the findings (peak infection, sensitivity to beta).
3. **Validation:** Mention that code was reviewed and results reproduced.

Save this as `results/report.md`.
```

**What to highlight:** Documentation is key. This prepares the material for the next layer of review (The "Scientist" persona).

---

## Notes for Presenter

- Run each prompt sequentially
- Let the output complete before moving to the next
- If the agent asks clarifying questions, answer them — this shows the interactive nature
- If there's an error, use it as a teaching moment about debugging
