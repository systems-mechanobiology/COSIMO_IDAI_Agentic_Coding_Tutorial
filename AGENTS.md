# AGENTS.md — Project Instructions for AI Assistants

This document explains the structure and logic of the COSIMO-IDAI Agentic Coding Tutorial project.

## Project Purpose

This is a **50-minute live seminar** demonstrating how AI coding agents can accelerate scientific research. The presenter (Fabian Spill) switches between:

1. **Slides** — Quarto RevealJS presentation (`slides/slides.qmd`)
2. **IDE** — Live coding with an AI agent (VS Code, Cursor, etc.)

The audience watches the AI build an SIR epidemic simulation from scratch.

---

## Directory Structure

```
COSIMO_IDAI_Agentic_Coding_Tutorial/
├── AGENTS.md                ← You are here
├── README.md                ← Quick start for presenters
├── slides/                  ← Presentation files
│   ├── slides.qmd           ← Main slide deck (Quarto RevealJS)
│   ├── _quarto.yml          ← Quarto config
│   └── custom.scss          ← Theme styling
├── planning/                ← Source material
│   └── contents_brainstorming.md  ← Master content document (includes all prompts)
├── examples/                ← Pre-made example code (fallback)
│   └── sir_simulation/      ← Working SIR implementation
├── data/                    ← Input data (if any)
├── results/                 ← Generated outputs (figures, reports)
└── .agent/workflows/        ← Agent behavior instructions
    └── live-coding.md       ← How the agent should behave during demos
```

---

## Content Flow: From Brainstorming → Slides → Live Demo

The **single source of truth** for all seminar content is `planning/contents_brainstorming.md`.

### Document Structure

| Section | Content | Used For |
|---------|---------|----------|
| §0. Series Context | COSIMO-IDAI purpose & goals | Opening slides |
| §0.5. Disclaimer | Policy, data warnings, community | Disclaimer slides |
| §0.8. The Challenge | SIR model introduction | Problem framing |
| §1. Narrative Arc | Theme: "syntax → intent" | Implicit flow |
| §2. Evolution of AI Coding | Autocomplete → Chatbots → Agents | History section |
| §3. Model Landscape | Thinking/Pro/Open tiers, Frameworks | Tools overview |
| §4. Scientific Intent | Bad vs Good prompts | Key insight slide |
| §5. Outlook | 2022 vs 2026, future sessions | Closing section |
| **§6. Master Prompt List** | **All live demo prompts** | **Copy into IDE** |
| §7. Q&A Prep | Common questions & answers | Presenter reference |

### The Prompts

All prompts for the live demo are in **Section 6** of `contents_brainstorming.md`:

- **Part 1 (1.1–1.3):** Setup prompts
- **Part 2 (2.1–2.10):** SIR Simulation prompts
- **Part 3 (3.0–3.3a):** Real Data Analysis prompts
  - **Option A:** Real COVID-19 data from JHU CSSE (Italy first wave)
  - **Option B:** Synthetic data fallback (if network issues)
- **Part 4 (4.1–4.1a):** Advanced extensions (time-varying β)
- **Part 5 (5.1–5.1a):** Scientific Writing (report generation + peer review)

**Data source:** See `planning/real_world_data_plan.md` for full implementation details.

During the demo, the presenter copies prompts directly from this section.

---

## Presentation Workflow

### Before the Seminar

1. Open **slides** in browser: `cd slides && quarto preview slides.qmd`
2. Open **IDE** (VS Code/Cursor) with this project
3. Open `planning/contents_brainstorming.md` in a split pane (for copying prompts)
4. Ensure Python environment is ready: `pip install -r requirements.txt`

### During the Seminar

The presenter follows this rhythm:

```
┌─────────────────────────────────────────────────────────────────┐
│  SLIDES (Theory)                                                 │
│  - Present context, evolution, concepts                          │
│  - Reach a "Live Demo" slide                                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    [Switch to IDE]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  IDE (Practice)                                                  │
│  - Copy prompt from contents_brainstorming.md §6                 │
│  - Paste into AI agent chat                                      │
│  - Watch agent generate code                                     │
│  - Narrate what's happening                                      │
│  - Show results (run code, view plots)                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                   [Switch back to Slides]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  SLIDES (Reflection)                                             │
│  - Discuss what we learned                                       │
│  - Move to next section                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Slide ↔ Prompt Synchronization

| Slide Section | Prompts to Use |
|---------------|----------------|
| "Part 2: Live Coding — Simulation" | §6 Part 2: Prompts 2.1 → 2.5 (or more) |
| "Part 3: Live Coding — Data Analysis" | §6 Part 3: Prompts 3.1 → 3.3 |

---

## For AI Assistants Working on This Project

### If Asked to Modify Content

1. **Brainstorming (`planning/contents_brainstorming.md`)** — Master source. All prompts live here.
2. **Slides (`slides/slides.qmd`)** — Derived from brainstorming. Keep concise.

### If Asked to Run the Demo

Follow `.agent/workflows/live-coding.md` for behavior guidelines:
- Write clean, well-commented code
- Use scientific naming conventions
- Create outputs in `results/`
- Explain what you're doing and why

### If Something Goes Wrong

The `examples/sir_simulation/` directory contains working fallback code if the live demo fails.

---

## Quick Commands

```bash
# Preview slides
cd slides && quarto preview slides.qmd

# Run the example simulation
python examples/sir_simulation/main.py

# Install dependencies
pip install -r requirements.txt
```

---

## Contact

Fabian Spill — f.spill@bham.ac.uk
