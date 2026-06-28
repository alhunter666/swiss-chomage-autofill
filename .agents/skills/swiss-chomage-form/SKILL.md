---
name: swiss-chomage-form
description: "Fills out Section 1 (calendar days) and Section 14 (independent earnings) on the Swiss Attestation de gain intermédiaire PDF form."
---

# Swiss Chomage Form Automation Skill

This skill automates filling out the recurring monthly PDF form ("Attestation de gain intermédiaire") for Geneva's OCE unemployment benefits.

## Triggers
This skill triggers automatically when the user:
- Asks to fill in or generate the unemployment/chômage PDF form for a specific month.
- Refers to their Geneva OCE form.
- Runs the `/fill-chomage` custom command.

## Instructions
1. Check that a `.env` file exists at the root of the workspace containing the client details (`NOM`, `PRENOM`, `AVS_SUFFIX`, `DOB`, `LIEU`).
2. Identify the worked days, month, year, and hourly rate from the user's prompt or inputs.
3. If any details are missing, clarify them with the user.
4. Execute the Python script at `scripts/fill_oce_form.py` in the skill folder using python to generate the filled PDF.
