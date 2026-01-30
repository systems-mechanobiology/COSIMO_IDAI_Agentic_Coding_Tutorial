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

1. Open slides in browser: `cd slides && quarto preview slides.qmd`
2. Open IDE (VS Code, Cursor) with `planning/contents_brainstorming.md` visible
3. When reaching live coding sections, copy prompts from §6 of the brainstorming doc
4. Paste prompts into your AI coding agent
5. Let the agent generate code while you narrate

## 📖 For Presenters

- See `AGENTS.md` for full project documentation
- See `.agent/workflows/live-coding.md` for agent behavior guidelines
- See `planning/contents_brainstorming.md` §6 for all demo prompts
