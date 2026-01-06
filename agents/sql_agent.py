import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

load_dotenv()

def get_sql_chain():
    # Ambil API Key dari environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Navigasi Path Database
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    db_path = os.path.join(base_dir, "olist.db")
    
    if not os.path.exists(db_path):
        # Fallback untuk Railway (biasanya ada di root /app/olist.db)
        db_path = "/app/olist.db" if os.path.exists("/app/olist.db") else "olist.db"

    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    
    # Inisialisasi LLM dengan API Key eksplisit
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0, 
        openai_api_key=api_key
    )
    
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="openai-tools",
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    return agent_executor