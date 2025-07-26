from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "/Users/sindhus/Desktop/Securin_Project/XML_Parsing_and_Database/cpe_data.db"

@app.route("/api/search", methods=["GET"])
def search_cpes_advanced():
    cpe_title = request.args.get("cpe_title")
    cpe_22_uri = request.args.get("cpe_22_uri")
    cpe_23_uri = request.args.get("cpe_23_uri")
    deprecation_date = request.args.get("deprecation_date")

    query = "SELECT * FROM cpe_entries WHERE 1=1"
    params = []

    if cpe_title:
        query += " AND cpe_title LIKE ?"
        params.append(f"%{cpe_title}%")
    if cpe_22_uri:
        query += " AND cpe_22_uri LIKE ?"
        params.append(f"%{cpe_22_uri}%")
    if cpe_23_uri:
        query += " AND cpe_23_uri LIKE ?"
        params.append(f"%{cpe_23_uri}%")
    if deprecation_date:
        query += " AND (cpe_22_deprecation_date < ? OR cpe_23_deprecation_date < ?)"
        params.append(deprecation_date)
        params.append(deprecation_date)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "cpe_title": row[1],
            "cpe_22_uri": row[2],
            "cpe_23_uri": row[3],
            "reference_links": row[4],
            "cpe_22_deprecation_date": row[5],
            "cpe_23_deprecation_date": row[6],
        })

    return jsonify({"data": data})



if __name__ == '__main__':
    app.run(debug=True)