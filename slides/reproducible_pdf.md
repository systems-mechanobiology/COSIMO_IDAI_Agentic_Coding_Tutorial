# Reproducible PDF Slide Generation

To generate high-quality PDF slides from your Quarto Revealjs source while ensuring consistent font rendering and layout, follow this workflow.

## 1. The Core Strategy
The most reliable way to preserve the CSS styling, custom SCSS variables, and font rendering of your Revealjs slides is to render them to HTML first, and then use a headless browser (like Chrome or Chromium) to "print" that HTML to a PDF.

## 2. Prerequisites
Ensure you have Quarto and a headless-capable browser installed. You can use your system's Google Chrome or install an isolated Chromium via Quarto:

```bash
quarto install tool chromium
```

## 3. The Reproducible Command Workflow

### Step A: Render to HTML
First, render the slides to their web format. This ensures all CSS/SCSS and assets are processed.

```bash
quarto render slides/slides.qmd --to revealjs
```

### Step B: Generate PDF via Headless Chrome
Run the following command in your terminal. This uses Chrome's print engine in the background:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --disable-gpu \
  --print-to-pdf="slides/_output/slides_reveal.pdf" \
  "file:///$(pwd)/slides/_output/slides.html?print-pdf"
```

> [!TIP]
> **Why `?print-pdf`?**
> Appending `?print-pdf` to the URL tells Revealjs to load a special CSS stylesheet optimized for printing, which removes slide fragments and ensures each slide fits perfectly on one page.

## 4. Troubleshooting Fonts
If fonts look inconsistent across machines:
1. **Explicit Check**: Use standard web-safe fonts in your `custom.scss` (like Arial, Helvetica, sans-serif) as fallbacks.
2. **Google Fonts**: If you need specific luxury fonts, import them via Google Fonts in your SCSS. This ensures the browser can fetch them during the print process regardless of what is installed locally on the system.
3. **Embed Assets**: Set `embed-resources: true` in your `_quarto.yml` if you want a single HTML file that is safer for transport before printing.

## 5. Summary of Outputs
In this project, the following files are produced in `slides/_output/`:
- `slides.html`: The interactive presentation.
- `slides_reveal.pdf`: The high-fidelity PDF export (preserves design).
- `slides.pdf`: (Optional) The standard LaTeX/Beamer-style PDF.
