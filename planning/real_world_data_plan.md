# Real-World COVID-19 Data: Implementation Plan

This document outlines a sequence of prompts to extend Part 3 of the seminar with **real COVID-19 data** from the JHU CSSE repository, replacing or supplementing the synthetic data currently used.

---

## Data Source

**JHU CSSE COVID-19 Dataset**  
Repository: https://github.com/CSSEGISandData/COVID-19

Key files (direct raw links):
```
https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv
https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv
```

**Citation (required if publishing):**
> Dong E, Du H, Gardner L. An interactive web-based dashboard to track COVID-19 in real time. Lancet Inf Dis. 20(5):533-534. doi: 10.1016/S1473-3099(20)30120-1

---

## Recommended Setup: Pre-Download Data

To avoid network issues during the live demo, we recommend pre-downloading a processed subset.

### Prompt 0.1: Download and Cache COVID-19 Data
```
Download the COVID-19 time series data from the JHU CSSE GitHub repository.

URLs:
- https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
- https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv
- https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv

Save these files to the data/ directory.

Then create a preprocessing script that:
1. Loads the three CSV files
2. Filters for a specific country (Italy)
3. Extracts the time period Feb 1, 2020 to May 31, 2020
4. Computes daily new cases from cumulative data
5. Estimates active infections: I(t) = Confirmed(t) - Recovered(t) - Deaths(t)
6. Saves the result to data/covid_italy_first_wave.csv with columns: date, confirmed, deaths, recovered, active
```

---

## Part 3: Real Data Analysis (Revised Prompts)

### Prompt 3.1: Load Real COVID-19 Data
```
Load the preprocessed COVID-19 data from data/covid_italy_first_wave.csv.
This contains daily data for Italy during the first pandemic wave (Feb-May 2020).

Create a visualization showing:
- Cumulative confirmed cases over time
- Active infections (estimated) over time
- Daily new cases as a bar chart

Use proper date formatting on the x-axis.
Add a vertical line marking Italy's national lockdown (March 9, 2020).
Save to results/covid_italy_overview.png
```

### Prompt 3.1a: Interpret the Data
```
Look at the plot results/covid_italy_overview.png.

Describe:
1. When did exponential growth begin?
2. How long after the lockdown did cases peak?
3. Why is there a delay between lockdown and peak? (Hint: incubation period + reporting delay)
4. What do you notice about the "recovered" estimate?
```

---

### Prompt 3.2: Fit SIR Model to Real Data
```
We want to calibrate our SIR model using the real COVID-19 data for Italy.

Create a fitting function that:
1. Takes (beta, gamma) as parameters
2. Runs the SIR simulation for 120 days
3. Uses Italy's population N = 60,360,000
4. Assumes initial conditions: I0 from the data on Feb 22, S0 = N - I0, R0 = 0
5. Interpolates the model's I(t) to match the dates in the data
6. Returns the Sum of Squared Errors between model I(t) and data active cases

Use scipy.optimize.minimize to find the best-fit beta and gamma.
Print the optimized parameters and the resulting R0 = beta/gamma.
```

### Prompt 3.2a: Interpret the Fitted Parameters
```
Based on the optimized beta and gamma:

1. What is the estimated R0 (basic reproduction number)?
2. How does this compare to published estimates for early COVID-19 (R0 ≈ 2.5-3.5)?
3. What is the implied infection duration (1/gamma in days)?
4. Does this match what we know about COVID-19 (typically 10-14 days infectious)?
```

---

### Prompt 3.3: Visualize the Fit
```
Create a publication-quality figure showing:
1. The real data (active cases) as scatter points
2. The best-fit SIR model as a smooth curve
3. The lockdown date as a vertical dashed line
4. Key parameters in a text box: β, γ, R0

Title: "SIR Model Fit to Italy COVID-19 First Wave"
Save to results/covid_italy_sir_fit.png at 300 DPI
```

### Prompt 3.3a: Critique the Fit
```
Critically evaluate the fit shown in results/covid_italy_sir_fit.png.

Consider:
1. Does the model capture the growth phase well?
2. Does it capture the peak timing?
3. Does it capture the decline?
4. Where does the constant-β assumption clearly fail?
5. What would we need to add to the model to capture the lockdown effect?
```

---

## Part 4: Advanced Extension (Optional)

These prompts extend beyond the basic SIR to address real-world complexity.

### Prompt 4.1: Time-Varying Transmission Rate
```
The basic SIR model assumes constant transmission rate β.
But Italy implemented a lockdown on March 9, 2020.

Modify the SIR model to use a piecewise β(t):
- β = β_pre   for t < lockdown_day
- β = β_post  for t ≥ lockdown_day

Fit the model with THREE parameters: β_pre, β_post, and γ.
Compare the fit quality to the constant-β model.
Calculate R0 before and after lockdown.
```

### Prompt 4.1a: Interpret the Intervention Effect
```
Based on the time-varying β fit:

1. What was R0 before lockdown?
2. What was R0 after lockdown?
3. Did the lockdown bring R0 below 1? (The epidemic control threshold)
4. What is the "intervention effectiveness" = 1 - (β_post/β_pre)?
```

---

### Prompt 4.2: Compare Multiple Countries
```
Repeat the SIR fitting for South Korea using the same time period.
South Korea used aggressive testing and contact tracing instead of lockdown.

Create a comparison figure showing:
- Italy data + fit (left panel)
- South Korea data + fit (right panel)
- A table comparing β, γ, and R0 for both countries

Discuss: Which country had lower R0? What strategies might explain this?
```

---

### Prompt 4.3: Uncertainty Quantification
```
Our point estimates for β and γ don't capture uncertainty.

Use scipy.optimize.minimize with method='L-BFGS-B' to get the Hessian.
Compute approximate confidence intervals from the inverse Hessian.

Alternatively, use a bootstrap approach:
1. Add noise to the data (resample residuals)
2. Refit 100 times
3. Report the 95% confidence interval for R0

Visualize the uncertainty as a shaded band around the model curve.
```

---

## Discussion Points for the Seminar

After running these prompts, the presenter can discuss:

| Topic | Teaching Point |
|-------|----------------|
| **Model-data mismatch** | SIR is too simple for COVID-19; useful for intuition, not prediction |
| **Data quality** | "Recovered" was poorly reported; active cases are estimates |
| **Interventions** | Constant β fails when behavior changes (lockdowns, masks, vaccines) |
| **R0 interpretation** | R0 depends on context; not an intrinsic property of the virus alone |
| **Extensions** | SEIR (exposed compartment), age structure, spatial models |

---

## Fallback: Keep Synthetic Data Option

If network fails or time is short, the existing synthetic data prompts (3.1-3.3 in contents_brainstorming.md) remain valid. Consider restructuring Part 3 as:

```
Part 3: Data Analysis
├── 3.1-3.3: Quick synthetic example (always works)
└── 3.4-3.7: Real COVID-19 data (if time permits)
```

---

## Files to Create

| File | Purpose |
|------|---------|
| `data/covid_italy_first_wave.csv` | Preprocessed Italy data (Feb-May 2020) |
| `data/covid_south_korea_first_wave.csv` | Preprocessed South Korea data (optional) |
| `src/data_loader.py` | Functions to load and preprocess COVID data |
| `src/sir_fitting.py` | Model fitting utilities |
| `results/covid_italy_overview.png` | Data exploration figure |
| `results/covid_italy_sir_fit.png` | Main fitting result |
| `results/country_comparison.png` | Multi-country comparison (optional) |

---

## Next Steps

1. [ ] Run Prompt 0.1 to download and preprocess the data
2. [ ] Test Prompts 3.1-3.3 to verify the fitting workflow
3. [ ] Decide which optional extensions (4.1-4.3) to include
4. [ ] Update contents_brainstorming.md with finalized prompts
5. [ ] Update slides.qmd to reference real data section
