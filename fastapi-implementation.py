import json
import pdfplumber
import re
from collections import defaultdict

def clean_text(text):
    """Clean and normalize extracted text."""
    return re.sub(r'\s+', ' ', text).strip()

def parse_policy_pdf(pdf_path, json_output="parsed_policy.json"):
    data = defaultdict(dict)
    current_section = None
    current_subsection = None

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            
            # Split into lines
            lines = text.split("\n")
            
            for line in lines:
                line = clean_text(line)

                # Detect main sections like "1.0 OVERVIEW AND PURPOSE"
                match_section = re.match(r'^(\d+\.\d*)\s+(.*)', line)
                if match_section:
                    section_id, section_title = match_section.groups()
                    current_section = section_title
                    data[current_section] = {"content": [], "subsections": {}}
                    current_subsection = None
                    continue

                # Detect subsections like "4.1 FIRST LINE: CHIEF DATA OFFICER (CDO)"
                match_sub = re.match(r'^(\d+\.\d+)\s+(.*)', line)
                if match_sub and current_section:
                    subsection_id, subsection_title = match_sub.groups()
                    current_subsection = subsection_title
                    data[current_section]["subsections"][current_subsection] = []
                    continue

                # Otherwise, assign line to current section or subsection
                if current_subsection:
                    data[current_section]["subsections"][current_subsection].append(line)
                elif current_section:
                    data[current_section]["content"].append(line)

    # Convert defaultdict to normal dict
    data = {k: dict(v) if isinstance(v, dict) else v for k, v in data.items()}

    # Save JSON
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return data

if __name__ == "__main__":
    pdf_file = "AEMP70-EnterpriseDataManagementOperatingPolicy.pdf"  # Your PDF file
    output_file = "parsed_policy.json"
    result = parse_policy_pdf(pdf_file, output_file)
    print(f"Parsing complete! JSON saved to {output_file}")