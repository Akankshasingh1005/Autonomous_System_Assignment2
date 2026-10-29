"""
Policy Agent
Answers questions regarding academic rules, regulations, examination policies,
grading, attendance, and curriculum requirements, with strict source citations.
Uses RAG retrieval over ChromaDB and an LLM client to synthesize answers.
"""

from typing import Dict, Any, List, Optional
from src.tools.rag_search import search_knowledge_base
from src.llm.client import LLMClient


class PolicyAgent:
    def __init__(self, name: str = "PolicyAgent", llm_client: Optional[LLMClient] = None):
        self.name = name
        self.llm = llm_client or LLMClient()

    def handle(self, query: str) -> Dict[str, Any]:
        """
        Process an academic policy, rule, or curriculum question.
        Retrieves relevant documents from ChromaDB and synthesizes an answer grounded in retrieved context.
        """
        # 1. Retrieve top-k relevant chunks from vector store
        search_res = search_knowledge_base(query, top_k=4)
        chunks = search_res.get("results", [])
        citations = search_res.get("citations", "")
        
        if not chunks:
            return {
                "agent": self.name,
                "answer": "I do not know. The requested information was not found in the official academic documents.",
                "citations": "",
                "sources_used": []
            }

        # 2. Format retrieved chunks into context string
        context_blocks = []
        for c in chunks:
            src = c.get("source", "Unknown")
            pg = c.get("page", 1)
            txt = c.get("content", "").strip()
            context_blocks.append(f"Source: {src} (Page {pg})\nContent: {txt}")
        
        context_str = "\n\n---\n\n".join(context_blocks)

        # 3. Formulate prompt for LLM synthesis
        system_prompt = (
            "You are the Academic Policy Specialist for the IIT Jodhpur Helpdesk. "
            "Your role is to provide accurate, grounded answers regarding academic regulations, "
            "attendance requirements, examination policies, degree credits, and course rules. "
            "Base your answer strictly on the provided official document context. "
            "Do not fabricate facts. If the context does not contain the answer, say you do not know."
        )

        user_prompt = (
            f"User Question: {query}\n\n"
            f"Official Document Context:\n{context_str}\n\n"
            f"Please provide a comprehensive, clear, and accurate answer based on the official documents above."
        )

        # 4. Invoke LLM client
        llm_answer = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt)

        # 5. Attach formatted citations
        if citations and citations not in llm_answer:
            full_answer = f"{llm_answer.strip()}\n\n{citations}"
        else:
            full_answer = llm_answer.strip()

        return {
            "agent": self.name,
            "answer": full_answer,
            "citations": citations,
            "sources_used": [c.get("source") for c in chunks]
        }
