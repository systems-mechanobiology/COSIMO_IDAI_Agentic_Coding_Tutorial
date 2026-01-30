---
title: "Scientific Report: SIR Epidemic Simulation"
author: "AI Coding Agent"
date: "2025-02-13"
geometry: margin=1in
fontsize: 11pt
header-includes:
  - \usepackage{float}
  - \let\origfigure\figure
  - \let\endorigfigure\endfigure
  - \renewenvironment{figure}[1][2] {\expandafter\origfigure\expandafter[H]} {\endorigfigure}
---

# Introduction


## 1. Methods

We implemented a deterministic **Susceptible-Infected-Recovered (SIR)** epidemic model to simulate the spread of an infectious disease in a closed population.

The model dynamics are defined by the following system of ordinary differential equations (ODEs):

$$
\begin{aligned}
\frac{dS}{dt} &= -\frac{\beta S I}{N} \\
\frac{dI}{dt} &= \frac{\beta S I}{N} - \gamma I \\
\frac{dR}{dt} &= \gamma I
\end{aligned}
$$

**Parameters:**
*   **Total Population ($N$):** 1000
*   **Initial Infected ($I_0$):** 1
*   **Transmission Rate ($\beta$):** 0.3 (Baseline)
*   **Recovery Rate ($\gamma$):** 0.1
*   **Duration:** 160 days

The system was solved numerically using `scipy.integrate.odeint`. The implementation was modularized into configuration, modeling, simulation, and visualization components.

## 2. Results

### Baseline Simulation ($\beta=0.3$)
The simulation revealed a classic epidemic wave (Figure 1):
*   **Peak Infection:** 300.78 individuals (~30% of the population).
*   **Time to Peak:** Day 38.24.
*   **Final Recovered:** 940.52 individuals (94% attack rate).

The epidemic ended due to the depletion of the susceptible pool (herd immunity), rather than total infection of the population.

![Baseline SIR simulation showing dynamics of Susceptible (Blue), Infected (Red), and Recovered (Green) populations over time.](/Users/spillf/Documents/GitHub/COSIMO_IDAI_Agentic_Coding_Tutorial/results/sir_simulation.png){#fig:baseline width=80%}

### Sensitivity Analysis
We investigated the impact of varying the transmission rate $\beta$ from 0.1 to 0.5 (Figure 2):
*   **Non-linear Impact:** Increasing $\beta$ resulted in a super-linear increase in peak infection count.
*   **Acceleration:** Higher $\beta$ values caused the epidemic to peak significantly earlier (exponential decay in time-to-peak).
*   **Threshold Behavior:** At lower $\beta$ values (closer to $\gamma=0.1$), the outbreak was significantly suppressed, demonstrating the critical nature of the basic reproduction number ($R_0 = \beta/\gamma$).

![Sensitivity analysis of transmission rate ($\beta$). Left panel: Peak infection count vs $\beta$. Right panel: Time to peak vs $\beta$.](/Users/spillf/Documents/GitHub/COSIMO_IDAI_Agentic_Coding_Tutorial/results/sensitivity_analysis.png){#fig:sensitivity width=90%}

## 3. Validation

The codebase underwent a structured review process:
1.  **Code Review:** Addressed hardcoded values, improved type safety, and enforced modular separation of concerns.
2.  **Reproduction:** The refactored simulation was verified to produce **identical** numerical results to the initial prototype, checking peak values and timing.
3.  **Visualization:** Automated tests generated plots for both the time-series dynamics and parameter sensitivity, confirming the qualitative behavior matches theoretical expectations.
