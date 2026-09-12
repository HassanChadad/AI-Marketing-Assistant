from dataclasses import dataclass, asdict
import chromadb
import ollama
import uuid

@dataclass
class ContentMetadata:
    topic: str
    platform: str

_client = chromadb.PersistentClient(path="./chroma_data")
_collection = None

def _get_collection():
    global _collection
    if _collection is None:
        _collection = _client.get_or_create_collection("content_history")
    return _collection

def _embed(text: str) -> list[float]:
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]

def store_draft(topic: str, platform: str, draft: str):
    collection = _get_collection()
    metadata = ContentMetadata(topic=topic, platform=platform)

    collection.add(
        ids=[str(uuid.uuid4())],
        embeddings=[_embed(topic)],
        documents=[draft],
        metadatas=[asdict(metadata)]
    )

def retrieve_similar_drafts(topic: str, platform: str, top_k: int = 2) -> list[str]:
    collection = _get_collection()
    if collection.count() == 0:
        return []

    query_embedding = _embed(topic)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"platform": platform}
    )
    return results["documents"][0] if results["documents"] else []