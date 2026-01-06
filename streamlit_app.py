import streamlit as st
import os
from agents.orchestrator import orchestrator # Import langsung logika AI Anda

st.set_page_config(page_title="Olist AI Assistant", page_icon="🤖")

st.title("🤖 Olist Multi-Agent System")
st.markdown("Sistem ini menganalisis data SQL dan dokumen RAG secara otomatis.")

# Input pengguna
user_query = st.text_input("Tanyakan sesuatu:", placeholder="Contoh: Berapa rata-rata harga produk kesehatan?")

if st.button("Kirim"):
    if user_query:
        with st.spinner("Agent sedang berdiskusi..."):
            try:
                # Memanggil fungsi orchestrator lokal (bukan lewat API internet)
                response = orchestrator(user_query)
                
                st.success("Jawaban AI:")
                st.write(response)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan sistem: {str(e)}")
    else:
        st.warning("Masukkan pertanyaan terlebih dahulu.")

st.sidebar.markdown("### Status Sistem")
st.sidebar.success("Mode: Integrated Docker (Local Engine)")