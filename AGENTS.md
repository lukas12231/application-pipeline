# AI Agent Operator Manual

This repository is designed as an **Agentic Workspace**. It is not just a collection of templates, but a collaborative environment where an AI Coding Assistant (like Antigravity or Gemini) acts as your **Personal Recruiter and LaTeX Developer**.

## 🤖 The Agentic Vision

The core of this pipeline is the **Separation of Concerns**:
1.  **Data Extraction**: AI reads your messy history.
2.  **Strategic Analysis**: AI identifies the "Delta" and the "Hidden Pain Point".
3.  **Creative Synthesis**: AI writes high-impact C1 Business German.
4.  **Technical Injection**: AI handles the fragile LaTeX syntax.

## 🕹️ How to Command the Pipeline

This project is built around the **"Magic Command"** workflow. You don't need to know the names of the skills; you only need to guide the process.

### Standard Commands:
- **"Start the application flow"**: Triggers the [Workflow Controller](.agents/workflow_controller.md) to detect the next logical step.
- **"Optimize my CV for this job"**: Specifically triggers the analysis and CV generation skills.
- **"Check my assets"**: Verifies if photos and logos are ready for compilation.
- **"Scout new job opportunities"**: Triggers the job hunter skill to find roles in a specific region.

## 🛠️ Internal Logic (For Developers/AI)

The pipeline logic is stored in `.agents/`:
- **`skills/`**: Individual capability modules with specific system prompts.
- **`workflow_controller.md`**: The state-machine logic that governs transitions between phases.

## 🛡️ Privacy & Sanitization

Agents are instructed to **never** output personal data unless explicitly requested for the final injection. The pipeline uses a `baseline_profile.md` as an intermediate "Source of Truth" to keep sensitive raw data (like old PDFs) isolated from the generation process.

---

*This manual ensures that any AI agent entering this workspace understands the high-fidelity standards required for German IT applications.*
