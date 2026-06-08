import streamlit as st
import requests
import re
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
# 🎨 تصميم بصري
# =========================
st.markdown("""
<style>
.main { background-color: #0B0F14; color: white; }

h1, h2, h3 { color: #D4AF37 !important; }

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
