"""
Tool: lookup_courses
Queries courses_floated.csv by department, level, course type, or keyword.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from src.config import COURSES_FLOATED_CSV

_courses_df = None

def get_courses_df() -> pd.DataFrame:
    global _courses_df
    if _courses_df is None:
        _courses_df = pd.read_csv(COURSES_FLOATED_CSV)
    return _courses_df


def lookup_courses(
    department: Optional[str] = None,
    level: Optional[int] = None,
    course_type: Optional[str] = None,
    search_term: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search floated courses by department, level, type, or search term.
    
    Args:
        department: Department code or name (e.g. 'CSE', 'HSS', 'Humanities', 'EE')
        level: Course level (e.g., 200, 300, 400, 500, 600, 700)
        course_type: Course category (e.g. 'OE', 'DE', 'PC', 'PE', 'HSS', 'BS')
        search_term: Keyword in title or description
        
    Returns:
        Dict with total count and matching course records.
    """
    df = get_courses_df()
    filtered = df.copy()
    
    if department:
        dept_clean = department.strip().upper()
        if dept_clean in ["HUMANITIES", "HSS", "HUMANITIES AND SOCIAL SCIENCES"]:
            filtered = filtered[filtered["department"].str.upper().isin(["HSS", "HUMANITIES"])]
        else:
            filtered = filtered[filtered["department"].str.upper().str.contains(dept_clean, na=False)]
            
    if level is not None:
        try:
            lvl_val = int(level)
            filtered = filtered[filtered["level"] == lvl_val]
        except (ValueError, TypeError):
            pass
            
    if course_type:
        filtered = filtered[filtered["type"].str.upper() == course_type.upper().strip()]
        
    if search_term:
        term = search_term.lower().strip()
        filtered = filtered[
            filtered["course_title"].str.lower().str.contains(term, na=False) |
            filtered["course_code"].str.lower().str.contains(term, na=False) |
            filtered["description"].str.lower().str.contains(term, na=False)
        ]
        
    records = filtered.to_dict(orient="records")
    return {
        "count": len(records),
        "results": records
    }
