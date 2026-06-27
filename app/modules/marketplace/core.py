COMMISSION_RULES = {
    "light_equipment_fixed": 100000,
    "heavy_or_deals_percent": 0.02
}


def calculate_commission(price: float, category: str = "heavy"):
    # light equipment rule
    if category == "light":
        return COMMISSION_RULES["light_equipment_fixed"]

    # heavy / deals rule
    return price * COMMISSION_RULES["heavy_or_deals_percent"]
