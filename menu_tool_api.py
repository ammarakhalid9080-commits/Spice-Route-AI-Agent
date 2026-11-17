
from flask import Flask, request, jsonify
from menu_tool import search_menu, check_dietary

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
