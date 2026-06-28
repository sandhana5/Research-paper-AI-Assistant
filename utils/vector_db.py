import chromadb


class VectorDatabase:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_papers"
        )

    def store_embeddings(
        self,
        chunks,
        embeddings,
        filename
    ):

        ids = []

        documents = []

        vectors = []

        metadatas = []

        existing = self.collection.count()

        for i, chunk in enumerate(chunks):

            ids.append(f"{filename}_{existing+i}")

            documents.append(chunk)

            vectors.append(
                embeddings[i].tolist()
            )

            metadatas.append({

                "filename": filename,

                "chunk": i

            })

        self.collection.add(

            ids=ids,

            documents=documents,

            embeddings=vectors,

            metadatas=metadatas

        )

        print("\nStored into ChromaDB!")

    def search(

        self,

        query_embedding,

        n_results=5

    ):

        results = self.collection.query(

            query_embeddings=[query_embedding.tolist()],

            n_results=n_results

        )

        return results