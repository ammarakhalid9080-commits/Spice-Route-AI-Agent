
import csv
from pathlib import Path

from menu_tool import get_reservation_rules, check_reservation

BASE_DIR = Path(__file__).parent
MENU_FILE = BASE_DIR / "database" / "menu.csv"


def search_menu(query):
    """Search menu items by name, category, or dietary tags."""

    query = query.lower().strip()

    if not query:
        return {
            "success": False,
            "items": [],
            "message": "Empty query"
        }

    results = []

    with open(MENU_FILE, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for item in reader:
            tags = [
                tag.strip().lower()
                for tag in item["dietary_tags"].split(",")
            ]

            if (
                query in tags
                or query in item["item_name"].lower()
                or query in item["category"].lower()
            ):
                results.append(item)

    return {
        "success": True,
        "query": query,
        "items": results,
        "message": f"Found {len(results)} matching items."
    }
