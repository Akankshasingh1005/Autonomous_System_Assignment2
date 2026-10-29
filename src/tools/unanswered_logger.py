"""
Tool: log_unanswered_question
Logs queries that the academic helpdesk cannot answer to a JSONL file for human review.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Any
from src.config import UNANSWERED_LOG


def log_unanswered_question(question: str, reason: str = "Out of domain") -> Dict[str, Any]:
    """
    Log an unanswered or out-of-scope question to logs/unanswered_questions.jsonl.
    
    Args:
        question: The user query
        reason: Explanation why it was unanswered (e.g. 'Out of scope - campus amenities')
        
    Returns:
        Dict confirming logging status.
    """
    UNANSWERED_LOG.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "reason": reason
    }
    
    with open(UNANSWERED_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
    return {
        "logged": True,
        "entry": entry
    }
