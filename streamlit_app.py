import streamlit as st
import requests

# Konfigurasi halaman
st.set_page_config(page_title="Olist AI Interface", page_icon="🤖")

st.title("🤖 Olist AI Assistant Interface")
st.markdown("---")

BASE_URL = "https://finproim4.up.railway.app"
API_URL = f"{BASE_URL}/ask"

user_query = st.text_input("Tanyakan sesuatu tentang data transaksi:", placeholder="Contoh: Berapa total transaksi?")

if st.button("Tanya AI"):
    if user_query:
        with st.spinner("Menghubungi API di Cloud..."):
            try:
                # Melakukan hit ke REST API FastAPI
                response = requests.get(API_URL, params={"query": user_query})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Analisis AI Selesai:")
                    st.write(data.get("explanation", "Tidak ada penjelasan."))
                    
                    with st.expander("Lihat Detail Teknis (SQL & Raw Data)"):
                        st.subheader("SQL Query yang Dijalankan:")
                        st.code(data.get("sql_query"), language="sql")
                        
                        st.subheader("Data Hasil Query:")
                        result_data = data.get("data")
                        if result_data:
                            st.dataframe(result_data)
                        else:
                            st.info("Query berhasil namun tidak ada data yang ditemukan.")
                
                elif response.status_code == 404:
                    st.error("Error 404: Endpoint tidak ditemukan. Pastikan URL diakhiri dengan '/ask'.")
                else:
                    st.error(f"Terjadi kesalahan server (Status: {response.status_code})")
                    
            except requests.exceptions.ConnectionError:
                st.error("Gagal terhubung ke server. Periksa koneksi internet atau status deployment Railway Anda.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")
    else:
        st.warning("Silakan masukkan pertanyaan terlebih dahulu.")

st.sidebar.markdown("### Status Sistem")
st.sidebar.info(f"Terhubung ke: {BASE_URL}")