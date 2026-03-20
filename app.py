import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- Page Config ---
st.set_page_config(page_title="BEU Bulk Result Downloader", page_icon="🎓")

# --- Blue & Black Theme CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 5px; border: none; font-weight: bold; width: 100%; height: 3em; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #007bff; }
    .stNumberInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #007bff; }
    .footer { text-align: center; margin-top: 50px; color: #8b949e; border-top: 1px solid #30363d; padding-top: 20px; font-size: 14px; }
    a { color: #58a6ff !important; text-decoration: none; }
    .result-card { border: 1px solid #007bff; padding: 15px; border-radius: 10px; margin-bottom: 10px; background: #161b22; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🟦 BEU Bulk Result Downloader")

# --- Inputs ---
st.info("Note: Paste the full URL from the BEU result page.")
sample_url = st.text_input("1. Paste Sample Result URL", 
                           placeholder="https://beu-bih.ac.in/result-three?name=B.Tech...")

col1, col2 = st.columns(2)
with col1:
    start_reg = st.number_input("Start Reg. No", value=23102125001, format="%d")
with col2:
    end_reg = st.number_input("End Reg. No", value=23102125010, format="%d")

# --- Logic ---
if st.button("Generate Result Links"):
    if not sample_url:
        st.error("Please paste a valid URL first!")
    elif "regNo=" not in sample_url:
        st.error("The URL must contain 'regNo'. Please copy the full link.")
    else:
        try:
            # URL Parsing
            parsed_url = urlparse(sample_url)
            query_params = parse_qs(parsed_url.query)
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://beu-bih.ac.in/"
            }
            
            found_count = 0
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_count = int(end_reg - start_reg + 1)
            
            st.markdown("### 📋 Found Results:")

            for i, current_reg in enumerate(range(int(start_reg), int(end_reg) + 1)):
                # Update the regNo in parameters
                query_params['regNo'] = [str(current_reg)]
                new_query = urlencode(query_params, doseq=True)
                final_link = urlunparse(parsed_url._replace(query=new_query))
                
                status_text.text(f"Checking Registration No: {current_reg}...")
                
                # Check if this specific result exists (Optional: but good for validation)
                # Note: Some BEU results might block direct scraping, so we show links directly
                
                st.markdown(f"""
                <div class="result-card">
                    <span>🎓 Reg. No: <b>{current_reg}</b></span>
                    <a href="{final_link}" target="_blank">🔍 Open Result</a>
                </div>
                """, unsafe_allow_html=True)
                
                found_count += 1
                progress_bar.progress((i + 1) / total_count)

            status_text.success(f"Generated {found_count} links successfully!")

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
