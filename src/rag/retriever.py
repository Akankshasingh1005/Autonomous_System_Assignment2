"""
ChromaDB Retriever module for searching academic documents with citations.
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.utils import embedding_functions
from src.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION


class AcademicRetriever:
    def __init__(self, persist_dir: Optional[str] = None, collection_name: Optional[str] = None):
        self.persist_dir = str(persist_dir or CHROMA_PERSIST_DIR)
        self.collection_name = collection_name or CHROMA_COLLECTION
        
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_collection(
            name=self.collection_name,
            embedding_function=self.emb_fn
        )

    def query(self, query_text: str, top_k: int = 5, distance_threshold: float = 1.2) -> List[Dict[str, Any]]:
        """
        Query the collection and return top matches with metadata and citation info.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        matches = []
        if not results or not results["documents"] or not results["documents"][0]:
            return matches
            
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0] if "distances" in results else [0.0] * len(docs)
        
        for doc_text, meta, dist in zip(docs, metas, dists):
            if dist is not None and dist > distance_threshold:
                continue
            matches.append({
                "content": doc_text,
                "source": meta.get("source", "Unknown"),
                "page": meta.get("page", 1),
                "title": meta.get("title", ""),
                "distance": float(dist) if dist is not None else 0.0
            })
            
        return matches

    def format_citation(self, matches: List[Dict[str, Any]]) -> str:
        """Format unique citations from matched chunks."""
        seen = set()
        citations = []
        for m in matches:
            key = (m["source"], m["page"])
            if key not in seen:
                seen.add(key)
                citations.append(f"- {m['source']} (Page {m['page']})")
        if not citations:
            return ""
        return "📄 Sources:\n" + "\n".join(citations)
