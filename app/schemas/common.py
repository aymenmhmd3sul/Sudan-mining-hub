from enum import Enum

class Currency(str, Enum):
    USD = "USD"
    SDG = "SDG"

class PaymentProvider(str, Enum):
    BANK_TRANSFER = "bank_transfer"
    STRIPE = "stripe"
    LOCAL_WALLET = "local_wallet"
    OTHER = "other"

class PaymentMethod(str, Enum):
    WIRE = "wire"
    CARD = "card"
    CASH = "cash"
