import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Solusi ModuleNotFoundError: Tambahkan path folder utama
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

try:
    from agents.sql_agent import get_sql_chain
    from agents.rag_agent import get_rag_chain
except ModuleNotFoundError:
    from sql_agent import get_sql_chain
    from rag_agent import get_rag_chain

load_dotenv()

def orchestrator(user_input: str):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY tidak ditemukan di Secrets/Variables."

    # Memuat chain secara fresh
    sql_agent = get_sql_chain()
    rag_chain = get_rag_chain()

    print(f"\n[ORCHESTRATOR] Menganalisis: {user_input}")
    
    # 1. RAG untuk mencari konteks ID Produk
    context_rag = rag_chain.invoke(f"Cari product_id terkait: {user_input}")
    
    # 2. SQL Agent untuk eksekusi query data
    enriched_query = f"Pertanyaan: {user_input}. Konteks: {context_rag}. Hitung rata-rata harga."
    res = sql_agent.invoke({"input": enriched_query})
    
    return res.get('output', 'Maaf, gagal mendapatkan data.')

if __name__ == "__main__":
    print(orchestrator("Berapa rata-rata harga produk kesehatan?"))