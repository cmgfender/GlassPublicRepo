import pdfplumber
import json
import re
import os
import sys

def validate_pdf(file_path):
    """
    Validates if the given file is a PDF.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.lower().endswith(".pdf"):
        raise ValueError(f"Invalid file type. Expected a PDF, got: {file_path}")

def extract_text_and_tables(file_path):
    """
    Extracts text and tables from a PDF using pdfplumber.
    """
    structured_data = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            tables = page.extract_tables()
            structured_data.append({
                "page": i + 1,
                "text": page_text.strip() if page_text else "",
                "tables": [table for table in tables if table]  # Add only non-empty tables
            })
    return structured_data

def organize_content(structured_data):
    """
    Organizes the extracted data into sections and subsections.
    """
    content = []
    current_section = None
    current_subsection = None
    section_pattern = re.compile(r"^[A-Z][A-Z &]+$")
    subsection_pattern = re.compile(r"^[A-Za-z0-9 ,.-]+:$")

    for page in structured_data:
        lines = page["text"].split("\n")
        for line in lines:
            line = line.strip()

            if section_pattern.match(line):
                if current_section:
                    if current_subsection:
                        current_section["subsections"].append(current_subsection)
                    content.append(current_section)
                current_section = {"title": line, "subsections": [], "tables": []}
                current_subsection = None

            elif subsection_pattern.match(line) and current_section:
                if current_subsection:
                    current_section["subsections"].append(current_subsection)
                current_subsection = {"title": line, "content": "", "tables": []}

            elif current_subsection:
                current_subsection["content"] += f"{line} "

        for table in page["tables"]:
            if current_subsection:
                current_subsection["tables"].append(table)
            elif current_section:
                current_section["tables"].append(table)

    if current_subsection and current_section:
        current_section["subsections"].append(current_subsection)
    if current_section:
        content.append(current_section)

    return content

def save_to_json(data, output_file):
    """
    Saves structured data to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_pdf.py <input_pdf_path> <output_json_path>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    output_json = sys.argv[2]

    try:
        validate_pdf(pdf_file)
        print("[INFO] Extracting text and tables from PDF...")
        extracted_data = extract_text_and_tables(pdf_file)

        print("[INFO] Organizing content...")
        structured_content = organize_content(extracted_data)

        print("[INFO] Saving output...")
        save_to_json(structured_content, output_json)

        print(f"[INFO] Process complete. JSON saved to {output_json}")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()