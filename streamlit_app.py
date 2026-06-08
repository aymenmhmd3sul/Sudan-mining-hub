import streamlit as st
import requests
import urllib.parse
import random

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="منصة تعدين السودان الرقمية",
    page_icon="⛏️",
    layout="wide"
)

# =========================
# 🎨 تصميم ثابت (مضمون 100%)
# =========================
st.markdown("""
<style>
.main {
    background-color: #0B0F14;
    color: white;
}

h1, h2, h3 {
    color: #D4AF37 !important;
}

.stMetric {
    background-color: #111827;
    border: 1px solid #D4AF37;
    padding: 12px;
    border-radius: 12px;
}

.stButton > button {
    background-color: #D4AF37;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}

section[data-testid="stSidebar"] {
    background-color: #0F172A;
}
</style>
""", unsafe_allow_html=True)

# =========================
# النظام
# =========================
API_URL = "https://sudan-mining-platform.onrender.com"
ADMIN_PASSWORD = "dev_mode"

# =========================
# سوق حي بسيط
# =========================
@st.cache_data(ttl=10)
def live_price():
    base = 115000
    change = random.randint(-900, 1200)
    return base + change, change

# =========================
# واتساب
# =========================
def whatsapp_link(order_id, category, specs):
    msg = f"طلب #{order_id} | {category} | {specs}"
    return "https://wa.me/?text=" + urllib.parse.quote(msg)

# =========================
# واجهة
# =========================
st.title("⛏️ منصة تعدين السودان الرقمية")
st.caption("نظام سوق الذهب والمعدات والفرص الاستثمارية")
st.markdown("---")

menu = st.sidebar.radio(
    "📌 القائمة",
    ["📊 السوق", "🚜 المعدات", "💎 الفرص", "🔐 الإدارة"]
)

# =========================
# 1) السوق
# =========================
if menu == "📊 السوق":

    price, change = live_price()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🇸🇩 المحلي", f"{price:,} SDG", f"{change:+}")
    c2.metric("🌍 العالمي", "75.56 USD")
    c3.metric("📊 الاتجاه", "صعود 🔥" if change > 0 else "هبوط 🔻")
    c4.metric("⚡ تحديث", "LIVE")

    st.markdown("---")

    st.line_chart([price + random.randint(-500, 500) for _ in range(20)])

    if change > 800:
        st.success("🚀 ارتفاع قوي")
    elif change < -800:
        st.error("⚠️ هبوط قوي")
    else:
        st.info("📊 حركة طبيعية")

# =========================
# 2) المعدات
# =========================
elif menu == "🚜 المعدات":

    role = st.radio("الدور:", ["مشتري", "تاجر"])

    if role == "مشتري":

        if "order_id" not in st.session_state:
            st.session_state.order_id = None

        if st.session_state.order_id:

            st.success(f"طلب #{st.session_state.order_id}")

            link = whatsapp_link(
                st.session_state.order_id,
                st.session_state.cat,
                st.session_state.specs
            )

            st.link_button("📤 إرسال للتجار", link)

            if st.button("طلب جديد"):
                st.session_state.order_id = None
                st.rerun()

        else:

            with st.form("buyer"):
                name = st.text_input("الاسم")
                phone = st.text_input("الواتساب")
                cat = st.selectbox("الفئة", ["بوكلين", "لودر", "مولد"])
                specs = st.text_area("المواصفات")

                if st.form_submit_button("نشر") and name and phone:

                    st.session_state.order_id = random.randint(1000, 9999)
                    st.session_state.cat = cat
                    st.session_state.specs = specs

                    st.rerun()

    else:

        st.subheader("غرفة العروض")

        code = st.text_input("كود الدخول")

        if code:

            st.success("تم الدخول")

            with st.form("offer"):
                make = st.text_input("الشركة")
                model = st.text_input("الموديل")
                price = st.number_input("السعر")

                if st.form_submit_button("إرسال"):
                    st.success("تم الإرسال")

# =========================
# 3) الفرص
# =========================
elif menu == "💎 الفرص":

    st.subheader("💎 مشاريع استثمارية")

    st.markdown("🏭 مشروع تعدين جاهز - نهر النيل")

    if st.button("طلب اهتمام"):
        st.success("تم تسجيلك")

# =========================
# 4) الإدارة
# =========================
elif menu == "🔐 الإدارة":

    pw = st.text_input("كلمة المرور", type="password")

    if pw == ADMIN_PASSWORD:
        st.success("تم الدخول")
        st.table({"طلب": ["#1001"], "حالة": ["نشط"]})
    elif pw:
        st.error("خطأ")
