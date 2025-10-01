from flask import Blueprint, request, jsonify
from gstchecker import gstchecker

gst_bp = Blueprint("gst_bp", __name__)

@gst_bp.route("/gst", methods=["POST"])
def check_gst():
    data = request.get_json()
    gst_number = data.get("gstNumber")

    if not gst_number:
        return jsonify({"message": "No GST number provided"}), 400

    gstchecker.check(gst_number)
    print(gst_number)
    # Check if attributes exist and have been set
    if hasattr(gstchecker, 'name') and gstchecker.name:
        result = {
            "Name": gstchecker.name,
            "PAN": gstchecker.pan,
            "Person": gstchecker.person,
            "Type": gstchecker.gst_type,
            "Address": gstchecker.add,
            "Date": gstchecker.date,
            "Status": gstchecker.status
        }
        return jsonify(result), 200
    else:
        return jsonify({"message": "No data found for this GST number"}), 404
