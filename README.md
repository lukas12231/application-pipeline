# Agentic Job Application Pipeline

A high-fidelity, AI-powered workspace designed to generate professional, tailored German job applications for the IT sector. This framework automates the entire process from data extraction to LaTeX compilation and PDF bundling.

## Table of Contents
- [🚀 Quick Start](#-quick-start)
- [🪄 Magic Command](#-magic-command)
- [🛠 Workflow Phases](#-workflow-phases)
- [🧠 Skill Deep Dive](#-skill-deep-dive)
- [📂 Project Structure](#-project-structure)
- [🤖 AI Operator Manual](#-ai-operator-manual)

---

## 🚀 Quick Start

### 1. Dependencies
Ensure you have the following installed:
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- A LaTeX distribution (e.g., [TeX Live](https://www.tug.org/texlive/), [MikTeX](https://miktex.org/))

### 2. Installation
Clone the repository and sync the environment:
```bash
uv sync
```

### 3. Data Preparation
- **Professional History:** Drop your existing CV (PDF/TXT) or LinkedIn export into the `import/` folder.
- **Target Job:** Paste the job description into `job_ad.txt`.

### 4. Run the Pipeline
Simply tell your AI agent:
> **"Start the application flow"**

---

## 🪄 Magic Command

This repository uses an agentic **Workflow Controller**. You do not need to trigger skills manually. By saying **"Start the application flow"**, the agent will:
1. Detect your current state.
2. Initialize your data if missing.
3. Perform analysis and strategy mapping.
4. Prompt you for specific metrics or image mapping.
5. Generate and inject the final LaTeX content.

---

## 🛠 Workflow Phases

| Phase | Description |
| :--- | :--- |
| **0. Initialization** | Bootstraps your professional history into a structured `baseline_profile.md`. |
| **0.5 Scouting** | (Optional) Automated discovery of suitable roles in Germany. |
| **1. Analysis** | Maps your profile against the job ad and identifies "Hidden Pain Points". |
| **2. Strategy** | Defines a winning narrative and pivoting strategy for the application. |
| **2.5 Skill Matrix Review** | Dedicated phase to review and adjust your technical competence matrix. |
| **3. Synthesis** | Rewrites CV bullets (XYZ Formula) and drafts a targeted cover letter. |
| **4. Injection** | Safely updates LaTeX templates and handles asset/logo mapping. |
| **5. Bundling** | Merges compiled PDFs and attachments into a single `Bewerbung.pdf`. |

---

## 🧠 Skill Deep Dive

### 00_init_workspace
Acts as a Digital Onboarding Assistant. It synthesizes messy input data from the `import/` folder into a clean, structured source of truth.

### 01_gap_analyzer
The "Tech Recruiter" agent. It performs a semantic comparison between you and the job ad, identifying critical gaps and asking targeted questions to fill them.

### 02_content_architect
The "Strategy Consultant". It doesn't write text yet; it defines the *narrative*—the specific "Angle" that will make you the perfect candidate for this specific company.

### 03_latex_compiler
The "Technical Developer". It handles character escaping and injects content into LaTeX. It includes a **Mandatory Asset Inquiry** to map company logos correctly.

### 04_application_letter
The "IT Copywriter". Generates a specialized German Anschreiben. It follows strict HR conventions: no AI-fluff, no subjunctive, and evidence-based arguments.

### 05_cv_content_optimizer
The "Resume Architect". Optimizes your CV experience using the **XYZ Formula** (Accomplished [X] as measured by [Y], by doing [Z]).

### 06_pdf_bundler
The "Final Assembly" agent. Provides a CLI-style interface to choose your bundle type and merge all documents into a professional submission package.

### 07_job_hunter
The "Automated Scout". Dynamically discovers, enriches, and filters job leads based on your `baseline_profile.md` and custom search criteria.

---

## 📂 Project Structure

- `cv/`: LaTeX CV template, style files, and images.
- `letter/`: LaTeX Cover Letter template.
- `import/`: Place your professional history here.
- `misc/`: Place certificates and references here for the final PDF.
- `.agents/`: Internal logic, skill definitions, and the workflow controller.

---

## 🤖 AI Operator Manual

For detailed instructions on how the agentic logic works or how to develop new skills, refer to the **[AGENTS.md](AGENTS.md)**.

---

## ⚖️ License
Personal Use. Please verify all AI-generated content before submission.
