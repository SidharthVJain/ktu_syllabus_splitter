# KTU syllabus Splitter

A Python script that splits a curriculum PDF into multiple PDFs, one per course, using the **course code** found on each course's starting page.

## Overview

Many curriculum documents contain multiple course descriptions in a single PDF. Each course section typically begins with a page that includes a **"Course Code"** field (e.g., `GAMAT401`, `PCCST402`).

This script scans the PDF page by page, detects these course codes, and splits the document so that each course is saved as its own PDF file named after its course code.

## Features

* Automatically detects course boundaries using the **"Course Code"** field.
* Saves each course section as a separate PDF.
* Names each output file using the detected course code.
* Works with curriculum PDFs containing multiple course sections.

## Requirements

* Python 3.7+
* PyMuPDF

Install dependencies:

```bash
pip install pymupdf
```

## Usage

Run the script from the command line:

```bash
python split_courses.py input.pdf
```

By default, output files will be written to a directory called `courses`.

### Specify an Output Directory

```bash
python split_courses.py input.pdf -o output_folder
```

## Example

Input:

```
curriculum.pdf
```

Output:

```
courses/
 ├── GAMAT401.pdf
 ├── PCCST402.pdf
 ├── PCCST403.pdf
 ├── PBCST404.pdf
 ├── PECST411.pdf
 ...
```

Each file contains all pages belonging to that course.

## License

This script is provided for educational and personal use.
