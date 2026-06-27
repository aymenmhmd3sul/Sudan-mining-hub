def calculate_commission(price: float, category: str = "heavy"):
    """
    Rules:
    - light equipment: fixed 100000
    - heavy / deals: 2%
    """

    if category == "light":
        return 100000

    return price * 0.02
