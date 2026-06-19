from pathlib import Path

file = Path("main.py")
code = file.read_text()

old = """def build_room_id(opportunity_id: str, buyer_id: str, seller_id: str):
    users = sorted([str(buyer_id), str(seller_id)])
    return f\"{opportunity_id}:{users[0]}:{users[1]}\""""

new = """def build_room_id(opportunity_id: str, buyer_id: str, seller_id: str):
    return f\"{opportunity_id}:{min(str(buyer_id), str(seller_id))}:{max(str(buyer_id), str(seller_id))}\""""

if old in code:
    code = code.replace(old, new)
    file.write_text(code)
    print("ROOM FIXED (STRICT STABLE ID)")
else:
    print("ROOM FUNCTION NOT FOUND EXACT MATCH")
