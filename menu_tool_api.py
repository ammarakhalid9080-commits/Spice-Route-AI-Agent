
from flask import Flask, request, jsonify
from menu_tool import search_menu, check_dietary
from menu_search_tool import (
    search_menu as search_menu_v2,
    get_reservation_rules,
    check_reservation
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "service": "Spice Route Menu Tool API"
    })


@app.route("/menu/search", methods=["POST"])
def menu_search():
    data = request.get_json(silent=True) or {}
    item_name = data.get("item_name", "").strip()

    if not item_name:
        return jsonify({"error": "Item name is required"}), 400

    result = search_menu(item_name)
    status = 404 if "error" in result else 200

    return jsonify(result), status


@app.route("/menu/dietary-check", methods=["POST"])
def dietary_check():
    data = request.get_json(silent=True) or {}

    item_name = data.get("item_name", "").strip()
    requirement = data.get("requirement", "").strip()

    if not item_name or not requirement:
        return jsonify({
            "error": "Item name and dietary requirement are required"
        }), 400

    result = check_dietary(item_name, requirement)
    status = 404 if "error" in result else 200

    return jsonify(result), status

@app.route("/restaurant/lookup", methods=["POST"])
def restaurant_lookup():
    data = request.get_json(silent=True) or {}

    action = data.get("action", "").strip()

    if action == "search_menu":
        query = data.get("query", "")
        return jsonify(search_menu_v2(query))

    elif action == "get_reservation_rules":
        return jsonify(get_reservation_rules())

    elif action == "check_reservation":
        try:
            party_size = int(data.get("party_size"))
            day = data.get("day", "")
            requested_time = data.get("requested_time", "")

            result = check_reservation(
                party_size, day, requested_time
            )
            return jsonify(result)

        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "message": "Invalid reservation input."
            }), 400

    return jsonify({
        "success": False,
        "message": "Unknown action."
    }), 400
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
