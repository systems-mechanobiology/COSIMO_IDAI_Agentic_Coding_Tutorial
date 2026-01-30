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
*   **Community:** Open call for contributors (coding & prompts) and skeptics (failure cases).
*   **Ethics:** Dedicated sessions coming later.

## 0.8. The Challenge (Intro)
*   **Context:** Remind audience of the Pandemic. The famous **R number**.
*   **Goal:** Simulate SIR (S -> I -> R) high-level concepts.
*   **Method:** Build, Visualize, Analyze.

## 1. The Narrative Arc
**Theme:** "From syntax to scientific intent."
**Hook:** "We used to suggest code; now we collaborate on solutions."

## 2. The Evolution of AI Coding (Deep Dive)

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
    1.  **Plan:** "I need to install numpy and write a script."
    2.  **Act:** Writes file `model.py`.
    3.  **Observe:** Runs `python model.py`. Sees `ImportError`.
    4.  **Refine:** Installs package. Runs again.
*   **Why it matters:** It closes the feedback loop *without human intervention*.

## 3. The Model Landscape (2026 Usage)

### 1. Instruction Models (The "Doers")
*   **Best for:** Quick refactors, simple functions, docs.
*   **Top Tier:** **GPT-5.2 Pro**, Kimi (Moonshot), DeepSeek V3.
*   **Open Source:** Llama 4 (405B), Mistral.

### 2. Reasoning Models (The "Thinkers")
*   **Best for:** Complex architecture, mathematical derivations.
*   **Top Tier:** OpenAI o3-high, DeepSeek R2, Gemini 3.0 Flash-Thinking.

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

## 6. Selected Demo Plan: SIR Model

**Goal:** Build a simulator for disease spread and fit it to data.

### Step 1: Blank Slate to Simulation
*   Prompt: "Create a Python project for an SIR (Susceptible-Infected-Recovered) model using `scipy.integrate.odeint`."
*   *Highlight:* It sets up folder structure (`src/`, `data/`) automatically.

### Step 2: Running the Model
*   Prompt: "Simulate an outbreak with N=1000, beta=0.3, gamma=0.1. Plot the curves."
*   *Highlight:* It chooses reasonable visualization defaults.

### Step 3: Adding Real Data (The "Extension")
*   *Idea:* Use a small hardcoded dataset or a CSV representing "Influenza 1918" or "COVID 2020".
*   Prompt: "Here is a list of weekly case counts: [10, 50, 200, 800...]. Plot this data on top of the simulation."
*   *Highlight:* Combining synthetic and real data.

### Step 4: Fitting (Advanced/Optional)
*   Prompt: "Use `scipy.optimize.minimize` to estimate the best `beta` and `gamma` that fit this data."
*   *Highlight:* This is a complex task that usually takes a human 30 mins; Agent takes 30 secs.

## 7. Q&A Prep
*   **"Can I run this on my sensitive patient data?"** -> Use Local Models (DeepSeek R2 / Llama 4) via Cline or Ollama.
*   **"It gets the math wrong."** -> Use a Reasoning Model (o3/R1) for the derivation step, then switched to an Instruction Model for the coding.
