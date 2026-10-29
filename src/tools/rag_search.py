"""
Tool: search_knowledge_base
Searches the ChromaDB collection for academic documents, returns matching chunks with citations.
"""

from typing import Dict, Any, List
from src.rag.retriever import AcademicRetriever

_retriever = None

def get_retriever() -> AcademicRetriever:
    global _retriever
    if _retriever is None:
        _retriever = AcademicRetriever()
    return _retriever


def search_knowledge_base(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Search the academic document knowledge base for relevant rules, curriculum, or policy.
    
    Args:
        query: Search question or keywords
        top_k: Number of relevant chunks to retrieve (default 5)
        
    Returns:
        Dict containing retrieved chunks and formatted citations.
    """
    retriever = get_retriever()
    matches = retriever.query(query, top_k=top_k)
    citations = retriever.format_citation(matches)
    
    return {
        "query": query,
        "num_results": len(matches),
        "results": matches,
        "citations": citations
    }
