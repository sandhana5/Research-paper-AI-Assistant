import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from ollama import chat

from utils.pdf_reader import extract_pdf_text
from utils.chunker import split_text
from utils.embedding import create_embeddings
from utils.vector_db import VectorDatabase
from utils.chatbot import ask_question
from utils.metadata import MetadataManager


# =====================================
# Select PDF
# =====================================

def select_pdf():

    root = Tk()
    root.withdraw()

    pdf_path = askopenfilename(
        title="Select Research Paper",
        filetypes=[("PDF Files", "*.pdf")]
    )

    return pdf_path


# =====================================
# Generate Summary using Qwen
# =====================================

def generate_summary(paper_text):

    paper_text = paper_text[:15000]

    prompt = f"""
You are an expert research analyst.

Analyze the following research paper and generate a detailed report.

Return ONLY the following sections:

1. Title
2. Authors
3. Research Domain
4. Problem Statement
5. Objectives
6. Methodology
7. Dataset Used
8. Key Findings
9. Results
10. Strengths
11. Limitations
12. Future Work
13. Research Gaps
14. Three Project Ideas Inspired by this Paper

Research Paper:

{paper_text}
"""

    response = chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# =====================================
# Save Summary
# =====================================

def save_summary(summary):

    os.makedirs("outputs", exist_ok=True)

    output_file = "outputs/research_summary.txt"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(summary)

    return output_file


# =====================================
# Main Program
# =====================================

def main():

    print("=" * 60)
    print("      RESEARCH PAPER AI ASSISTANT")
    print("=" * 60)

    pdf_path = select_pdf()

    if not pdf_path:
        print("\nNo PDF selected.")
        return

    metadata = MetadataManager()

    print(f"\nSelected File:\n{pdf_path}")

    # ---------------------------------
    # Existing PDF
    # ---------------------------------

    if metadata.already_indexed(pdf_path):

        print("\nPDF already indexed.")

        db = VectorDatabase()

        # Load text again for summary generation
        paper_text = extract_pdf_text(pdf_path)

    # ---------------------------------
    # New PDF
    # ---------------------------------

    else:

        print("\nNew PDF detected.")

        print("\nExtracting text...")

        paper_text = extract_pdf_text(pdf_path)

        print(f"\nExtracted {len(paper_text)} characters.")

        print("\nSplitting into chunks...")

        chunks = split_text(paper_text)

        print(f"Created {len(chunks)} chunks.")

        print("\nCreating embeddings...")

        embeddings = create_embeddings(chunks)

        print(f"Created {len(embeddings)} embeddings.")

        db = VectorDatabase()

        filename = os.path.basename(pdf_path)

        print("\nSaving embeddings into ChromaDB...")

        db.store_embeddings(

            chunks,

            embeddings,

            filename

        )

        metadata.add_file(pdf_path)

        print("\nDocument indexed successfully.")

    print("\nResearch Paper Ready!")

    print("\nYou can now ask questions.")

    # =====================================
    # Chat Loop
    # =====================================

    while True:

        print("\n" + "-" * 60)

        question = input("\nAsk a question (type 'summary' or 'exit'): ")

        if question.lower() == "exit":

            print("\nGoodbye!")

            break

        elif question.lower() == "summary":

            print("\nGenerating Summary...\n")

            summary = generate_summary(paper_text)

            print(summary)

            output = save_summary(summary)

            print(f"\nSummary saved to:\n{output}")

        else:

            print("\nSearching ChromaDB...")

            answer = ask_question(db, question)

            print("\nAnswer:\n")

            print(answer)


# =====================================
# Run
# =====================================

if __name__ == "__main__":

    main()