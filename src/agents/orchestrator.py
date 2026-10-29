"""
Academic Helpdesk Orchestrator Agent
The main root agent that classifies queries, routes them to specialized sub-agents,
handles out-of-scope refusal ("I do not know"), and logs unanswered questions.
"""

from typing import Dict, Any, Optional
import re
from src.agents.policy_agent import PolicyAgent
from src.agents.schedule_agent import ScheduleAgent
from src.agents.email_agent import EmailAgent
from src.tools.unanswered_logger import log_unanswered_question
from src.llm.client import LLMClient

# Keywords defining out-of-scope non-academic queries
OUT_OF_SCOPE_KEYWORDS = [
    "dining", "food", "mess", "canteen", "cafe", "restaurant", "lunch", "dinner", "breakfast",
    "city center", "reach the campus", "travel", "flight", "train", "taxi", "cab", "bus",
    "weather", "climate", "temperature", "shopping", "tourism", "hotel", "cinema", "movie",
    "tourist", "sightseeing", "places to visit", "attractions"
]


class AcademicHelpdeskOrchestrator:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm = llm_client or LLMClient()
        self.policy_agent = PolicyAgent(llm_client=self.llm)
        self.schedule_agent = ScheduleAgent(llm_client=self.llm)
        self.email_agent = EmailAgent(llm_client=self.llm)

    def classify_intent(self, query: str) -> str:
        """
        Classify query intent into:
        - 'out_of_scope': Non-academic query that must be refused
        - 'email': Leave application or makeup exam drafting
        - 'schedule': Timetable, slot, or course offerings query
        - 'policy': Academic rules, regulations, attendance, credits, curriculum
        """
        q_lower = query.lower()
        
        # 1. Out of scope check
        for kw in OUT_OF_SCOPE_KEYWORDS:
            if kw in q_lower:
                return "out_of_scope"
                
        # 2. Email drafting check (requires explicit drafting / writing intent)
        if any(w in q_lower for w in ["write an email", "draft an email", "send an email", "draft email", "draft a mail", "write email", "write mail"]) or ("apply for" in q_lower and "leave" in q_lower):
            return "email"
            
        # 3. Degree / Credit requirement / Curriculum / Academic rules check
        if any(w in q_lower for w in ["credits do i need", "credit requirement", "degree", "graduation", "earn in order", "attendance", "grade", "grading", "rule", "regulation", "policy", "minimum credit", "what happens if", "absent", "missed exam", "make-up"]):
            return "policy"

        # 4. Schedule / Timetable check
        if any(w in q_lower for w in ["slot", "timetable", "timing", "room", "when is", "when does", "meet", "classroom", "floated", "schedule"]):
            return "schedule"
        if "elective" in q_lower and any(w in q_lower for w in ["how many", "offered", "department", "semester"]):
            return "schedule"
            
        # 5. Default to academic policy / curriculum
        return "policy"

    def handle(self, query: str) -> Dict[str, Any]:
        """
        Process user query through multi-agent orchestration.
        """
        intent = self.classify_intent(query)
        
        if intent == "out_of_scope":
            # Refuse politely without guessing
            refusal_msg = "I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors."
            log_unanswered_question(query, reason="Out-of-scope non-academic question")
            return {
                "intent": "out_of_scope",
                "agent": "Orchestrator",
                "answer": refusal_msg,
                "refused": True,
                "logged": True
            }
            
        elif intent == "email":
            res = self.email_agent.handle(query)
            res["intent"] = "email"
            return res
            
        elif intent == "schedule":
            res = self.schedule_agent.handle(query)
            res["intent"] = "schedule"
            return res
            
        else:  # policy
            res = self.policy_agent.handle(query)
            res["intent"] = "policy"
            return res
