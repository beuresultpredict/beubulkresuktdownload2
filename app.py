import streamlit as st
import requests
import io

# --- Page Config ---
st.set_page_config(page_title="BEU Bulk Result Downloader", page_icon="🎓")

# --- Blue & Black Theme CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 5px; border: none; font-weight: bold; width: 100%; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #007bff; }
    .footer { text-align: center; margin-top: 50px; color: #8b949e; border-top: 1px solid #30363d; padding-top: 20px; font-size: 14px; }
    a { color: #58a6ff !important; text-decoration: none; }
    .result-box { border: 1px solid #30363d; padding: 10px; border-radius: 5px; margin-bottom: 5px; background: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🟦 BEU Bulk Result Downloader")

# --- Inputs ---
sample_url = st.text_input("1. Paste Sample Result URL from BEU Website", 
                           placeholder="https://beu-bih.ac.in/result-three?name=...")

col1, col2 = st.columns(2)
with col1:
    start_reg = st.number_input("Start Reg. No", value=23102125001, step=1)
with col2:
    end_reg = st.number_input("End Reg. No", value=23102125010, step=1)

# --- Logic ---
if st.button("Check & Get Links"):
    if not sample_url:
        st.error("Please provide a sample URL!")
    else:
        try:
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
            parsed_url = urlparse(sample_url)
            params = parse_qs(parsed_url.query)
            
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            
            found_results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total = int(end_reg - start_reg + 1)
            
            for i, reg in enumerate(range(int(start_reg), int(end_reg) + 1)):
                params['regNo'] = [str(reg)]
                new_url = urlunparse(parsed_url._replace(query=urlencode(params, doseq=True)))
                
                status_text.text(f"Scanning: {reg}...")
                
                # Check if result exists
                response = requests.get(new_url, headers=headers, timeout=10)
                
                # Agar page par student ka naam ya SGPA mil raha hai (BEU logic)
                if response.status_code == 200 and "Registration No" in response.text:
                    found_results.append({"reg": reg, "url": new_url})
                
                progress_bar.progress((i + 1) / total)

            status_text.empty()
            
            if found_results:
                st.success(f"Found {len(found_results)} Results!")
                for item in found_results:
                    with st.container():
                        st.markdown(f"""
                        <div class="result-box">
                            <span>✅ Registration No: <b>{item['reg']}</b></span>
                            <a href="{item['url']}" target="_blank" style="float:right;">🔗 View Result</a>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.info("Note: BEU generates dynamic HTML. You can print these pages as PDF (Ctrl+P) directly from your browser.")
            else:
                st.warning("No results found on the BEU server for this range. Please check if the URL is correct or if the results are declared.")

        except Exception as e:
            st.error(f"Error connecting to BEU: {e}")

# --- Footer ---
st.markdown(f"""
    <div class="footer">
        <p>This Bulk Result Downloader is designed and developed by <b>Krishna Raj</b>,<br>
        a student of <b>Rashtrakavi Ramdhari Singh Dinkar College of Engineering</b>, Batch 2023,<br>
        from the Mechanical Engineering Department.</p>
        <p>In the future, major updates and improvements will be introduced in this SGPA Calculator to enhance accuracy and user experience.</p>
        <p>Connect with me on <a href="https://www.linkedin.com/in/krishna-raj-528108310" target="_blank">LinkedIn</a>.</p>
    </div>
    """, unsafe_allow_html=True)
