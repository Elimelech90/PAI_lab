"""
ingest.py — Load Pakistani law PDFs, chunk them, embed, save to FAISS index.
Run this ONCE before starting the app: python ingest.py
"""

import os
import pickle
import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
PDF_DIR       = "data/laws"
INDEX_DIR     = "vectorstore"
INDEX_FILE    = os.path.join(INDEX_DIR, "faiss.index")
CHUNKS_FILE   = os.path.join(INDEX_DIR, "chunks.pkl")
MODEL_NAME    = "all-MiniLM-L6-v2"   # Free, fast, good quality
CHUNK_SIZE    = 500                   # characters per chunk
CHUNK_OVERLAP = 100                   # overlap between chunks

# ── Category mapping by filename keyword ────────────────────────────────────
CATEGORY_MAP = {
    "constitution": "Constitutional Law",
    "ppc":          "Criminal Law (PPC)",
    "crpc":         "Criminal Procedure (CrPC)",
    "property":     "Property & Tenancy",
    "rent":         "Property & Tenancy",
    "peca":         "Cyber Crime (PECA 2016)",
    "cyber":        "Cyber Crime (PECA 2016)",
    "labor":        "Labour Law",
    "industrial":   "Labour Law",
    "family":       "Family Law",
    "muslim":       "Family Law",
    "consumer":     "Consumer Rights",
    "traffic":      "Traffic Law",
}

def get_category(filename: str) -> str:
    fname = filename.lower()
    for keyword, category in CATEGORY_MAP.items():
        if keyword in fname:
            return category
    return "General Law"

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def chunk_text(text: str, source: str, category: str) -> list[dict]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if len(chunk) > 50:  # skip tiny fragments
            chunks.append({
                "text":     chunk,
                "source":   source,
                "category": category,
            })
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def build_index():
    os.makedirs(INDEX_DIR, exist_ok=True)
    pdf_files = list(Path(PDF_DIR).glob("*.pdf"))

    if not pdf_files:
        print(f"⚠️  No PDFs found in '{PDF_DIR}/'")
        print("    Add Pakistani law PDFs there and run ingest.py again.")
        print("    Creating a DEMO index with sample text so the app still works.\n")
        _build_demo_index()
        return

    print(f"📄 Found {len(pdf_files)} PDF(s). Processing...")
    model = SentenceTransformer(MODEL_NAME)

    all_chunks = []
    for pdf_path in pdf_files:
        name     = pdf_path.name
        category = get_category(name)
        print(f"  → {name}  [{category}]")
        text   = extract_text_from_pdf(str(pdf_path))
        chunks = chunk_text(text, name, category)
        all_chunks.extend(chunks)
        print(f"     {len(chunks)} chunks extracted")

    print(f"\n🧠 Embedding {len(all_chunks)} chunks with '{MODEL_NAME}'...")
    texts      = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)
    embeddings = np.array(embeddings, dtype="float32")

    dim   = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"\n✅ Index saved → {INDEX_FILE}")
    print(f"✅ Chunks saved → {CHUNKS_FILE}")
    print(f"✅ Total chunks indexed: {len(all_chunks)}\n")

def _build_demo_index():
    """
    Builds a small demo FAISS index from hardcoded Pakistani law facts.
    This lets the app run immediately even without PDF files.
    """
    demo_chunks = [
        {"text": "Section 54 of the Code of Criminal Procedure (CrPC) 1898: A police officer may arrest without a warrant any person who has been concerned in any cognizable offence, or against whom a reasonable complaint has been made, or credible information has been received, or a reasonable suspicion exists of his having been so concerned.", "source": "CrPC 1898", "category": "Criminal Procedure (CrPC)"},
        {"text": "Article 10 of the Constitution of Pakistan 1973 — Safeguards as to arrest and detention: No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest, nor shall he be denied the right to consult and be defended by a legal practitioner of his choice. Every person who is arrested and detained in custody shall be produced before a magistrate within a period of twenty-four hours of such arrest.", "source": "Constitution of Pakistan 1973", "category": "Constitutional Law"},
        {"text": "Section 299 of the Pakistan Penal Code defines Qatl (homicide). Section 300 defines Qatl-i-Amd (intentional murder). The punishment for Qatl-i-Amd under Section 302 PPC includes death penalty, imprisonment for life, or fine as qisas or tazir.", "source": "Pakistan Penal Code", "category": "Criminal Law (PPC)"},
        {"text": "Muslim Family Laws Ordinance 1961 Section 7: Talaq — Any man who wishes to divorce his wife shall, as soon as may be after the pronouncement of talaq in any form whatsoever, give the Chairman notice in writing of his having done so, and shall supply a copy thereof to the wife. Talaq shall not be effective until the expiration of ninety days from the day on which notice is delivered to the Chairman.", "source": "Muslim Family Laws Ordinance 1961", "category": "Family Law"},
        {"text": "Section 8 of the Muslim Family Laws Ordinance 1961 on Dissolution of Marriage: A woman seeking khula (dissolution of marriage at her request) may approach the Union Council. The Union Council shall constitute an Arbitration Council to take all steps necessary to bring about a reconciliation between the parties.", "source": "Muslim Family Laws Ordinance 1961", "category": "Family Law"},
        {"text": "Transfer of Property Act 1882 Section 106: In the absence of a contract or local usage to the contrary, a lease of immovable property for agricultural or manufacturing purposes shall be deemed to be a lease from year to year, terminable, on the part of either lessor or lessee, by six months' notice expiring with the end of a year of the tenancy. A lease of immovable property for any other purpose shall be deemed to be a lease from month to month, terminable by fifteen days' notice.", "source": "Transfer of Property Act 1882", "category": "Property & Tenancy"},
        {"text": "PECA 2016 (Prevention of Electronic Crimes Act) Section 20 — Offences against dignity of natural person: Whoever intentionally and publicly exhibits or displays or transmits any information through any information system, which he knows to be false, and intimidates or harms the reputation or privacy of a natural person, shall be punished with imprisonment for a term which may extend to three years or with fine which may extend to one million rupees, or with both.", "source": "PECA 2016", "category": "Cyber Crime (PECA 2016)"},
        {"text": "PECA 2016 Section 21 — Offences against modesty of a natural person and minor: Whoever intentionally and publicly exhibits or displays or transmits any information which superimposes a photograph of the face of a natural person over any sexually explicit image, shall be punished with imprisonment for a term which may extend to five years or with fine up to five million rupees, or with both.", "source": "PECA 2016", "category": "Cyber Crime (PECA 2016)"},
        {"text": "The Industrial and Commercial Employment (Standing Orders) Ordinance 1968 requires employers to give one month's notice or pay in lieu of notice before terminating a permanent worker. A worker terminated without cause is entitled to gratuity at the rate of thirty days wages for each year of service completed.", "source": "Industrial Employment Ordinance 1968", "category": "Labour Law"},
        {"text": "The Punjab Rented Premises Act 2009: A landlord cannot evict a tenant without obtaining an eviction order from the Rent Controller. Grounds for eviction include non-payment of rent for more than two months, subletting without permission, or use of premises for purposes other than agreed. The tenant must be given proper notice before eviction proceedings begin.", "source": "Punjab Rented Premises Act 2009", "category": "Property & Tenancy"},
        {"text": "Article 25 of the Constitution of Pakistan 1973: All citizens are equal before law and are entitled to equal protection of law. There shall be no discrimination on the basis of sex. Nothing in this Article shall prevent the State from making any special provision for the protection of women and children.", "source": "Constitution of Pakistan 1973", "category": "Constitutional Law"},
        {"text": "Section 489-F of the Pakistan Penal Code — Punishment for dishonoured cheque: Whoever dishonestly issues a cheque towards repayment of a loan or fulfillment of an obligation which is dishonoured on presentation shall be punishable with imprisonment which may extend to three years, or with fine, or with both.", "source": "Pakistan Penal Code", "category": "Criminal Law (PPC)"},
        {"text": "The Consumer Protection Act Punjab 2005: A consumer has the right to seek compensation for goods or services that are defective, substandard, or not as described. Complaints can be filed with the Consumer Court. The seller is liable to replace the product, refund the price, or pay compensation for any injury caused by the defective product.", "source": "Consumer Protection Act Punjab 2005", "category": "Consumer Rights"},
        {"text": "Section 406 of the Pakistan Penal Code — Punishment for criminal breach of trust: Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both. This applies to situations where someone misappropriates money or property entrusted to them.", "source": "Pakistan Penal Code", "category": "Criminal Law (PPC)"},
        {"text": "Article 9 of the Constitution of Pakistan 1973: Security of person — No person shall be deprived of life or liberty save in accordance with law. Article 14: Inviolability of dignity of man — The dignity of man and, subject to law, the privacy of home, shall be inviolable. No person shall be subjected to torture for the purpose of extracting evidence.", "source": "Constitution of Pakistan 1973", "category": "Constitutional Law"},
        {"text": "Succession under Muslim Personal Law in Pakistan: Sons receive double the share of daughters. A widow receives 1/8 of the estate if there are children, and 1/4 if there are no children. A widower receives 1/4 if there are children and 1/2 if there are none. Parents each receive 1/6 if the deceased has children.", "source": "Muslim Personal Law (Shariat) Application Act 1962", "category": "Family Law"},
        {"text": "Section 376 Pakistan Penal Code — Punishment for rape: Whoever commits rape shall be punished with death or imprisonment of either description for a term which shall not be less than ten years or more than twenty-five years and shall also be liable to fine. When rape is committed by two or more persons, each person shall be punished with death or imprisonment for life.", "source": "Pakistan Penal Code", "category": "Criminal Law (PPC)"},
        {"text": "The Motor Vehicles Ordinance 1965: Driving without a valid license is a punishable offence. A license holder must carry their license while driving. Driving under the influence of alcohol or drugs is a serious offence. In case of an accident causing injury or death, the driver must stop, assist the injured, and report to the nearest police station.", "source": "Motor Vehicles Ordinance 1965", "category": "Traffic Law"},
        {"text": "Section 124-A Pakistan Penal Code — Sedition: Whoever by words, either spoken or written, or by signs, or by visible representation, or otherwise, excites or attempts to excite disaffection towards the Government established by law in Pakistan shall be punished with imprisonment for life, to which fine may be added, or with imprisonment which may extend to three years.", "source": "Pakistan Penal Code", "category": "Criminal Law (PPC)"},
        {"text": "Bail rights in Pakistan under CrPC: Every accused person has the right to apply for bail. In bailable offences, bail is a right. In non-bailable offences, bail is discretionary and granted by a Sessions Court or High Court. Factors considered include the severity of the offence, risk of fleeing, and criminal history. Bail can be cancelled if conditions are violated.", "source": "Code of Criminal Procedure 1898", "category": "Criminal Procedure (CrPC)"},
    ]

    print(f"🔧 Building demo index with {len(demo_chunks)} built-in law facts...")
    model      = SentenceTransformer(MODEL_NAME)
    texts      = [c["text"] for c in demo_chunks]
    embeddings = model.encode(texts, show_progress_bar=False)
    embeddings = np.array(embeddings, dtype="float32")

    dim   = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(demo_chunks, f)

    print(f"✅ Demo index ready — app will work immediately!")
    print(f"   Add real PDFs to '{PDF_DIR}/' and re-run to upgrade.\n")

if __name__ == "__main__":
    build_index()
