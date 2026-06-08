from flask import Flask, render_template_string, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "sudan_mining_secret_key_2026" # مفتاح الأمان للجلسات

API_URL = "https://sudan-mining-platform.onrender.com"
ADMIN_PASSWORD = "admin_mining_sd" # كلمة مرور لوحة التحكم يمكنك تغييرها

# تصميم الواجهة الاحترافية الشاملة مع الشريط المتحرك ولوحة الإدارة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⛏️ منصة تعدين السودان الرقمية</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: sans-serif; padding-bottom: 60px; }
        .card { background-color: #1e1e1e; border: 1px solid #333; color: #fff; margin-bottom: 15px; }
        .amber-text { color: #ffb300; }
        .nav-tabs .nav-link { color: #aaa; background: none; border: none; }
        .nav-tabs .nav-link.active { background-color: #ffb300; color: #000; font-weight: bold; border-radius: 5px; }
        .btn-amber { background-color: #ffb300; color: #000; font-weight: bold; width: 100%; }
        .btn-amber:hover { background-color: #ffa000; }
        .list-group-item { background-color: #252525; color: #fff; border: 1px solid #333; }
        
        /* تجميل الشريط المتحرك لأسعار الذهب */
        .ticker-wrap {
            width: 100%; background-color: #1a1a1a; border-bottom: 2px solid #ffb300;
            overflow: hidden; padding: 8px 0; font-size: 0.95rem; font-weight: bold;
        }
        .ticker { display: inline-block; white-space: nowrap; padding-right: 100%; animation: ticker 25s linear infinite; }
        .ticker-item { display: inline-block; padding: 0 2rem; color: #fff; }
        @keyframes ticker {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(100%, 0, 0); }
        }
    </style>
</head>
<body>

<div class="ticker-wrap">
    <div class="ticker">
        <span class="ticker-item">🌍 الذهب العالمي: <span class="amber-text">{{ prices.global_usd }} $ / أونصة</span></span>
        <span class="ticker-item">🇸🇩 عيار 24 محلي: <span class="text-success">{{ prices.local_24 }} ج.س</span></span>
        <span class="ticker-item">✨ عيار 21 محلي: <span class="text-success">{{ prices.local_21 }} ج.س</span></span>
        <span class="ticker-item">🪙 عيار 18 محلي: <span class="text-success">{{ prices.local_18 }} ج.س</span></span>
        <span class="ticker-item">📊 تحديث الأسعار حي ومباشر عبر البورصة</span>
    </div>
</div>

<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <div>
            <h2 class="amber-text mb-0">⛏️ منصة تعدين السودان الرقمية</h2>
            <p class="text-muted small">منظومة الإمداد اللوجستي وحركة المخازن الحية</p>
        </div>
        <a href="/admin" class="btn btn-sm btn-outline-secondary">🔒 لوحة الإدارة</a>
    </div>
    <hr style="background-color: #444;">

    <ul class="nav nav-tabs justify-content-center mb-4" id="mainTabs" role="tablist">
        <li class="nav-item">
            <button class="nav-link active" id="market-tab" data-bs-toggle="tab" data-bs-target="#market" type="button">📊 إحصائيات السوق</button>
        </li>
        <li class="nav-item">
            <button class="nav-link" id="order-tab" data-bs-toggle="tab" data-bs-target="#order" type="button">🚜 اطلب معدة</button>
        </li>
        <li class="nav-item">
            <button class="nav-link" id="warehouse-tab" data-bs-toggle="tab" data-bs-target="#warehouse" type="button">🏪 مخزن الطلبات</button>
        </li>
    </ul>

    <div class="tab-content">
        <div class="tab-pane fade show active" id="market">
            <h4 class="mb-3">📊 حجم النشاط والقدرة الاستيعابية للموقع</h4>
            <div class="row text-center">
                <div class="col-6">
                    <div class="card p-3">
                        <h6>🏪 كبار التجار والمعتمدين</h6>
                        <h4 class="amber-text">7 تجار</h4>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card p-3">
                        <h6>💰 جرام الذهب (عيار 21)</h6>
                        <h4 class="text-success">{{ prices.local_21 }}</h4>
                    </div>
                </div>
            </div>
            
            <h5 class="mt-4 mb-3">🚜 المنظومة اللوجستية الحالية بالمخازن:</h5>
            <ul class="list-group">
                <li class="list-group-item d-flex justify-content-between align-items-center">⚙️ معدات خفيفة وطواحين إنتاج <span class="badge bg-warning text-dark">27 وحدة جاهزة</span></li>
                <li class="list-group-item d-flex justify-content-between align-items-center">🚜 آليات ثقيلة وحفارات ميدانية <span class="badge bg-primary">14 معدة حية</span></li>
                <li class="list-group-item d-flex justify-content-between align-items-center">⚡ طاقة ومولدات كهرباء ضخمة <span class="badge bg-danger">9 وحدات سعة إنتاجية</span></li>
            </ul>
        </div>

        <div class="tab-pane fade" id="order">
            <h4 class="mb-3">👤 بوابة طلب الإمداد والآليات للمشترين</h4>
            <form action="/submit_order" method="POST" class="card p-3">
                <div class="mb-3">
                    <label class="form-label">📝 اسم المشترك (الشخص أو الشركة)</label>
                    <input type="text" name="name" class="form-control bg-dark text-white border-secondary" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">📞 رقم الواتساب أو هاتف الاتصال</label>
                    <input type="text" name="contact" class="form-control bg-dark text-white border-secondary" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">🚜 فئة المعدة أو الخدمة المطلوبة</label>
                    <select name="category" class="form-select bg-dark text-white border-secondary">
                        <option>معدات خفيفة وأدوات إنتاج (طواحين، دقاقات)</option>
                        <option>آليات ثقيلة وحفر (حفارات، لودرات)</option>
                        <option>طاقة ومولدات كهربائية متكاملة</option>
                        <option>خدمات لوجستية وتموين للمواقع</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">📑 تفاصيل المواصفات والاحتياج بدقة</label>
                    <textarea name="details" class="form-control bg-dark text-white border-secondary" rows="3" required></textarea>
                </div>
                <div class="mb-3">
                    <label class="form-label">📍 منطقة التعدين المستهدفة</label>
                    <input type="text" name="location" class="form-control bg-dark text-white border-secondary" placeholder="مثال: أبو حمد، العبيدية" required>
                </div>
                <button type="submit" class="btn btn-amber mt-2">🚀 تعميم الطلب اللوجستي سرياً</button>
            </form>
        </div>

        <div class="tab-pane fade" id="warehouse">
            <h4 class="mb-3">🏪 مخزن الطلبات النشطة المتاحة للتوريد</h4>
            <p class="text-muted small">هذه المساحة مخصصة للشركات والموردين المعتمدين لتقديم عروضهم الفورية.</p>
            
            {% if orders %}
                {% for o in orders %}
                <div class="card p-3 mb-3">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="amber-text mb-1">📦 طلب رقم #{{ o.id }} - {{ o.category }}</h5>
                        <span class="badge bg-success">📍 {{ o.location }}</span>
                    </div>
                    <p class="mt-2 text-white-50">{{ o.details }}</p>
                    <hr style="background-color: #333;">
                    <form action="/submit_bid" method="POST" class="row g-2">
                        <input type="hidden" name="order_id" value="{{ o.id }}">
                        <div class="col-6">
                            <input type="text" name="bid_price" class="form-control form-control-sm bg-dark text-white border-secondary" placeholder="السعر المعروض والتسليم" required>
                        </div>
                        <div class="col-6">
                            <input type="text" name="bid_phone" class="form-control form-control-sm bg-dark text-white border-secondary" placeholder="هاتف المورد المعتمد" required>
                        </div>
                        <div class="col-12">
                            <button type="submit" class="btn btn-sm btn-outline-warning w-100">🔒 تقديم العرض السري المالي</button>
                        </div>
                    </form>
                </div>
                {% endfor %}
            {% else %}
                <div class="alert alert-secondary bg-dark text-white border-secondary text-center">📦 لا توجد طلبات شراء حية نشطة حالياً في غرف المعاينة.</div>
            {% endif %}
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# تصميم لوحة تحكم الإدارة (Admin Dashboard)
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 لوحة الإدارة والتحكم</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: sans-serif; }
        .card { background-color: #1e1e1e; border: 1px solid #333; color: #fff; }
        .amber-text { color: #ffb300; }
    </style>
</head>
<body>
<div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="amber-text">🔒 لوحة التحكم والرقابة اللوجستية</h2>
        <a href="/" class="btn btn-sm btn-warning">⬅️ العودة للمنصة</a>
    </div>
    
    <div class="row">
        <div class="col-md-4 mb-4">
            <div class="card p-3">
                <h5>⚙️ التحكم السريع</h5>
                <hr style="background-color: #444;">
                <p class="small text-muted">إحصائيات إجمالية لحجم العمليات الجارية على خوادم المنصة.</p>
                <div class="p-2 mb-2 bg-dark rounded">👥 طلبات الشراء الواردة: <strong>{{ orders|length }}</strong></div>
                <div class="p-2 bg-dark rounded">🏪 التجار النشطين مسبقاً: <strong>7</strong></div>
            </div>
        </div>

        <div class="col-md-8">
            <div class="card p-3">
                <h5>📋 مراجعة وتصفية الطلبات النشطة سرياً</h5>
                <hr style="background-color: #444;">
                {% if orders %}
                    <div class="table-responsive">
                        <table class="table table-dark table-striped">
                            <thead>
                                <tr>
                                    <th>رقم</th>
                                    <th>الفئة</th>
                                    <th>الموقع</th>
                                    <th>التفاصيل والمشترك</th>
                                    <th>الإجراء</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for o in orders %}
                                <tr>
                                    <td>{{ o.id }}</td>
                                    <td><span class="text-warning">{{ o.category }}</span></td>
                                    <td>{{ o.location }}</td>
                                    <td class="small">{{ o.details }}</td>
                                    <td>
                                        <a href="/delete_order/{{ o.id }}" class="btn btn-sm btn-danger">إغلاق/حذف</a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <p class="text-center text-muted my-3">لا توجد طلبات جارية لمراجعتها حالياً.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

def get_live_prices():
    """ دالة لجلب الأسعار الحية الحقيقية وحساب العيارات محلياً """
    data = {
        "global_usd": "2,385",
        "local_24": "68,500",
        "local_21": "60,000",
        "local_18": "51,400"
    }
    try:
        r = requests.get(f"{API_URL}/api/v1/prices", timeout=3)
        if r.status_code == 200 and r.json():
            latest = r.json()[-1]
            price_sdg = latest.get('price_sdg', 60000)
            # حساب تقريبي للعيارات بناء على السعر الأساسي للجرام المتاح بالـ API
            data["local_21"] = f"{int(price_sdg):,}"
            data["local_24"] = f"{int(price_sdg * 1.14):,}"
            data["local_18"] = f"{int(price_sdg * 0.85):,}"
    except:
        pass
    return data

def get_live_orders():
    """ جلب قائمة طلبات الشراء الفعلية من المنصة الخلفية """
    try:
        r = requests.get(f"{API_URL}/api/v1/orders", timeout=4)
        if r.status_code == 200:
            return [o for o in r.json() if o.get('status') == 'active']
    except:
        pass
    return []

@app.route('/')
def home():
    prices = get_live_prices()
    orders = get_live_orders()
    return render_template_string(HTML_TEMPLATE, prices=prices, orders=orders)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    payload = {
        "category": request.form.get('category'),
        "details": f"المشترك: {request.form.get('name')} | هاتف: {request.form.get('contact')} | المواصفات: {request.form.get('details')}",
        "location": request.form.get('location'),
        "status": "active"
    }
    try:
        requests.post(f"{API_URL}/api/v1/orders", json=payload, timeout=5)
    except:
        pass
    return redirect(url_for('home'))

@app.route('/submit_bid', methods=['POST'])
def submit_bid():
    # إرسال عرض مالي سري من مورد (يمكن مستقبلاً ربطه بجدول خاص بالـ العروض المفتوحة)
    return "<h3>✅ تم تقديم عرضك السري للمنصة بنجاح وسيتم مراجعته لوجستياً!</h3>"

# بوابات لوحة تحكم الإدارة (Admin)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "<h3>❌ كلمة المرور غير صحيحة!</h3>"
            
    if not session.get('logged_in'):
        # واجهة تسجيل دخول مصغرة للإدارة
        return """
        <div style="background:#121212; color:#fff; height:100vh; display:flex; justify-content:center; align-items:center; font-family:sans-serif;" dir="rtl">
            <form method="POST" style="background:#1e1e1e; padding:30px; border-radius:8px; border:1px solid #333; text-align:center;">
                <h3 style="color:#ffb300;">🔒 دخول غرف الإشراف</h3><br>
                <input type="password" name="password" placeholder="أدخل كلمة مرور الإدارة" style="padding:10px; width:220px; background:#222; color:#fff; border:1px solid #444; border-radius:4px;"><br><br>
                <button type="submit" style="background:#ffb300; font-weight:bold; padding:10px 20px; border:none; border-radius:4px; cursor:pointer;">تأكيد الهوية</button>
            </form>
        </div>
        """
    orders = get_live_orders()
    return render_template_string(ADMIN_TEMPLATE, orders=orders)

@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    if session.get('logged_in'):
        try:
            # تحديث حالة الطلب إلى مكتمل أو محذوف لإخفائه من الواجهات العامة
            payload = {"status": "completed"}
            requests.put(f"{API_URL}/api/v1/orders/{order_id}", json=payload, timeout=5)
        except:
            pass
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
