from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/api/cpes', methods=['GET'])
def get_cpes():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    offset = (page - 1) * page_size

    conn = sqlite3.connect("/Users/sindhus/Desktop/Securin_Project/XML_Parsing_and_Database/cpe_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cpe_entries LIMIT ? OFFSET ?", (page_size, offset))
    rows = cursor.fetchall()
    conn.close()

    cpes = []
    for row in rows:
        cpes.append({
            "id": row[0],
            "cpe_title": row[1],
            "cpe_22_uri": row[2],
            "cpe_23_uri": row[3],
            "reference_links": row[4],
            "cpe_22_deprecation_date": row[5],
            "cpe_23_deprecation_date": row[6],
        })

    return jsonify(cpes)

if __name__ == '__main__':
    app.run(debug=True)
