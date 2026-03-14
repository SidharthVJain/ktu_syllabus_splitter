import fitz  # PyMuPDF
import re
import os
import argparse


def extract_course_code(text):
    """
    Extract course code like GAMAT401, PCCST402 etc.
    """
    match = re.search(r"Course Code\s+([A-Z0-9]+)", text)
    if match:
        return match.group(1)
    return None


def split_pdf(input_pdf, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(input_pdf)

    current_pages = []
    current_code = None

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()

        code = extract_course_code(text)

        if code:
            # Save previous course if exists
            if current_code and current_pages:
                new_doc = fitz.open()

                for p in current_pages:
                    new_doc.insert_pdf(doc, from_page=p, to_page=p)

                output_path = os.path.join(output_dir, f"{current_code}.pdf")
                new_doc.save(output_path)
                new_doc.close()

                current_pages = []

            current_code = code

        current_pages.append(page_num)

    # Save last course
    if current_code and current_pages:
        new_doc = fitz.open()

        for p in current_pages:
            new_doc.insert_pdf(doc, from_page=p, to_page=p)

        output_path = os.path.join(output_dir, f"{current_code}.pdf")
        new_doc.save(output_path)
        new_doc.close()

    print("Splitting complete!")


def main():
    parser = argparse.ArgumentParser(description="Split curriculum PDF by course code")
    parser.add_argument("input_pdf", help="Path to input PDF")
    parser.add_argument("-o", "--output", default="courses", help="Output directory")

    args = parser.parse_args()

    split_pdf(args.input_pdf, args.output)


if __name__ == "__main__":
    main()
