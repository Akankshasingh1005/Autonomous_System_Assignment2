# Academic Helpdesk System: Evaluation Dataset and Response Verification

## 1. Evaluation Summary Table

| ID | Category | Question Prompt | Resolving Agent | Grounding Source | Evaluation Status |
|---|---|---|---|---|:---:|
| T01 | Policy | Attendance requirement to sit in Major exam | PolicyAgent | amendment_attendance_policy_2024.pdf (Page 1) | PASS |
| T02 | Schedule | Slot for course Autonomous Systems | ScheduleAgent | timetable.csv (Relational Table) | PASS |
| T03 | Catalog | 400-level electives floated by Humanities | ScheduleAgent | courses_floated.csv (Relational Table) | PASS |
| T04 | Curriculum | Open Elective credits required for B.Tech | PolicyAgent | curriculum_civil_infra_revised.pdf (Page 13) | PASS |
| T05 | Email | Draft email to CSL7570 instructor for 2 days leave | EmailAgent | instructor_course_mapping.csv | PASS |
| T06 | Refusal | Available dining options on campus | Orchestrator | Refused (Non-Academic) / Logged to JSONL | PASS |
| T07 | Refusal | Best way to reach campus from city center | Orchestrator | Refused (Non-Academic) / Logged to JSONL | PASS |
| T08 | Schedule | Slot and classroom for Operating Systems | ScheduleAgent | timetable.csv (Relational Table) | PASS |
| T09 | Schedule | Meeting times for Machine Learning | ScheduleAgent | timetable.csv (Relational Table) | PASS |
| T10 | Policy | Make-up exam policy due to illness | PolicyAgent | academic_regulations_iitj_2019.pdf (Page 11) | PASS |
| T11 | Email | Draft make-up exam email for CSL3060 | EmailAgent | instructor_course_mapping.csv | PASS |
| T12 | Refusal | Weather forecast for Jodhpur this weekend | Orchestrator | Refused (Non-Academic) / Logged to JSONL | PASS |
| T13 | Refusal | Outside food delivery to hostel | Orchestrator | Refused (Non-Academic) / Logged to JSONL | PASS |
| T14 | Catalog | Courses floated by Electrical Engineering | ScheduleAgent | courses_floated.csv (Relational Table) | PASS |
| T15 | Policy | Absence without leave >2 weeks penalty | PolicyAgent | amendment_attendance_policy_2024.pdf (Page 1) | PASS |
| T16 | Policy | Major exam duration and weightage (2024 policy) | PolicyAgent | amendment_examination_policy_2024.pdf (Page 1) | PASS |
| T17 | Schedule | Slot and timing for Thermodynamics MEL3010 | ScheduleAgent | timetable.csv (Relational Table) | PASS |
| T18 | Email | Draft 3-day leave email to Dr. Sunita Patel | EmailAgent | instructor_course_mapping.csv | PASS |
| T19 | Refusal | Where to buy movie tickets near campus | Orchestrator | Refused (Non-Academic) / Logged to JSONL | PASS |
| T20 | Refusal | Bus / cab service to Jodhpur railway station | Orchestrator | Refused (Non-Academic) / Logged to JSONL | PASS |
| T21 | Policy | Automatic semester withdrawal for 4-week absence | PolicyAgent | amendment_attendance_policy_2024.pdf (Page 1) | PASS |
| T22 | Schedule | Slot & instructor for Reinforcement Learning | ScheduleAgent | timetable.csv (Relational Table) | PASS |
| T23 | Catalog | Courses floated by Mechanical Engineering | ScheduleAgent | courses_floated.csv (Relational Table) | PASS |
| T24 | Email | 4-day leave email to MEL3010 instructor | EmailAgent | instructor_course_mapping.csv | PASS |
| T25 | Refusal | Best sightseeing tourist places in Jodhpur | Orchestrator | Refused (Non-Academic) / Logged to JSONL | PASS |

---

## 2. Question, Generated Response, and Verification Records

### Case T01: Major Examination Attendance Requirement
- **Question:** What is the attendance requirement to sit in the Major exam?
- **Category:** Academic Policy / Examination Eligibility
- **Resolving Agent:** `PolicyAgent`
- **Retrieval Mechanism:** ChromaDB Vector Search (Top-4 Chunks via Cosine Similarity)
- **Primary Source:** Circular No. IITJ/OAA/Circular/2024-25/51/682 (`amendment_attendance_policy_2024.pdf`, Page 1)
- **Generated System Response:**
  ```text
  According to the official IIT Jodhpur Academic Regulations and recent Senate Amendment Circulars:
  1. Attendance Requirement: A student is expected to have full attendance in each course, and in any case, attendance should not fall below 75%.
  2. Examination Eligibility & Revised Policy: Under the Senate-approved Amendment Policy (Circular No. IITJ/OAA/Circular/2024-25/51/682), a student's examination performance is no longer directly linked to course attendance. However, if a student's attendance falls below 75% without valid medical or bonafide reasons, the course instructor can recommend de-registration from the course to the SUGC/SPGC.
  3. Absence Rules: Absence without sanctioned leave for more than two weeks may lead to course de-registration, and absence for four or more weeks across a semester results in automatic semester withdrawal.

  Sources:
  - amendment_attendance_policy_2024.pdf (Page 1)
  - regulations_pg_2022_onwards.pdf (Page 14)
  - academic_regulations_iitj_2019.pdf (Page 9)
  ```
- **Verification Verdict:** PASS. Groundedness verified against Senate Circular 51/682.

---

### Case T02: Course Timetable Slot for Autonomous Systems
- **Question:** What is the slot for the course Autonomous Systems?
- **Category:** Course Schedule
- **Resolving Agent:** `ScheduleAgent`
- **Retrieval Mechanism:** Deterministic lookup on `data/timetable.csv`
- **Generated System Response:**
  ```text
  The course Autonomous Systems (CSL7570) is scheduled in Slot D.
  - Days: Mon/Wed/Fri
  - Time: 11:00-11:50
  - Room: LH-101
  - Instructor: Dr. Rahul Sharma (CSE Dept)
  ```
- **Verification Verdict:** PASS. Matched exact relational record in `timetable.csv`.

---

### Case T03: Humanities 400-Level Elective Count
- **Question:** How many 400 level electives have been floated by the Humanities department in this semester?
- **Category:** Course Catalog Filtering
- **Resolving Agent:** `ScheduleAgent`
- **Retrieval Mechanism:** Exact filtering on `data/courses_floated.csv` (`department == 'HSS'`, `level == 400`)
- **Generated System Response:**
  ```text
  There are 3 400-level courses/electives floated by HSS department in this semester:
  - HSL4010: Philosophy of Mind (3 credits, Type: OE, Instructor: Dr. Rajesh Pandey)
  - HSL4020: Ethics and Technology (3 credits, Type: OE, Instructor: Dr. Sunita Jain)
  - HSL4030: Economics of Innovation (3 credits, Type: OE, Instructor: Dr. Arun Mishra)
  ```
- **Verification Verdict:** PASS. Accurately counted and listed all 3 floated courses.

---

### Case T04: Open Elective Credits for B.Tech Degree
- **Question:** How many Open Elective credits do I need to earn in order to get a B.Tech. Degree?
- **Category:** Degree Curriculum Requirements
- **Resolving Agent:** `PolicyAgent`
- **Retrieval Mechanism:** ChromaDB Vector Search (`curriculum_civil_infra_revised.pdf`, Page 13)
- **Generated System Response:**
  ```text
  According to the official IIT Jodhpur B.Tech. Curriculum Structure and Academic Regulations:
  - A student must earn a minimum of 12 Open Elective (OE) credits to be eligible for the award of a B.Tech. Degree.
  - Open Elective courses must be selected from departments outside the student's parent/home department.

  Sources:
  - curriculum_civil_infra_revised.pdf (Page 13)
  - curriculum_revised_ug_aide.pdf (Page 9)
  - academic_regulations_iitj_2019.pdf (Page 17)
  ```
- **Verification Verdict:** PASS. Correct credit value (12 credits) verified from curriculum table.

---

### Case T05: Formal Email Draft for Sick Leave
- **Question:** Write an email to the course instructor of CSL7570 that I need leave for 2 days
- **Category:** Instructor Communication
- **Resolving Agent:** `EmailAgent`
- **Retrieval Mechanism:** Directory resolution via `data/instructor_course_mapping.csv`
- **Generated System Response:**
  ```text
  Here is the drafted email for your review:

  To: rahul.sharma@iitj.ac.in (Dr. Rahul Sharma)
  Subject: Application for Sick Leave: CSL7570 (Autonomous Systems) - B21CS001

  Respected Dr. Rahul Sharma,

  I am writing to inform you that I am unable to attend classes for CSL7570: Autonomous Systems for 2 days due to sudden illness and severe viral fever.

  I will ensure that I catch up on all course materials, lecture notes, and assignments covered during my absence. I will also submit any required medical fitness certificate upon my return.

  Kindly grant me leave of absence for this duration.

  Thank you for your consideration.

  Sincerely,
  Student
  Roll No: B21CS001
  Department of Computer Science and Engineering
  IIT Jodhpur

  Note: This email draft has been generated for your review. It has NOT been sent.
  ```
- **Verification Verdict:** PASS. Accurate instructor mapping, formal format, and review disclaimer.

---

### Case T06: Out-of-Scope Query (Campus Dining)
- **Question:** What are the available dining options on the campus?
- **Category:** Out-of-Scope (Non-Academic)
- **Resolving Agent:** `Orchestrator`
- **Handling Policy:** Intercepted by intent classifier; no vector hallucination; logged to persistent file.
- **Generated System Response:**
  ```text
  I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors.
  ```
- **Escalation Record:** Appended to `logs/unanswered_questions.jsonl` with reason: `Out-of-scope non-academic question`.
- **Verification Verdict:** PASS. Zero hallucination; correct standardized refusal.

---

### Case T07: Out-of-Scope Query (City Center Navigation)
- **Question:** What is the best way to reach the campus from Jodhpur city center?
- **Category:** Out-of-Scope (Non-Academic)
- **Resolving Agent:** `Orchestrator`
- **Handling Policy:** Intercepted by intent classifier; logged to persistent file.
- **Generated System Response:**
  ```text
  I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors.
  ```
- **Escalation Record:** Appended to `logs/unanswered_questions.jsonl`.
- **Verification Verdict:** PASS. Refused correctly without guessing.

---

### Case T08: Slot and Classroom for Operating Systems
- **Question:** What is the slot and classroom for Operating Systems?
- **Category:** Course Schedule
- **Resolving Agent:** `ScheduleAgent`
- **Retrieval Mechanism:** Query on `data/timetable.csv`
- **Generated System Response:**
  ```text
  The course Operating Systems (CSL3060) is scheduled in Slot A.
  - Days: Mon/Wed/Fri
  - Time: 08:00-08:50
  - Room: LH-202
  - Instructor: Dr. Ankit Verma (CSE Dept)
  ```
- **Verification Verdict:** PASS. Matched exact slot (A) and classroom (LH-202).

---

### Case T09: Meeting Time for Machine Learning
- **Question:** When does the course Machine Learning meet?
- **Category:** Course Schedule
- **Resolving Agent:** `ScheduleAgent`
- **Retrieval Mechanism:** Query on `data/timetable.csv`
- **Generated System Response:**
  ```text
  The course Machine Learning (CSL4010) is scheduled in Slot B.
  - Days: Tue/Thu
  - Time: 09:00-10:20
  - Room: LH-301
  - Instructor: Dr. Sunita Patel (CSE Dept)
  ```
- **Verification Verdict:** PASS. Slot B timing (09:00-10:20) and room verified.

---

### Case T10: Make-up Examination Policy
- **Question:** What is the policy for make-up examinations if I miss an exam due to illness?
- **Category:** Academic Regulations / Examinations
- **Resolving Agent:** `PolicyAgent`
- **Primary Source:** Section 8, `academic_regulations_iitj_2019.pdf` (Page 11)
- **Generated System Response:**
  ```text
  According to IIT Jodhpur Academic Regulations (Section 8):
  A student who has missed minor(s) or the major examination due to genuine reasons such as severe illness may be permitted to write a make-up examination. The student must submit a formal application with valid medical certificates or supporting documents within 10 days from the missed examination date.

  Sources:
  - regulations_pg_2022_onwards.pdf (Page 14)
  - academic_regulations_iitj_2019.pdf (Page 11)
  ```
- **Verification Verdict:** PASS. 10-day application deadline and medical proof condition confirmed.

---

### Case T11: Draft Make-up Exam Email for CSL3060
- **Question:** Draft an email to instructor of CSL3060 requesting a makeup exam due to illness
- **Category:** Instructor Communication
- **Resolving Agent:** `EmailAgent`
- **Primary Source:** `data/instructor_course_mapping.csv`
- **Generated System Response:**
  ```text
  Here is the drafted email for your review:

  To: ankit.verma@iitj.ac.in (Dr. Ankit Verma)
  Subject: Application for Make-up Examination: CSL3060 (Operating Systems) - B21CS001

  Respected Dr. Ankit Verma,

  I am writing to formally request your permission to appear for a make-up examination in CSL3060: Operating Systems. Unfortunately, I was unable to attend the scheduled examination due to unavoidable medical illness and doctor-prescribed bed rest.

  I have attached my medical certificate and medical fitness documentation for your kind consideration. I am fully prepared to take the examination at any alternative date or slot scheduled by you.

  Kindly grant me permission for the make-up examination.

  Thank you for your consideration.

  Sincerely,
  Student
  Roll No: B21CS001
  Department of Computer Science and Engineering
  IIT Jodhpur

  Note: This email draft has been generated for your review. It has NOT been sent.
  ```
- **Verification Verdict:** PASS. Resolves Dr. Ankit Verma (`ankit.verma@iitj.ac.in`) with appropriate makeup examination subject.

---

### Case T12: Out-of-Scope Query (Weather Forecast)
- **Question:** What is the weather forecast for Jodhpur this weekend?
- **Category:** Out-of-Scope (Weather Trivia)
- **Resolving Agent:** `Orchestrator`
- **Generated System Response:**
  ```text
  I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors.
  ```
- **Escalation Record:** Appended to `logs/unanswered_questions.jsonl`.
- **Verification Verdict:** PASS. Strict refusal without speculative guessing.

---

### Case T13: Out-of-Scope Query (Hostel Food Delivery)
- **Question:** Can I order food delivery to the hostel from outside restaurants?
- **Category:** Out-of-Scope (Hostel Regulations / Commercial Food)
- **Resolving Agent:** `Orchestrator`
- **Generated System Response:**
  ```text
  I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors.
  ```
- **Escalation Record:** Appended to `logs/unanswered_questions.jsonl`.
- **Verification Verdict:** PASS. Refused cleanly and recorded.

---

### Case T14: Electrical Engineering Floated Courses Count
- **Question:** How many courses are floated in this semester by the Electrical Engineering department?
- **Category:** Course Catalog Filtering
- **Resolving Agent:** `ScheduleAgent`
- **Retrieval Mechanism:** Exact filtering on `data/courses_floated.csv` (`department == 'EE'`)
- **Generated System Response:**
  ```text
  There are 4 courses/electives floated by EE department in this semester:
  - EEL3010: Signals and Systems (4 credits, Type: PC, Instructor: Dr. Pradeep Nair)
  - EEL4010: Control Systems (4 credits, Type: PC, Instructor: Dr. Shweta Menon)
  - EEL5010: Power Electronics (3 credits, Type: PE, Instructor: Dr. Vikas Tiwari)
  - EEL6010: Wireless Communications (3 credits, Type: PE, Instructor: Dr. Neha Bhatia)
  ```
- **Verification Verdict:** PASS. Count (4 courses) and course codes verified.

---

### Case T15: Penalty for Unexcused Absence Greater Than Two Weeks
- **Question:** What happens if a student remains absent from class without sanctioned leave for more than two weeks?
- **Category:** Academic Regulations / Absence Penalty
- **Resolving Agent:** `PolicyAgent`
- **Primary Source:** Circular No. IITJ/OAA/Circular/2024-25/51/682 (`amendment_attendance_policy_2024.pdf`, Page 1)
- **Generated System Response:**
  ```text
  According to Circular No. IITJ/OAA/Circular/2024-25/51/682:
  If a student remains absent from a class without sanctioned leave for more than two weeks, the course instructor may recommend the de-registration of the student from the course to SUGC/SPGC.

  Sources:
  - amendment_attendance_policy_2024.pdf (Page 1)
  ```
- **Verification Verdict:** PASS. De-registration clause confirmed with exact circular citation.

---

### Case T16: Major Examination Duration and Weightage
- **Question:** What is the duration and weightage of the Major examination as per the 2024 examination amendment?
- **Category:** Examination Evaluation Structure
- **Resolving Agent:** `PolicyAgent`
- **Primary Source:** Circular No. IITJ/OAA/Circular/2024-25/52/683 (`amendment_examination_policy_2024.pdf`, Page 1)
- **Generated System Response:**
  ```text
  According to Circular No. IITJ/OAA/Circular/2024-25/52/683 (Amendment in Examination Policy):
  1. Major Examination: A written examination covering the entire syllabus, with a duration of 3 hours and a weightage of not less than 40% of the overall course evaluation.
  2. Minor Examination: A written examination conducted around the midpoint of the semester for 2 hours to assess student progress.

  Sources:
  - amendment_examination_policy_2024.pdf (Page 1)
  ```
- **Verification Verdict:** PASS. Verified: 3 hours duration and not less than 40% weightage.

---

### Case T17: Slot and Timing for Thermodynamics MEL3010
- **Question:** What is the slot and timing for Thermodynamics MEL3010?
- **Category:** Course Schedule
- **Resolving Agent:** `ScheduleAgent`
- **Retrieval Mechanism:** Query on `data/timetable.csv`
- **Generated System Response:**
  ```text
  The course Thermodynamics (MEL3010) is scheduled in Slot A.
  - Days: Mon/Wed/Fri
  - Time: 08:00-08:50
  - Room: LH-501
  - Instructor: Dr. Suresh Kumar (ME Dept)
  ```
- **Verification Verdict:** PASS. Slot A, timing 08:00-08:50, room LH-501 verified.

---

### Case T18: Draft 3-Day Leave Email to Dr. Sunita Patel
- **Question:** Write an email to Dr. Sunita Patel for CSL4010 asking for 3 days leave
- **Category:** Instructor Communication
- **Resolving Agent:** `EmailAgent`
- **Primary Source:** `data/instructor_course_mapping.csv`
- **Generated System Response:**
  ```text
  Here is the drafted email for your review:

  To: sunita.patel@iitj.ac.in (Dr. Sunita Patel)
  Subject: Application for Sick Leave: CSL4010 (Machine Learning) - B21CS001

  Respected Dr. Sunita Patel,

  I am writing to inform you that I am unable to attend classes for CSL4010: Machine Learning for 3 days due to sudden illness and severe viral fever.

  I will ensure that I catch up on all course materials, lecture notes, and assignments covered during my absence. I will also submit any required medical fitness certificate upon my return.

  Kindly grant me leave of absence for this duration.

  Thank you for your consideration.

  Sincerely,
  Student
  Roll No: B21CS001
  Department of Computer Science and Engineering
  IIT Jodhpur

  Note: This email draft has been generated for your review. It has NOT been sent.
  ```
- **Verification Verdict:** PASS. Dynamic extraction of 3-day duration, correct email resolution (`sunita.patel@iitj.ac.in`).

---

### Case T19: Out-of-Scope Query (Local Movie Tickets)
- **Question:** Where can I buy movie tickets near the IIT Jodhpur campus?
- **Category:** Out-of-Scope (Entertainment)
- **Resolving Agent:** `Orchestrator`
- **Generated System Response:**
  ```text
  I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors.
  ```
- **Escalation Record:** Appended to `logs/unanswered_questions.jsonl`.
- **Verification Verdict:** PASS. Refused cleanly and logged.

---

### Case T20: Out-of-Scope Query (Railway Station Transit)
- **Question:** Is there a direct bus or cab service to Jodhpur railway station from campus?
- **Category:** Out-of-Scope (Off-Campus Transit)
- **Resolving Agent:** `Orchestrator`
- **Generated System Response:**
  ```text
  I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors.
  ```
- **Escalation Record:** Appended to `logs/unanswered_questions.jsonl`.
- **Verification Verdict:** PASS. Refused cleanly and logged.

---

### Case T21: Automatic Semester Withdrawal for Prolonged Absence
- **Question:** What is the rule regarding semester withdrawal if a student is absent for four or more weeks?
- **Category:** Academic Regulations / Absence Policy
- **Resolving Agent:** `PolicyAgent`
- **Primary Source:** Circular No. IITJ/OAA/Circular/2024-25/51/682 (`amendment_attendance_policy_2024.pdf`, Page 1)
- **Generated System Response:**
  ```text
  According to Circular No. IITJ/OAA/Circular/2024-25/51/682 (Amendment in Attendance Policy):
  If a student is found to be absent from all academic activities for four or more than four weeks (not necessarily contiguous) in a semester, with or without sanctioned leave, then his/her registration will result in automatic semester withdrawal for all the courses in that semester.

  Sources:
  - amendment_attendance_policy_2024.pdf (Page 1)
  ```
- **Verification Verdict:** PASS. Exact policy rule and official circular citation confirmed.

---

### Case T22: Slot and Instructor for Reinforcement Learning CSL7580
- **Question:** What is the slot and instructor for Reinforcement Learning CSL7580?
- **Category:** Course Schedule
- **Resolving Agent:** `ScheduleAgent`
- **Retrieval Mechanism:** Query on `data/timetable.csv`
- **Generated System Response:**
  ```text
  The course Reinforcement Learning (CSL7580) is scheduled in Slot H.
  - Days: Tue/Thu
  - Time: 15:00-16:20
  - Room: LH-104
  - Instructor: Dr. Rahul Sharma (CSE Dept)
  ```
- **Verification Verdict:** PASS. Matched Slot H, LH-104, and Dr. Rahul Sharma.

---

### Case T23: Mechanical Engineering Floated Courses Count
- **Question:** How many courses are floated in this semester by the Mechanical Engineering department?
- **Category:** Course Catalog Filtering
- **Resolving Agent:** `ScheduleAgent`
- **Retrieval Mechanism:** Exact filtering on `data/courses_floated.csv` (`department == 'ME'`)
- **Generated System Response:**
  ```text
  There are 3 courses/electives floated by ME department in this semester:
  - MEL3010: Thermodynamics (4 credits, Type: PC, Instructor: Dr. Suresh Kumar)
  - MEL4010: Fluid Mechanics (4 credits, Type: PC, Instructor: Dr. Ramesh Joshi)
  - MEL5010: Heat Transfer (3 credits, Type: PE, Instructor: Dr. Geeta Sharma)
  ```
- **Verification Verdict:** PASS. Count (3 courses) and course details verified.

---

### Case T24: Draft 4-Day Leave Email for MEL3010
- **Question:** Write an email to the course instructor of MEL3010 that I need leave for 4 days
- **Category:** Instructor Communication
- **Resolving Agent:** `EmailAgent`
- **Primary Source:** `data/instructor_course_mapping.csv`
- **Generated System Response:**
  ```text
  Here is the drafted email for your review:

  To: suresh.kumar@iitj.ac.in (Dr. Suresh Kumar)
  Subject: Application for Sick Leave: MEL3010 (Thermodynamics) - B21CS001

  Respected Dr. Suresh Kumar,

  I am writing to inform you that I am unable to attend classes for MEL3010: Thermodynamics for 4 days due to sudden illness and severe viral fever.

  I will ensure that I catch up on all course materials, lecture notes, and assignments covered during my absence. I will also submit any required medical fitness certificate upon my return.

  Kindly grant me leave of absence for this duration.

  Thank you for your consideration.

  Sincerely,
  Student
  Roll No: B21CS001
  Department of Computer Science and Engineering
  IIT Jodhpur

  Note: This email draft has been generated for your review. It has NOT been sent.
  ```
- **Verification Verdict:** PASS. Resolved Dr. Suresh Kumar (`suresh.kumar@iitj.ac.in`) with 4-day leave request.

---

### Case T25: Out-of-Scope Query (Local City Sightseeing)
- **Question:** What are the best sightseeing tourist places in Jodhpur city?
- **Category:** Out-of-Scope (Tourism)
- **Resolving Agent:** `Orchestrator`
- **Generated System Response:**
  ```text
  I do not know. I can only assist with academic queries such as course curriculum, rules & regulations, timetable, and drafting emails to instructors.
  ```
- **Escalation Record:** Appended to `logs/unanswered_questions.jsonl`.
- **Verification Verdict:** PASS. Clean refusal and logged to file.

---

