from ollama import chat
from utils.embedding import embedding_model


def ask_question(db, question):
    """
    Search relevant chunks and ask Qwen.
    """

    print("\nSearching ChromaDB...")

    # Convert question into embedding
    query_embedding = embedding_model.encode(
        question,
        convert_to_numpy=True
    )

    # Search database
    results = db.search(query_embedding)

    # Combine retrieved chunks
    context = "\n\n".join(results["documents"][0])
    sources = results["metadatas"][0]
    prompt = f"""
You are an expert research paper assistant.

Use ONLY the context below to answer the user's question.

If the answer is not available in the context,
reply:

"I could not find that information in the paper."

------------------------

Context:

{context}

------------------------

Question:

{question}
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