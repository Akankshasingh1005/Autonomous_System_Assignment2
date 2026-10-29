"""
Quick verification of all required assignment queries.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
from src.agents.orchestrator import AcademicHelpdeskOrchestrator

test_queries = [
    "What is the attendance requirement to sit in the Major exam?",
    "What is the slot for the course Autonomous Systems?",
    "How many 400 level electives have been floated by the Humanities department in this semester?",
    "How many Open Elective credits do I need to earn in order to get a B.Tech. Degree?",
    "Write an email to the course instructor of CSL7570 that I need leave for 2 days",
    "What are the available dining options on the campus?",
    "What is the best way to reach the campus from Jodhpur city center?"
]

orchestrator = AcademicHelpdeskOrchestrator()

for i, q in enumerate(test_queries, 1):
    print(f"\n{'='*20} TEST {i}: '{q}' {'='*20}")
    res = orchestrator.handle(q)
    print(f"Intent: {res.get('intent')} | Agent: {res.get('agent')}")
    print(res.get("answer"))
