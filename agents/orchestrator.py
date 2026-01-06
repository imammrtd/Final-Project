import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Menangani import agar kompatibel dengan Streamlit Cloud dan Lokal
try:
    # Menggunakan Relative Import (dengan tanda titik)
    # Ini mengharuskan folder 'agents' memiliki file __init__.py
    from .sql_agent import get_sql_chain
    from .rag_agent import get_rag_chain
except (ImportError, ModuleNotFoundError):
    # Fallback jika dijalankan langsung sebagai script (python orchestrator.py)
    from sql_agent import get_sql_chain
    from rag_agent import get_rag_chain

load_dotenv()

def orchestrator(user_input: str):
    # Mengambil API Key dari Environment (Streamlit Secrets / Railway)
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return "Error: OPENAI_API_KEY tidak ditemukan. Pastikan sudah disetel di Secrets/Variables."

    # 2. Inisialisasi Agent
    # Pastikan sql_agent dan rag_agent juga menggunakan os.getenv("OPENAI_API_KEY")
    sql_agent = get_sql_chain()
    rag_chain = get_rag_chain()

    if not sql_agent or not rag_chain:
        return "Error: Gagal menginisialisasi SQL atau RAG Agent."

    print(f"\n[ORCHESTRATOR] Menganalisis: {user_input}")
    
    # 3. Eksekusi RAG untuk konteks
    context_rag = rag_chain.invoke(f"Cari product_id terkait kategori: {user_input}")
    
    # 4. Eksekusi SQL Agent dengan bantuan konteks RAG
    enriched_query = f"""
    Pertanyaan Pengguna: {user_input}
    Konteks Produk dari Dokumen: {context_rag}
    Tugas: Hitung rata-rata harga produk berdasarkan product_id di atas.
    """
    
    res = sql_agent.invoke({"input": enriched_query})
    
    return res.get('output', 'Maaf, saya tidak dapat menemukan data tersebut.')

if __name__ == "__main__":
    # Uji coba lokal
    query = "Berapa rata-rata harga produk kesehatan?"
    print(orchestrator(query))