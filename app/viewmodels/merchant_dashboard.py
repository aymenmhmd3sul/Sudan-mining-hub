from dataclasses import dataclass

@dataclass
class MerchantDealCard:
    title: str
    buyer_name: str
    status: str
    amount: str
    invoice_number: str

def map_invoice(invoice):
    buyer_map = {
        1: "شركة نهر النيل للتعدين",
        2: "أعمال القضارف للتعدين",
        3: "شركة البحر الأحمر للتعدين"
    }

    status_map = {
        "PAID": "في مرحلة Escrow",
        "completed": "مكتملة وموقعة",
        "draft": "بانتظار التأكيد"
    }

    return MerchantDealCard(
        title="توريد 500 جرام ذهب خام",
        buyer_name=buyer_map.get(invoice.buyer_id, "عميل تجاري"),
        status=status_map.get(invoice.status, invoice.status),
        amount=f"{invoice.total_amount:,.0f} ج.س",
        invoice_number=invoice.invoice_number or f"INV-{invoice.id}"
    )
