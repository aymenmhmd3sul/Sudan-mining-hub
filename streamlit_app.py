import streamlit as st

st.set_page_config(page_title="منصة تعدين السودان", layout="wide")

# ===== SIDEBAR =====
st.sidebar.title("📌 التحكم")

page = st.sidebar.radio(
    "التنقل",
    ["📊 الداشبورد", "🛒 المشتري", "🏪 التاجر", "🤝 الصفقات", "⚙️ النظام"]
)

# ===== DASHBOARD =====
if page == "📊 الداشبورد":
    st.title("📊 الداشبورد")
    st.success("النظام مستقر ويعمل الآن")

# ===== BUYER =====
elif page == "🛒 المشتري":
    st.title("🛒 المشتري")

    category = st.selectbox(
        "نوع الطلب",
        ["معدات خفيفة", "معدات ثقيلة", "أخرى (بحث حر)"]
    )

    search = st.text_input("ابحث عن المنتج")

    st.write("النتائج ستظهر هنا حسب التاجر")

# ===== SELLER =====
elif page == "🏪 التاجر":
    st.title("🏪 التاجر")
    st.info("لوحة التاجر - إدارة المنتجات")

# ===== DEALS =====
elif page == "🤝 الصفقات":
    st.title("🤝 الصفقات")
    st.warning("الصفقات النشطة ستظهر هنا")

# ===== SYSTEM =====
elif page == "⚙️ النظام":
    st.title("⚙️ معلومات النظام")
    st.write("حالة السيرفر: يعمل")
