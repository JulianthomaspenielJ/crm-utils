from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup
import json

table_bp = Blueprint("table_bp", __name__)

@table_bp.route("/compliance", methods=["POST"])
def extract_table():
    data = request.get_json()
    url = data.get("link")

    if not url:
        return jsonify({"message": "No URL provided"}), 400

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')

        if not table:
            print("No table found on the provided URL")
            return jsonify({"message": "No table found on the provided URL"}), 404

        data_list = []  # List to hold the entire row data

        # Iterate over each row in the table
        for row in table.find_all('tr'):
            cells = row.find_all(['td', 'th'])
            # Get the entire row data
            if cells:
                row_data = [cell.get_text(strip=True) for cell in cells]
                data_list.append(row_data)

        return jsonify(data_list), 200

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return jsonify({"message": f"Request failed: {str(e)}"}), 500