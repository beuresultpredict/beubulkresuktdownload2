import streamlit as st
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- Page Config ---
st.set_page_config(page_title="BEU BULK RESULT FINDER", page_icon="🎓", layout="centered")

# --- Custom CSS (Advanced Blue & Black Professional Theme) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { 
        background-color: #0b0e14; 
        color: #e6edf3; 
    }
    
    /* Header Container Styling */
    .header-box {
        text-align: center;
        padding: 30px 10px;
        background: linear-gradient(180deg, #161b22 0%, #0b0e14 100%);
        border-bottom: 2px solid #007bff;
        margin-bottom: 40px;
        border-radius: 0 0 20px 20px;
    }
    .uni-name {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .sub-title {
        color: #007bff;
        font-size: 20px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    
    /* Big Action Button */
    .stButton>button {
        background: linear-gradient(90deg, #007bff, #00c6ff);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        padding: 20px;
        width: 100%;
        transition: 0.4s;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 25px rgba(0, 123, 255, 0.6);
        color: white;
    }

    /* Result Card Styling */
    .result-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 6px solid #007bff;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.3s;
    }
    .result-card:hover {
        border-color: #007bff;
        background: #1c2128;
    }

    /* Download Link Button */
    .btn-link {
        background-color: #238636;
        color: white !important;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        text-decoration: none !important;
        display: inline-block;
    }
    .btn-link:hover {
        background-color: #2ea043;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        margin-top: 80px;
        padding: 40px 20px;
        background: #0d1117;
        border-top: 1px solid #30363d;
        color: #8b949e;
        font-size: 14px;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logo & Heading ---
col_l, col_r = st.columns([1, 4])
with col_l:
    # Yahan aap apna logo.png upload karke uska naam likh sakte hain
    # Filhal main placeholder image use kar raha hoon
    st.image("https://beu-bih.ac.in/images/logo.png", width=100)

with col_r:
    st.markdown("""
        <div style='padding-top: 10px;'>
            <div style='color: #ffffff; font-size: 28px; font-weight: 800;'>Bihar Engineering University, Patna</div>
            <div style='color: #007bff; font-size: 18px; font-weight: 600;'>BEU Bulk Result Finder</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Form Section ---
st.markdown("### 📝 Enter Details")
url_input = st.text_input("🔗 Paste any student's Result URL from BEU Website", 
                          placeholder="Example: https://beu-bih.ac.in/result-three?name=...")

c1, c2 = st.columns(2)
with c1:
    start_num = st.number_input("Start Registration No.", value=23102125001, format="%d")
with c2:
    end_num = st.number_input("End Registration No.", value=23102125010, format="%d")

# --- Execution ---
if st.button("🚀 GENERATE ALL LINKS"):
    if not url_input or "regNo=" not in url_input:
        st.error("⚠️ Please enter a valid URL that contains 'regNo'.")
    else:
        try:
            parsed = urlparse(url_input)
            params = parse_qs(parsed.query)
            
            st.markdown("### 📋 Result Links Generated")
            st.info("Click 'Open Result' and press **Ctrl + P** to save as PDF.")
            
            for r in range(int(start_num), int(end_num) + 1):
                params['regNo'] = [str(r)]
                new_q = urlencode(params, doseq=True)
                final_url = urlunparse(parsed._replace(query=new_q))
                
                st.markdown(f"""
                <div class="result-card">
                    <span style="font-size:16px;">🎓 Reg No: <b>{r}</b></span>
                    <a href="{final_url}" target="_blank" class="btn-link">📄 Open Result</a>
                </div>
                """, unsafe_allow_html=True)
                
            st.balloons()
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- Footer ---
st.markdown(f"""
    <div class="footer">
        <p>This Bulk Result Downloader is designed and developed by <b>Krishna Raj</b>,<br>
        a student of <b>Rashtrakavi Ramdhari Singh Dinkar College of Engineering</b>, Batch 2023,<br>
        from the Mechanical Engineering Department.</p>
        <p>In the future, major updates and improvements will be introduced in this SGPA Calculator to enhance accuracy and user experience.</p>
        <p>Connect with me on <a href="https://www.linkedin.com/in/krishna-raj-%F0%9F%87%AE%F0%9F%87%B3-528108310" target="_blank">LinkedIn</a>.</p>
    </div>
    """, unsafe_allow_html=True)
