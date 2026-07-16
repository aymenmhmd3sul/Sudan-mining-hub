from sqlalchemy.orm import relationship
from app.models.user import User
from app.models.market_core import MarketListing, MarketOrder

def apply_patches():
    User.listings = relationship("MarketListing", foreign_keys=[MarketListing.publisher_id], backref="publisher")
    User.orders = relationship("MarketOrder", foreign_keys=[MarketOrder.buyer_id], backref="buyer")
    User.verified_listings = relationship("MarketListing", foreign_keys=[MarketListing.verified_agent_id], backref="verified_agent")
    print("✅ [PATCH_SUCCESS] تم حقن العلاقات.")

apply_patches()
