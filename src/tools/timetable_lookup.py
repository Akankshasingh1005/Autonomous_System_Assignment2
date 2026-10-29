"""
Tool: lookup_timetable
Queries the timetable CSV for slot, days, time, room, instructor, and department.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
from src.config import TIMETABLE_CSV

_timetable_df = None

def get_timetable_df() -> pd.DataFrame:
    global _timetable_df
    if _timetable_df is None:
        _timetable_df = pd.read_csv(TIMETABLE_CSV)
    return _timetable_df


def lookup_timetable(
    course_code: Optional[str] = None,
    course_name: Optional[str] = None,
    slot: Optional[str] = None
) -> Dict[str, Any]:
    """
    Look up timetable details including slot, timing, room, and instructor.
    
    Args:
        course_code: Course code, e.g., 'CSL7570'
        course_name: Course title or keywords, e.g., 'Autonomous Systems'
        slot: Slot letter, e.g., 'D'
        
    Returns:
        Dict with matching timetable entries.
    """
    df = get_timetable_df()
    filtered = df.copy()
    
    if course_code:
        filtered = filtered[filtered["course_code"].str.upper().str.contains(course_code.upper().strip(), na=False)]
    if course_name:
        filtered = filtered[filtered["course_title"].str.lower().str.contains(course_name.lower().strip(), na=False)]
    if slot:
        filtered = filtered[filtered["slot"].str.upper() == slot.upper().strip()]
        
    records = filtered.to_dict(orient="records")
    return {
        "count": len(records),
        "results": records
    }
