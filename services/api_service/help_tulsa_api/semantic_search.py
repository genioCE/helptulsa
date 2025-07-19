# help_tulsa_api/semantic_search.py
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

class SemanticSearch:
    def __init__(self, host="qdrant", port=6333, collection="help_resources"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = QdrantClient(host=host, port=port)
        self.collection = collection

    def query(self, text: str, top_k: int = 5):
        vector = self.model.encode(text).tolist()
        hits = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=top_k,
        )
        return [
            {
                "score": float(round(hit.score, 4)),
                "resource": hit.payload
            }
            for hit in hits
        ]
