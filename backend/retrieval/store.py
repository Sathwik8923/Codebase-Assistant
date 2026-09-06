import chromadb
from sentence_transformers import SentenceTransformer

# Loads once, reused across calls — this model is small (~80MB) and fast on CPU
model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent client writes to disk so your index survives between runs
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="codesage_chunks")


def embed_and_store(chunks: list[dict]):
    """Takes chunk dicts from ingestion and stores them with embeddings in Chroma."""
    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"chunk_{i}")
        documents.append(chunk["content"])
        metadatas.append({
            "file_path": chunk["file_path"],
            "type": chunk["type"],
            "name": chunk["name"],
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
        })

    embeddings = model.encode(documents, show_progress_bar=True).tolist()

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB")


def query_chunks(query_text: str, top_k: int = 5):
    """Embeds a query and retrieves the top_k most similar chunks."""
    query_embedding = model.encode([query_text]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )
    return results