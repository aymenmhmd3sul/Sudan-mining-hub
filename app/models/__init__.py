# 1. الموديلات الأساسية (التي لا تعتمد على غيرها)
from app.models.user import User
from app.models.role import Role, Permission, user_roles, role_permissions
from app.models.identity import Organization, Membership
from app.models.marketplace import MiningAsset

# 2. الموديلات الوسيطة
from app.models.opportunities import Opportunity
from app.models.market_core import AssetItem, MarketListing, MarketOrder

# 3. الموديلات التي تمثل الأصول (Parents)
from app.models.negotiation import MarketDeal, DealMilestone

# 4. الموديلات التي تعتمد على ما سبق (Logs/Trades/Operations)
from app.models.communication import Notification, DealEventLog
from app.models.analytics import MarketPriceTicker, AIRecommendation
from app.models.trade_desk import GlobalTradeDeskRequest, GlobalTradeBid
from app.models.operations import SubscriptionPlan, FinancialTransaction, SystemSetting
from app.models.investor_core import InvestorProfile, LetterOfIntent, LOIAuditTrail
