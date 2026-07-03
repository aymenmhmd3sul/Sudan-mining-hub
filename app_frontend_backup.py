import streamlit as st
import requests

# إعدادات الصفحة لتناسب شاشات الهواتف تماماً
st.set_page_config(
    page_title="Sudan Mining Hub - Preview",
    page_icon="🪙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تخصيص واجهة المستخدم بصرياً لمحاكاة روح تطبيق بنكك الفاخر
st.markdown("""
    <style>
    /* إخفاء القوائم العلوية الافتراضية لتقديم تجربة تطبيق كاملة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #fcfcfc;
    }
    
    /* الحاوية الرئيسية للتطبيق */
    .app-card {
        max-width: 420px;
        margin: auto;
        background: #ffffff;
        border-radius: 24px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06);
        overflow: hidden;
        font-family: 'Cairo', sans-serif;
    }
    
    /* الشريط العلوي المستوحى من اللون الأحمر الأنيق لبنكك */
    .top-banner {
        background: linear-gradient(135deg, #cc1818 0%, #990000 100%);
        padding: 35px 20px;
        text-align: center;
        color: white;
    }
    
    .brand-logo {
        font-size: 36px;
        font-weight: 900;
        letter-spacing: 1px;
    }
    
    .brand-sub {
        font-size: 14px;
        opacity: 0.85;
        margin-top: 5px;
    }
    
    /* محتوى الاستمارات الداخلي */
    .form-content {
        padding: 30px 25px;
    }
    
    /* جعل حقول الإدخال دائرية وأنيقة مع محاذاة النص بالمنتصف */
    .stTextInput > div > div > input {
        border-radius: 14px !important;
        border: 1.5px solid #e2e8f0 !important;
        padding: 14px !important;
        font-size: 16px !important;
        text-align: center !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #cc1818 !important;
        box-shadow: 0 0 0 3px rgba(204,24,24,0.1) !important;
    }
    
    /* زر دخول عريض وأنيق يعطي إحساس بالضغط الفعلي */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(90deg, #cc1818 0%, #b31414 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        padding: 14px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(204,24,24,0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(204,24,24,0.3) !important;
    }
    </style>
""", unsafe_html=True)

# الرابط السحابي للباكيند المستقر الذي أطلقناه معاً
BACKEND_URL = "https://sudan-mining-hub-3.onrender.com"

# بناء الهيكل البصري للتطبيق
st.markdown('<div class="app-card">', unsafe_html=True)

# تفعيل الشريط العلوي الملون
st.markdown("""
    <div class="top-banner">
        <div class="brand-logo">🪙 MINING HUB</div>
        <div class="brand-sub">بوابة تعدين السودان الذكية</div>
    </div>
""", unsafe_html=True)

# تفعيل منطقة الإدخال
st.markdown('<div class="form-content">', unsafe_html=True)

username = st.text_input("رقم المعرف المالي أو اسم المستخدم", placeholder="مثال: 9691029", key="preview_user")
password = st.text_input("كلمة المرور الخاصة بالحساب", placeholder="أدخل كلمة المرور هنا", type="password", key="preview_pass")

st.markdown('<div style="margin-top: 25px;"></div>', unsafe_html=True)

if st.button("تسجيل الدخول الآمن"):
    if username and password:
        with st.spinner("جاري التحقق الرقمي..."):
            try:
                response = requests.post(f"{BACKEND_URL}/auth/login", data={"username": username, "password": password})
                if response.status_code == 200:
                    st.success("تم التوثيق بنجاح! جاري الانتقال للوحة التحكم الخاصة بك.")
                else:
                    st.error("المعرف أو كلمة المرور غير مطابقة للسجلات الرسمية.")
            except:
                st.error("تعذر الاتصال بقاعدة البيانات.")
    else:
        st.warning("الرجاء كتابة البيانات كاملة للمعاينة.")

st.markdown('</div></div>', unsafe_html=True)
