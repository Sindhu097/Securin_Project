from flask import Flask, render_template, request
import sqlite3
import ast
from datetime import datetime

app = Flask(__name__)
DB_PATH = "/Users/sindhus/Desktop/Securin_Project/XML_Parsing_and_Database/cpe_data.db"

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
    except:
        return ""

def query_database(filters, page, per_page):
    offset = (page - 1) * per_page
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT cpe_title, cpe_22_uri, cpe_23_uri, reference_links, cpe_22_deprecation_date, cpe_23_deprecation_date FROM cpe_entries WHERE 1=1"
    params = []

    if filters["cpe_title"]:
        query += " AND cpe_title LIKE ?"
        params.append(f"%{filters['cpe_title']}%")
    if filters["cpe_22_uri"]:
        query += " AND cpe_22_uri LIKE ?"
        params.append(f"%{filters['cpe_22_uri']}%")
    if filters["cpe_23_uri"]:
        query += " AND cpe_23_uri LIKE ?"
        params.append(f"%{filters['cpe_23_uri']}%")

    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM cpe_entries WHERE 1=1" + 
        (" AND cpe_title LIKE ?" if filters["cpe_title"] else "") +
        (" AND cpe_22_uri LIKE ?" if filters["cpe_22_uri"] else "") +
        (" AND cpe_23_uri LIKE ?" if filters["cpe_23_uri"] else ""),
        tuple([f"%{filters['cpe_title']}%"] if filters["cpe_title"] else [] + [f"%{filters['cpe_22_uri']}%"] if filters["cpe_22_uri"] else [] + [f"%{filters['cpe_23_uri']}%"] if filters["cpe_23_uri"] else [])
    )
    total = cursor.fetchone()[0]
    conn.close()

    data = []
    for row in rows:
        data.append({
            "cpe_title": row[0],
            "cpe_22_uri": row[1],
            "cpe_23_uri": row[2],
            "reference_links": ast.literal_eval(row[3]) if row[3] else [],
            "cpe_22_deprecation_date": format_date(row[4]),
            "cpe_23_deprecation_date": format_date(row[5])
        })

    return data, total

@app.route("/", methods=["GET"])
def index():
    filters = {
        "cpe_title": request.args.get("cpe_title", ""),
        "cpe_22_uri": request.args.get("cpe_22_uri", ""),
        "cpe_23_uri": request.args.get("cpe_23_uri", "")
    }

    try:
        page = int(request.args.get("page", 1))
    except:
        page = 1

    try:
        per_page = int(request.args.get("per_page", 15))
        if per_page < 15 or per_page > 50:
            per_page = 15
    except:
        per_page = 15

    data, total = query_database(filters, page, per_page)
    total_pages = (total + per_page - 1) // per_page

    return render_template("index.html",results=data,filters=filters,page=page,per_page=per_page,total=total,total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)
