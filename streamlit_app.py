import streamlit as st
import requests

# إعداد الصفحة
st.set_page_config(page_title="منصة تعدين السودان الرقمية", page_icon="⛏️", layout="wide")

# Render رابط السيرفر الفعلي المرفوع على
API_URL = "https://sudan-mining-platform.onrender.com"

# =======================================================
# طبقة جلب البيانات (Data Layer & Caching)
# =======================================================

@st.cache_data(ttl=30)  # كاش لمدة 30 ثانية لتحديث البيانات بسلاسة
def fetch_dashboard_metrics():
    """جلب ومعالجة الجداول الفارغة من الـ API بشكل حي"""
    metrics = {
        "sites_count": 0,
        "equipment_count": 0,
        "reports_count": 0,
        "total_production": 0.0,
        "gold_price": "في انتظار التحديث"
    }
    
    try:
        # 1. جلب المواقع
        r_sites = requests.get(f"{API_URL}/api/v1/sites", timeout=5)
        if r_sites.status_code == 200:
            metrics["sites_count"] = len(r_sites.json())
            
        # 2. جلب المعدات
        r_eq = requests.get(f"{API_URL}/api/v1/equipment", timeout=5)
        if r_eq.status_code == 200:
            metrics["equipment_count"] = len(r_eq.json())
            
        # 3. جلب البلاغات
        r_rep = requests.get(f"{API_URL}/api/v1/reports", timeout=5)
        if r_rep.status_code == 200:
            metrics["reports_count"] = len(r_rep.json())
            
        # 4. جلب وحساب إجمالي الإنتاج
        r_prod = requests.get(f"{API_URL}/api/v1/production", timeout=5)
        if r_prod.status_code == 200:
            productions = r_prod.json()
            if productions:
                metrics["total_production"] = sum(item.get("gold_weight", 0.0) for item in productions)
                
        # 5. جلب آخر سعر للذهب
        r_price = requests.get(f"{API_URL}/api/v1/prices", timeout=5)
        if r_price.status_code == 200:
            prices = r_price.json()
            if prices and len(prices) > 0:
                metrics["gold_price"] = f"{prices[-1].get('local_price', 0.0):,}"
                
    except Exception as e:
        pass  # الاحتفاظ بالقيم الافتراضية بدلاً من انهيار الواجهة
        
    return metrics

# جلب البيانات الحية لبدء تشغيل اللوحة
live_data = fetch_dashboard_metrics()

# عنوان المنصة الرئيسي
st.title("⛏️ منصة تعدين السودان الرقمية - Sudan Mining Hub")
st.markdown("---")

# القائمة الجانبية المحدثة لإدارة صفقات المعدات والمخزن الافتراضي
menu = st.sidebar.radio(
    "📂 تصفح أقسام المنصة",
    [
        "📊 لوحة المؤشرات (المستثمرين)",
        "👤 طلب معدة جديدة (للمشترين)",
        "🏪 مخزن عروض التجار (سري)",
        "💬 غرف التفاوض والاتفاق",
        "🗺️ مواقع التعدين",
        "💰 تحديث بورصة الأسعار",
        "📝 تسجيل حساب جديد"
    ]
)

# =======================================================
# 1. لوحة المؤشرات (القسم الرئيسي للمستثمرين)
# =======================================================
if menu == "📊 لوحة المؤشرات (المستثمرين)":
    st.header("📈 لوحة الأداء العام والمؤشرات الاستثمارية")
    st.write("نظام متكامل لتتبع وإدارة عمليات مواقع التعدين، الآليات، البلاغات، والإنتاج الحي في السودان.")
    
    st.markdown("### 🏷️ المؤشرات الحية (من واقع قاعدة البيانات)")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="🗺️ مواقع التعدين النشطة", value=f"{live_data['sites_count']}")
    col2.metric(label="🚜 المعدات المسجلة", value=f"{live_data['equipment_count']}")
    col3.metric(label="🚨 البلاغات المفتوحة", value=f"{live_data['reports_count']}")
    col4.metric(label="🏆 إجمالي إنتاج الذهب (جرام)", value=f"{live_data['total_production']:.2f}")
    col5.metric(label="💰 سعر الخام الحالي (SDG)", value=live_data['gold_price'])
    
    st.markdown("---")
    st.info("💡 لوحة المستثمرين هذه تحدث بياناتها تلقائياً من خادم PostgreSQL لضمان أعلى درجات الشفافية والموثوقية.")

# =======================================================
# 2. قسم طلب معدة جديدة (للمشترين)
# =======================================================
elif menu == "👤 طلب معدة جديدة (للمشترين)":
    st.header("👤 بوابة المشتري - اطلب معدتك مجاناً")
    st.write("أدخل مواصفات المعدة الثقيلة أو خط الإنتاج الذي تبحث عنه. طلبك سيظهر للتجار المعتمدين لتقديم عروضهم سرياً.")
    
    with st.form("buyer_order_form"):
        buyer_name = st.text_input("اسم المشتري أو اسم الشركة طالبة المعدة")
        buyer_phone = st.text_input("رقم هاتف المشتري (سيكون مخفياً تماماً عن التجار ولن يعرض إلا بعد قبولك لعرضهم)")
        eq_type = st.selectbox("نوع المعدة المطلوبة", ["بوكلين / حافرة", "لودر / شاحنة", "بلدوزر", "طاحونة رطبة / جافة", "خط إنتاج سيانيد كامل", "مولد كهربائي ضخم"])
        specs = st.text_area("المواصفات الفنية والشروط المطلوبة (مثلاً: الموديل، سنة الصنع، الحالة التشغيلية)")
        
        submit_order = st.form_submit_button("🚀 إرسال الطلب إلى سوق المناقصات")
        
        if submit_order:
            if buyer_name and buyer_phone and specs:
                payload = {
                    "buyer_name": buyer_name,
                    "buyer_phone": buyer_phone,
                    "equipment_type": eq_type,
                    "specifications": specs,
                    "status": "نشط"
                }
                try:
                    res = requests.post(f"{API_URL}/api/v1/orders", json=payload)
                    if res.status_code in [200, 201]:
                        st.success("✅ تم نشر طلبك بنجاح في سوق المناقصات! انتظر عروض التجار في غرفة التفاوض.")
                    else:
                        st.error(f"❌ خطأ من السيرفر: {res.status_code}")
                except Exception as e:
                    st.error("❌ فشل الاتصال بالسيرفر لإرسال الطلب.")
            else:
                st.warning("⚠️ الرجاء ملء جميع الحقول الأساسية لإتمام الطلب.")

# =======================================================
# 3. قسم مخزن عروض التجار (سري)
# =======================================================
elif menu == "🏪 مخزن عروض التجار (سري)":
    st.header("🏪 بوابة التجار الـ 7 المعتمدين (المخزن الافتراضي)")
    st.write("هنا يمكنك مراجعة طلبات المشترين الحالية وتقديم عروض أسعار سرية ومباشرة من مخزنك الافتراضي.")
    
    try:
        res_orders = requests.get(f"{API_URL}/api/v1/orders")
        if res_orders.status_code == 200:
            orders = [o for o in res_orders.json() if o.get("status") == "نشط"]
            
            if not orders:
                st.info("📦 لا توجد طلبات شراء نشطة حالياً من المشترين.")
            else:
                for order in orders:
                    with st.expander(f"📋 طلب رقم #{order['id']} - مطلوب: {order['equipment_type']}"):
                        st.write(f"**المواصفات المطلوبة:** {order['specifications']}")
                        st.write(f"**تاريخ الطلب:** {order['created_at']}")
                        st.markdown("---")
                        st.subheader("📝 تقديم عرض سعر سري لهذا الطلب")
                        
                        # نموذج تقديم العرض داخل الإكسباندر
                        with st.form(f"bid_form_{order['id']}"):
                            merchant_name = st.selectbox("اختر اسمك (التاجر المعتمد)", [f"التاجر المعتمد #{i}" for i in range(1, 8)])
                            merchant_phone = st.text_input("رقم هاتف التاجر الخاص بالصفقة")
                            price = st.number_input("السعر المعروض للبيع", min_value=1.0, step=1000.0)
                            currency = st.selectbox("العملة", ["جنيه سوداني (SDG)", "درهم إماراتي (AED)", "دولار أمريكي (USD)"])
                            location_sudan = st.text_input("موقع المعدة الحالي للمعاينة (مثال: أبو حمد، بربر، الخرطوم)")
                            image_url = st.text_input("رابط صورة المعدة للمعاينة البصرية (أو اتركه فارغاً)")
                            
                            st.caption("ℹ️ ملاحظة: بموجب شروط المنصة، يدفع التاجر عمولة مرنة تتراوح بين 0.5% إلى 2% بعد إتمام عملية البيع للمشتري.")
                            
                            submit_bid = st.form_submit_button("📥 إرسال العرض سرياً للمشتري")
                            
                            if submit_bid:
                                if merchant_phone and location_sudan:
                                    bid_payload = {
                                        "order_id": order['id'],
                                        "merchant_name": merchant_name,
                                        "merchant_phone": merchant_phone,
                                        "price": price,
                                        "currency": currency,
                                        "location_in_sudan": location_sudan,
                                        "image_url": image_url if image_url else None,
                                        "commission_rate": 1.0,
                                        "commission_status": "معلقة"
                                    }
                                    res_bid = requests.post(f"{API_URL}/api/v1/bids", json=bid_payload)
                                    if res_bid.status_code in [200, 201]:
                                        st.success("🎯 تم إرسال عرضك السري بنجاح للمشتري!")
                                    else:
                                        st.error("❌ فشل إرسال العرض، راجع السيرفر.")
                                else:
                                    st.warning("⚠️ يرجى إدخال رقم الهاتف وموقع المعاينة الجغرافي.")
    except Exception as e:
        st.error("❌ فشل الاتصال بقاعدة البيانات لجلب طلبات المشترين.")

# =======================================================
# 4. غرف التفاوض والاتفاق واستخراج الأدلة
# =======================================================
elif menu == "💬 غرف التفاوض والاتفاق":
    st.header("💬 غرف التفاوض الذكية والموافقة على الصفقات")
    st.write("أدخل اسمك كمشتري أو رقم طلبك لاستعراض العروض السرية المقدمة لك من التجار، والتفاوض ومعاينة الصور والمواقع الجغرافية.")
    
    order_id_input = st.number_input("أدخل رقم طلبك (Order ID) لعرض عروض الأسعار المقدمة لك:", min_value=1, step=1)
    
    if order_id_input:
        try:
            res_bids = requests.get(f"{API_URL}/api/v1/bids/order/{order_id_input}")
            if res_bids.status_code == 200:
                bids = res_bids.json()
                
                if not bids:
                    st.info("⏳ لم يقم أي تاجر بتقديم عرض على هذا الطلب حتى الآن. العروض تظهر هنا فور إرسالها.")
                else:
                    st.success(f"🎉 تم العثور على ({len(bids)}) عروض سرية مقدمة لطلبك!")
                    
                    for idx, bid in enumerate(bids):
                        st.markdown(f"### 📦 العرض المتاح رقم {idx+1}")
                        
                        col_left, col_right = st.columns([2, 1])
                        
                        with col_left:
                            st.write(f"**💰 السعر المعروض:** {bid['price']:,} {bid['currency']}")
                            st.write(f"**📍 موقع المعدة الجغرافي للمعاينة بالسودان:** {bid['location_in_sudan']}")
                            st.write(f"**🤝 التزام العمولة (يدفعها التاجر للمنصة):** {bid['commission_text']}")
                            st.warning("🔒 هوية التاجر ورقم هاتفه مخفيان لحماية حقوق المنصة وتجنب البيع الخارجي.")
                        
                        with col_right:
                            if bid.get('image_url'):
                                st.image(bid['image_url'], caption="صورة المعدة المرفوعة من مخزن التاجر الافتراضي", use_container_width=True)
                            else:
                                st.info("🖼️ لا توجد صورة مرفقة مع هذا العرض.")
                        
                        # زر القبول والاتفاق الرسمي لتوليد سجل المراسلات كدليل للعمولة
                        if st.button(f"🤝 قبول هذا العرض والاتفاق الرسمي (عرض رقم #{bid['id']})"):
                            # 1. تحديث حالة الطلب إلى تم الاتفاق
                            requests.put(f"{API_URL}/api/v1/orders/{order_id_input}/status?status=تم الاتفاق مع {bid['merchant_name']}")
                            
                            st.balloons()
                            st.success("🎉 مبروك! تم إتمام الاتفاق برغبتك الحرة بالكامل.")
                            
                            # كشف الهويات والأرقام بعد الضغط بشكل آمن
                            st.markdown("#### 📱 بيانات التواصل المباشر للمعاينة والتسليم:")
                            st.info(f"📞 **رقم هاتف التاجر (البائع الملتزم بالعمولة):** {bid['merchant_phone']}")
                            
                            # استخراج سجل المراسلات الموقّع كدليل قانوني وإداري للمنصة
                            st.markdown("#### 📝 سجل المراسلات المستخرج كدليل (رسمي للمنصة):")
                            evidence_text = f"""
                            ------------------------------------------
                            📄 دليل اتفاق منصة تعدين السودان الرقمية
                            ------------------------------------------
                            - رقم طلب الشراء: {order_id_input}
                            - رقم العرض المقبول: {bid['id']}
                            - السعر المتفق عليه برغبة الطرفين: {bid['price']:,} {bid['currency']}
                            - موقع المعدة للمعاينة والتسليم: {bid['location_in_sudan']}
                            - الطرف الملزم بدفع العمولة: التاجر ({bid['merchant_name']})
                            - نسبة العمولة المعتمدة: {bid['commission_rate']}%
                            - حالة العمولة الحالية: قيد الدفع بعد الفحص والاستلام الميداني
                            - تاريخ وتوقيت العملية الآلي: {bid['created_at']}
                            ------------------------------------------
                            تنبيه: هذا السجل مستخرج برمجياً ومحفوظ في السيرفر لضمان حق المنصة في العمولة التي يدفعها التاجر الملتزم.
                            """
                            st.code(evidence_text, language="text")
                            st.info("💡 تم حفظ هذا السجل تلقائياً، يرجى التواصل مع التاجر على الرقم أعلاه لترتيب المعاينة الميدانية بـأبو حمد أو موقعها الجغرافي.")
                        st.markdown("---")
        except Exception as e:
            st.error("❌ خطأ أثناء جلب العروض من السيرفر.")

# =======================================================
# 5. قسم مواقع التعدين (الأصلية)
# =======================================================
elif menu == "🗺️ مواقع التعدين":
    st.header("🗺️ تتبع مواقع التعدين والامتياز")
    st.subheader("➕ تسجيل موقع تعدين جديد")
    site_name = st.text_input("اسم موقع التعدين")
    site_state = st.text_input("الولاية / المنطقة")
    
    if st.button("💾 حفظ الموقع"):
        if site_name and site_state:
            payload = {"name": site_name, "state": site_state, "is_active": True}
            try:
                res = requests.post(f"{API_URL}/api/v1/sites", json=payload)
                if res.status_code in [200, 201]:
                    st.success(f"✔️ تم تسجيل موقع {site_name} بنجاح في قاعدة البيانات.")
                    st.cache_data.clear()  # تفريغ الكاش لتحديث الأرقام فوراً
                else:
                    st.error(f"❌ خطأ من السيرفر: {res.status_code}")
            except Exception as e:
                st.error("❌ فشل الاتصال بالخادم السحابي.")
        else:
            st.warning("⚠️ الرجاء إدخال اسم الموقع والولاية أولاً.")

# =======================================================
# 6. قسم تحديث بورصة الأسعار (الأصلية)
# =======================================================
elif menu == "💰 تحديث بورصة الأسعار":
    st.header("💰 الإدارة التشغيلية لبورصة أسعار الذهب")
    st.write("تحديث أسعار الذهب الخام المعتمدة في السوق المحلي لتنعكس حية في لوحة المستثمرين.")
    
    new_price = st.number_input("سعر جرام الذهب الحالي (بالجنيه السوداني)", min_value=0.0, step=100.0)
    
    if st.button("🔄 تحديث وضع السعر الآن"):
        payload = {"local_price": float(new_price), "global_ounce": 0.0, "usd_rate": 0.0}
        try:
            res = requests.post(f"{API_URL}/api/v1/prices", json=payload)
            if res.status_code in [200, 201]:
                st.success(f"🎉 تم تحديث قاعدة بيانات الأسعار بنجاح إلى: {new_price:,} ج.س")
                st.cache_data.clear()
            else:
                st.error(f"❌ فشل التحديث: {res.status_code}")
        except Exception as e:
            st.error("❌ خطأ في الاتصال بالـ API.")

# =======================================================
# 7. قسم تسجيل حساب جديد (الأصلية)
# =======================================================
elif menu == "📝 تسجيل حساب جديد":
    st.header("📝 إنشاء حساب جديد في المنصة")
    username = st.text_input("اسم المستخدم")
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    
    if st.button("🚀 تنفيذ التسجيل"):
        try:
            response = requests.post(f"{API_URL}/api/v1/users/register", json={"username": username, "email": email, "password": password})
            if response.status_code in [200, 201]:
                st.success("🎉 تم إنشاء الحساب بنجاح!")
            else:
                st.error(f"❌ خطأ: {response.json().get('detail', 'فشل التسجيل')}")
        except Exception as e:
            st.error("❌ خطأ في الاتصال بالخادم.")
