
from flask import Flask, request, jsonify
import csv
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

DATABASE = Path(__file__).parent / "database"
DATABASE.mkdir(exist_ok=True)

CSV_FILE = DATABASE / "guest_inquiries.csv"


# Create CSV file with headings if it does not exist
if not CSV_FILE.exists():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp",
            "guest_name",
            "guest_message",
            "party_size"
        ])


@app.route("/")
def home():
    return jsonify({
        "project": "Spice Route",
        "status": "API is running successfully"
    })


@app.route("/api/inquiries", methods=["POST"])
def receive_inquiry():

    data = request.get_json(silent=True) or {}

    errors = []

    guest_name = data.get("guest_name")
    guest_message = data.get("guest_message")
    party_size = data.get("party_size")

    # Validate guest name
    if not isinstance(guest_name, str) or not guest_name.strip():
        errors.append("Guest name is required.")

    # Validate guest message
    if not isinstance(guest_message, str) or not guest_message.strip():
        errors.append("Guest message is required.")

    # Clean and validate party size
    if party_size is not None:
        try:
            party_size = int(str(party_size).strip())

            if not 1 <= party_size <= 10:
                errors.append("Party size must be between 1 and 10.")

        except (ValueError, TypeError):
            errors.append("Party size must be a valid number.")

    # Return validation errors
    if errors:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    # Save valid inquiry in CSV
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            guest_name.strip(),
            guest_message.strip(),
            party_size
        ])

    return jsonify({
        "success": True,
        "message": "Guest inquiry received and saved successfully."
    }), 200


def read_csv_file(filename):

    file_path = DATABASE / filename

    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)


@app.route("/api/menu", methods=["GET"])
def get_menu():
    return jsonify(read_csv_file("menu.csv"))


@app.route("/api/operating-hours", methods=["GET"])
def get_operating_hours():
    return jsonify(read_csv_file("operating_hours.csv"))


@app.route("/api/reservation-rules", methods=["GET"])
def get_reservation_rules():
    return jsonify(read_csv_file("reservation_rules.csv"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
