import streamlit as st
from services import get_gold_prices

st.set_page_config(page_title="منصة تعدين السودان", layout="wide")

# ====== SIDEBAR ======
st.sidebar.title("📌 القائمة")

page = st.sidebar.radio("التنقل", [
    "📊 الداشبورد",
    "🛒 السوق",
    "👤 المستخدم"
])

user_type = st.sidebar.selectbox("نوع المستخدم", [
    "مشتري",
    "تاجر"
])

# ====== DATA ======
data = get_gold_prices()

# ====== DASHBOARD ======
if page == "📊 الداشبورد":
    st.title("📊 لوحة الأسعار")

    col1, col2, col3 = st.columns(3)

    col1.metric("🇸🇩 المحلي", f"{data['local']} SDG")
    col2.metric("🌍 العالمي", f"{data['global']} USD")
    col3.metric("📊 الاتجاه", data['direction'])

    st.line_chart([
        data['local'] - 150,
        data['local'] - 80,
        data['local']
    ])

# ====== MARKET ======
elif page == "🛒 السوق":
    st.title("🛒 السوق")

    st.subheader("المعدات المتاحة")

    category = st.selectbox("تصنيف المعدات", [
        "معدات خفيفة",
        "معدات ثقيلة",
        "أخرى (بحث حر)"
    ])

    search = st.text_input("ابحث عن أي معدات")

    if user_type == "مشتري":
        st.info("عرض خاص للمشتري")
    else:
        st.success("لوحة التاجر")

    st.button("طلب / إضافة إعلان")

# ====== USER ======
else:
    st.title("👤 المستخدم")

    st.write("نوع الحساب:", user_type)
    st.write("حالة النظام: نشط")
