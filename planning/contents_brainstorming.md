# Seminar Content Brainstorming & Source Material

## 0. Series Context: COSIMO-IDAI
**Title:** Accelerating Research with Agentic AI and LLMs
**Purpose:** AI tools are integral but fragmented/opaque.
**Goals:**
*   Equip researchers with practical, model-agnostic skills.
*   **Be faster, more robust, and more reproducible!**
*   Develop critical literacy (failure modes).
*   Promote best practices (reproducibility).
*   Create shared institutional culture.
**Audience:** PhDs, Postdocs, PIs, RSEs.

## 0.5. Disclaimer & Community
*   **Policy:** University supports M365 Copilot only (currently).
*   **Warning:** NO sensitive data (GDPR/Export Control) in these tools.
*   **Best Practice:** Use **isolated environments** (VMs, containers, clean non-admin accounts).
*   **Community:** Open call for contributors (coding & prompts) and skeptics (failure cases).
*   **Ethics:** Dedicated sessions coming later.

## 0.8. The Challenge (Intro)
*   **Context:** Remind audience of the Pandemic. The famous **R number**.
*   **Goal:** Simulate SIR (S -> I -> R) high-level concepts.
*   **Method:** Build, Visualize, Analyze.

## 1. The Narrative Arc
**Theme:** "From syntax to scientific intent."
**Hook:** "We used to suggest code; now we collaborate on solutions."

## 2. The Evolution of AI Coding (Brief History)

### Path A: The "Inline" Evolution (Autocomplete)
*   **Era 1: Static Analysis (1990s-2015):** IntelliSense (VB6, early VS). Types, methods. "Dumb" but correct.
*   **Era 2: The Plugin Era (2018-2020):** TabNine (VS Code Extension). Statistical completion, often helpful but hallucinated.
*   **Era 3: Context-Aware Completion (2021-2024):** GitHub Copilot. Reads open tabs. Great for boilerplate.
*   **Limitation:** It is **passive**. It waits for you to type. It cannot "see" the error it just caused.

### Path B: The "Conversational" Evolution (Chatbots)
*   **Era 1: The "Clipboard Wall" (2022-2023):** ChatGPT web UI. You paste code -> It suggests fix -> You paste back.
    *   *Friction:* Context loss. "My code is too long for the window."
*   **Era 2: Integrated Chat (2023-2024):** Copilot Chat / Cursor Chat. It can "see" your file, but acts like a smart consultant.
*   **Limitation:** It is **theoretical**. It generates code that *looks* right but might not run.

### The Convergence: Agentic Coding (2025-2026)
*   **Definition:** An LLM with **Tool Use** (Terminal, File I/O, Browser).
*   **The Paradigm Shift:**
    *   Old: REPL (Read-Eval-Print Loop) controlled by Human.
    *   New: **Plan-Act-Observe Loop** controlled by Agent.
*   **The Loop:**
    1.  **Plan:** "I need to calculate the pairwise distances between 1000 atoms."
    2.  **Act:** Writes python script using `scipy.spatial`.
    3.  **Observe:** Runs script. Sees `MemoryError` (matrix too big).
    4.  **Refine:** "Switch to a sparse matrix or iterative interactions."
*   **Why it matters:** It closes the feedback loop *without human intervention*.

## 3. The Model Landscape (2026 Usage)

### 1. The "Thinking" Tier (Reasoning Models)
*   **Best for:** Reliable daily coding, refactoring, docs.
*   **Examples:**
    *   **OpenAI:** GPT-5.2 Thinking.
    *   **DeepSeek:** DeepSeek R2.
    *   **Anthropic:** Claude 4.5 Sonnet.

### 2. The "Pro" Tier (Instruction Models)
*   **Best for:** Complex architecture, mathematical derivations, hard debugging.
*   **Examples:**
    *   **OpenAI:** GPT-5.2 Pro.
    *   **Google:** Gemini DeepThink.
    *   **Anthropic:** Claude 4.5 Opus.

### 3. Open Weights (Local-able)
*   **Note:** Often called "Open Source" but technically "Open Weights".
*   **Examples:** Llama 4 (405B), Mistral Large, DeepSeek V3 (Weights available).

### 3. Agentic Frameworks (The "Drivers")
*   **Leading Tools:**
    *   **Cursor:** "Composer" mode.
    *   **GitHub Copilot Agent:** Deep integration in VS Code ecosystem.
    *   **Claude Code:** Anthropic's CLI-based agent.
    *   **Cline:** Open-source, flexible backend.

## 4. Key Concept: Scientific Intent

**The Shift:** Stop talking like a coder ("Make a class with a get_data method") and start talking like a scientist ("Load the experimental CSV and normalize by the control group").

### Examples of "Intent" Prompts:
*   **Bad:** "Write a for-loop from i=0 to N that adds dt*dx to x."
*   **Good:** "Implement Euler integration for the velocity equation."
    *   *Why:* The model knows the math better than you remember the syntax.
*   **Bad:** "Use matplotlib to make a red line plot."
*   **Good:** "Create a publication-quality figure comparing Treatment A vs B. Use 'seaborn-v0_8-paper' style, remove top/right spines, add error bars (SEM), and annotate significance with brackets."
    *   *Why:* "Publication-quality" is vague; specific style tokens steer the model better.

## 5. Outlook: Software Engineering 2022-2026

**How it changed:**
*   **2022:** Copy-pasting from ChatGPT.
*   **2026:** Managing **MCP Servers** and defining **Agent Skills**.

**Note:** We won't cover MCP server configuration today.
**Next Session:** "Building Custom Agent Skills" (in 2 weeks).
**Today's Focus:** The practical example (SIR Model).

## 6. Master Prompt List (Copy/Paste Ready)

### Part 1: Setup

**Prompt 1.1: Understand Workspace**
```
Can you look at this workspace and tell me what it contains? 
Summarize the project structure and its purpose.
```

**Prompt 1.2: Env Setup**
```
Set up a Python virtual environment for this project. 
We'll need numpy, scipy, matplotlib, and pandas for scientific computing.
Create a requirements.txt file.
```

**Prompt 1.3: Scaffolding**
```
Create a basic Python project structure for a scientific simulation.
Include:
- A main.py entry point
- A src/ directory for modules
- A tests/ directory for unit tests
- A data/ directory (empty, for input data)
- A results/ directory (empty, for outputs)
```

### Part 2: SIR Simulation

**Prompt 2.1: Project Init**
```
Create a Python project structure for simulating an SIR epidemic model.
Include:
- A main simulation script
- A module for the model equations
- A visualization script
- Proper docstrings and type hints
```

**Prompt 2.2: Implement Model**
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

**Prompt 2.3: Run Sim**
```
Update the main script to run a simulation with these parameters:
- Population N = 1000
- Initial infected I0 = 1
- Transmission rate β = 0.3
- Recovery rate γ = 0.1
- Simulate for 160 days

Print summary statistics at the end (peak infection, time to peak, final recovered).
```

**Prompt 2.4: Visualize**
```
Create a visualization that shows S, I, R curves over time.
Requirements:
- Clear axis labels with units (days, population)
- Legend identifying each curve
- Title including the key parameters (β, γ)
- Use a clean, publication-ready style (not default matplotlib)
- Save the figure to results/sir_simulation.png at 300 DPI
```

**Prompt 2.5: Explain Results**
```
Look at the plot `results/sir_simulation.png` (or the code used to generate it).
Explain what is happening in the simulation.
- What is the peak number of infected people?
- When does it occur?
- Why does the epidemic end?
```

**Prompt 2.6: Sensitivity**
```
Create a function that runs the SIR model for a range of β values (0.1 to 0.5).
For each β, record the peak infection count and time to peak.
Plot these as a function of β in a two-panel figure.
```

**Prompt 2.6a: Explain Change**
```
Look at the new results.
- How did changing beta to 0.5 affect the peak parameters?
- Is the relationship linear?
```

**Prompt 2.7: Agent Reviewer**
```
Act as a Senior Python Engineer Code Reviewer.
Review the current codebase (model.py, main.py, visualize.py).
Identify issues in:
1. **Hardcoded values** (should be constants/config)
2. **Type Hints** and Documentation
3. **Modularity**

Provide specific refactoring instructions but DO NOT apply them yet.
```

**Prompt 2.8: Apply Fixes**
```
Here is the code review feedback:
[PASTE REVIEW FEEDBACK HERE]

Please apply these changes to the codebase. Ensure the simulation still produces the same results after refactoring.
```

**Prompt 2.9: Write Report**
```
Write a brief "Scientific Report" (latex/pdf convertible markdown) summarizing the work:
1. **Methods:** Description of the SIR model and parameters used.
2. **Results:** Summary of the findings (peak infection, sensitivity to beta).
3. **Validation:** Mention that code was reviewed and results reproduced.

Save this as `results/report.md`.
Then, run a terminal command to convert it to PDF using pandoc: `pandoc results/report.md -o results/report.pdf`
```

**Prompt 2.10: Science Reviewer**
```
Act as a Senior Epidemiologist.
Read the report at `results/report.md`.
Critique the scientific quality:
1. **Clarity:** Is the methodology well-explained?
2. **Results:** Do the findings make sense for an SIR model?
3. **Limitations:** Did the author mention the limitations of fixed parameters?

Provide constructive feedback for the next manuscript draft.
```

### Part 3: Real Data Analysis

> **Note:** This section uses real COVID-19 data from the JHU CSSE repository. A synthetic fallback is provided at the end for network issues or time constraints.

---

#### Option A: Real COVID-19 Data (Recommended)

**Prompt 3.0: Download COVID-19 Data (Pre-Demo Setup)**
```
Download the COVID-19 time series data from the JHU CSSE GitHub repository.

URLs:
- https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv
- https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv
- https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv

Save these files to the data/ directory.

Then create a preprocessing script that:
1. Loads the three CSV files
2. Filters for Italy
3. Extracts the time period Feb 22, 2020 to May 31, 2020 (first wave)
4. Computes active infections: I(t) = Confirmed(t) - Recovered(t) - Deaths(t)
5. Saves the result to data/covid_italy_first_wave.csv with columns: date, confirmed, deaths, recovered, active
```

**Prompt 3.1: Load Real COVID-19 Data**
```
Load the preprocessed COVID-19 data from data/covid_italy_first_wave.csv.
This contains daily data for Italy during the first pandemic wave (Feb-May 2020).

Create a visualization showing:
- Active infections over time as a line plot
- Daily new cases as a bar chart (secondary panel)

Use proper date formatting on the x-axis.
Add a vertical line marking Italy's national lockdown (March 9, 2020).
Save to results/covid_italy_overview.png
```

**Prompt 3.1a: Interpret the Data**
```
Look at the plot results/covid_italy_overview.png.

Describe:
1. When did exponential growth begin?
2. How long after the lockdown did cases peak?
3. Why is there a delay between lockdown and peak? (Hint: incubation period + reporting delay)
```

**Prompt 3.2: Fit SIR Model to Real Data**
```
We want to calibrate our SIR model using the real COVID-19 data for Italy.

Create a fitting function that:
1. Takes (beta, gamma) as parameters
2. Runs the SIR simulation for 100 days
3. Uses Italy's population N = 60,360,000
4. Assumes initial conditions: I0 from the data on Feb 22, S0 = N - I0, R0 = 0
5. Interpolates the model's I(t) to match the dates in the data
6. Returns the Sum of Squared Errors between model I(t) and data active cases

Use scipy.optimize.minimize to find the best-fit beta and gamma.
Print the optimized parameters and the resulting R0 = beta/gamma.
```

**Prompt 3.2a: Interpret the Fitted Parameters**
```
Based on the optimized beta and gamma:

1. What is the estimated R0 (basic reproduction number)?
2. How does this compare to published estimates for early COVID-19 (R0 ≈ 2.5-3.5)?
3. What is the implied infection duration (1/gamma in days)?
4. Does this match what we know about COVID-19 (typically 10-14 days infectious)?
```

**Prompt 3.3: Visualize the Fit**
```
Create a publication-quality figure showing:
1. The real data (active cases) as scatter points
2. The best-fit SIR model as a smooth curve
3. The lockdown date (March 9) as a vertical dashed line
4. Key parameters in a text box: β, γ, R0

Title: "SIR Model Fit to Italy COVID-19 First Wave"
Save to results/covid_italy_sir_fit.png at 300 DPI
```

**Prompt 3.3a: Critique the Fit**
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

#### Option B: Synthetic Data (Fallback)

> Use this if network issues prevent downloading real data, or if time is limited.

**Prompt 3.1-alt: Load Synthetic Data**
```
Create a synthetic dataset representing "Real World Statistics" for an outbreak.
- Weeks: 0 to 8
- Cases: [15, 60, 250, 900, 2800, 4500, 3000, 900, 100]
- Total Population: 10,000

Load this into a pandas DataFrame and plot it as scatter points with error bars (assume sqrt(N) error).
```

**Prompt 3.2-alt: Fit Model to Synthetic Data**
```
We want to fit our SIR model to this data.
Create a function that:
1. Takes (beta, gamma) as inputs.
2. Runs the simulation for 60 days.
3. Interpolates the simulation results to match the "Weekly" data points.
4. Returns the Sum of Squared Errors (SSE) between model and data.

Then, use `scipy.optimize.minimize` to find the best beta and gamma.
```

**Prompt 3.3-alt: Final Plot (Synthetic)**
```
Create a final plot showing:
1. The "Real Data" as scatter points with error bars.
2. The "Best Fit Simulation" as a smooth curve.
3. Display the optimized R0 value (beta/gamma) in the title.
4. Save as `results/fitted_model.png`.
```

---

### Part 4: Advanced Extensions (Optional)

> These go beyond the basic demo if time permits.

**Prompt 4.1: Time-Varying Transmission Rate**
```
The basic SIR model assumes constant transmission rate β.
But Italy implemented a lockdown on March 9, 2020.

Modify the SIR model to use a piecewise β(t):
- β = β_pre   for t < lockdown_day (day 16 in our data)
- β = β_post  for t ≥ lockdown_day

Fit the model with THREE parameters: β_pre, β_post, and γ.
Compare the fit quality to the constant-β model.
Calculate R0 before and after lockdown.
```

**Prompt 4.1a: Interpret the Intervention Effect**
```
Based on the time-varying β fit:

1. What was R0 before lockdown?
2. What was R0 after lockdown?
3. Did the lockdown bring R0 below 1? (The epidemic control threshold)
4. What is the "intervention effectiveness" = 1 - (β_post/β_pre)?
```

---

### Part 5: Scientific Writing

> Use the AI to synthesize all results into a coherent scientific report.

**Prompt 5.1: Write a Scientific Report**
```
Write a scientific report summarizing our COVID-19 SIR model analysis.

The report should include:

## 1. Introduction
- Brief context on the COVID-19 pandemic and Italy's first wave
- The purpose of this analysis: calibrating an SIR model to real data

## 2. Methods
- Description of the SIR model equations (S, I, R compartments)
- Data source: JHU CSSE COVID-19 repository
- Time period: February 22 – May 31, 2020 (Italy)
- How "active infections" were estimated from the data
- Fitting procedure: scipy.optimize.minimize, objective function (SSE)

## 3. Results
- Present the fitted parameters: β, γ, and R0
- Include the figure `results/covid_italy_overview.png` showing the data
- Include the figure `results/covid_italy_sir_fit.png` showing the model fit
- Discuss the quality of the fit

## 4. Discussion
- Compare estimated R0 to published literature values (2.5-3.5)
- Explain why our estimate might differ (averaging pre/post lockdown)
- Discuss limitations of the basic SIR model for COVID-19
- Suggest improvements: time-varying β, SEIR model, age structure

## 5. Conclusion
- Summary of key findings
- The value of simple models for building intuition

Save the report as `results/covid_analysis_report.md`.
Then convert to PDF using: `pandoc results/covid_analysis_report.md -o results/covid_analysis_report.pdf`
```

**Prompt 5.1a: Review the Report**
```
Act as a peer reviewer for an epidemiology journal.
Read the report at `results/covid_analysis_report.md`.

Evaluate:
1. **Clarity**: Is the methodology clearly explained?
2. **Accuracy**: Are the R0 interpretations correct?
3. **Completeness**: Are limitations adequately discussed?
4. **Figures**: Are the figures properly referenced and captioned?

Provide constructive feedback for improving the manuscript.
```

## 7. Q&A Prep
*   **"Can I run this on my sensitive patient data?"** -> Use Local Models (DeepSeek R2 / Llama 4) via Cline or Ollama.
*   **"It gets the math wrong."** -> Use a Reasoning Model (o3/R1) for the derivation step, then switched to an Instruction Model for the coding.
