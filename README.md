# Research Paper AI Assistant

An offline AI-powered Research Paper Assistant that leverages **Retrieval-Augmented Generation (RAG)** with a **Local Large Language Model (Qwen3)** to analyze, summarize, and answer questions from research papers.

---

## Overview

Research Paper AI Assistant is a desktop application built with **Streamlit**, **Ollama**, **ChromaDB**, and **Sentence Transformers**.

The application enables users to upload research papers in PDF format, automatically process the document, generate semantic embeddings, store them in a vector database, and interact with the paper using natural language.

Unlike cloud-based AI applications, this project runs completely offline using a local LLM, ensuring privacy and eliminating API costs.

---

## Key Features

- Upload research papers in PDF format
- Automatic text extraction using PyMuPDF
- Intelligent text chunking
- Semantic embeddings using Sentence Transformers
- ChromaDB vector database
- Retrieval-Augmented Generation (RAG)
- AI-powered research paper summarization
- Interactive question answering
- Local inference using Ollama and Qwen3
- Fully offline workflow

---

## Technology Stack

| Category | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Local LLM | Qwen3 (Ollama) |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| PDF Processing | PyMuPDF |
| NLP | Sentence Transformers |
| Retrieval | RAG Pipeline |

---
