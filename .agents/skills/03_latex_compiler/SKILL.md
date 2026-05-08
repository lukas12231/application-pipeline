---
name: 03_latex_compiler
description: A specialized LaTeX compiler agent. Reads the optimized Markdown components and directly injects them into the existing LaTeX files using safe file-editing tools. Handles all LaTeX escaping.
---

**Inputs:**
- `./cv_injection_data.md`
- `./skill_matrix.md`
- `./letter_injection_data.md`
- `./cv/document.tex`
- `./letter/document.tex`
- `./.agents/skills/03_latex_compiler/resources/latex_rules.md` (Rules for LaTeX injection)

**Outputs:**
- Modifies `./cv/document.tex`
- Modifies `./letter/document.tex`

---

**INSTRUCTIONS:**

**STEP 0: MANDATORY ASSET INQUIRY (HARD STOP)**
Before you read any files or perform any edits, you **MUST** ask the user these two questions in the chat:
1.  "Möchten Sie ein Profilbild in den Lebenslauf einbinden?"
2.  "Möchten Sie Firmenlogos für Ihre Arbeitsstationen einbinden?"

**CRITICAL RULE:** You are **strictly forbidden** from proceeding to any other step until the user has provided clear "Yes/No" answers and completed the logo mapping if required.

**STEP 1: Parse the Markdown Data**
Read `cv_injection_data.md`, `skill_matrix.md`, and `letter_injection_data.md`. Ensure all text is LaTeX-safe (escape %, &, $).

**STEP 2: Asset Handling & Mapping (IF YES)**
1.  **IF "NO" to images:** Comment out `\roundpic` and set logo arguments to `{}`.
2.  **IF "YES" to Logos:** Ask for mapping (Image -> Company). Set unmapped ones to `{}`.

**STEP 3: Inject the CV Content**
- **Summary:** Replace `Kurzprofil`.
- **Experience:** 
    - For each project in Markdown, use `\cvproject{[Name]}{[Itemize-List]}`.
    - Wrap multiple projects within the description field of `\cvevent`.
    - Use `[nosep,leftmargin=*,label=\textbullet]` for `itemize`.
- **Kompetenzmatrix:** Replace the rows in the matrix table.
    - Convert numerical levels (1-4) from `skill_matrix.md` to `\faStar` commands.
    - Level 1: `\faStar\faStarO\faStarO\faStarO`
    - Level 2: `\faStar\faStar\faStarO\faStarO`
    - Level 3: `\faStar\faStar\faStar\faStarO`
    - Level 4: `\faStar\faStar\faStar\faStar`
- **Sonstiges:** Update section.

**STEP 4: Inject the Cover Letter Content**
- Replace subject and body paragraphs.

**STEP 5: Verification & Compilation**
1. Report modified lines.
2. **Offer Compilation:** Ask the user: "Soll ich den Lebenslauf und das Anschreiben direkt für Sie kompilieren?"
3. **If "Yes":** Run `latexmk -pdf -interaction=nonstopmode document.tex` in both `cv/` and `letter/` directories.
4. If successful, confirm that the PDFs are ready for bundling.
