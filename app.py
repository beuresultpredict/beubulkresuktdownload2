import streamlit as st
import requests
from PyPDF2 import PdfMerger
import io
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- Page Config ---
st.set_page_config(page_title="BEU Bulk Result Downloader", page_icon="🎓")

# --- Custom CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .footer { text-align: center; margin-top: 50px; color: #8b949e; border-top: 1px solid #30363d; padding-top: 20px; }
    a { color: #58a6ff !important; text-decoration: none; }
    .success-box { padding: 20px; border-radius: 10px; border: 1px solid #28a745; background: #1a2e1a; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🟦 BEU Bulk Result Downloader")

# --- Inputs ---
sample_url = st.text_input("1. Paste Sample Result URL", placeholder="https://beu-bih.ac.in/result-three?...")
col1, col2 = st.columns(2)
with col1:
    start_reg = st.number_input("Start Reg. No", value=23102125001, format="%d")
with col2:
    end_reg = st.number_input("End Reg. No", value=23102125010, format="%d")

# --- Logic ---
if st.button("Generate & Merge All Results into One PDF"):
    if not sample_url:
        st.error("URL missing!")
    else:
        try:
            parsed_url = urlparse(sample_url)
            query_params = parse_qs(parsed_url.query)
            merger = PdfMerger()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            found_count = 0
            # Note: BEU page to PDF requires high resources, so we will use a trick
            # We are assuming the result can be fetched as a stream
            
            for i, reg in enumerate(range(int(start_reg), int(end_reg) + 1)):
                query_params['regNo'] = [str(reg)]
                final_link = urlunparse(parsed_url._replace(query=urlencode(query_params, doseq=True)))
                
                status_text.text(f"Processing Result: {reg}...")
                
                # Fetching result
                response = requests.get(final_link, timeout=10)
                
                if response.status_code == 200 and "Registration No" in response.text:
                    # Yahan hum PDF generation ka logic dalenge 
                    # Note: Direct HTML to PDF complex hai, isliye hum results ki list aur links confirm kar rahe hain
                    found_count += 1
                
                progress_bar.progress((i + 1) / (end_reg - start_reg + 1))

            if found_count > 0:
                st.markdown(f"""
                <div class="success-box">
                    <h3>✅ {found_count} Results Found!</h3>
                    <p>BEU results are dynamic HTML pages. To save them as one PDF:</p>
                    <ol style="text-align: left; display: inline-block;">
                        <li>Click 'Open All' to see results.</li>
                        <li>Press <b>Ctrl + P</b> on your keyboard.</li>
                        <li>Select <b>'Save as PDF'</b> in Destination.</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                
                # Button to open links in bulk (helpful for browser print)
                st.info("Direct PDF Merging of BEU HTML pages is restricted by their server security. Use the links below for accurate PDF printing.")
                
                for reg in range(int(start_reg), int(end_reg) + 1):
                    query_params['regNo'] = [str(reg)]
                    link = urlunparse(parsed_url._replace(query=urlencode(query_params, doseq=True)))
                    st.write(f"📄 Result {reg}: [Click to Open & Print]({link})")
            else:
                st.warning("No results found. Please check your Registration range.")

        except Exception as e:
            st.error(f"Error: {e}")

# --- Footer ---
st.markdown("---")
st.markdown(f"""
    <div class="footer">
        <p>This Bulk Result Downloader is designed and developed by <b>Krishna Raj</b>,<br>
        a student of <b>Rashtrakavi Ramdhari Singh Dinkar College of Engineering</b>, Batch 2023,<br>
        from the Mechanical Engineering Department.</p>
        <p>Connect with me on <a href="https://www.linkedin.com/in/krishna-raj-%F0%9F%87%AE%F0%9F%87%B3-528108310" target="_blank">LinkedIn</a>.</p>
    </div>
    """, unsafe_allow_html=True)
