def calculate_commission(amount, founder=False):
if amount < 5000000:
commission = 25000
elif amount < 20000000:
commission = 50000
elif amount < 100000000:
commission = 100000
else:
commission = amount * 0.005

if founder:
    commission *= 0.90

return round(commission)

FOUNDER_LIMIT = 50

def founder_benefits():
return {
"discount": "10%",
"badge": "تاجر مؤسس",
"priority": True
}
