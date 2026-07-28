STAGES = [
    "request_created",
    "offer_received",
    "negotiation",
    "deal_closed"
]


def next_stage(current: str):
    if current not in STAGES:
        return None
    idx = STAGES.index(current)
    if idx + 1 >= len(STAGES):
        return None
    return STAGES[idx + 1]
