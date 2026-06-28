import os
import argparse
import sys
import pypdf

# Mapping of day number (1-31) to field name in the PDF calendar
# Note: Day 11 is '2.56' because '2.55' is skipped in the form definition.
DAY_TO_FIELD = {
    1: "2.45",
    2: "2.46",
    3: "2.47",
    4: "2.48",
    5: "2.49",
    6: "2.50",
    7: "2.51",
    8: "2.52",
    9: "2.53",
    10: "2.54",
    11: "2.56",  # skipped 2.55
    12: "2.57",
    13: "2.58",
    14: "2.59",
    15: "2.60",
    16: "2.61",
    17: "2.62",
    18: "2.63",
    19: "2.64",
    20: "2.65",
    21: "2.66",
    22: "2.67",
    23: "2.68",
    24: "2.69",
    25: "2.70",
    26: "2.71",
    27: "2.72",
    28: "2.73",
    29: "2.74",
    30: "2.75",
    31: "2.76"
}

def load_env():
    # Search upwards from the script location to find the .env file
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = None
    while curr_dir:
        test_path = os.path.join(curr_dir, ".env")
        if os.path.exists(test_path):
            env_path = test_path
            break
        parent = os.path.dirname(curr_dir)
        if parent == curr_dir:
            break
        curr_dir = parent
        
    env_config = {}
    if env_path:
        print(f"Reading configuration from: {env_path}")
        with open(env_path, "r", encoding="utf-8") as f_env:
            for line in f_env:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    env_config[k.strip()] = v.strip().strip("'\"")
    else:
        print("Warning: .env configuration file not found. Falling back to default values.")
        
    return env_config

def fill_form(template_path, output_path, month, year, days_worked, hourly_rate, lieu, material_costs):
    print(f"Loading template: {template_path}")
    reader = pypdf.PdfReader(template_path)
    writer = pypdf.PdfWriter()
    writer.append(reader)
    
    # Load env config
    config = load_env()
        
    # 1. Prepare static personal data from config
    fields_to_fill = {
        "1.2": config.get("NOM", "YANG"),
        "1.3": config.get("PRENOM", "BOYOU"),
        "Textfeld 101": config.get("AVS_SUFFIX", "8609631634"),  # AVS suffix
        "Textfeld 102": config.get("DOB", "22111987"),  # Date of birth
        "5.17": lieu or config.get("LIEU", "GENÈVE"),
    }
    
    # 2. Add Month/Year (Format: MMYYYY)
    month_str = f"{month:02d}"
    year_str = f"{year}"
    fields_to_fill["Textfeld 106"] = f"{month_str}{year_str}"
    
    # 3. Add Signature Date (Format: DDMMYYYY, defaulting to last day of the month)
    import calendar
    last_day = calendar.monthrange(year, month)[1]
    fields_to_fill["Textfeld 95"] = f"{last_day:02d}{month_str}{year_str}"
    
    # 4. Set calendar hours for each day
    for day, field_name in DAY_TO_FIELD.items():
        if day in days_worked:
            fields_to_fill[field_name] = "1"
        else:
            fields_to_fill[field_name] = ""
            
    # 5. Income calculations
    total_hours = len(days_worked)
    gross_income = total_hours * hourly_rate
    fields_to_fill["1.77"] = str(gross_income)
    fields_to_fill["1.81"] = str(material_costs)
    
    # 6. Checkbox to attach documents
    fields_to_fill["Kontrollkästchen 19"] = "/Ja"
    
    # Keep other checkboxes / radio buttons standard
    extra_fields = {
        "Kontrollkästchen 10": "/Off",
        "Kontrollkästchen 18": "/Off",
        "Kontrollkästchen 20": "/Off",
        "Kontrollkästchen 7": "/Off",
        "Kontrollkästchen 8": "/Off",
        "Kontrollkästchen 9": "/Off",
        "Optionsfeld 1": "/",
        "Optionsfeld 2": "/",
        "Optionsfeld 20": "/",
        "Optionsfeld 21": "/",
        "Optionsfeld 22": "/",
        "Optionsfeld 23": "/",
        "Optionsfeld 3": "/",
        "Optionsfeld 30": "/",
        "Optionsfeld 31": "/",
        "Optionsfeld 4": "/",
        "Optionsfeld 71": "/"
    }
    fields_to_fill.update(extra_fields)
    
    # Update field values on all pages
    for page_idx in range(len(writer.pages)):
        writer.update_page_form_field_values(writer.pages[page_idx], fields_to_fill)
        
    print(f"Saving prefilled form to: {output_path}")
    with open(output_path, "wb") as f_out:
        writer.write(f_out)
        
    print("PDF filled successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill out Geneva OCE Attestation de gain intermédiaire PDF form.")
    parser.add_argument("--template", default="e3907e43-194e-45cb-8790-4849f1a5f29a.pdf", help="Path to empty template PDF")
    parser.add_argument("--output", default="June.pdf", help="Path to output PDF")
    parser.add_argument("--month", type=int, default=6, help="Month number (1-12)")
    parser.add_argument("--year", type=int, default=2026, help="Year")
    parser.add_argument("--days", default="1,9,10,12,16,17,19", help="Comma-separated list of days worked")
    parser.add_argument("--rate", type=int, default=30, help="Hourly rate in CHF")
    parser.add_argument("--lieu", default="", help="Lieu of signature")
    parser.add_argument("--costs", type=int, default=0, help="Material costs in CHF")
    
    args = parser.parse_args()
    
    # Locate template and output paths.
    # We resolve paths relative to the current working directory.
    template_abs = os.path.abspath(args.template)
    output_abs = os.path.abspath(args.output)
    
    days_list = [int(d.strip()) for d in args.days.split(",") if d.strip()]
    
    fill_form(template_abs, output_abs, args.month, args.year, days_list, args.rate, args.lieu, args.costs)
