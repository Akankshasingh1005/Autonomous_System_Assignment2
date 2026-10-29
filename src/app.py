"""
Interactive CLI for Academic Helpdesk Agent
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path regardless of how the script is launched
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.agents.orchestrator import AcademicHelpdeskOrchestrator


def main():
    print("=" * 65)
    print("🎓 IIT Jodhpur Academic Helpdesk Agent (Multi-Agent System)")
    print("=" * 65)
    print("Type your academic query or 'exit'/'quit' to exit.\n")
    
    orchestrator = AcademicHelpdeskOrchestrator()
    
    while True:
        try:
            query = input("User > ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
                
            response = orchestrator.handle(query)
            print(f"\n[Agent: {response.get('agent', 'Helpdesk')} | Intent: {response.get('intent', 'unknown')}]")
            print("-" * 50)
            print(response.get("answer", ""))
            print("-" * 50 + "\n")
            
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break


if __name__ == "__main__":
    main()
