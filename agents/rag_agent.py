import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def get_rag_chain():
    """
    Membangun RAG Chain menggunakan LCEL untuk stabilitas maksimal.
    """
    # 1. Koneksi ke Qdrant Cloud/Local
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    # 2. Inisialisasi Vector Store dengan Embedding OpenAI
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="olist_data",
        embedding=embeddings
    )
    
    # 3. Konfigurasi Retriever (Mencari 3 dokumen terdekat)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 4. LLM untuk Generator
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # 5. Struktur Prompt yang Lebih Ketat
    template = """
    Anda adalah Asisten Pakar Olist. Tugas Anda adalah menjawab pertanyaan berdasarkan konteks dokumen yang diberikan.
    
    KONTEKS:
    {context}
    
    PERTANYAAN: 
    {input}
    
    INSTRUKSI:
    1. Jika jawaban tidak ada dalam konteks, katakan bahwa Anda tidak tahu.
    2. Jawablah dengan bahasa yang profesional dan sopan.
    3. Jika konteks menyebutkan ID produk, sertakan dalam jawaban.
    
    JAWABAN:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    # Fungsi pembantu untuk membersihkan dokumen
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # 6. LCEL Pipeline (Ini adalah 'jantung' dari LangChain Modern)
    # Ini menggantikan 'RetrievalQA.from_chain_type' yang sudah usang/sering error.
    rag_chain = (
        {
            "context": retriever | format_docs, 
            "input": RunnablePassthrough()
        }
        | prompt 
        | llm 
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    print("--- Memulai Uji Coba RAG Agent ---")
    try:
        rag_agent = get_rag_chain()
        print("✅ RAG Agent Berhasil Dimuat.")
    except Exception as e:
        print(f"❌ RAG Agent Gagal: {e}")