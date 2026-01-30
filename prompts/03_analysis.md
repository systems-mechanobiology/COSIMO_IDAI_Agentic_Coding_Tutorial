# Data Analysis Prompts

These prompts build a data analysis pipeline for experimental data.

---

## Pre-Demo Setup

Create a sample dataset before this section (or use the prompt below):

```
Create a sample experimental dataset in data/measurements.csv.
It should contain:
- 50 measurements total
- Two groups: "control" (n=25) and "treatment" (n=25)
- A continuous outcome variable "response"
- Treatment group should have a slightly higher mean (effect size ~0.5)
- Include some missing values (3-4 NaNs) to make it realistic
```

---

## Prompt 3.1: Load and Explore Data

```
Load the experimental data from data/measurements.csv.
Show me:
- The first few rows
- Data types for each column
- Basic statistics (mean, std, count)
- Any missing values

Provide a brief summary of what you observe.
```

**What to highlight:** The agent provides interpretation, not just code output.

---

## Prompt 3.2: Data Cleaning

```
Handle the missing values in the dataset.
- Report how many missing values exist and where
- Use an appropriate strategy (e.g., median imputation or removal)
- Explain your choice
- Save the cleaned data to data/measurements_clean.csv
```

**What to highlight:** Asking for explanation shows the agent's reasoning.

---

## Prompt 3.3: Statistical Analysis

```
Compare the response variable between control and treatment groups.
- First check for normality (Shapiro-Wilk or similar)
- Choose an appropriate test based on the data distribution
- Report: test statistic, p-value, 95% confidence interval, and effect size (Cohen's d)
- Interpret the results in plain English
```

**What to highlight:** We specify *what* to do (compare groups) and *how to report* (effect size), but not *which test* — the agent chooses based on data.

---

## Prompt 3.4: Publication-Quality Figure

```
Create a publication-quality figure comparing control and treatment groups.
Include:
- Box plots or violin plots showing distributions
- Overlay individual data points (jittered)
- Error bars showing 95% CI of the mean
- Significance annotation (star notation: * p<0.05, ** p<0.01, etc.)
- Clean style: no top/right spines, readable font sizes
- Save as both results/comparison.png and results/comparison.pdf at 300 DPI
```

**What to highlight:** Detailed visual requirements produce polished output.

---

## Prompt 3.5: Automated Report (if time permits)

```
Generate a brief analysis report as a markdown file (results/analysis_report.md).
Include:
- Summary of the dataset
- Statistical test results
- Embedded figure
- Conclusion statement
```

**What to highlight:** The agent can produce documentation, not just code.

---

## Debugging Prompt (if errors occur)

```
This analysis failed with [paste error message].
I expect the code to [describe expected behavior].
The data shape is [mention if relevant].
Can you fix this?
```

---

## Notes for Presenter

- Ensure the sample data exists before starting this section
- If time is short, skip to Prompt 3.3 (statistical analysis) and Prompt 3.4 (figure)
- The figure prompt usually produces impressive visual output
