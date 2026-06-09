import streamlit as st
import time
from services import get_gold_prices

st.set_page_config(page_title="منصة تعدين السودان الرقمية", layout="wide")

st.title("📊 منصة تعدين السودان الرقمية")
st.subheader("نظام سوق الذهب والمعدات - LIVE")

placeholder = st.empty()

while True:
    data = get_gold_prices()

    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🇸🇩 المحلي", f"{data['local']} SDG", f"{data['change']}")
        col2.metric("🌍 العالمي", f"{data['global']} USD")
        col3.metric("📊 الاتجاه", data['direction'])
        col4.metric("⚡ الحالة", "LIVE")

        st.line_chart([data['local'] - 200, data['local'] - 100, data['local']])

        st.caption(f"آخر تحديث: {data['timestamp']}")

    time.sleep(3)
