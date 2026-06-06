import streamlit as st
import requests

# إعداد الصفحة
st.set_page_config(page_title="منصة تعدين السودان الرقمية", page_icon="⛏️", layout="wide")

# رابط السيرفر الفعلي المرفوع على Render
API_URL = "https://sudan-mining-platform.onrender.com"

# ==========================================
# طبقة جلب البيانات (Data Layer & Caching)
# ==========================================

@st.cache_data(ttl=60)  # تحديث البيانات كل دقيقة تلقائياً لتقليل الضغط على السيرفر
def fetch_dashboard_metrics():
    """جلب المؤشرات الخمسة الأساسية من الـ API بشكل حي"""
    metrics = {
        "sites_count": 0,
        "equipment_count": 0,
        "reports_count": 0,
        "total_production": 0.0,
        "gold_price": "لا يوجد اتصال"
    }
    
    try:
        # 1. عدد المواقع
        r_sites = requests.get(f"{API_URL}/api/v1/sites", timeout=5)
        if r_sites.status_code == 200:
            metrics["sites_count"] = len(r_sites.json())
            
        # 2. عدد المعدات
        r_eq = requests.get(f"{API_URL}/api/v1/equipment", timeout=5)
        if r_eq.status_code == 200:
            metrics["equipment_count"] = len(r_eq.json())
            
        # 3. عدد البلاغات النشطة
        r_rep = requests.get(f"{API_URL}/api/v1/reports", timeout=5)
        if r_rep.status_code == 200:
            metrics["reports_count"] = len(r_rep.json())
            
        # 4. إجمالي الإنتاج
        r_prod = requests.get(f"{API_URL}/api/v1/production", timeout=5)
        if r_prod.status_code == 200:
            # حساب مجموع حقول الإنتاج المسجلة
            productions = r_prod.json()
            metrics["total_production"] = sum(item.get("amount", 0) for item in productions)
            
        # 5. آخر سعر للذهب
        r_price = requests.get(f"{API_URL}/api/v1/prices", timeout=5)
        if r_price.status_code == 200:
            prices = r_price.json()
            if prices:
                # جلب آخر سعر مضاف في المصفوفة
                metrics["gold_price"] = f"{prices[-1].get('price', 0):,} ج.س"
    except Exception as e:
        st.warning("⚠️ تعذر الاتصال اللحظي ببعض مسارات السيرفر، يتم عرض البيانات المحلية.")
        
    return metrics

# جلب البيانات الحية لبدء تشغيل اللوحة
live_data = fetch_dashboard_metrics()

# عنوان المنصة الرئيسي
st.title("⛏️ منصة تعدين السودان الرقمية - Sudan Mining Hub")
st.markdown("---")

# القائمة الجانبية لكافة أقسام المنصة
menu = st.sidebar.radio(
    "📂 تصفح أقسام المنصة",
    [
        "📊 لوحة المؤشرات (المستثمرين)",
        "🚜 تتبع المعدات والآليات",
        "🗺️ مواقع التعدين",
        "💰 أسعار الذهب اليوم",
        "📝 تسجيل حساب جديد",
        "🔑 دخول"
    ]
)

# ==========================================
# 1. لوحة المؤشرات (القسم الرئيسي للمستثمرين)
# ==========================================
if menu == "📊 لوحة المؤشرات (المستثمرين)":
    st.header("📈 لوحة الأداء العام والمؤشرات الاستثمارية")
    st.write("سحابي متكامل لتتبع وإدارة عمليات ومواقع التعدين، الآليات، والإنتاج الحي في السودان.")
    
    st.markdown("### 🏷️ المؤشرات الحية للمنصة (من واقع قاعدة البيانات)")
    
    # توزيع المؤشرات الخمسة الاستثمارية في مربعات رقمية جذابة
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric(label="🗺️ مواقع التعدين النشطة", value=f"{live_data['sites_count']} موقع")
    col2.metric(label="🚜 المعدات المسجلة", value=f"{live_data['equipment_count']} آلية")
    col3.metric(label="🚨 البلاغات المفتوحة", value=f"{live_data['reports_count']} بلاغ")
    col4.metric(label="🏆 إجمالي إنتاج الذهب", value=f"{live_data['total_production']} جرام")
    col5.metric(label="💰 سعر الذهب الحالي", value=live_data['gold_price'])

    st.markdown("---")
    st.info("💡 هذه اللوحة تحدث بياناتها تلقائياً من خادم PostgreSQL السحابي لتقديم رؤية دقيقة للشركاء والمستثمرين.")

# ==========================================
# 2. قسم المعدات والآليات
# ==========================================
elif menu == "🚜 تتبع المعدات والآليات":
    st.header("🚜 إدارة وتتبع الآليات والمعدات")
    st.write("يمكنك مراقبة الوقود، ساعات العمل، ومواقع الجرافات والمولدات في البيئة الحية.")
    
    st.subheader("➕ إضافة معدة جديدة للموقع")
    eq_name = st.text_input("اسم المعدة / الآلية")
    eq_type = st.selectbox("نوع المعدة", ["مولد كهربائي", "جرافة (Digger)", "مضخة مياه"])
    
    if st.button("حفظ المعدة"):
        if eq_name:
            # تجهيز البيانات للإرسال إلى السيرفر
            payload = {"name": eq_name, "type": eq_type, "status": "active"}
            try:
                res = requests.post(f"{API_URL}/api/v1/equipment", json=payload, timeout=5)
                if res.status_code in [200, 201]:
                    st.success(f"✔️ تم تسجيل {eq_name} بنجاح وجاري ربطها بنظام التتبع!")
                    st.cache_data.clear() # تفريغ الكاش لتحديث الأرقام فوراً في القائمة الرئيسية
                else:
                    st.error(f"خطأ من السيرفر: {res.status_code}")
            except Exception as e:
                st.error("❌ فشل الاتصال بالسيرفر لإضافة المعدة.")
        else:
            st.warning("الرجاء إدخال اسم المعدة أولاً.")

# ==========================================
# 3. قسم مواقع التعدين
# ==========================================
elif menu == "🗺️ مواقع التعدين":
    st.header("🗺️ تتبع مواقع التعدين والامتياز")
    st.write("عرض تفصيلي لمناطق الإنتاج والتعدين الأهلي والشركات.")
    st.info("...جاري تحميل الخرائط الإحداثية للمواقع النشطة في ولايات السودان المختلفة...")

# ==========================================
# 4. قسم أسعار الذهب
# ==========================================
elif menu == "💰 أسعار الذهب اليوم":
    st.header("💰 مؤشر أسعار الذهب في السوق المحلي والعالمي")
    st.write("تحديثات بورصة الذهب اللحظية.")
    
    st.table({
        "العيار": ["عيار 24", "عيار 21", "عيار 18", "الخام المحلي (جرام)"],
        "السعر الحالي (تقديري)": ["105,000 ج.س", "91,875 ج.س", "78,750 ج.س", "جاري السحب الحقيقي..."]
    })

# ==========================================
# 5. قسم التسجيل ودخول المستخدمين
# ==========================================
elif menu == "📝 تسجيل حساب جديد":
    st.header("📝 إنشاء حساب جديد في المنصة")
    username = st.text_input("اسم المستخدم")
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    
    if st.button("تنفيذ التسجيل"):
        try:
            response = requests.post(f"{API_URL}/api/v1/users/register", json={"username": username, "email": email, "password": password}, timeout=5)
            if response.status_code in [200, 201]:
                st.success("🎉 تم إنشاء الحساب بنجاح في قاعدة البيانات السحابية!")
            else:
                st.error(f"خطأ: {response.json().get('detail', 'تعذر التسجيل')}")
        except Exception as e:
            st.error("🚨 خطأ في الاتصال بالخادم، يرجى التحقق من حالة الـ API.")

elif menu == "🔑 دخول":
    st.header("🔑 تسجيل الدخول للنظام")
    email_login = st.text_input("البريد الإلكتروني أو اسم المستخدم")
    password_login = st.text_input("كلمة المرور الكودية", type="password")
    if st.button("دخول"):
        st.info("جاري التحقق من الصلاحيات وشهادة التشفير...")
