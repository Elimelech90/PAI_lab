# ⚖️ Pakistani Law Assistant
### A Free RAG-Based Legal Q&A System for Pakistani Citizens

---

## 🚀 Quick Start (5 Minutes)

### Step 1 — Get a Free Groq API Key
1. Go to **https://console.groq.com**
2. Sign up for free (no credit card needed)
3. Go to API Keys → Create API Key
4. Copy your key

### Step 2 — Setup the Project
```bash
# Clone / download this folder, then:
cd pakistani-law-assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Step 3 — Add Your API Key
```bash
# Copy the example env file
copy .env.example .env       # Windows
# cp .env.example .env       # Mac/Linux

# Open .env and replace:
GROQ_API_KEY=paste_your_key_here
```

### Step 4 — Run!
```bash
python app.py
```
Open **http://localhost:5000** in your browser. Done! 🎉

---

## 📄 Adding Real Law PDFs (Optional but Recommended)

The app works immediately with 20 built-in law facts (demo mode).
To upgrade with real Pakistani law documents:

1. Download free PDFs from:
   - **pakistancode.gov.pk** — PPC, CrPC, Transfer of Property Act
   - **na.gov.pk** — Constitution of Pakistan 1973
   - **moitt.gov.pk** — PECA 2016
   - **ilo.org** — Pakistani Labour Laws
   - Punjab Government website — Punjab Rented Premises Act

2. Place PDFs in the `data/laws/` folder

3. Name them clearly (the system reads the filename):
   ```
   data/laws/
   ├── constitution_1973.pdf
   ├── ppc.pdf
   ├── crpc_1898.pdf
   ├── peca_2016.pdf
   ├── property_act.pdf
   ├── muslim_family_laws.pdf
   ├── labor_ordinance.pdf
   └── consumer_protection.pdf
   ```

4. Run ingestion:
   ```bash
   python ingest.py
   ```

5. Restart the app:
   ```bash
   python app.py
   ```

---

## 🏗️ Project Structure

```
pakistani-law-assistant/
├── app.py              ← Flask server (run this)
├── rag_pipeline.py     ← RAG: embed → search → answer
├── ingest.py           ← Load PDFs → FAISS index
├── requirements.txt    ← All dependencies
├── .env                ← Your API keys (create this)
├── .env.example        ← Template for .env
│
├── data/
│   └── laws/           ← Put Pakistani law PDFs here
│
├── vectorstore/        ← Auto-created by ingest.py
│   ├── faiss.index     ← Vector search index
│   └── chunks.pkl      ← Law text chunks
│
└── templates/
    └── index.html      ← Full web UI
```

---

## 💡 Features

- ✅ Ask legal questions in English or Roman Urdu
- ✅ Answers cite exact law name + section number
- ✅ Filter by legal category (Criminal, Family, Cyber, etc.)
- ✅ Download answer as PDF
- ✅ Copy answer to clipboard
- ✅ 10 sample questions to get started
- ✅ Works with or without real law PDFs
- ✅ 100% free to run

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | Flask |
| LLM | Groq API — llama3-70b (free tier) |
| Embeddings | sentence-transformers (runs locally) |
| Vector Search | FAISS (Facebook, free) |
| PDF Reading | PyMuPDF |
| PDF Export | fpdf2 |

**Monthly Cost: Rs. 0/-**

---

## 📚 Legal Categories Covered

- 🏛️ Constitutional Law (Article 9, 10, 14, 25...)
- 🚔 Criminal Law — PPC (murder, theft, fraud, cheque bounce...)
- 👮 Criminal Procedure — CrPC (arrest, bail, FIR...)
- 🏠 Property & Tenancy (eviction, rent, landlord rights...)
- 👨‍👩‍👧 Family Law (divorce, talaq, khula, inheritance, custody...)
- 💻 Cyber Crime — PECA 2016 (harassment, deepfakes, hacking...)
- 💼 Labour Law (firing, notice period, gratuity...)
- 🛒 Consumer Rights (refunds, defective products...)
- 🚗 Traffic Law (license, accidents, challans...)

---

## ⚠️ Disclaimer

This tool provides general legal information based on Pakistani law documents.
It is not a substitute for professional legal advice.
For your specific situation, always consult a licensed lawyer.

---

*Built for Programming for AI — 4th Semester Project*
