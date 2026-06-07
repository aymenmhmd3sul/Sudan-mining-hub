import streamlit as st
import requests

# 1. إعداد الصفحة بالتنسيق الافتراضي المستقر تماماً ودعم الشاشات العريضة
st.set_page_config(
    page_title="منصة تعدين السودان الرقمية", 
    page_icon="⛏️", 
    layout="wide"
)

# رابط السيرفر الخلفي على ريندر
API_URL = "https://sudan-mining-platform.onrender.com"

# =========================================================================
# طبقة جلب البيانات والمؤشرات الذكية
# =========================================================================
@st.cache_data(ttl=20)
def fetch_platform_metrics():
    metrics = {
        "merchants_count": 7,
        "light_equipment": 27,
        "heavy_equipment": 14,
        "generators": 9,
        "logistics": 22,
        "gold_price": "في انتظار التحديث"
    }
    try:
        r_price = requests.get(f"{API_URL}/api/v1/prices", timeout=5)
        if r_price.status_code == 200:
            prices = r_price.json()
            if prices:
                metrics["gold_price"] = f"{prices[-1].get('price_sdg', 'في انتظار التحديث')} ج.س"
    except:
        pass
    return metrics

platform_stats = fetch_platform_metrics()

# عنوان المنصة الرئيسي
st.title("⛏️ منصة تعدين السودان الرقمية - منظومة الإمداد اللوجستي")
st.markdown("---")

# القائمة الجانبية للتنقل (بالتنسيق والاتجاه الافتراضي المستقر)
menu = st.sidebar.radio(
    "📁 تصفح أقسام المنصة",
    [
        "📊 إحصائيات السوق الحية",
        "👤 اطلب معدة أو خدمة (للمشترين)",
        "🏪 مخزن طلبات الشراء (للتجار المعتمدين)",
        "🗺️ مواقع التعدين وبورصة الذهب"
    ]
)

# =========================================================================
# 1. واجهة إحصائيات السوق الحية
# =========================================================================
if menu == "📊 إحصائيات السوق الحية":
    st.header("📈 حجم النشاط والقدرة الاستيعابية للسوق")
    st.write("شبكة ربط لوجستية مغلقة تجمع كبار مستثمري التعدين بأكبر مزودي الخدمات وموردي المعدات في السودان.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏪 شبكة كبار التجار المعتمدين", f"{platform_stats['merchants_count']} تجار رئيسيين")
    with col2:
        st.metric("⚙️ إجمالي المواد والخدمات الجاهزة", "جاهزة للتلبية")
    with col3:
        st.metric("💰 سعر جرام الذهب العالمي الحالي", platform_stats['gold_price'])
        
    st.markdown("---")
    st.subheader("🚜 المنظومة اللوجستية المتوفرة حالياً في المخازن:")
    
    st.info(f"⚙️ معدات خفيفة المتوفر: {platform_stats['light_equipment']} وحدة")
    st.info(f"🚜 آليات ثقيلة المتوفر: {platform_stats['heavy_equipment']} وحدة")
    st.info(f"⚡ طاقة ومولدات المتوفر: {platform_stats['generators']} وحدة")
    st.info(f"💧 خدمات وتموين المتوفر: {platform_stats['logistics']} آلية/خدمة")
    
    st.markdown("---")
    st.caption("💡 ملحوظة: حظر طلبات ومواصفات العرض والأسعار مباشرة برابط خاص ومشفر يحفظ سرية التعاملات التجارية لشركاء المنصة.")

# =========================================================================
# 2. بوابة المشتري (طلب معدة أو خدمة)
# =========================================================================
elif menu == "👤 اطلب معدة أو خدمة (للمشترين)":
    st.header("📥 تقديم طلب إمداد جديد")
    st.write("أرسل احتياجاتك مباشرة إلى شبكة الموردين المعتمدين لتلقي عروض الأسعار.")
    
    with st.form("order_form"):
        o_type = st.selectbox("📦 تصنيف الطلب", ["معدات خفيفة", "آليات ثقيلة", "طاقة ومولدات", "خدمات وتموين"])
        o_details = st.text_area("📝 تفاصيل ومواصفات الخدمة أو المعدة المطلوبة بدقة")
        o_loc = st.text_input("📍 موقع التعدين المستهدف (الولاية / المنطقة)")
        
        submit_order = st.form_submit_button("🚀 إرسال الطلب إلى شبكة التجار")
        if submit_order:
            if o_details and o_loc:
                order_payload = {
                    "category": o_type,
                    "details": o_details,
                    "location": o_loc,
                    "status": "active"
                }
                try:
                    res = requests.post(f"{API_URL}/api/v1/orders", json=order_payload, timeout=5)
                    if res.status_code == 201:
                        st.success("✅ تم تعميم طلبك على شبكة التجار بنجاح! انتظر العروض قريباً.")
                    else:
                        st.error("⚠️ فشل في إرسال الطلب، يرجى المحاولة مرة أخرى.")
                except:
                    st.error("❌ خطأ في الاتصال بالسيرفر الخلفي.")
            else:
                st.warning("⚠️ يرجى ملء حقول تفاصيل الطلب والموقع لتتمكن من الإرسال.")

# =========================================================================
# 3. بوابة التجار (مخزن طلبات الشراء)
# =========================================================================
elif menu == "🏪 مخزن طلبات الشراء (للتجار المعتمدين)":
    st.header("🏪 لوحة تحكم التجار المعتمدين")
    st.write("استعرض طلبات الشراء الحالية واعرض معداتك وموقعها بناءً على طلب المشتري لضمان عدم حرق الأسعار.")
    
    try:
        res_orders = requests.get(f"{API_URL}/api/v1/orders", timeout=5)
        if res_orders.status_code == 200:
            orders = [o for o in res_orders.json() if o.get('status') == 'active']
            if not orders:
                st.info("📦 لا توجد طلبات شراء نشطة من الزبائن حالياً.")
            else:
                for idx, order in enumerate(orders):
                    with st.expander(f"📋 طلب توريد متاح - معرف الطلب #{order.get('id', idx+1)}"):
                        st.markdown(f"**📑 تفاصيل الاحتياج وموقع الطلب:** {order.get('details')}")
                        st.write(f"📅 **تاريخ الطلب:** {order.get('created_at', 'غير محدد')}")
                        st.markdown("---")
                        
                        with st.form(f"bid_form_{order.get('id', idx)}"):
                            m_name = st.selectbox("👤 اسم التاجر/المؤسسة", ["مجموعة خدمات التعدين والتموين", "الشركة العربية للمعدات"])
                            m_phone = st.text_input("📞 هاتف التواصل (يظهر للزبون عند الاعتماد)")
                            price = st.number_input("💰 السعر المعروض لتلبية الطلب", min_value=0)
                            currency = st.selectbox("💵 العملة", ["ج.س (جنيه سوداني)", "دولار أمريكي"])
                            loc = st.text_input("📍 الموقع الحالي للمعدة/الخدمة")
                            img = st.text_input("🔗 رابط صورة المعدة (اختياري)")
                            
                            st.caption("🔒 يتم حماية السعر والبيانات وإرسالها بشكل سري ومباشر لصاحب الطلب فقط.")
                            submit_bid = st.form_submit_button("🤝 تقديم العرض المالي واللوجستي")
                            
                            if submit_bid:
                                if m_phone and price > 0:
                                    bid_payload = {
                                        "order_id": order.get('id'),
                                        "merchant_name": m_name,
                                        "merchant_phone": m_phone,
                                        "price": price,
                                        "currency": currency,
                                        "location": loc,
                                        "image_url": img
                                    }
                                    res_bid = requests.post(f"{API_URL}/api/v1/bids", json=bid_payload, timeout=5)
                                    if res_bid.status_code == 201:
                                        st.success("🎯 تم إرسال عرضك بنجاح وبشكل سري 🔒")
                                    else:
                                        st.warning("⚠️ عذراً، هناك بيانات مطلوبة لإتمام المزايدة.")
                                else:
                                    st.error("⚠️ يرجى تعبئة رقم الهاتف والسعر لتقديم العرض.")
    except:
        st.error("❌ خطأ في الاتصال بالمنصة الخلفية لجلب الطلبات.")

# =========================================================================
# 4. إدارة المواقع والأسعار
# =========================================================================
elif menu == "🗺️ مواقع التعدين وبورصة الذهب":
    st.header("🗺️ إدارة المواقع وتحديث أسعار السوق")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("➕ إضافة موقع تعدين أو إنتاج")
        s_name = st.text_input("📌 اسم موقع التعدين الجديد")
        s_state = st.text_input("📍 الولاية/المنطقة التابعة لها")
        
        if st.button("💾 حفظ الموقع الميداني"):
            if s_name and s_state:
                site_payload = {"name": s_name, "state": s_state}
                try:
                    res_site = requests.post(f"{API_URL}/api/v1/sites", json=site_payload, timeout=5)
                    if res_site.status_code == 201:
                        st.success("✔️ تمت إضافة الموقع إلى قاعدة البيانات")
                    else:
                        st.error("❌ فشل حفظ الموقع.")
                except:
                    st.error("❌ السيرفر الخلفي لا يستجيب.")
            else:
                st.warning("⚠️ يرجى ملء كافة الحقول.")
                
    with col_b:
        st.subheader("💰 تحديث أسعار الذهب اللحظية والمحلية")
        gold_region = st.text_input("📍 البورصة المحلية (مثال: الخرطوم، نهر النيل)")
        g_price = st.number_input("💵 سعر جرام الذهب عيار 21 (ج.س)", min_value=0)
        
        if st.button("🔄 تحديث السعر والبورصة الآن"):
            if gold_region and g_price > 0:
                price_payload = {"region": gold_region, "price_sdg": g_price}
                try:
                    res_p = requests.post(f"{API_URL}/api/v1/prices", json=price_payload, timeout=5)
                    if res_p.status_code == 201:
                        st.success("✅ تم تحديث بورصة أسعار الذهب بنجاح وبثها على المنصة")
                        st.rerun()
                    else:
                        st.error("❌ فشل التحديث.")
                except:
                    st.error("❌ خطأ في الوصول للسيرفر.")
            else:
                st.warning("⚠️ يرجى تحديد المنطقة والسعر الصحيح.")
