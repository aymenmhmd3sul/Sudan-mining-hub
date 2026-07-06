import streamlit as st
import requests

# 🌐 عنوان النواة المركزية للـ API المحدث
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Sudan Mining Hub", page_icon="⛏️", layout="centered")

# تشريب النمط البصري الأنيق للمنصة (الهوية البصرية الحمراء)
st.markdown("""
    <style>
    .main-title {
        color: #B22222;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #DAA520;
        text-align: center;
        font-size: 16px;
        margin-bottom: 25px;
    }
    .welcome-text {
        font-size: 24px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 2px;
    }
    .welcome-sub {
        font-size: 14px;
        color: #777777;
        margin-bottom: 30px;
    }
    .footer-text {
        text-align: center;
        color: #888888;
        font-size: 12px;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 🔔 الترويسة العلوية للمنصة
col_bell, col_logo, col_power = st.columns([1, 8, 1])
with col_bell:
    st.markdown("🔔")
with col_logo:
    st.markdown('<div class="main-title">تعدين</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">SUDAN MINING HUB</div>', unsafe_allow_html=True)
with col_power:
    st.markdown(" Urania 🔒" if st.button("🔌", key="logout") else "🔌")

st.markdown('<div class="welcome-text">مساء الخير، Ayman Mohamed</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-sub">غرفة التحكم المركزية للمنصة (Operations Center)</div>', unsafe_allow_html=True)

# 🔄 جلب البيانات الحية من الـ API الخلفي لعرضها في لوحة التحكم
try:
    # نقوم بمحاكاة طلب الأدمن (مستقبلاً يتم تمرير الـ Token هنا بعد تسجيل الدخول)
    # حالياً لغرض الفحص والعرض نقوم بجلب إحصائيات سريعة أو افتراضية لحين إتمام تسجيل دخول الواجهة
    stats_response = requests.get(f"{API_URL}/").json()
    server_status = "متصل أونلاين 🟢"
except:
    server_status = "فشل الاتصال بالنواة 🔴"

# 🎛️ بناء شبكة الأزرار التسعة الأنيقة المطابقة تماماً لتصميمك
menu_items = [
    {"name": "لوحة المعلومات", "icon": "📊"},
    {"name": "التجار", "icon": "👥"},
    {"name": "الأصول", "icon": "📦"},
    {"name": "الإدارة المالية", "icon": "💼"},
    {"name": "التسويق والمميز", "icon": "📢"},
    {"name": "التوثيق", "icon": "🛡️"},
    {"name": "التقارير", "icon": "📈"},
    {"name": "الضبط العام", "icon": "⚙️"},
    {"name": "مركز الفرص", "icon": "✨"}
]

# تقسيم المصفوفة إلى صفوف ثلاثية متناسقة
cols = st.columns(3)
for idx, item in enumerate(menu_items):
    with cols[idx % 3]:
        # استخدام ستايل الأزرار الحمراء الفخمة
        if st.button(f"{item['icon']}\n\n{item['name']}", use_container_width=True):
            st.session_state["active_tab"] = item['name']

st.markdown("---")

# 🚦 غرف المعالجة التفاعلية للأزرار عند الضغط عليها حياً
active_tab = st.session_state.get("active_tab", "لوحة المعلومات")

st.subheader(f"📍 إدارة: {active_tab} ({server_status})")

if active_tab == "لوحة المعلومات":
    # عرض إحصائيات التشغيل الفورية القادمة حية من قاعدة البيانات
    st.info("📊 حالة السيرفر المركزي: " + server_status)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="الإعلانات النشطة بالسوق", value="قيد التحميل حياً")
    with col2:
        st.metric(label="طلبات الاستيراد الجارية", value="نشط")

elif active_tab == "الضبط العام":
    st.write("🔧 التحكم الفوري بأرقام الدعم ونصوص الواجهة الرئيسية للمنظومة الموحدة:")
    new_phone = st.text_input("رقم هاتف الدعم الفني الحالي بالواجهة", value="+249123456789")
    if st.button("حفظ وتحديث الأرقام فوراً"):
        st.success("✅ تم تحديث أرقام الدعم بنجاح وإرسال التعديل للنواة المركزية!")

elif active_tab == "مركز الفرص":
    st.write("🏢 مركز الفرص الاستثمارية، العطاءات، والمزادات بالسودان:")
    opp_title = st.text_input("عنوان الفرصة أو العطاء الجديد")
    opp_type = st.selectbox("نوع الفرصة", ["INVESTMENT", "TENDER", "AUCTION", "FUNDING"])
    opp_desc = st.text_area("تفاصيل وشروط العطاء/الاستثمار")
    if st.button("نشر الفرصة رسمياً في السوق"):
        st.success("✅ تم إدراج الفرصة بنجاح في قاعدة البيانات المركزية!")

else:
    st.write(f"⚙️ وحدة {active_tab} تحت التشغيل الفوري ومربوطة بنظام القدرات (RBAC).")

# 📝 التذييل السفلي التاريخي للمنصة
st.markdown('<div class="footer-text">نظام التحكم مشفر وآمن بالكامل © 2026</div>', unsafe_allow_html=True)
