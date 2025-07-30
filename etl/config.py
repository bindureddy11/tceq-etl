# etl/config.py
# Centralized configuration for ETL pipeline
import os

# URL of the TCEQ proposed rules page
TCEQ_PROPOSED_RULES_URL = "https://www.tceq.texas.gov/rules/prop.html"

# Base URL for TCEQ links
BASE_STATE_URL = "https://www.tceq.texas.gov"

# Output file path for JSON data
OUTPUT_JSON_PATH = "output/proposed_rules.json"

# Log directory
LOG_DIR = "logs"

# Log file path
LOG_FILE_PATH = os.path.join(LOG_DIR, "etl.log")

# Number of PDF pages to extract text from
PDF_PAGES_TO_EXTRACT = 2 # None means extract all pages

# PDF request timeout (seconds)
PDF_REQUEST_TIMEOUT = 10

# Minimum number of cells expected in a row for valid data extraction
MIN_ROW_CELLS = 3

# Agency name for metadata
AGENCY_NAME = "Texas Commission on Environmental Quality (TCEQ)"