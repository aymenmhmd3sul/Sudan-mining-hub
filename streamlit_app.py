import streamlit as st
import requests

st.set_page_config(page_title="منصة تعدين السودان", page_icon="⛏️", layout="wide")

st.title("⛏️ منصة تعدين السودان الرقمية")
st.markdown("---")

API_URL = "https://sudan-mining-platform.onrender.com"

menu = st.sidebar.radio("القائمة", ["🏠 الرئيسية", "📝 تسجيل", "🔑 دخول", "👤 ملفي"])

if menu == "📝 تسجيل":
    st.header("إنشاء حساب جديد")
    username = st.text_input("اسم المستخدم")
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("تسجيل"):
        try:
            response = requests.post(f"{API_URL}/api/v1/register", json={"username": username, "email": email, "password": password})
            if response.status_code in [200, 201]:
                st.success("تم التسجيل بنجاح!")
            else:
                st.error(f"خطأ: {response.json().get('detail', 'فشل التسجيل')}")
        except:
            st.error("خطأ في الاتصال بالخادم")

elif menu == "🔑 دخول":
    st.header("تسجيل الدخول")
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        st.info("سيتم إضافة وظيفة تسجيل الدخول قريباً")

elif menu == "👤 ملفي":
    st.header("معلومات المستخدم")
    st.info("سجل الدخول أولاً")

else:
    st.header("مرحباً بك في منصة تعدين السودان")
    st.write("استخدم القائمة الجانبية للتسجيل أو الدخول")
