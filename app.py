import streamlit as st
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- Page Config ---
st.set_page_config(page_title="BEU BULK RESULT FINDER", page_icon="🎓", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e6edf3; }
    .uni-title { color: #ffffff; font-size: 28px; font-weight: 800; margin-bottom: 5px; text-align: center; }
    .sub-title { color: #007bff; font-size: 18px; font-weight: 600; text-align: center; margin-bottom: 30px; text-transform: uppercase; }
    .stTextInput>div>div>input { background-color: #161b22 !important; color: white !important; border: 1px solid #30363d !important; border-radius: 10px !important; }
    .stButton>button { background: linear-gradient(90deg, #007bff, #00c6ff); color: white; border-radius: 10px; font-weight: bold; padding: 15px; width: 100%; transition: 0.3s; border: none; }
    .result-card { background: #161b22; border: 1px solid #30363d; border-left: 5px solid #007bff; padding: 15px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .btn-link { background-color: #238636; color: white !important; padding: 8px 15px; border-radius: 6px; text-decoration: none !important; font-size: 14px; font-weight: bold; }
    .footer { text-align: center; margin-top: 60px; padding: 30px; border-top: 1px solid #30363d; color: #8b949e; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- Logo Logic ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Check if logo.png exists in the current directory
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        # Fallback to Wikipedia link if local file fails
        st.image("https://upload.wikimedia.org/wikipedia/en/3/3a/Bihar_Engineering_University_logo.png", width=120)

st.markdown("<div class='uni-title'>Bihar Engineering University, Patna</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>BEU Bulk Result Finder</div>", unsafe_allow_html=True)

# --- Input Section ---
st.markdown("---")
url_input = st.text_input("🔗 Paste Sample Result URL (with regNo=)", placeholder="https://beu-bih.ac.in/result-three?...")

c1, c2 = st.columns(2)
with c1:
    start_val = st.number_input("Start Registration No.", value=23102125001, format="%d")
with c2:
    end_val = st.number_input("End Registration No.", value=23102125010, format="%d")

# --- Logic ---
if st.button("🚀 GENERATE BULK LINKS"):
    if not url_input or "regNo=" not in url_input:
        st.error("❌ Valid URL missing!")
    else:
        try:
            parsed = urlparse(url_input)
            params = parse_qs(parsed.query)
            st.markdown("### 📋 Results List")
            for r in range(int(start_val), int(end_val) + 1):
                params['regNo'] = [str(r)]
                final_url = urlunparse(parsed._replace(query=urlencode(params, doseq=True)))
                st.markdown(f"""
                <div class="result-card">
                    <span>🎓 Reg: <b>{r}</b></span>
                    <a href="{final_url}" target="_blank" class="btn-link">📄 View Result</a>
                </div>
                """, unsafe_allow_html=True)
            st.success("Links Ready!")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Footer ---
st.markdown(f"""
    <div class="footer">
        <p>This Bulk Result Downloader is designed and developed by <b>Krishna Raj</b>,<br>
        a student of <b>Rashtrakavi Ramdhari Singh Dinkar College of Engineering</b>, Batch 2023,<br>
        from the Mechanical Engineering Department.</p>
        <p>Connect with me on <a href="https://www.linkedin.com/in/krishna-raj-%F0%9F%87%AE%F0%9F%87%B3-528108310" target="_blank">LinkedIn</a>.</p>
    </div>
    """, unsafe_allow_html=True)
