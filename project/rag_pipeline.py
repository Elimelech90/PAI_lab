"""
rag_pipeline.py — Core RAG logic: embed query → search FAISS → call Groq LLM
"""

import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

INDEX_FILE  = "vectorstore/faiss.index"
CHUNKS_FILE = "vectorstore/chunks.pkl"
MODEL_NAME  = "all-MiniLM-L6-v2"
TOP_K       = 4   # how many law chunks to retrieve

_embedder = None
_index    = None
_chunks   = None
_groq     = None

def _load_resources():
    global _embedder, _index, _chunks, _groq

    if _embedder is None:
        print("Loading embedding model...")
        _embedder = SentenceTransformer(MODEL_NAME)

    if _index is None:
        if not os.path.exists(INDEX_FILE):
            raise FileNotFoundError(
                "FAISS index not found. Please run: python ingest.py"
            )
        _index = faiss.read_index(INDEX_FILE)
        with open(CHUNKS_FILE, "rb") as f:
            _chunks = pickle.load(f)

    if _groq is None:
        api_key = os.getenv("GROQ_API_KEY", "")
        _groq = Groq(api_key=api_key)


def retrieve(query: str, category_filter: str = "All") -> list[dict]:
    """Embed query, search FAISS, return top-K relevant chunks."""
    _load_resources()

    q_emb = _embedder.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = _index.search(q_emb, TOP_K * 3)  # fetch extra for filter

    results = []
    for idx in indices[0]:
        if idx < 0 or idx >= len(_chunks):
            continue
        chunk = _chunks[idx]
        if category_filter != "All" and chunk["category"] != category_filter:
            continue
        results.append(chunk)
        if len(results) == TOP_K:
            break

    return results


SYSTEM_PROMPT = """You are a Pakistani legal assistant AI. Your job is to help Pakistani citizens understand their legal rights.

Rules:
1. ONLY answer based on the provided law context below.
2. Always cite the exact law name and section number.
3. Give a clear, plain-English explanation anyone can understand.
4. Structure your answer as:
   - **Legal Answer**: Direct answer to the question
   - **Relevant Law**: Law name + section cited
   - **What This Means For You**: Plain English explanation
   - **Recommended Next Step**: Practical advice
5. If the context does not contain enough information, say: "I don't have enough information in my database for this specific question. Please consult a licensed lawyer."
6. Never give personal legal advice. Always end with the standard disclaimer.
7. Keep tone professional but warm and accessible.
8. If the question is in Roman Urdu, answer in English with key Urdu terms where helpful.
"""

def answer(query: str, category_filter: str = "All") -> dict:
    """
    Full RAG pipeline:
    1. Retrieve relevant law chunks
    2. Build prompt with context
    3. Call Groq LLM
    4. Return structured response
    """
    _load_resources()

    chunks = retrieve(query, category_filter)

    if not chunks:
        return {
            "answer":   "I couldn't find relevant information for your question in my database. Please consult a licensed lawyer.",
            "sources":  [],
            "category": category_filter,
            "query":    query,
        }

    # Build context block
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Source {i}: {chunk['source']} — {chunk['category']}]\n{chunk['text']}"
        )
    context = "\n\n".join(context_parts)

    user_message = f"""LEGAL QUESTION: {query}

RELEVANT LAW CONTEXT:
{context}

Please answer the question using only the context above."""

    api_key = os.getenv("GROQ_API_KEY", "")
    
    if not api_key or api_key == "your_groq_api_key_here":
        # Fallback: return raw retrieved context formatted nicely
        raw_answer = _format_fallback(query, chunks)
        sources = list({c["source"] for c in chunks})
        return {
            "answer":   raw_answer,
            "sources":  sources,
            "category": chunks[0]["category"] if chunks else "General",
            "query":    query,
            "fallback": True,
        }

    try:
        response = _groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            temperature=0.2,
            max_tokens=1024,
        )
        ai_answer = response.choices[0].message.content
    except Exception as e:
        ai_answer = _format_fallback(query, chunks)

    sources = list({c["source"] for c in chunks})

    return {
        "answer":   ai_answer,
        "sources":  sources,
        "category": chunks[0]["category"] if chunks else "General",
        "query":    query,
    }


def _format_fallback(query: str, chunks: list[dict]) -> str:
    """Format raw chunks nicely when no API key is present."""
    lines = [f"**Relevant Legal Information for your question:**\n"]
    for chunk in chunks:
        lines.append(f"📘 **{chunk['source']}** [{chunk['category']}]\n{chunk['text']}\n")
    lines.append("\n*Note: Add your GROQ_API_KEY in .env for AI-generated explanations.*")
    return "\n".join(lines)
