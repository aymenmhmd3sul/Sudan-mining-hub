import streamlit as st

st.set_page_config(page_title="منصة تعدين السودان الرقمية", layout="wide")

===== SIDEBAR =====

st.sidebar.title("📌 القائمة")

page = st.sidebar.radio(
"التنقل",
["📊 الداشبورد", "🛒 المشتري", "🏪 التاجر", "🤝 الصفقات", "⭐ المؤسسون", "⚙️ النظام"]
)

st.title("📊 منصة تعدين السودان الرقمية")

===== DASHBOARD =====

if page == "📊 الداشبورد":
st.subheader("لوحة الأسعار")
st.metric("السوق المحلي", "114186 SDG")
st.metric("السوق العالمي", "75.56 USD")

===== BUYER =====

elif page == "🛒 المشتري":
st.subheader("طلب شراء")
st.text_input("ما الذي تريد شراءه؟")
st.text_area("وصف الطلب")

===== SELLER =====

elif page == "🏪 التاجر":
st.subheader("تسجيل تاجر")
st.text_input("اسم التاجر")
st.text_input("رقم الهاتف")
st.selectbox("نوع النشاط", ["معدات خفيفة", "معدات ثقيلة", "ذهب", "نقل", "خدمات"])

===== DEALS =====

elif page == "🤝 الصفقات":
st.info("لا توجد صفقات حالياً")

===== FOUNDERS

elif page == "⭐ المؤسسون":
st.success("أول 50 تاجر يحصلون على خصم 10%")

===== SYSTEM

elif page == "⚙️ النظام":
st.write("النظام يعمل بشكل مستقر")
