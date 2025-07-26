schema.sql 

-- Database: cpe_data.db
-- Table: cpe_entries

-- This script contains the schema and sample queries used to verify the database content.
-- NOTE: Data insertion is handled automatically by the parser.py script.

-- 🏗️ TABLE CREATION (already done in parser.py)
CREATE TABLE IF NOT EXISTS cpe_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpe_title TEXT,
    cpe_22_uri TEXT,
    cpe_23_uri TEXT,
    reference_links TEXT,
    cpe_22_deprecation_date TEXT,
    cpe_23_deprecation_date TEXT
);

-- ⚠️ NOTE:
-- The actual insertion of CPE data is performed by the parser.py script.
-- Each entry is parsed from XML and inserted using Python’s sqlite3 module.
-- Sample insertion code:
-- 
-- cursor.execute("""
--     INSERT INTO cpe_entries (
--         cpe_title,
--         cpe_22_uri,
--         cpe_23_uri,
--         reference_links,
--         cpe_22_deprecation_date,
--         cpe_23_deprecation_date
--     ) VALUES (?, ?, ?, ?, ?, ?)
-- """, (
--     cpe_title,
--     cpe_22_uri,
--     cpe_23_uri,
--     json.dumps(references),
--     cpe_22_deprecation,
--     cpe_23_deprecation
-- ))

-- ✅ TERMINAL COMMANDS TO VERIFY THE DATABASE:

-- Open the database:
sqlite3 cpe_data.db

-- Enable column display and headers:
.mode column
.headers on

-- View table list:
.tables

-- Count total entries:
SELECT COUNT(*) FROM cpe_entries;

-- View entries where cpe_22_deprecation_date is not null:
SELECT id, cpe_title, cpe_22_deprecation_date
FROM cpe_entries
WHERE cpe_22_deprecation_date IS NOT NULL
LIMIT 10;

-- View entries where cpe_23_deprecation_date is not null:
SELECT id, cpe_title, cpe_23_deprecation_date
FROM cpe_entries
WHERE cpe_23_deprecation_date IS NOT NULL
LIMIT 10;

-- View sample CPE titles:
SELECT id, cpe_title
FROM cpe_entries
WHERE cpe_title IS NOT NULL
LIMIT 10;

-- View sample CPE 22 URIs:
SELECT id, cpe_22_uri
FROM cpe_entries
WHERE cpe_22_uri IS NOT NULL
LIMIT 10;

-- View sample CPE 23 URIs:
SELECT id, cpe_23_uri
FROM cpe_entries
WHERE cpe_23_uri IS NOT NULL
LIMIT 10;

-- View sample reference links:
SELECT id, reference_links
FROM cpe_entries
WHERE reference_links IS NOT NULL
LIMIT 10;

