# Agent Workflow Controller

This document defines the logic for the "Start the application flow" command.

## State Detection Logic

When the user says "Start/Continue the application flow", the agent must:

1.  **Check Initialization**:
    - If `baseline_profile.md` is missing:
        - Check `import/` folder.
        - Trigger `00_init_workspace`.
2.  **Check Job Context**:
    - If `baseline_profile.md` exists but `job_ad.txt` is missing or contains the placeholder:
        - Stop and ask the user to provide the job advertisement in `job_ad.txt`.
3.  **Check Analysis State**:
    - If `job_ad.txt` is ready but `target_profile.md` or `interview_questions.md` is missing:
        - Trigger `01_gap_analyzer`.
4.  **Check Strategic Intent**:
    - If `target_profile.md` exists but `application_strategy.md` is missing:
        - Trigger `02_content_architect`.
5.  **Check Synthesis State**:
    - If `interview_questions.md` exists and contains answers:
        - If `cv_injection_data.md` or `letter_injection_data.md` is missing:
            - Trigger `05_cv_content_optimizer` and `04_application_letter`.
        - **Skill Matrix Review:** Once `skill_matrix.md` is generated, **STOP**. Ask the user to review the categories and star ratings (1-4). Explain the rating definitions.
6.  **Check Injection State**:
    - If injection data exists but `cv/document.tex` or `letter/document.tex` still contain placeholders:
        - **Asset Inquiry (MANDATORY):** You **MUST** stop and ask the user if they want a profile photo and/or company logos.
        - **HARD STOP:** Do not execute `03_latex_compiler` until the user has answered and (if logos are desired) provided the file-to-company mapping.
        - Trigger `03_latex_compiler`.
7.  **Check Bundling State**:
    - If the `.tex` files are updated and `.pdf` files exist in `cv/` and `letter/`:
        - Trigger `06_pdf_bundler`.

## Transition Rules
- Never skip a step unless the output file already exists and is valid.
- If a step requires user input (like answering questions), stop and wait for the user.
