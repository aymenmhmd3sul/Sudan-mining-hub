from typing import List, Dict, Optional

TRADERS_DB: List[Dict] = []
REQUESTS_DB: List[Dict] = []

def add_trader(trader: Dict):
    TRADERS_DB.append(trader)
    return trader

def add_request(request: Dict):
    REQUESTS_DB.append(request)
    return request

def match_request(category: str):
    category = category.lower()
    matches = []

    for trader in TRADERS_DB:
        if category in trader.get("specialty", "").lower():
            matches.append(trader)

    return matches

def attach_images(item: Dict, images: Optional[List[str]] = None):
    item["images"] = images or []
    return item

def get_items():
    return REQUESTS_DB

def add_item(item: Dict):
    return add_request(item)
