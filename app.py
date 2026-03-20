import streamlit as st
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- Page Config ---
st.set_page_config(page_title="BEU Bulk Result Downloader", page_icon="🎓")

# --- Custom CSS (Blue & Black Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 8px; font-weight: bold; width: 100%; height: 3.5em; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #007bff; }
    .footer { text-align: center; margin-top: 50px; color: #8b949e; border-top: 1px solid #30363d; padding-top: 20px; font-size: 14px; }
    a { color: #58a6ff !important; text-decoration: none; font-weight: bold; }
    .result-card { border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 12px; background: #161b22; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🟦 BEU Bulk Result Downloader")

# --- Inputs ---
st.info("💡 Paste the result URL of any student from the BEU site below.")
sample_url = st.text_input("1. Paste Sample Result URL", 
                           placeholder="https://beu-bih.ac.in/result-three?name=...")

col1, col2 = st.columns(2)
with col1:
    start_reg = st.number_input("Start Reg. No", value=23102125001, format="%d")
with col2:
    end_reg = st.number_input("End Reg. No", value=23102125010, format="%d")

# --- Logic ---
if st.button("Generate Bulk Result Links"):
    if not sample_url or "regNo=" not in sample_url:
        st.error("Please paste a correct BEU Result URL containing 'regNo'.")
    else:
        try:
            # URL Parsing
            parsed_url = urlparse(sample_url)
            query_params = parse_qs(parsed_url.query)
            
            st.success(f"Successfully generated links for range {start_reg} to {end_reg}")
            
            st.markdown("### 📋 Result List:")
            st.write("Click the links below to view/print results. (Use Ctrl+P to save as PDF)")

            for reg in range(int(start_reg), int(end_reg) + 1):
                # Update regNo dynamically
                query_params['regNo'] = [str(reg)]
                new_query = urlencode(query_params, doseq=True)
                final_link = urlunparse(parsed_url._replace(query=new_query))
                
                # Show cards for each student
                st.markdown(f"""
                <div class="result-card">
                    <span>🎓 Reg. No: <b>{reg}</b></span>
                    <a href="{final_link}" target="_blank">📄 View & Download PDF</a>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error generating links: {e}")

# --- Footer ---
st.markdown("---")
st.markdown(f"""
    <div class="footer">
        <p>This Bulk Result Downloader is designed and developed by <b>Krishna Raj</b>,<br>
        a student of <b>Rashtrakavi Ramdhari Singh Dinkar College of Engineering</b>, Batch 2023,<br>
        from the Mechanical Engineering Department.</p>
        <p>In the future, major updates and improvements will be introduced in this SGPA Calculator to enhance accuracy and user experience.</p>
        <p>Connect with me on <a href="https://www.linkedin.com/in/krishna-raj-%F0%9F%87%AE%F0%9F%87%B3-528108310" target="_blank">LinkedIn</a>.</p>
    </div>
    """, unsafe_allow_html=True)
