import streamlit as st
import requests

st.set_page_config(page_title="Olist AI Assistant", page_icon="🤖")
st.title("🤖 Olist Multi-Agent System")

# URL API Backend
API_URL = st.sidebar.text_input("API Endpoint", "https://imammrtd-fp.hf.space/ask")

user_query = st.text_input("Tanyakan sesuatu:", placeholder="Contoh: Berapa rata-rata harga produk kesehatan?")

if st.button("Kirim"):
    if user_query:
        # Menggunakan st.status untuk merepresentasikan tahapan kerja Multi-Agent
        with st.status("Agent sedang bekerja...", expanded=True) as status:
            st.write("🔍 Mencari referensi di RAG (Qdrant)...")
            st.write("📊 Mengambil data dari SQL (Olist Database)...")
            
            try:
                # Memanggil Rest API Backend
                response = requests.post(API_URL, json={"prompt": user_query})
                
                if response.status_code == 200:
                    answer = response.json().get("answer")
                    # Jawaban dimasukkan ke dalam kotak hijau (st.success)
                    st.success(f"**Jawaban AI:** \n\n {answer}")
                else:
                    st.error(f"Kesalahan API: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Gagal terhubung ke API: {e}")
            
            status.update(label="Analisis Selesai!", state="complete")
    else:
        st.warning("Silakan masukkan pertanyaan.")