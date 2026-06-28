from sentence_transformers import SentenceTransformer

# Load the embedding model only once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Converts text chunks into embedding vectors.
    """

    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings