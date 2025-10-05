import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import torch

load_dotenv()

DATA_DIR = "data/fetched_texts"
VECTOR_DIR = "vector_store"

def build_vector_store():
    # Using local model for embeddings and use device per availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs={"device": device})

    texts = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
                texts.append(f.read())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.create_documents(texts)

    db = Chroma.from_documents(docs, embeddings, persist_directory=VECTOR_DIR)
    db.persist()
    print(f"Vector db built and saved at '{VECTOR_DIR}'!")

if __name__ == "__main__":
    build_vector_store()
