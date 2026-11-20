
from flask import Flask, request, jsonify
import csv
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

DATABASE = Path(__file__).parent / "database"
DATABASE.mkdir(exist_ok=True)

CSV_FILE = DATABASE / "guest_inquiries.csv"
LOG_FILE = DATABASE / "workflow_logs.csv"


# Create guest inquiries CSV
if not CSV_FILE.exists():
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp",
            "guest_name",
            "guest_message",
            "party_size"
        ])


# Create workflow logs CSV
if not LOG_FILE.exists():
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp",
            "execution_status",
            "workflow_step",
            "action",
            "http_status",
            "message"
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

    if not isinstance(guest_name, str) or not guest_name.strip():
        errors.append("Guest name is required.")

    if not isinstance(guest_message, str) or not guest_message.strip():
        errors.append("Guest message is required.")

    if party_size is not None:
        try:
            party_size = int(str(party_size).strip())

            if not 1 <= party_size <= 10:
                errors.append("Party size must be between 1 and 10.")

        except (ValueError, TypeError):
            errors.append("Party size must be a valid number.")

    if errors:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400

    try:
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

    except Exception:
        app.logger.exception("Failed to save guest inquiry")
        return jsonify({
            "success": False,
            "message": "Could not save guest inquiry."
        }), 500


# Workflow success and failure logging endpoint
@app.route("/api/workflow-logs", methods=["POST"])
def save_workflow_log():

    data = request.get_json(silent=True) or {}

    execution_status = data.get("execution_status")
    workflow_step = data.get("workflow_step")
    action = data.get("action")
    http_status = data.get("http_status")
    message = data.get("message")

    if execution_status not in ["success", "failure"]:
        return jsonify({
            "success": False,
            "error": "execution_status must be success or failure."
        }), 400

    if not all([
        isinstance(workflow_step, str) and workflow_step.strip(),
        isinstance(action, str) and action.strip(),
        isinstance(message, str) and message.strip()
    ]):
        return jsonify({
            "success": False,
            "error": "workflow_step, action and message are required."
        }), 400

    timestamp = datetime.now().isoformat(timespec="seconds")

    try:
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                execution_status,
                workflow_step.strip(),
                action.strip(),
                http_status if http_status is not None else "",
                message.strip()
            ])

        return jsonify({
            "success": True,
            "message": "Workflow execution logged successfully."
        }), 200

    except Exception:
        app.logger.exception("Failed to write workflow log")
        return jsonify({
            "success": False,
            "error": "Could not save workflow log."
        }), 500


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
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
