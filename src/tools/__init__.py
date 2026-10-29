"""
Tools package for Academic Helpdesk Agent
"""

from src.tools.rag_search import search_knowledge_base
from src.tools.timetable_lookup import lookup_timetable
from src.tools.course_lookup import lookup_courses
from src.tools.faculty_lookup import get_instructor_email
from src.tools.email_drafter import draft_email
from src.tools.unanswered_logger import log_unanswered_question

__all__ = [
    "search_knowledge_base",
    "lookup_timetable",
    "lookup_courses",
    "get_instructor_email",
    "draft_email",
    "log_unanswered_question",
]
