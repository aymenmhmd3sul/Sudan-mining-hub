import streamlit as st
from streamlit_autorefresh import st_autorefresh
from services import get_gold_prices

st.set_page_config(page_title="منصة تعدين السودان الرقمية", layout="wide")

# تحديث تلقائي
st_autorefresh(interval=3000, key="refresh")

# Sidebar Navigation
st.sidebar.title("📌 الأقسام")

page = st.sidebar.radio("اختر القسم", [
    "📊 الأسعار",
    "🛒 السوق",
    "ℹ️ معلومات"
])

# ========== الصفحة 1 ==========
if page == "📊 الأسعار":
    st.title("📊 أسعار الذهب المباشرة")

    data = get_gold_prices()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🇸🇩 المحلي", f"{data['local']} SDG", f"{data['change']}")
    col2.metric("🌍 العالمي", f"{data['global']} USD")
    col3.metric("📊 الاتجاه", data['direction'])
    col4.metric("⚡ الحالة", "LIVE")

    st.line_chart([data['local'] - 200, data['local'] - 100, data['local']])

    st.caption(f"آخر تحديث: {data['timestamp']}")

# ========== الصفحة 2 ==========
elif page == "🛒 السوق":
    st.title("🛒 سوق المعدات")

    st.info("هنا سيتم عرض أجهزة التنقيب والمعدات قريباً")

    st.selectbox("اختر نوع الجهاز", [
        "جهاز تنقيب ذهب",
        "معدات حفر",
        "معدات فصل المعادن"
    ])

    st.button("طلب الآن")

# ========== الصفحة 3 ==========
else:
    st.title("ℹ️ معلومات النظام")
    st.write("منصة تعدين السودان الرقمية - نسخة تجريبية")
