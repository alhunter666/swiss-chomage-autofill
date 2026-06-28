# Swiss Chomage Form Automation

A localized agent automation tool and custom Google Antigravity Skill to automate filling out the recurring monthly Geneva OCE unemployment PDF form ("Attestation de gain intermédiaire").

## Repository Structure

* `.agents/skills/swiss-chomage-form/`: The Google Antigravity Skill manifest and automation logic.
  * `SKILL.md`: Skill definition and prompt routing triggers.
  * `scripts/fill_oce_form.py`: Core python script to edit and prefill form data using `pypdf`.
* `.env.example`: A template for configuring your private parameters.
* `e3907e43-194e-45cb-8790-4849f1a5f29a.pdf`: The empty official PDF form template.

---

## Getting Started

### 1. Setup Environment
Copy `.env.example` to `.env` and fill in your personal details:
```bash
cp .env.example .env
```
Open `.env` and configure:
* `NOM`: Your last name (e.g. `YANG`)
* `PRENOM`: Your first name (e.g. `BOYOU`)
* `AVS_SUFFIX`: The suffix of your AVS number (the part after 756, e.g. `8609631634`)
* `DOB`: Your date of birth in DDMMYYYY format (e.g. `22111987`)
* `LIEU`: Your default signing location (e.g. `GENÈVE`)

### 2. Install Dependencies
Install `pypdf` using pip:
```bash
pip install pypdf
```

### 3. Usage
Run the script to generate a prefilled form:
```bash
python .agents/skills/swiss-chomage-form/scripts/fill_oce_form.py \
  --template e3907e43-194e-45cb-8790-4849f1a5f29a.pdf \
  --output June.pdf \
  --month 6 \
  --year 2026 \
  --days "1,9,10,12,16,17,19" \
  --rate 30
```

---

## Using with Google Antigravity

Because this is packaged as an Antigravity Agent Skill under `.agents/skills/`, it is automatically detected by any Antigravity instance in this workspace. You can run it via commands or plain text prompts such as:
* `/fill-chomage --month 7 --days 3,10,15 --rate 30`
* *"Please fill out my chômage form for July. I worked on the 3rd, 10th, and 15th for 1 hour each, at 30 CHF/hour."*
