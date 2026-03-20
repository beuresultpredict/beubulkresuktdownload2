import streamlit as st
import requests
from PyPDF2 import PdfMerger
import io
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# --- Page Config ---
st.set_page_config(page_title="BEU Bulk Result Downloader", page_icon="🎓")

# --- Blue & Black Theme CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 5px; border: none; }
    .stTextInput>div>div>input { background-color: #161b22; color: white; border: 1px solid #007bff; }
    .footer { text-align: center; margin-top: 50px; color: #8b949e; border-top: 1px solid #30363d; padding-top: 20px; }
    a { color: #58a6ff !important; text-decoration: none; }
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
if st.button("Generate & Merge Results"):
    if not sample_url:
        st.error("Please provide a sample URL!")
    else:
        try:
            parsed_url = urlparse(sample_url)
            params = parse_qs(parsed_url.query)
            merger = PdfMerger()
            found_count = 0
            
            headers = {"User-Agent": "Mozilla/5.0"} # Browser jaisa behave karne ke liye
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, reg in enumerate(range(int(start_reg), int(end_reg) + 1)):
                params['regNo'] = [str(reg)]
                new_url = urlunparse(parsed_url._replace(query=urlencode(params, doseq=True)))
                
                status_text.text(f"Checking: {reg}...")
                response = requests.get(new_url, headers=headers)
                
                if response.status_code == 200:
                    # Yahan hum check kar rahe hain ki kya response PDF hai
                    pdf_data = io.BytesIO(response.content)
                    try:
                        merger.append(pdf_data)
                        found_count += 1
                    except:
                        pass # Agar PDF nahi hai toh skip karega
                
                progress_bar.progress((i + 1) / (end_reg - start_reg + 1))

            if found_count > 0:
                output = io.BytesIO()
                merger.write(output)
                st.success(f"Done! Found {found_count} results.")
                st.download_button("📥 Download All Results (Merged PDF)", 
                                   data=output.getvalue(), 
                                   file_name="BEU_Bulk_Results.pdf")
            else:
                st.warning("No results found. Check the URL or Reg Nos.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Footer ---
st.markdown(f"""
    <div class="footer">
        <p>This Bulk Result Downloader is designed and developed by <b>Krishna Raj</b>,<br>
        a student of <b>Rashtrakavi Ramdhari Singh Dinkar College of Engineering</b>, Batch 2023,<br>
        from the Mechanical Engineering Department.</p>
        <p>In the future, major updates and improvements will be introduced in this SGPA Calculator to enhance accuracy and user experience.</p>
        <p>Connect with me on <a href="https://www.linkedin.com/in/krishna-raj-🇮🇳-528108310" target="_blank">LinkedIn</a>.</p>
    </div>
    """, unsafe_allow_html=True)
