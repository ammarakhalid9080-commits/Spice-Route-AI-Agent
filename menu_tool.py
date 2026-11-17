
import csv
from pathlib import Path

MENU_FILE = Path(__file__).parent / "database" / "menu.csv"


def search_menu(item_name):
    """Search for a menu item and return its details."""

    with open(MENU_FILE, "r", newline="", encoding="utf-8") as file:
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


if __name__ == "__main__":
    print("Spice Route Menu Tool")
    print(search_menu("Chicken Biryani"))
    print(check_dietary("Fresh Juice", "Vegan"))
