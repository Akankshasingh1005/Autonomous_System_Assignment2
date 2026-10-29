"""
Document Ingestion Script
Extracts text from real PDF documents in data/documents/, chunks them,
and indexes them into a local persistent ChromaDB collection.
"""

import os
import sys
import glob
import fitz  # PyMuPDF
import chromadb
from chromadb.utils import embedding_functions

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "documents"))
CHROMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "chromadb"))
COLLECTION_NAME = "academic_docs"

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

# Exact transcripts for official circulars that are scanned image PDFs
SCANNED_PDF_TRANSCRIPTS = {
    "amendment_attendance_policy_2024.pdf": [
        {
            "page": 1,
            "text": (
                "Indian Institute of Technology Jodhpur\n"
                "No. IITJ/OAA/Circular/2024-25/51/682 Dated: 08 July 2024\n"
                "CIRCULAR\n"
                "Subject: Amendment in the Attendance Policy of the Institute for the Students\n"
                "The Senate in its 38th Meeting held on 26th June 2024 vide resolution number 38.2.7 approved an amendment to the existing attendance Policy.\n"
                "Existing policy: As per the current policy for attendance in courses, a student should have full attendance in each course. "
                "Unless the student takes a leave of absence for valid reasons, the student has to attend every lecture, tutorial, or lab session. "
                "The attendance records must be made available to the student after every lecture. Even if the student's attendance falls below 75%, "
                "the student will be allowed to appear for the exams. Students not meeting the attendance criterion of 75% will be required to score "
                "at least a C grade to pass a course. These students would be awarded an F grade if their marks are lower than the cut-off for a C grade in a course.\n"
                "Revised Policy: According to the recent Senate and Board-approved policy, students' examination performance is no longer linked to their "
                "course attendance. As per the amendment in attendance policy a student is expected to have full attendance in each course unless the student "
                "takes a leave of absence for valid medical or bonafide reasons. In any case, the attendance of a student should not fall below 75% in a course. "
                "The attendance records must be made available weekly to all students enrolled in a course by the instructors/TAs. The Course Instructor/TAs "
                "must inform students about the attendance policy of the course at the beginning of the course in the First Course Handout (FCH), and:\n"
                "- If a student remains absent from a class without sanctioned leave for more than two weeks, then the course instructor may recommend the de-registration of the student from the course.\n"
                "- If a student is found to be absent from all academic activities for four or more than four weeks (not necessarily contiguous) in a semester, with or without sanctioned leave, then his/her registration will result in automatic semester withdrawal for all the courses."
            )
        },
        {
            "page": 2,
            "text": (
                "Indian Institute of Technology Jodhpur - Amendment in Attendance Policy (Page 2)\n"
                "- If a student's attendance falls below 75% without any valid reason, the instructor can recommend de-registration from the course to the SUGC/SPGC.\n"
                "- This policy supersedes the earlier policy in totality.\n"
                "Signed by Ravi Jingar, Assistant Registrar (Office of Academic Affairs), 08 July 2024."
            )
        }
    ],
    "amendment_examination_policy_2024.pdf": [
        {
            "page": 1,
            "text": (
                "Indian Institute of Technology Jodhpur\n"
                "No. IITJ/OAA/Circular/2024-25/52/683 Dated: 08 July 2024\n"
                "CIRCULAR\n"
                "Subject: To conduct one Minor and one Major examination for evaluation in all Academic Programs\n"
                "The Senate in its 38th meeting held on 26th June 2024 vide resolution number 38.2.6 approved to conduct one Minor and one Major examination for evaluation in all Academic Programs.\n"
                "The evaluation scheme approved by the Senate for all Academic Programs is as under:\n"
                "1. The Minor Examination will occur around the midpoint of the Semester to evaluate Students' progress and to offer prompt feedback on their academic performance. The Minor examination will be a written examination for 2 hours.\n"
                "2. The Major Examination will take place at the end of the Semester to assess students' thorough grasp of the concepts taught throughout the Semester. The Major examination will encompass the entire syllabus and assess learning across the entire course.\n"
                "3. The Major examination will be a written examination with a weightage not less than 40% of the overall evaluation. The duration of the major examination will be 3 hours.\n"
                "4. The examinations from Academic Year 2024-25 Semester-I onwards would be decentralized where the Office of Academics would provide the examination calendar, venue details, and examination copies. The Faculty Members would conduct examinations with the support of their Teaching Assistant (TA) and prepare seating arrangements.\n"
                "5. Instructors will determine the weightage of Minor examination and other components of continuous evaluation.\n"
                "6. All the Faculty Members shall share the course evaluation scheme with the students at least two days before the very first day of the Class, in the First Course Handout (FCH).\n"
                "7. This policy supersedes the earlier policy regarding evaluation in totality.\n"
                "Signed by Ravi Jingar, Assistant Registrar (Office of Academic Affairs), 08 July 2024."
            )
        }
    ]
}


def clean_text(text: str) -> str:
    """Clean extra whitespaces and line breaks."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
    """Simple character/word chunker with overlap."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunk = " ".join(chunk_words)
        if len(chunk.strip()) > 20:
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def extract_and_chunk_pdf(pdf_path: str):
    """Extract text from PDF page by page and generate chunks with metadata."""
    filename = os.path.basename(pdf_path)
    title = filename.replace(".pdf", "").replace("_", " ").title()
    chunks_with_meta = []
    
    # Check if scanned PDF with known official transcript
    if filename in SCANNED_PDF_TRANSCRIPTS:
        for item in SCANNED_PDF_TRANSCRIPTS[filename]:
            p_text = clean_text(item["text"])
            p_chunks = chunk_text(p_text)
            for c_idx, c_text in enumerate(p_chunks):
                chunks_with_meta.append({
                    "text": c_text,
                    "metadata": {
                        "source": filename,
                        "page": item["page"],
                        "title": title,
                        "chunk_index": c_idx
                    }
                })
        return chunks_with_meta

    try:
        doc = fitz.open(pdf_path)
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            page_text = page.get_text()
            cleaned = clean_text(page_text)
            if not cleaned:
                continue
            
            page_chunks = chunk_text(cleaned)
            for c_idx, c_text in enumerate(page_chunks):
                chunks_with_meta.append({
                    "text": c_text,
                    "metadata": {
                        "source": filename,
                        "page": page_idx + 1,
                        "title": title,
                        "chunk_index": c_idx
                    }
                })
        doc.close()
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
        
    return chunks_with_meta


def ingest_all():
    print(f"Ingesting documents from: {DOCS_DIR}")
    os.makedirs(CHROMA_DIR, exist_ok=True)
    
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    emb_fn = embedding_functions.DefaultEmbeddingFunction()
    
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Cleared existing collection '{COLLECTION_NAME}'")
    except Exception:
        pass
        
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    pdf_files = sorted(glob.glob(os.path.join(DOCS_DIR, "*.pdf")))
    print(f"Found {len(pdf_files)} authentic PDF documents.")
    
    all_docs = []
    all_metas = []
    all_ids = []
    
    total_chunks = 0
    for idx, pdf_path in enumerate(pdf_files, 1):
        filename = os.path.basename(pdf_path)
        chunks = extract_and_chunk_pdf(pdf_path)
        print(f"[{idx:2d}/{len(pdf_files)}] {filename} -> {len(chunks)} chunks")
        
        for c_idx, item in enumerate(chunks):
            chunk_id = f"{filename}_p{item['metadata']['page']}_c{c_idx}"
            all_docs.append(item["text"])
            all_metas.append(item["metadata"])
            all_ids.append(chunk_id)
            total_chunks += 1
            
            if len(all_docs) >= 200:
                collection.add(
                    documents=all_docs,
                    metadatas=all_metas,
                    ids=all_ids
                )
                all_docs, all_metas, all_ids = [], [], []
                
    if all_docs:
        collection.add(
            documents=all_docs,
            metadatas=all_metas,
            ids=all_ids
        )
        
    print(f"\n[DONE] Successfully indexed {total_chunks} chunks from {len(pdf_files)} documents into ChromaDB!")


if __name__ == "__main__":
    ingest_all()
