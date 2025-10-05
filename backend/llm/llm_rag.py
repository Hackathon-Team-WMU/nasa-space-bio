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
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs={"device": device})

# Load the existing Chroma vector store
db = Chroma(persist_directory=VECTOR_DIR, embedding_function=embeddings)

client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY")
)

# Import this method into flask (hopefully or thats my idea atleast or alternatively later create a rest endpoint)
def query(question: str):
    results = db.similarity_search(question, k=5)
    context = "\n\n".join(r.page_content for r in results)

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324-fast",
        max_tokens=512,
        temperature=0.3,
        messages=[
            {"role": "system", "content": "Answer only using the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )

    return completion.choices[0].message.content
