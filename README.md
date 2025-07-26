# Securin_Project
README.md)

# CPE Data Collection and API Project

## Overview
This project retrieves Common Platform Enumeration (CPE) data from the official XML dictionary, extracts specific fields, stores it in an SQLite database, and exposes it through a RESTful API built using Flask.


## Components
### 1. XML Parsing (`parser.py`)
- Parses the CPE XML file (`official-cpe-dictionary_v2.3.xml`)
- Extracts the following:
  - CPE Title
  - CPE 22 URI
  - CPE 23 URI
  - Reference Links (as a list)
  - CPE 22 Deprecation Date
  - CPE 23 Deprecation Date
- Stores all parsed records into `cpe_data.db`

### 2. REST API Endpoints

#### A. `GET /api/cpes` — Get All CPEs (Paginated)
- Query Parameters:
  - `page` (default: 1)
  - `limit` (default: 10)
- Response: Paginated list of CPE entries ordered by ID.

#### B. `GET /search_cpes` — Search CPEs
- Query Parameters:
  - `title`
  - `cpe_22_uri`
  - `cpe_23_uri`
- Response: Filtered results based on the query.




## 🏗️ How to Run

1. Clone or unzip the project folder:
cd your_project_folder/

2. Parse the XML Data:
   - Make sure you have the `official-cpe-dictionary_v2.3.xml` file in your project directory.

3. Pass all the data into the SQLite database:
   - The parser script will extract and insert the required fields into `cpe_data.db`.

4. Install required dependencies:
   pip install flask

5. Create and activate a virtual environment (recommended):
   python3 -m venv venv
   source venv/bin/activate

6. Run the XML parser script:
   python parser.py

7. Verify the database:
   - Open SQLite:
     sqlite3 cpe_data.db
   - Check data:
     .tables
     SELECT COUNT(*) FROM cpe_entries;

8. Start the API server:
   - Run one of the following:
     python get_all_cpes.py
     # or
     python search_cpes.py

9. Use CURL or a browser to test the endpoints:
   Example:
   curl "http://127.0.0.1:5000/search_cpes?title=1password"


## 🧾 Dependencies
- Python 3.8+
- Flask
- sqlite3 (built-in)
- xml.etree.ElementTree (built-in)
