# Texas Proposed Regulations ETL Pipeline

This project extracts, processes, and normalizes metadata about **proposed state regulations** published by the [Texas Commission on Environmental Quality (TCEQ)](https://www.tceq.texas.gov/rules/prop.html). The pipeline scrapes structured meta data about proposed rules, downloads and parses linked PDF documents (such as Chapter revisions), and outputs a clean, structured JSON dataset.

---

## Features

- Extracts regulation metadata (title, ID, dates, chapters)
- Captures links to source documents (PDFs)
- Parses **Chapter documents** to include the full proposed rule text
- Saves output as a structured JSON file
- Organized into ETL modules for clarity and maintainability

---

## Project Structure

```
etl/
├── extract.py      # Web scraper for TCEQ rules
├── transform.py    # Full-text extraction from chapter PDFs
└── load.py         # Saves output to JSON
main.py             # Orchestrates the ETL process
requirements.txt    # Python dependencies
output/
└── proposed_rules.json
tests/
├── test_extract.py      # pytest for extaction
├── test_transform.py    # pytest for transformation
└── test_load.py         # pytest for load
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/tceq-etl.git
   cd tceq-etl
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the ETL pipeline**
   ```bash
   python main.py
   ```

**Output format**

```json
{
    "title": "Chapter 115 VOC Rule Revisions for the Bexar County 2015 Eight Hour Ozone Serious Nonattainment AreaThe new and amended rules implemented through this rulemaking, if adopted, are necessary to address required federal Clean Air Act state implementation plan elements for the Bexar County serious ozone nonattainment area.",
    "identifier": "2025-006-115-AI",
    "proposed_date": "2025-07-09 00:00:00",
    "comments_due": "2025-08-25 00:00:00",
    "chapters": [ "Ch. 115" ],
    "sources": [
      "https://www.tceq.texas.gov/downloads/rules/current/25006115_correction.pdf",
      "https://www.tceq.texas.gov/downloads/rules/current/25006115_pex.pdf",
      "https://www.tceq.texas.gov/downloads/rules/current/25006115_pro.pdf"
    ],
    "full_text": "Texas Commission on Environmental Quality Page ...."
}
```