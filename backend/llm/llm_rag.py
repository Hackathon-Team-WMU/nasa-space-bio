#!/usr/bin/env python3
"""
NASA BioExplorer - RAG (Retrieval-Augmented Generation) Pipeline

AI Usage Disclosure (NASA Space Apps Challenge 2025):
- This RAG pipeline was developed with assistance from ChatGPT AI code assistant
- All AI-generated code was reviewed, tested, and modified by human developers
- Algorithm design and implementation validated by the development team
- See AI_DISCLOSURE.md for complete details
"""

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
def query(question: str, role: str):
    results = db.similarity_search(question, k=5)

    # Build context for LLM with numbered sources
    context = ""
    for i, r in enumerate(results):
        title = r.metadata.get("title", "Unknown Title")
        url = r.metadata.get("url", "No URL")
        context += f"[Source {i+1}] {title} - {url}\n{r.page_content}\n\n"

    #role based system prompts
    role_prompts = {
        "manager":("You are an investor evaluating NASA's space bioscience research portfolio. Summarize the key findings from human, plant, and microbial experiments conducted in space, highlighting breakthroughs that have influenced mission planning, technology development, and potential commercial opportunities. Focus on high-level insights that show how research progress reduces risks, improves efficiency, or creates opportunities for innovation in Moon and Mars exploration. Your summary should be concise, actionable, and easy for decision-makers to understand, strictly using the provided context without adding external information."),

        "architect":("You are a NASA mission architect responsible for planning safe and efficient human exploration of the Moon and Mars. Summarize the key findings from human, plant, and microbial experiments conducted in space, emphasizing results that impact mission design, spacecraft systems, astronaut health, habitat planning, and operational efficiency. Highlight insights that inform risk reduction, technology development, and optimization of long-duration missions. Provide a concise, research-focused summary strictly based on the provided context, without adding external information or assumptions."),

        "scientist":("You are an AI research scientist specializing in space biosciences and astrobiology. Your purpose is to assist other scientists in understanding NASA bioscience publications related to human, plant, and microbial experiments conducted in space. Answer strictly using the provided context. Answer strictly exclusively based on the provided context and do not add external information or assume anything. Summarize findings, highlight experimental results, research impacts, and implications for future lunar and Martian exploration. Maintain a concise, factual, and research-focused tone suitable for scientific communication."),

        "student":("You are an AI tutor helping students understand NASA's space bioscience research. Summarize the key findings from human, plant, and microbial experiments conducted in space in a way that is comprehensive and easy to understand for learners. Use important keywords from the context to explain scientific concepts clearly. Highlight the purpose of the research, major breakthroughs, and how these experiments help humans explore the Moon and Mars safely and efficiently. Provide explanations that are structured, educational, and engaging, strictly using the provided context without adding external information or assumptions.") }


    # selects system prompt based on role, scientist is default role
    system_prompt = role_prompts.get(role, role_prompts["scientist"])

    # Query the model
    completion = client.chat.completions.create(
        model="nvidia/Llama-3_1-Nemotron-Ultra-253B-v1",
        max_tokens=10000,
        temperature=0.2,
        top_p=0.9,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\n\nWhen responding, cite sources inline as [Source 1], [Source 2], etc., corresponding to the listed references."}
        ]
    )

    answer = completion.choices[0].message.content

    # Separate structured list of sources for UI display and Deduplicate sources by URL
    unique_sources = {}
    for i, r in enumerate(results):
        url = r.metadata.get("url", "No URL")
        if url not in unique_sources:
            unique_sources[url] = {
                "id": f"Source {len(unique_sources)+1}",
                "title": r.metadata.get("title", "Unknown Title"),
                "url": url
            }
    sources = list(unique_sources.values())

    return {"response": answer, "sources": sources}
