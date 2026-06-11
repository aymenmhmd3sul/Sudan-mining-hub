from streamlit_autorefresh import st_autorefresh

# تحديث كل 180 ثانية (3 دقائق)
st_autorefresh(interval=180000, key="gold_refresh")
