
import csv
from pathlib import Path
from datetime import datetime

# Database file paths
BASE_DIR = Path(__file__).parent
MENU_FILE = BASE_DIR / "database" / "menu.csv"
RULES_FILE = BASE_DIR / "database" / "reservation_rules.csv"
HOURS_FILE = BASE_DIR / "database" / "operating_hours.csv"


def search_menu(item_name):
    """Search for a menu item and return its details."""

    with open(MENU_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for item in reader:
            if item_name.lower() in item["item_name"].lower():
                return {
                    "name": item["item_name"],
                    "price": float(item["price"]),
                    "category": item["category"],
                    "dietary_tags": item["dietary_tags"]
                }

    return {"error": "Menu item not found"}


def check_dietary(item_name, dietary_requirement):
    """Check whether a menu item matches a dietary requirement."""

    item = search_menu(item_name)

    if "error" in item:
        return item

    tags = [
        tag.strip().lower()
        for tag in item["dietary_tags"].split(",")
    ]

    requirement = dietary_requirement.strip().lower()

    return {
        "item": item["name"],
        "requirement": dietary_requirement,
        "suitable": requirement in tags
    }


def get_reservation_rules():
    """Retrieve reservation rules from the database."""

    rules = {}

    with open(RULES_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rules[row["rule_name"]] = {
                "value": row["rule_value"],
                "description": row["description"]
            }

    return {
        "success": True,
        "reservation_rules": rules
    }


def check_reservation(party_size, day, requested_time):
    """Check party size, restaurant opening day, and operating hours."""

    rules_data = get_reservation_rules()["reservation_rules"]

    minimum = int(rules_data["minimum_party_size"]["value"])
    maximum = int(rules_data["maximum_party_size"]["value"])

    if not minimum <= party_size <= maximum:
        return {
            "success": False,
            "message": f"Party size must be between {minimum} and {maximum}."
        }

    with open(HOURS_FILE, "r", newline="", encoding="utf-8-sig") as file:
        hours = list(csv.DictReader(file))

    day_info = next(
        (row for row in hours if row["day"].lower() == day.lower()),
        None
    )

    if not day_info or day_info["is_open"].lower() != "true":
        return {
            "success": False,
            "message": "Restaurant is closed on this day."
        }

    requested = datetime.strptime(requested_time, "%H:%M").time()
    opening = datetime.strptime(day_info["opening_time"], "%H:%M").time()
    closing = datetime.strptime(day_info["closing_time"], "%H:%M").time()

    within_hours = opening <= requested < closing

    return {
        "success": True,
        "party_size": party_size,
        "day": day_info["day"],
        "requested_time": requested_time,
        "within_operating_hours": within_hours,
        "opening_time": day_info["opening_time"],
        "closing_time": day_info["closing_time"],
        "message": (
            "Request is within operating hours. Actual table availability is not confirmed."
            if within_hours
            else "Requested time is outside operating hours."
        )
    }


if __name__ == "__main__":
    print("Spice Route Menu Tool")

    print("\nMenu Search:")
    print(search_menu("Chicken Biryani"))

    print("\nDietary Check:")
    print(check_dietary("Fresh Juice", "Vegan"))

    print("\nReservation Rules:")
    print(get_reservation_rules())

    print("\nReservation Check:")
    print(check_reservation(4, "Monday", "20:00"))
