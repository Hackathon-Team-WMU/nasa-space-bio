import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI
import torch

load_dotenv()

VECTOR_DIR = "vector_store"
# Using local model for embeddings and use device per availability
device = "cuda" if torch.cuda.is_available() else "cpu"
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": device}
)

# Load the existing Chroma vector store
db = Chroma(persist_directory=VECTOR_DIR, embedding_function=embeddings)

client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY")
)

# Import this method into flask (hopefully or thats my idea atleast or alternatively later create a rest endpoint)
def query(question: str):
    # Retrieve top documents
    results = db.similarity_search(question, k=5)

    # Build context for LLM with numbered sources
    context = ""
    for i, r in enumerate(results):
        title = r.metadata.get("title", "Unknown Title")
        url = r.metadata.get("url", "No URL")
        context += f"[Source {i+1}] {title} - {url}\n{r.page_content}\n\n"

    # Query the model
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324-fast",
        max_tokens=3000,
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": "You are an AI research scientist specializing in space biosciences and astrobiology. Your purpose is to assist other scientists in understanding NASA bioscience publications related to human, plant, and microbial experiments conducted in space. Answer strictly using the provided context. Answer strictly exclusively based on the provided context and do not add external information or assume anything. Summarize findings, highlight experimental results, research impacts, and implications for future lunar and Martian exploration. Maintain a concise, factual, and research-focused tone suitable for scientific communication."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}\n\nWhen responding, cite sources inline as [Source 1], [Source 2], etc., corresponding to the listed references."
            }
        ]
    )

    answer = completion.choices[0].message.content

    # Separate structured list of sources for UI display
    sources = []
    for i, r in enumerate(results):
        src = {
            "id": f"Source {i+1}",
            "title": r.metadata.get("title", "Unknown Title"),
            "url": r.metadata.get("url", "No URL")
        }
        sources.append(src)

    return {
        "response": answer,
        "sources": sources
    }
