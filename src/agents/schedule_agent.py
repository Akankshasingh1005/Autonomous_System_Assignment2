"""
Schedule Agent
Answers questions regarding course timetables, slots, class timings, lecture rooms,
and floating courses by department or level using structured CSV tools.
"""

from typing import Dict, Any, List, Optional
import re
from src.tools.timetable_lookup import lookup_timetable
from src.tools.course_lookup import lookup_courses
from src.llm.client import LLMClient


class ScheduleAgent:
    def __init__(self, name: str = "ScheduleAgent", llm_client: Optional[LLMClient] = None):
        self.name = name
        self.llm = llm_client or LLMClient()

    def handle(self, query: str) -> Dict[str, Any]:
        """
        Process timetable, slot, or course catalog query using structured data tools.
        """
        q_lower = query.lower()
        
        # 1. Course Slot, Timetable, Room, Meeting Time Query
        if any(w in q_lower for w in ["slot", "timing", "room", "when is", "when does", "meet", "classroom", "schedule"]):
            # Extract potential course code (e.g., CSL7570, MEL3010)
            code_match = re.search(r'\b([A-Za-z]{2,3}\d{4})\b', query)
            course_code = code_match.group(1).upper() if code_match else None
            
            # Extract potential course name keywords
            course_name = None
            known_titles = [
                "autonomous systems", "operating systems", "machine learning",
                "computer networks", "deep learning", "natural language processing",
                "data structures", "database management", "signals and systems",
                "control systems", "power electronics", "wireless communications",
                "thermodynamics", "fluid mechanics", "heat transfer",
                "introduction to sociology", "classical mechanics", "quantum mechanics",
                "calculus", "probability and statistics", "reinforcement learning",
                "compiler design", "biotechnology", "genomics", "numerical methods"
            ]
            for title in known_titles:
                if title in q_lower:
                    course_name = title
                    break
                    
            res = lookup_timetable(course_code=course_code, course_name=course_name)
            if res.get("results"):
                item = res["results"][0]
                answer = (
                    f"The course **{item['course_title']} ({item['course_code']})** is scheduled in **Slot {item['slot']}**.\n"
                    f"- **Days**: {item['days']}\n"
                    f"- **Time**: {item['time']}\n"
                    f"- **Room**: {item['room']}\n"
                    f"- **Instructor**: {item['instructor']} ({item['department']} Dept)"
                )
                return {
                    "agent": self.name,
                    "answer": answer,
                    "data": item
                }
            else:
                return {
                    "agent": self.name,
                    "answer": f"I could not find timetable information for the requested course in the current semester schedule.",
                    "data": None
                }

        # 2. Floated Electives / Courses Count Query (e.g. Humanities 400-level electives)
        if any(w in q_lower for w in ["elective", "electives", "floated", "offered", "courses", "how many"]):
            # Detect Department
            dept = None
            if any(w in q_lower for w in ["humanities", "hss", "sola", "social science"]):
                dept = "HSS"
            elif any(w in q_lower for w in ["electrical", "ee"]):
                dept = "EE"
            elif any(w in q_lower for w in ["computer science", "cse"]):
                dept = "CSE"
            elif any(w in q_lower for w in ["mechanical", "me"]):
                dept = "ME"
            elif any(w in q_lower for w in ["mathematics", "math", "ma"]):
                dept = "MA"
            elif any(w in q_lower for w in ["physics", "ph"]):
                dept = "PH"
            elif any(w in q_lower for w in ["biology", "bio", "bsbe"]):
                dept = "BIO"
            elif any(w in q_lower for w in ["sme", "management", "mba"]):
                dept = "SME"
                
            # Detect Level (100, 200, 300, 400, 500, 600, 700)
            level = None
            for lvl in [100, 200, 300, 400, 500, 600, 700]:
                if str(lvl) in q_lower:
                    level = lvl
                    break
            
            res = lookup_courses(department=dept, level=level)
            count = res["count"]
            courses = res["results"]
            
            dept_name = f"{dept} department" if dept else "the institute"
            lvl_str = f"{level}-level " if level else ""
            
            if courses:
                course_list_str = "\n".join([
                    f"- **{c['course_code']}**: {c['course_title']} ({c['credits']} credits, Type: {c['type']}, Instructor: {c['instructor']})"
                    for c in courses
                ])
                answer = (
                    f"There are **{count}** {lvl_str}courses/electives floated by {dept_name} in this semester:\n"
                    f"{course_list_str}"
                )
            else:
                answer = f"No {lvl_str}courses were found for {dept_name} in the current semester course catalog."

            return {
                "agent": self.name,
                "answer": answer,
                "count": count,
                "data": courses
            }

        # Fallback
        return {
            "agent": self.name,
            "answer": "I could not resolve the schedule query. Please specify a course code, course name, or department.",
            "data": None
        }
