import os
import tempfile
import streamlit as st

from utils.pdf_reader import extract_pdf_text
from utils.chunker import split_text
from utils.embedding import create_embeddings
from utils.vector_db import VectorDatabase
from utils.metadata import MetadataManager


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Research Paper AI Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# SAFE CSS LOADER
# =========================
def load_css():
    try:
        with open("style.css", "r", encoding="utf-8") as css:
            st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
    except:
        pass

load_css()


# =========================
# SESSION STATE
# =========================
if "paper_loaded" not in st.session_state:
    st.session_state.paper_loaded = False
if "paper_text" not in st.session_state:
    st.session_state.paper_text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "db" not in st.session_state:
    st.session_state.db = None
if "chunks" not in st.session_state:
    st.session_state.chunks = 0
if "characters" not in st.session_state:
    st.session_state.characters = 0
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# HEADER
# =========================
st.title("Research Paper AI Assistant")

st.divider()


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## System Info")
    st.write("Model: Qwen 3 (Ollama)")
    st.write("Embeddings: Sentence Transformers")
    st.write("Vector DB: ChromaDB")

    st.divider()

    if st.session_state.paper_loaded:
        st.success("Document Loaded")
    else:
        st.warning("No Document Loaded")


# =========================
# UPLOAD PDF
# =========================
uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"])

if uploaded_file:

    metadata = MetadataManager()
    db = st.session_state.db or VectorDatabase()

    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    # Extract text
    with st.spinner("Reading PDF..."):
        paper_text = extract_pdf_text(pdf_path)

    st.session_state.paper_text = paper_text

    # Process only if not indexed
    if not metadata.already_indexed(pdf_path):

        with st.spinner("Splitting text..."):
            chunks = split_text(paper_text)

        with st.spinner("Creating embeddings..."):
            embeddings = create_embeddings(chunks)

        with st.spinner("Storing in vector DB..."):
            db.store_embeddings(chunks, embeddings, uploaded_file.name)

        metadata.add_file(pdf_path)

    st.session_state.paper_loaded = True
    st.session_state.db = db
    st.session_state.characters = len(paper_text)
    st.session_state.chunks = len(split_text(paper_text))

    st.success("PDF processed successfully!")


# =========================
# STATS
# =========================
st.subheader("Paper Stats")

c1, c2, c3 = st.columns(3)

c1.metric("Characters", st.session_state.characters)
c2.metric("Chunks", st.session_state.chunks)
c3.metric("Status", "Ready" if st.session_state.paper_loaded else "Upload PDF")

st.divider()


# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["Summary", "💬 Chat", "📤 Export"])


# =========================
# SUMMARY TAB
# =========================
with tab1:

    st.markdown("### Generate Paper Summary")

    if st.session_state.paper_loaded:

        if st.button("Generate Summary"):

            with st.spinner("Thinking..."):
                from ollama import chat

                text = st.session_state.paper_text[:15000]

                prompt = f"""
You are a research assistant.

Analyze the paper and give:

1. Title
2. Problem
3. Methodology
4. Key Findings
5. Limitations
6. Future Work

Paper:
{text}
"""

                try:
                    res = chat(
                        model="qwen3:8b",
                        messages=[{"role": "user", "content": prompt}]
                    )

                    st.session_state.summary = res["message"]["content"]

                except Exception as e:
                    st.error(str(e))

        if st.session_state.summary:
            st.markdown(st.session_state.summary)

    else:
        st.info("Upload a PDF first.")


# =========================
# CHAT TAB
# =========================
with tab2:

    st.markdown("### Ask Questions")

    if st.session_state.paper_loaded:

        from utils.chatbot import ask_question

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        question = st.chat_input("Ask something...")

        if question:

            st.session_state.messages.append({"role": "user", "content": question})

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Searching..."):
                    try:
                        answer = ask_question(st.session_state.db, question)
                    except Exception as e:
                        answer = f"Error: {e}"

                    st.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})

    else:
        st.info("Upload a PDF to start chat.")


# =========================
# EXPORT TAB
# =========================
with tab3:

    st.markdown("### Export Data")

    if st.session_state.summary:
        st.download_button(
            "Download Summary",
            st.session_state.summary,
            file_name="summary.txt"
        )

    chat_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.messages]
    )

    if chat_text:
        st.download_button(
            "Download Chat History",
            chat_text,
            file_name="chat.txt"
        )