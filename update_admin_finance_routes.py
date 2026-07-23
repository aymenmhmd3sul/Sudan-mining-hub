import os

router_path = 'app/routers/admin_finance.py'
if os.path.exists(router_path):
    with open(router_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # التأكد من إضافة مسار الفواتير بشكل صريح
    if '@router.get(\"/finance/invoices\")' not in content and '@router.get(\"/invoices\")' not in content:
        new_route = """
@router.get("/finance/invoices")
async def admin_finance_invoices(request: Request):
    return templates.TemplateResponse("admin/finance/invoices.html", {"request": request})
"""
        content += new_route
        with open(router_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Added explicit /finance/invoices route to admin_finance.py")
else:
    print("admin_finance.py not found, checking other routers...")
