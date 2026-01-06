import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# Import fungsi dari file agent lokal
from sql_agent import get_sql_chain
from rag_agent import get_rag_chain

load_dotenv()

# Inisialisasi Agent
sql_agent = get_sql_chain()
rag_chain = get_rag_chain()

def call_sql(query: str):
    return sql_agent.invoke({"input": query})

def call_rag(query: str):
    return rag_chain.invoke(query)

def orchestrator(user_input: str):
    print(f"\n[ORCHESTRATOR] Menganalisis: {user_input}")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # 1. Cek dulu ke RAG: Apakah ada info kategori/produk terkait?
    print("-> Mencari referensi kategori di RAG...")
    context_rag = call_rag(f"Sebutkan beberapa product_id yang termasuk dalam kategori: {user_input}")
    
    # 2. Kirim instruksi super spesifik ke SQL Agent
    print("-> Menginstruksikan SQL Agent dengan data dari RAG...")
    
    # Kita menggabungkan hasil RAG ke dalam prompt untuk SQL
    enriched_query = f"""
    Pertanyaan Pengguna: {user_input}
    
    Konteks Tambahan dari Dokumen:
    {context_rag}
    
    Tugas Anda:
    1. Cari tabel yang memiliki kolom 'price' (kemungkinan olist_transactions).
    2. Gunakan 'product_id' yang disebutkan dalam konteks di atas untuk melakukan filter.
    3. Jika tidak ada kolom kategori, gunakan filter: WHERE product_id IN ('ID1', 'ID2', ...) berdasarkan konteks.
    4. Hitung rata-rata harganya.
    """
    
    res = call_sql(enriched_query)
    output = res.get('output', '')
    
    # 3. Final Check jika SQL masih bebal
    if "don't know" in output.lower() or "tidak menemukan" in output.lower():
        print("-> SQL Agent masih gagal. Memberikan jawaban berbasis RAG saja.")
        return f"Database SQL tidak memiliki kolom kategori, namun berdasarkan dokumen RAG: {context_rag}"
    
    return output

if __name__ == "__main__":
    print("--- Multi-Agent Olist System: Mode Agresif ---")
    query = "Berapa rata-rata harga produk di kategori kesehatan?"
    try:
        response = orchestrator(query)
        print(f"\n--------------------------------------------------")
        print(f"HASIL AKHIR:\n{response}")
        print(f"--------------------------------------------------")
    except Exception as e:
        print(f"❌ Error: {e}")