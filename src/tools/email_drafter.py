"""
Tool: draft_email
Drafts formal student-to-instructor emails for sick leave, makeup exams, or course queries.
"""

from typing import Dict, Any, Optional
from src.tools.faculty_lookup import get_instructor_email


def draft_email(
    course_code: str,
    reason: str,
    num_days: Optional[int] = None,
    email_type: str = "sick_leave",
    student_name: str = "Student",
    student_roll: str = "B21CS001",
    dates: Optional[str] = None
) -> Dict[str, Any]:
    """
    Draft a formal email to a course instructor for review before sending.
    
    Args:
        course_code: Course code, e.g. 'CSL7570'
        reason: Justification (e.g., 'suffering from viral fever', 'family emergency')
        num_days: Number of leave days requested (e.g. 2)
        email_type: 'sick_leave', 'makeup_exam', or 'general'
        student_name: Name of the student
        student_roll: Student Roll Number
        dates: Specific dates if mentioned
        
    Returns:
        Dict with email fields: To, Subject, Body, and instructor details.
    """
    inst_info = get_instructor_email(course_code=course_code)
    
    if inst_info.get("found"):
        to_name = inst_info["instructor_name"]
        to_email = inst_info["instructor_email"]
        course_title = inst_info.get("course_title", course_code)
    else:
        to_name = "Course Instructor"
        to_email = "instructor@iitj.ac.in"
        course_title = course_code
        
    code_upper = course_code.upper().strip()
    
    if email_type == "makeup_exam":
        subject = f"Request for Make-up Examination: {code_upper} ({course_title}) - {student_roll}"
        body = (
            f"Respected {to_name},\n\n"
            f"I am writing to respectfully request permission to appear for a make-up examination for "
            f"{code_upper}: {course_title}.\n\n"
            f"Due to {reason}, I was unable to attend the scheduled examination. "
            f"I have attached the necessary supporting medical certificate / documentation for your kind perusal.\n\n"
            f"As per institute academic regulations, I request your approval to be scheduled for the make-up exam.\n\n"
            f"Thank you for your time and understanding.\n\n"
            f"Sincerely,\n"
            f"{student_name}\n"
            f"Roll No: {student_roll}\n"
            f"Department of Computer Science and Engineering\n"
            f"IIT Jodhpur"
        )
    else:  # sick leave / general leave
        days_str = f"for {num_days} days" if num_days else "for medical leave"
        date_str = f" on {dates}" if dates else ""
        subject = f"Application for Sick Leave: {code_upper} ({course_title}) - {student_roll}"
        body = (
            f"Respected {to_name},\n\n"
            f"I am writing to inform you that I am unable to attend classes for {code_upper}: {course_title} "
            f"{days_str}{date_str} due to {reason}.\n\n"
            f"I will ensure that I catch up on all course materials, lecture notes, and assignments covered "
            f"during my absence. I will also submit any required medical fitness certificate upon my return.\n\n"
            f"Kindly grant me leave of absence for this duration.\n\n"
            f"Thank you for your consideration.\n\n"
            f"Sincerely,\n"
            f"{student_name}\n"
            f"Roll No: {student_roll}\n"
            f"Department of Computer Science and Engineering\n"
            f"IIT Jodhpur"
        )
        
    return {
        "status": "drafted",
        "to_name": to_name,
        "to_email": to_email,
        "course_code": code_upper,
        "subject": subject,
        "body": body,
        "note": "Draft ready for student review. Email has NOT been sent."
    }
