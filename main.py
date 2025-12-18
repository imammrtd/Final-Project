import os
import sqlite3
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = FastAPI(title="Olist AI Assistant API")

# --- Logika SQL Agent ---
class SQLAgent:
    def __init__(self, db_path):
        self.db_path = db_path
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan di environment variables")
        
        genai.configure(api_key=api_key)
        # Menggunakan model stabil yang tersedia di akun Anda
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def _get_schema(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        schema = "\n".join([f"Table: {row[0]}\nSQL: {row[1]}" for row in cursor.fetchall()])
        conn.close()
        return schema

    def handle_query(self, user_query):
        schema = self._get_schema()
        prompt = f"""
        Anda adalah SQL expert. Berdasarkan schema berikut:
        {schema}
        
        Jawab pertanyaan user: "{user_query}"
        Berikan jawaban dalam format JSON:
        {{
            "sql": "QUERY_SQL_DISINI",
            "explanation": "Penjelasan singkat dalam Bahasa Indonesia"
        }}
        Hanya berikan JSON, tanpa markdown.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Membersihkan response jika ada karakter markdown
            clean_json = response.text.replace('```json', '').replace('```', '').strip()
            import json
            data = json.loads(clean_json)
            
            # Eksekusi SQL
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(data['sql'], conn)
            conn.close()
            
            return {
                "input": user_query,
                "sql_query": data['sql'],
                "explanation": data['explanation'],
                "data": df.to_dict(orient='records')
            }
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")

# Inisialisasi Agent
agent = SQLAgent("olist.db")

# --- Routes FastAPI ---

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to Olist AI REST API"}

@app.get("/ask")
def ask_ai(query: str = Query(..., example="Berapa total transaksi?")):
    try:
        result = agent.handle_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))