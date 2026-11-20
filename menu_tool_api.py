
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
import logging

from menu_tool import search_menu, check_dietary
from menu_search_tool import (
    search_menu_v2,
    get_reservation_rules,
    check_reservation
)

app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "service": "Spice Route Menu Tool API"
    })


@app.route("/menu/search", methods=["POST"])
def menu_search():
    try:
        data = request.get_json(silent=True) or {}
        item_name = data.get("item_name", "")

        if not isinstance(item_name, str) or not item_name.strip():
            logger.error("Invalid input: Item name is required")
            return jsonify({
                "success": False,
                "error": "Item name is required"
            }), 400

        result = search_menu(item_name.strip())
        status = 404 if "error" in result else 200

        return jsonify(result), status

    except Exception:
        logger.exception("Menu search API failure")
        return jsonify({
            "success": False,
            "error": "Menu search failed. Please try again."
        }), 500


@app.route("/menu/dietary-check", methods=["POST"])
def dietary_check():
    try:
        data = request.get_json(silent=True) or {}

        item_name = data.get("item_name", "")
        requirement = data.get("requirement", "")

        if (
            not isinstance(item_name, str)
            or not isinstance(requirement, str)
            or not item_name.strip()
            or not requirement.strip()
        ):
            logger.error(
                "Invalid input: Item name or dietary requirement missing"
            )
            return jsonify({
                "success": False,
                "error": "Item name and dietary requirement are required"
            }), 400

        result = check_dietary(
            item_name.strip(),
            requirement.strip()
        )

        status = 404 if "error" in result else 200
        return jsonify(result), status

    except Exception:
        logger.exception("Dietary check API failure")
        return jsonify({
            "success": False,
            "error": "Dietary check failed. Please try again."
        }), 500


@app.route("/restaurant/lookup", methods=["POST"])
def restaurant_lookup():
    try:
        data = request.get_json(silent=True) or {}

        action = data.get("action", "")

        if not isinstance(action, str) or not action.strip():
            logger.error("Invalid input: Action is missing")
            return jsonify({
                "success": False,
                "message": "Action is required."
            }), 400

        action = action.strip()

        if action == "search_menu":
            query = data.get("query", "")

            if not isinstance(query, str) or not query.strip():
                logger.error("Invalid input: Menu search query is missing")
                return jsonify({
                    "success": False,
                    "message": "Menu search query is required."
                }), 400

            return jsonify(search_menu_v2(query.strip()))

        elif action == "get_reservation_rules":
            return jsonify(get_reservation_rules())

        elif action == "check_reservation":
            party_size = data.get("party_size")
            day = data.get("day", "")
            requested_time = data.get("requested_time", "")

            if not isinstance(day, str) or not isinstance(requested_time, str):
                logger.error("Invalid reservation input: Day or time has invalid type")
                return jsonify({
                    "success": False,
                    "message": "Day and time must be text values."
                }), 400

            result = check_reservation(
                party_size,
                day,
                requested_time
            )

            if not result.get("success"):
                logger.error(
                    "Reservation validation failed: %s",
                    result
                )
                return jsonify(result), 400

            return jsonify(result), 200

        logger.error("Invalid action received: %s", action)

        return jsonify({
            "success": False,
            "message": "Unknown action."
        }), 400

    except Exception:
        logger.exception("Restaurant lookup API failure")
        return jsonify({
            "success": False,
            "message": "Request could not be completed. Please try again."
        }), 500


# Global error handler
@app.errorhandler(Exception)
def handle_unexpected_error(error):

    if isinstance(error, HTTPException):
        return jsonify({
            "success": False,
            "error": error.description
        }), error.code

    logger.exception("Unexpected application error")

    return jsonify({
        "success": False,
        "error": "An unexpected error occurred. Please try again."
    }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
