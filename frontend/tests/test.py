import streamlit as st

st.set_page_config(page_title="HTML Test")

st.html("""
<div style="
    background:#ff5a36;
    color:white;
    padding:40px;
    border-radius:20px;
    font-size:30px;
    font-weight:bold;
">
    Shop<span style="color:#111827;">Ease</span>
</div>
""")