from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.orchestrator import orchestrator
import uvicorn
import os

app = FastAPI(title="Olist Multi-Agent API")

class QueryRequest(BaseModel):
    prompt: str

@app.get("/")
def health_check():
    return {"status": "online", "message": "Olist Multi-Agent API is running"}

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        # Menjalankan logika orchestrator yang memanggil SQL & RAG
        result = orchestrator(request.prompt)
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # HF akan memberikan port 7860 secara otomatis
    port = int(os.environ.get("PORT", 7860)) 
    uvicorn.run(app, host="0.0.0.0", port=port)