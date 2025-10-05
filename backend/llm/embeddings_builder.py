import os
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import torch

DATA_DIR = "data/fetched_texts"
CSV_PATH = "data/SB_publication_PMC.csv"
VECTOR_DIR = "vector_store"

def build_vector_store():
    # Using local model for embeddings and use device per availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", model_kwargs={"device": device})

    # Load CSV and attach filenames (1.txt, 2.txt, etc.) in order as they correspond to each of the lines in the SB_Publications CSV file
    df = pd.read_csv(CSV_PATH)
    df["filename"] = [f"{i+1}.txt" for i in range(len(df))]

    texts = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
                texts.append(f.read())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = []

    # Iterate through CSV rows and match each row to its text file so that we don't get metadata mismatches
    for _, row in df.iterrows():
        file_path = os.path.join(DATA_DIR, str(row["filename"]))
        if not os.path.exists(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = splitter.split_text(text)

        for chunk in chunks:
            docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "title": str(row.get("Title", "Unknown Title")),
                        "url": str(row.get("Link", "No URL")),  # Corrected here
                        "filename": str(row["filename"])
                    }
                )
            )

    db = Chroma.from_documents(docs, embeddings, persist_directory=VECTOR_DIR)
    db.persist()
    print(f"Vector db built and saved at '{VECTOR_DIR}'!")

if __name__ == "__main__":
    build_vector_store()
