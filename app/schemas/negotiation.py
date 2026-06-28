from pydantic import BaseModel, Field

# ---------------- CREATE ROOM ----------------
class CreateRoom(BaseModel):
    offer_id: int = Field(..., gt=0)


# ---------------- MESSAGE ----------------
class MessageIn(BaseModel):
    room_id: int = Field(..., gt=0)
    message: str = Field(..., min_length=1, max_length=2000)
