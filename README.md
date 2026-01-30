# COSIMO-IDAI Agentic Coding Tutorial

A 50-minute seminar demonstrating how to use AI coding agents for scientific problems.

## 🚀 Quick Start

```bash
# Preview the slides
cd slides
quarto preview slides.qmd
```

## 📁 Structure

```
├── AGENTS.md           # Project instructions for AI assistants
├── slides/             # Presentation files
│   ├── slides.qmd      # Main slide deck
│   └── custom.scss     # Theme styling
├── planning/           # Seminar planning & content
│   └── contents_brainstorming.md  # Master document (includes all prompts)
├── examples/           # Pre-made fallback code
│   └── sir_simulation/ # Working SIR implementation
└── .agent/workflows/   # Instructions for the coding agent
```

## 🎯 During the Seminar

1. **Part 1-2**: Simulation from scratch (Basic Python)
2. **Part 3**: Real-World Data Analysis (Italy COVID-19)
    - Data loading & visualization
    - Fitting SIR model to real data
    - Critiquing the fit
3. **Part 4**: Advanced Extensions
    - Time-varying parameters (Lockdown modeling)
    - Country comparisons (Italy vs South Korea)
    - Uncertainty quantification
4. **Part 5**: Scientific Writing
    - AI generating full scientific reports
    - AI peer reviewing the reports

## 📁 Key Files

- `planning/contents_brainstorming.md`: Master prompt list for all sections
- `data/`: COVID-19 time series data (JHU CSSE)
- `src/`: Example implementation scripts
    - `fit_sir_model.py`: Basic fitting
    - `fit_sir_timevarying.py`: Advanced piecewise fitting
    - `compare_countries.py`: Italy vs South Korea comparison

## 🚀 Quick Start

```bash
# 1. Preview slides
cd slides && quarto preview slides.qmd

# 2. Run the UK analysis (University of Birmingham Special)
python3 src/analyze_uk.py

# 3. View the generated report
open results/covid_analysis_report.pdf
```

## 📖 For Presenters

- See `AGENTS.md` for full project documentation
- See `planning/contents_brainstorming.md` §6 for all demo prompts

