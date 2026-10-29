"""
Global configuration and paths for Academic Helpdesk.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Paths
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = DATA_DIR / "documents"
CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", str(DATA_DIR / "chromadb")))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "academic_docs")

TIMETABLE_CSV = DATA_DIR / "timetable.csv"
FACULTY_CSV = DATA_DIR / "faculty.csv"
COURSES_FLOATED_CSV = DATA_DIR / "courses_floated.csv"
INSTRUCTOR_MAPPING_CSV = DATA_DIR / "instructor_course_mapping.csv"

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
UNANSWERED_LOG = Path(os.getenv("UNANSWERED_LOG", str(LOGS_DIR / "unanswered_questions.jsonl")))

# Model configurations
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "ollama/qwen3:8b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
