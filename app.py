import streamlit as st
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- Page Config ---
st.set_page_config(page_title="BEU BULK RESULT FINDER", page_icon="🎓", layout="centered")

# --- Modern Dark Blue & Black Theme CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { 
        background-color: #0b0e14; 
        color: #e6edf3; 
    }
    
    /* Elegant Header Section */
    .header-container {
        text-align: center;
        padding: 40px 10px;
        background: linear-gradient(180deg, #161b22 0%, #0b0e14 100%);
        border-bottom: 3px solid #007bff;
        margin-bottom: 40px;
        border-radius: 0 0 30px 30px;
    }
    .uni-title {
        color: #ffffff;
        font-size: clamp(24px, 5vw, 36px);
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }
    .sub-title {
        color: #007bff;
        font-size: clamp(14px, 3vw, 20px);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* Input Fields Customization */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 16px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 10px rgba(0, 123, 255, 0.3) !important;
    }

    /* Action Button */
    .stButton>button {
        background: linear-gradient(90deg, #007bff, #00c6ff);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        padding: 20px;
        width: 100%;
        margin-top: 10px;
        transition: 0.4s;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 123, 255, 0.6);
        color: white;
    }

    /* Result Cards */
    .result-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 6px solid #007bff;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.3s;
    }
    .result-card:hover {
        background: #1c2128;
        border-color: #007bff;
    }

    /* Direct Link Button */
    .btn-link {
        background-color: #238636;
        color: white !important;
        padding: 10px 22px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 700;
        text-decoration: none !important;
    }
    .btn-link:hover {
        background-color: #2ea043;
    }
    
    /* Professional Footer */
    .footer {
        text-align: center;
        margin-top: 80px;
        padding: 40px 20px;
        background: #0d1117;
        border-top: 1px solid #30363d;
        color: #8b949e;
        font-size: 14px;
        line-height: 1.7;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Clean Header (No Logo) ---
st.markdown("""
    <div class="header-container">
        <div class="uni-title">Bihar Engineering University, Patna</div>
        <div class="sub-title">BEU Bulk Result Finder</div>
    </div>
    """, unsafe_allow_html=True)

# --- User Inputs ---
st.markdown("### ⚙️ Search Configuration")
sample_url = st.text_input("🔗 Paste Student Result URL", 
                           placeholder="Ex: https://beu-bih.ac.in/result-three?name=...")

col1, col2 = st.columns(2)
with col1:
    start_reg = st.number_input("Start Reg. No", value=23102125001, format="%d")
with col2:
    end_reg = st.number_input("End Reg. No", value=23102125010, format="%d")

st.markdown("---")

# --- Logic Implementation ---
if st.button("🚀 FETCH BULK RESULT LINKS"):
    if not sample_url or "regNo=" not in sample_url:
        st.error("⚠️ Error: Please provide a valid BEU Result URL containing 'regNo'.")
    else:
        try:
            # Parse URL and prepare generation
            parsed_url = urlparse(sample_url)
            query_params = parse_qs(parsed_url.query)
            
            st.subheader("📋 Generated Results")
            st.info("Results generated! Open each link and use **Ctrl + P** to save as PDF.")
            
            for reg in range(int(start_reg), int(end_reg) + 1):
                # Swap the registration number
                query_params['regNo'] = [str(reg)]
                new_query = urlencode(query_params, doseq=True)
                final_link = urlunparse(parsed_url._replace(query=new_query))
                
                # Dynamic Card Display
                st.markdown(f"""
                <div class="result-card">
                    <span style="font-size: 17px; font-weight: 500;">🎓 Reg No: <b>{reg}</b></span>
                    <a href="{final_link}" target="_blank" class="btn-link">📄 VIEW RESULT</a>
                </div>
                """, unsafe_allow_html=True)
            
            st.balloons()

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# --- Footer Section ---
st.markdown(f"""
    <div class="footer">
        <p>This Bulk Result Downloader is designed and developed by <b>Krishna Raj</b>,<br>
        a student of <b>Rashtrakavi Ramdhari Singh Dinkar College of Engineering</b>, Batch 2023,<br>
        from the Mechanical Engineering Department.</p>
        <p>In the future, major updates and improvements will be introduced in this SGPA Calculator to enhance accuracy and user experience.</p>
        <p>Connect with me on <a href="https://www.linkedin.com/in/krishna-raj-%F0%9F%87%AE%F0%9F%87%B3-528108310" target="_blank">LinkedIn</a>.</p>
    </div>
    """, unsafe_allow_html=True)
