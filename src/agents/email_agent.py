"""
Email Agent
Extracts course information, looks up instructor contact details,
and drafts formal emails (sick-leave, makeup exam requests) for student review.
"""

from typing import Dict, Any, Optional
import re
from src.tools.email_drafter import draft_email
from src.tools.faculty_lookup import get_instructor_email
from src.llm.client import LLMClient


class EmailAgent:
    def __init__(self, name: str = "EmailAgent", llm_client: Optional[LLMClient] = None):
        self.name = name
        self.llm = llm_client or LLMClient()

    def handle(self, query: str) -> Dict[str, Any]:
        """
        Extract request parameters and generate formal email draft.
        """
        q_lower = query.lower()
        
        # 1. Extract course code (e.g. CSL7570, CSL3060, MEL3010)
        match_code = re.search(r'\b([A-Za-z]{2,3}\d{4})\b', query)
        course_code = match_code.group(1).upper() if match_code else "CSL7570"
        
        # 2. Extract number of days (e.g. "for 2 days", "3 days leave")
        match_days = re.search(r'(\d+)\s*days?', q_lower)
        num_days = int(match_days.group(1)) if match_days else 2
        
        # 3. Determine email type and reason
        if any(w in q_lower for w in ["makeup", "make-up", "missed exam", "permission for exam"]):
            email_type = "makeup_exam"
            reason = "unavoidable medical illness and doctor-prescribed bed rest"
        else:
            email_type = "sick_leave"
            reason = "sudden illness and severe viral fever"
            
        # 4. Generate formal draft via tool
        draft = draft_email(
            course_code=course_code,
            reason=reason,
            num_days=num_days,
            email_type=email_type,
            student_name="Student",
            student_roll="B21CS001"
        )
        
        formatted_answer = (
            f"Here is the drafted email for your review:\n\n"
            f"**To**: `{draft['to_email']}` ({draft['to_name']})\n"
            f"**Subject**: `{draft['subject']}`\n\n"
            f"```\n{draft['body']}\n```\n\n"
            f"⚠️ *Note: This email draft has been generated for your review. It has NOT been sent.*"
        )
        
        return {
            "agent": self.name,
            "answer": formatted_answer,
            "draft": draft
        }
