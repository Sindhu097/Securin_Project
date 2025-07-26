import sqlite3
import xml.etree.ElementTree as ET
import json

# Namespaces
ns = {
    "cpe-dict": "http://cpe.mitre.org/dictionary/2.0",
    "cpe-23": "http://scap.nist.gov/schema/cpe-extension/2.3"
}


# 1. Connect to SQLite
conn = sqlite3.connect("cpe_data.db")
cursor = conn.cursor()

# 2. Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS cpe_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpe_title TEXT,
    cpe_22_uri TEXT,
    cpe_23_uri TEXT,
    reference_links TEXT,
    cpe_22_deprecation_date TEXT,
    cpe_23_deprecation_date TEXT
)
""")
conn.commit()

# 3. Load and parse XML
tree = ET.parse("/Users/sindhus/Desktop/Securin_Project/XML_Parsing_and_Database/official-cpe-dictionary_v2.3.xml")
root = tree.getroot()
items = root.findall(".//cpe-dict:cpe-item", ns)

# 4. Open output file
with open("cpe_output.txt", "w", encoding="utf-8") as f:
    # 5. Process each CPE item
    for item in items:
        cpe_22_uri = item.get("name")

        title_elem = item.find("cpe-dict:title", ns)
        cpe_title = title_elem.text if title_elem is not None else None

        references = []
        for ref in item.findall(".//cpe-dict:reference", ns):
            href = ref.get("href")
            if href:
                references.append(href)
        
        cpe_23_elem = item.find("cpe-23:cpe23-item", ns)
        cpe_23_uri = cpe_23_elem.get("name") if cpe_23_elem is not None else None
        
        cpe_23_deprecation = None
        if cpe_23_elem is not None:
            deprecation_elem = cpe_23_elem.find("cpe-23:deprecation", ns)
        if deprecation_elem is not None:
            cpe_23_deprecation = deprecation_elem.get("date")

        # cpe-22 deprecation comes as attribute
        cpe_22_deprecation = item.get("deprecation_date")

        # cpe-23 deprecation is a nested tag
        cpe_23_deprecation_elem = item.find("cpe-23:deprecation", ns)
        cpe_23_deprecation = cpe_23_deprecation_elem.get("date") if cpe_23_deprecation_elem is not None else None

        # Insert into database
        cursor.execute("""
            INSERT INTO cpe_entries (
                cpe_title,
                cpe_22_uri,
                cpe_23_uri,
                reference_links,
                cpe_22_deprecation_date,
                cpe_23_deprecation_date
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            cpe_title,
            cpe_22_uri,
            cpe_23_uri,
            json.dumps(references),
            cpe_22_deprecation,
            cpe_23_deprecation
        ))

        # Write to output file
        f.write(json.dumps({
            "cpe_title": cpe_title,
            "cpe_22_uri": cpe_22_uri,
            "cpe_23_uri": cpe_23_uri,
            "reference_links": references,
            "cpe_22_deprecation_date": cpe_22_deprecation,
            "cpe_23_deprecation_date": cpe_23_deprecation
        }, ensure_ascii=False) + "\n")

# Finalize
conn.commit()
conn.close()
