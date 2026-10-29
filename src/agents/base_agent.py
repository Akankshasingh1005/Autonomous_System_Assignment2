"""
Base Academic Helpdesk Agent (Single-Agent Baseline)
Monolithic agent that has access to all tools (RAG search, timetable lookup,
course catalog, email drafting, unanswered question logging) in a single workflow.
Serves as the baseline for comparison against the Multi-Agent architecture.
"""

from typing import Dict, Any, Optional
import re
from src.tools.rag_search import search_knowledge_base
from src.tools.timetable_lookup import lookup_timetable
from src.tools.course_lookup import lookup_courses
from src.tools.faculty_lookup import get_instructor_email
from src.tools.email_drafter import draft_email
from src.tools.unanswered_logger import log_unanswered_question
from src.llm.client import LLMClient

# Non-academic keywords
OUT_OF_SCOPE_KEYWORDS = [
    "dining", "food", "mess", "canteen", "cafe", "restaurant", "lunch", "dinner", "breakfast",
    "city center", "reach the campus", "travel", "flight", "train", "taxi", "cab", "bus",
    "weather", "climate", "temperature", "shopping", "tourism", "hotel", "cinema", "movie",
    "tourist", "sightseeing", "places to visit", "attractions"
]


class BaseHelpdeskAgent:
    """
    Single-agent implementation of the Academic Helpdesk.
    Handles all queries in a single monolithic decision flow.
    """
    def __init__(self, name: str = "BaseSingleAgent", llm_client: Optional[LLMClient] = None):
        self.name = name
        self.llm = llm_client or LLMClient()

    def handle(self, query: str) -> Dict[str, Any]:
        q_lower = query.lower()

        # 1. Out-of-scope detection
        if any(kw in q_lower for kw in OUT_OF_SCOPE_KEYWORDS):
            refusal_msg = "I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors."
            log_unanswered_question(query, reason="Out-of-scope non-academic question (BaseAgent)")
            return {
                "agent": self.name,
                "intent": "out_of_scope",
                "answer": refusal_msg,
                "refused": True,
                "logged": True
            }

        # 2. Email drafting
        if any(w in q_lower for w in ["write an email", "draft an email", "send an email", "draft email", "write email"]):
            match_code = re.search(r'\b([A-Za-z]{2,3}\d{4})\b', query)
            course_code = match_code.group(1).upper() if match_code else "CSL7570"
            match_days = re.search(r'(\d+)\s*days?', q_lower)
            num_days = int(match_days.group(1)) if match_days else 2
            
            email_type = "makeup_exam" if ("makeup" in q_lower or "make-up" in q_lower) else "sick_leave"
            draft = draft_email(
                course_code=course_code,
                reason="illness",
                num_days=num_days,
                email_type=email_type,
                student_name="Student",
                student_roll="B21CS001"
            )
            ans = (
                f"Here is the drafted email for your review:\n\n"
                f"**To**: `{draft['to_email']}` ({draft['to_name']})\n"
                f"**Subject**: `{draft['subject']}`\n\n"
                f"```\n{draft['body']}\n```\n\n"
                f"⚠️ *Note: This email draft has been generated for your review. It has NOT been sent.*"
            )
            return {
                "agent": self.name,
                "intent": "email",
                "answer": ans,
                "draft": draft
            }

        # 3. Schedule / Timetable lookup
        if any(w in q_lower for w in ["slot", "timing", "room", "when is", "when does", "meet", "classroom"]):
            code_match = re.search(r'\b([A-Za-z]{2,3}\d{4})\b', query)
            course_code = code_match.group(1).upper() if code_match else None
            course_name = "Autonomous Systems" if "autonomous" in q_lower else None
            
            res = lookup_timetable(course_code=course_code, course_name=course_name)
            if res.get("results"):
                item = res["results"][0]
                ans = f"The course **{item['course_title']} ({item['course_code']})** is scheduled in **Slot {item['slot']}** ({item['days']} {item['time']} in {item['room']})."
                return {"agent": self.name, "intent": "schedule", "answer": ans}

        # 4. Floated electives count
        if "elective" in q_lower or "floated" in q_lower:
            dept = "HSS" if ("humanities" in q_lower or "hss" in q_lower) else None
            level = 400 if "400" in q_lower else None
            res = lookup_courses(department=dept, level=level)
            ans = f"There are **{res['count']}** courses/electives floated by {dept or 'the department'} in this semester."
            return {"agent": self.name, "intent": "schedule", "answer": ans}

        # 5. RAG Policy search
        search_res = search_knowledge_base(query, top_k=3)
        chunks = search_res.get("results", [])
        citations = search_res.get("citations", "")
        if chunks:
            context_str = "\n".join([f"- {c['content']}" for c in chunks[:2]])
            llm_ans = self.llm.generate(f"Context: {context_str}\n\nQuestion: {query}")
            ans = f"{llm_ans}\n\n{citations}" if citations else llm_ans
            return {"agent": self.name, "intent": "policy", "answer": ans, "citations": citations}

        # Fallback refusal
        log_unanswered_question(query, reason="Unresolved query in BaseAgent")
        return {
            "agent": self.name,
            "intent": "unresolved",
            "answer": "I do not know. The requested information could not be retrieved from academic documents.",
            "refused": True
        }
