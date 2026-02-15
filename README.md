# COSIMO-IDAI Agentic Coding Tutorial

A 50-minute seminar demonstrating how to use AI coding agents for scientific problems.

⚠️ **Scope note:** This repository contains code produced from live-demo prompts for the first Agentic Coding Tutorial. It is intended for teaching and seminar use, not production deployment. The code may prioritize speed and clarity over production hardening, full validation, and long-term maintainability. Robust engineering practices (tests, stricter validation, packaging, and reproducibility controls) are covered in later seminar sessions.

## 🚀 Quick Start

```bash
# Preview the slides
cd slides
quarto preview slides.qmd
```

## 📁 Structure

```
├── AGENTS.md           # Project instructions for AI assistants
├── LICENSE              # Project licensing (MIT + CC BY 4.0)
├── requirements.txt     # Python dependencies
├── README.md
├── .agent/
│   └── workflows/      # Demo behavior instructions
│       └── live-coding.md
├── data/               # COVID-19 CSV inputs and data helper scripts
├── results/            # Figures and generated reports from analyses
├── slides/             # Presentation files
│   ├── slides.qmd      # Main slide deck
│   ├── custom.scss     # Theme styling
│   └── _quarto.yml     # Quarto config
├── planning/           # Seminar planning & content
│   └── contents_brainstorming.md  # Master document (includes all prompts)
├── examples/           # Pre-made fallback code
│   └── sir_simulation/ # Working SIR implementation
├── src/                # Core analysis scripts and reusable modules
└── main.py             # Optional convenience entrypoint
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
- `.agent/workflows/live-coding.md`: Agent behavior guide for live demos
- `data/`: COVID-19 time series data (JHU CSSE)
- `src/`: Example implementation scripts
    - `fit_sir_model.py`: Basic SIR fitting
    - `fit_sir_improved.py`: Fitting with preprocessing and bounds checks
    - `fit_sir_timevarying.py`: Piecewise time-varying β
    - `compare_countries.py`: Italy vs South Korea comparison
    - `analyze_uk.py`: University of Birmingham special run
    - `visualize_*.py`: Figure generation helpers
    - `sir/`: Reusable module package (`core.py`, `fitting.py`)

## 🚀 Quick Start (Full)

```bash
# 1. Preview slides
cd slides && quarto preview slides.qmd

# 2. Run the UK analysis (University of Birmingham Special)
python3 src/analyze_uk.py

# 3. Or run the standalone SIR example
python3 examples/sir_simulation/main.py

# 3. View the generated report
open results/covid_analysis_report.pdf
```

## 📖 For Presenters

- See `AGENTS.md` for full project documentation
- See `planning/contents_brainstorming.md` §6 for all demo prompts

## ⚖️ License

This project uses a dual-licensing approach:

- **Code**: All source code, simulation scripts, and implementation examples are licensed under the [MIT License](LICENSE).
- **Content**: All presentation slides, documentation, and planning materials are licensed under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Copyright (c) 2026 Fabian Spill
