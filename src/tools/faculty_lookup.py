"""
Tool: get_instructor_email
Finds instructor name, email, department, and office from course mapping or faculty directory.
"""

from typing import Dict, Any, Optional
import pandas as pd
from src.config import INSTRUCTOR_MAPPING_CSV, FACULTY_CSV

_mapping_df = None
_faculty_df = None

def get_mapping_df() -> pd.DataFrame:
    global _mapping_df
    if _mapping_df is None:
        _mapping_df = pd.read_csv(INSTRUCTOR_MAPPING_CSV)
    return _mapping_df

def get_faculty_df() -> pd.DataFrame:
    global _faculty_df
    if _faculty_df is None:
        _faculty_df = pd.read_csv(FACULTY_CSV)
    return _faculty_df


def get_instructor_email(
    course_code: Optional[str] = None,
    instructor_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get instructor details (name, email, department) for a course or instructor name.
    
    Args:
        course_code: Course code, e.g. 'CSL7570'
        instructor_name: Instructor full or partial name, e.g. 'Rahul Sharma'
        
    Returns:
        Dict with instructor contact info.
    """
    mapping = get_mapping_df()
    faculty = get_faculty_df()
    
    if course_code:
        code_clean = course_code.strip().upper()
        match = mapping[mapping["course_code"].str.upper() == code_clean]
        if not match.empty:
            row = match.iloc[0]
            return {
                "found": True,
                "course_code": row["course_code"],
                "course_title": row["course_title"],
                "instructor_name": row["instructor_name"],
                "instructor_email": row["instructor_email"],
                "department": row["department"]
            }
            
    if instructor_name:
        name_clean = instructor_name.strip().lower()
        match = faculty[faculty["name"].str.lower().str.contains(name_clean, na=False)]
        if not match.empty:
            row = match.iloc[0]
            return {
                "found": True,
                "course_code": course_code or "",
                "instructor_name": row["name"],
                "instructor_email": row["email"],
                "department": row["department"],
                "designation": row.get("designation", "")
            }
            
    return {
        "found": False,
        "message": f"Instructor not found for course {course_code} or name {instructor_name}"
    }
