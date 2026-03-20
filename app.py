import streamlit as st
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- Page Config ---
st.set_page_config(page_title="BEU BULK RESULT FINDER", page_icon="🎓", layout="centered")

# --- Custom CSS (Modern Professional Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e6edf3; }
    
    /* Header Container */
    .header-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding: 20px;
        border-bottom: 2px solid #007bff;
        margin-bottom: 30px;
    }
    .uni-title {
        color: #ffffff;
        font-size: clamp(20px, 5vw, 32px);
        font-weight: 800;
        margin: 0;
    }
    .sub-title {
        color: #007bff;
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }

    /* Button */
    .stButton>button {
        background: linear-gradient(90deg, #007bff, #00c6ff);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        padding: 15px;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 123, 255, 0.5);
    }

    /* Result Cards */
    .result-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 5px solid #007bff;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .btn-link {
        background-color: #238636;
        color: white !important;
        padding: 8px 15px;
        border-radius: 6px;
        text-decoration: none !important;
        font-size: 14px;
        font-weight: bold;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 60px;
        padding: 30px;
        border-top: 1px solid #30363d;
        color: #8b949e;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
# Wikipedia direct image link for BEU Logo
logo_url = "https://upload.wikimedia.org/wikipedia/en/3/3a/Bihar_Engineering_University_logo.png"

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image(logo_url, width=120)
    st.markdown("<h1 style='text-align: center; color: white; margin-top: 10px;'>Bihar Engineering University, Patna</h1>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>BEU Bulk Result Finder</div>", unsafe_allow_html=True)

# --- Input Section ---
st.markdown("### 🛠 Setup Range")
url_input = st.text_input("🔗 Paste Result URL (Must contain 'regNo=')", 
                          placeholder="https://beu-bih.ac.in/result-three?name=...")

c1, c2 = st.columns(2)
with c1:
    start_val = st.number_input("Start Registration No.", value=23102125001, format="%d")
with c2:
    end_val = st.number_input("End Registration No.", value=23102125010, format="%d")

# --- Execution ---
if st.button("🚀 GENERATE BULK LINKS"):
    if not url_input or "regNo=" not in url_input:
        st.error("❌ Please provide a valid BEU result URL with a registration number.")
    else:
        try:
            parsed = urlparse(url_input)
            params = parse_qs(parsed.query)
            
            st.markdown("---")
            st.subheader("📋 Results Found")
            
            for r in range(int(start_val), int(end_val) + 1):
                params['regNo'] = [str(r)]
                new_url = urlunparse(parsed._replace(query=urlencode(params, doseq=True)))
                
                st.markdown(f"""
                <div class="result-card">
                    <span>🎓 Registration: <b>{r}</b></span>
                    <a href="{new_url}" target="_blank" class="btn-link">📄 Open & Print</a>
                </div>
                """, unsafe_allow_html=True)
            
            st.success("All links generated! Use Ctrl+P to save any result as PDF.")
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")

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
