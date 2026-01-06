import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

# Pastikan Pydantic kompatibel dengan Python 3.13
try:
    from langchain_core.caches import BaseCache
    SQLDatabaseToolkit.model_rebuild(_types_namespace={'BaseCache': BaseCache})
except Exception:
    pass

load_dotenv()

def get_sql_chain():
    """
    Menginisialisasi SQL Agent dengan path database yang dinamis.
    """
    # Navigasi Path: agents/sql_agent.py -> agents -> root (tempat olist.db)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    db_path = os.path.join(base_dir, "olist.db")
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database 'olist.db' tidak ditemukan di: {db_path}")

    # Koneksi Database
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    
    # Konfigurasi LLM (GPT-4o-mini dipilih karena efisiensi biaya dan performa SQL)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    # Toolkit untuk berinteraksi dengan SQL
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    # Agent Executor dengan kemampuan koreksi query otomatis
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="openai-tools",
        handle_parsing_errors=True,
        max_iterations=10 # Memberikan kesempatan agent untuk memperbaiki query yang salah
    )
    
    return agent_executor

if __name__ == "__main__":
    print("--- Memulai Uji Coba SQL Agent ---")
    try:
        sql_agent = get_sql_chain()
        # Test sederhana
        # res = sql_agent.invoke({"input": "Berapa jumlah baris di tabel olist_transactions?"})
        print("✅ SQL Agent Berhasil Dimuat.")
    except Exception as e:
        print(f"❌ SQL Agent Gagal: {e}")