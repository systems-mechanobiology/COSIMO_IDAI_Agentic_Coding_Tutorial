# COSIMO-IDAI Agentic Coding Tutorial

A 50-minute seminar demonstrating how to use AI coding agents for scientific problems.

## 🚀 Quick Start

```bash
# Preview the slides
quarto preview slides.qmd

# Render to HTML
quarto render slides.qmd
```

## 📁 Structure

```
├── slides.qmd          # Main presentation
├── prompts/            # Prompts for live coding demos
│   ├── 01_setup.md     # Initial setup prompts
│   ├── 02_simulation.md # Simulation code prompts
│   └── 03_analysis.md  # Data analysis prompts
├── examples/           # Generated code (created during demo)
└── .agent/workflows/   # Instructions for the coding agent
```

## 🎯 During the Seminar

1. Open `slides.qmd` in presentation mode
2. When reaching live coding sections, open the corresponding prompt file
3. Copy prompts into your AI coding agent (VS Code, Cursor, etc.)
4. Let the agent generate code while you narrate

## 📖 For Presenters

See `.agent/workflows/live-coding.md` for detailed agent instructions.
