import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI

load_dotenv()

DATA_DIR = "data/fetched_texts"
VECTOR_DIR = "vector_store"

# Load all the text files extracted from the bs4 fetch script
texts = []
for file in os.listdir(DATA_DIR):
    if file.endswith(".txt"):
        with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
            texts.append(f.read())

# Split into smaller chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = splitter.create_documents(texts)

# Create embeddings and store in Chroma
embeddings = OpenAIEmbeddings(
    api_key=os.getenv("NEBIUS_API_KEY"),
    base_url="https://api.studio.nebius.com/v1/"
)

db = Chroma.from_documents(docs, embeddings, persist_directory=VECTOR_DIR)
db.persist()

client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY")
)

def query(question):
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
