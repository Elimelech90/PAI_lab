import os
import io
import json
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from rag_pipeline import answer

# PDF generation
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

CATEGORIES = [
    "All",
    "Constitutional Law",
    "Criminal Law (PPC)",
    "Criminal Procedure (CrPC)",
    "Property & Tenancy",
    "Family Law",
    "Cyber Crime (PECA 2016)",
    "Labour Law",
    "Consumer Rights",
    "Traffic Law",
    "General Law",
]

SAMPLE_QUESTIONS = [
    "Can police arrest me without a warrant?",
    "How is inheritance divided in Pakistan?",
    "What are my rights as a tenant if my landlord wants to evict me?",
    "What is the punishment for a bounced cheque?",
    "How do I get a divorce (talaq) in Pakistan?",
    "What are my rights if I am fired without notice?",
    "What does PECA 2016 say about online harassment?",
    "What are my constitutional rights if arrested?",
    "How do I file a consumer complaint against a defective product?",
    "What is bail and when can I get it?",
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        categories=CATEGORIES,
        sample_questions=SAMPLE_QUESTIONS,
    )


@app.route("/ask", methods=["POST"])
def ask():
    data     = request.get_json()
    query    = (data.get("query") or "").strip()
    category = data.get("category", "All")

    if not query:
        return jsonify({"error": "Please enter a question."}), 400
    if len(query) < 5:
        return jsonify({"error": "Question too short. Please be more specific."}), 400

    try:
        result = answer(query, category)
        return jsonify(result)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    if not PDF_AVAILABLE:
        return jsonify({"error": "PDF generation not available"}), 500

    data     = request.get_json()
    query    = data.get("query", "")
    answer_text = data.get("answer", "")
    sources  = data.get("sources", [])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    # Header
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(1, 55, 105)
    pdf.cell(0, 12, "Pakistani Law Assistant", ln=True, align="C")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, "Know Your Rights - Free Legal Information", ln=True, align="C")
    pdf.ln(5)

    # Divider
    pdf.set_draw_color(1, 55, 105)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(8)

    # Question
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, "Your Question:", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 7, query)
    pdf.ln(5)

    # Answer
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 8, "Legal Answer:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)

    # Clean markdown bold markers for PDF
    clean_answer = answer_text.replace("**", "").replace("*", "")
    pdf.multi_cell(0, 6, clean_answer)
    pdf.ln(5)

    # Sources
    if sources:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, "Sources Referenced:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(1, 55, 105)
        for src in sources:
            pdf.cell(0, 6, f"  • {src}", ln=True)
        pdf.ln(5)

    # Disclaimer
    pdf.set_draw_color(220, 220, 220)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(150, 150, 150)
    disclaimer = (
        "DISCLAIMER: This document provides general legal information based on Pakistani law and "
        "is not a substitute for professional legal advice. For your specific situation, please "
        "consult a licensed lawyer or legal aid organization."
    )
    pdf.multi_cell(0, 5, disclaimer)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    buf = io.BytesIO(pdf_bytes)
    buf.seek(0)

    return send_file(
        buf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="pakistani_law_answer.pdf",
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Pakistani Law Assistant is running"})


if __name__ == "__main__":
    # Auto-run ingest if index doesn't exist
    if not os.path.exists("vectorstore/faiss.index"):
        print("📚 No index found. Running ingest.py automatically...")
        import subprocess, sys
        subprocess.run([sys.executable, "ingest.py"], check=True)

    print("\n" + "="*50)
    print("⚖️  Pakistani Law Assistant")
    print("   Running at: http://127.0.0.1:5000")
    print("="*50 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
