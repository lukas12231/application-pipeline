# Agent Workflow Controller (Refined)

This document defines the state-machine logic for the end-to-end "Start the application flow" command.

## 🔄 Pipeline State Machine

### 🏁 Phase 0: Discovery & Onboarding
1.  **Check Profile**: Verify `baseline_profile.md` exists and is authentic.
    - **IF MISSING/PLACEHOLDER**:
        - List `import/`. If empty, **STOP** and ask the user: *"Please provide your professional history (PDF/LinkedIn) in the 'import/' folder."*
        - If files exist, trigger `00_init_workspace`.
2.  **Check Scouting Intent**: If `baseline_profile.md` is valid but no `job_ad.txt` exists:
    - **ASK USER**: *"Do you have a specific job link, or should I scout suitable job ads for you in Germany?"*
    - **IF SCOUT REQUESTED**:
        - Ask for: **Target Role, Location, Min Salary**.
        - Update `hunter_config.json`.
        - Trigger `07_job_hunter`.
        - **RESULT**: High-fidelity scouting results are written to `job_leads.md`.
        - **USER ACTION**: Open `job_leads.md`, select a lead, and paste its full description into `job_ad.txt`.
    - **IF SCOUT SKIPPED**:
        - **ASK USER**: *"Please paste your target job advertisement into 'job_ad.txt' to continue."*
        - **STOP** and wait for file creation.

    ### 🔍 Phase 1: Analysis & Strategy
    3.  **Gap Analysis**: If `job_ad.txt` contains a single, valid job description:
    - Trigger `01_gap_analyzer`.

    - **STOP** and wait for the user to answer `interview_questions.md`.
4.  **Strategic Narrative**: If questions are answered but `application_strategy.md` is missing:
    - Trigger `02_content_architect`.

### ✍️ Phase 2: Synthesis & Review
5.  **Content Optimization**: If strategy exists:
    - Trigger `05_cv_content_optimizer` and `04_application_letter`.
    - **STOP** for **Skill Matrix Review**: Ask the user to verify the `skill_matrix.md` ratings (1-4).

### 🏗️ Phase 3: Injection & Bundling
6.  **LaTeX Injection**: If review is complete:
    - **Asset Inquiry (MANDATORY)**: Ask for profile photo and company logos.
    - Trigger `03_latex_compiler`.
7.  **Final Assembly**:
    - Trigger `06_pdf_bundler`.

## ⚖️ Transition Rules
- **Proactivity**: Always suggest the next step.
- **Integrity**: Never proceed with placeholders.
- **Flexibility**: Allow the user to skip the scouting phase at any time.
