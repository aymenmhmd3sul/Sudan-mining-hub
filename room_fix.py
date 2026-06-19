
def build_room_id(opportunity_id: str, buyer_id: str, seller_id: str):
    # تثبيت الترتيب لمنع اختلاف الغرفة بين الطرفين
    users = sorted([str(buyer_id), str(seller_id)])
    return f"{opportunity_id}:{users[0]}:{users[1]}"

