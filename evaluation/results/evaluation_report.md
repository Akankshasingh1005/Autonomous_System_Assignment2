# 📊 Academic Helpdesk Agent — Evaluation Report
**Generated on:** 2026-10-29 14:23:55
**Evaluated Prompts:** 25 test cases
**Target System:** IIT Jodhpur Multi-Agent Academic Helpdesk

## 1. Quantitative Performance Metrics
| Metric | Multi-Agent (Qwen3-8B) | Multi-Agent (Llama 3.1 8B) | Base Single-Agent | Target |
|---|---|---|---|---|
| **Intent Routing Accuracy** | 100.0% | 100.0% | N/A (Monolithic) | ≥ 95% |
| **Answer Accuracy** | 100.0% | 100.0% | 80.0% | ≥ 90% |
| **Groundedness (Citations)** | 100.0% | 100.0% | 83.33% | 100% |
| **Out-of-Scope Refusal Rate** | 100.0% | 100.0% | 100.0% | 100% |
| **Unanswered Logs Recorded** | 62 entries | 62 entries | 62 entries | Persistent |

## 2. Comparative Analysis: Multi-Agent vs. Base Single-Agent
- **Specialization vs Monolithic Design:** The Multi-Agent Orchestrator routes each query to an expert sub-agent (`PolicyAgent`, `ScheduleAgent`, `EmailAgent`), preventing context clutter and tool hallucination.
- **Tool Efficiency:** In the base single-agent, RAG search is occasionally invoked unnecessarily for timetable questions or course catalog queries, adding latency and noise. In contrast, the `ScheduleAgent` queries indexed structured CSV data directly.
- **Out-of-Scope Isolation:** The Orchestrator intercepts non-academic questions (dining, transport, city center, weather) immediately, avoiding expensive RAG embedding queries and ensuring zero hallucination.

## 3. Cross-Run & Model Consistency Analysis
All answers remained strictly deterministic and consistent across both model configurations.

## 4. Detailed Test Case Results

| ID | Category | Question | Expected Agent | Actual Agent | Citations Grounded | Status |
|---|---|---|---|---|---|---|
| `T01` | policy | What is the attendance requirement to sit in the Major exam? | `PolicyAgent` | `PolicyAgent` | Yes | ✅ PASS |
| `T02` | schedule | What is the slot for the course Autonomous Systems? | `ScheduleAgent` | `ScheduleAgent` | Yes | ✅ PASS |
| `T03` | course_catalog | How many 400 level electives have been floated by the Humanities department in this semester? | `ScheduleAgent` | `ScheduleAgent` | Yes | ✅ PASS |
| `T04` | curriculum | How many Open Elective credits do I need to earn in order to get a B.Tech. Degree? | `PolicyAgent` | `PolicyAgent` | Yes | ✅ PASS |
| `T05` | email | Write an email to the course instructor of CSL7570 that I need leave for 2 days | `EmailAgent` | `EmailAgent` | Yes | ✅ PASS |
| `T06` | refusal | What are the available dining options on the campus? | `Orchestrator` | `Orchestrator` | Yes | ✅ PASS |
| `T07` | refusal | What is the best way to reach the campus from Jodhpur city center? | `Orchestrator` | `Orchestrator` | Yes | ✅ PASS |
| `T08` | schedule | What is the slot and classroom for Operating Systems? | `ScheduleAgent` | `ScheduleAgent` | Yes | ✅ PASS |
| `T09` | schedule | When does the course Machine Learning meet? | `ScheduleAgent` | `ScheduleAgent` | Yes | ✅ PASS |
| `T10` | policy | What is the policy for make-up examinations if I miss an exam due to illness? | `PolicyAgent` | `PolicyAgent` | Yes | ✅ PASS |
| `T11` | email | Draft an email to instructor of CSL3060 requesting a makeup exam due to illness | `EmailAgent` | `EmailAgent` | Yes | ✅ PASS |
| `T12` | refusal | What is the weather forecast for Jodhpur this weekend? | `Orchestrator` | `Orchestrator` | Yes | ✅ PASS |
| `T13` | refusal | Can I order food delivery to the hostel from outside restaurants? | `Orchestrator` | `Orchestrator` | Yes | ✅ PASS |
| `T14` | course_catalog | How many courses are floated in this semester by the Electrical Engineering department? | `ScheduleAgent` | `ScheduleAgent` | Yes | ✅ PASS |
| `T15` | policy | What happens if a student remains absent from class without sanctioned leave for more than two weeks? | `PolicyAgent` | `PolicyAgent` | Yes | ✅ PASS |
| `T16` | policy | What is the duration and weightage of the Major examination as per the 2024 examination amendment? | `PolicyAgent` | `PolicyAgent` | Yes | ✅ PASS |
| `T17` | schedule | What is the slot and timing for Thermodynamics MEL3010? | `ScheduleAgent` | `ScheduleAgent` | Yes | ✅ PASS |
| `T18` | email | Write an email to Dr. Sunita Patel for CSL4010 asking for 3 days leave | `EmailAgent` | `EmailAgent` | Yes | ✅ PASS |
| `T19` | refusal | Where can I buy movie tickets near the IIT Jodhpur campus? | `Orchestrator` | `Orchestrator` | Yes | ✅ PASS |
| `T20` | refusal | Is there a direct bus or cab service to Jodhpur railway station from campus? | `Orchestrator` | `Orchestrator` | Yes | ✅ PASS |
| `T21` | policy | What is the rule regarding semester withdrawal if a student is absent for four or more weeks? | `PolicyAgent` | `PolicyAgent` | Yes | ✅ PASS |
| `T22` | schedule | What is the slot and instructor for Reinforcement Learning CSL7580? | `ScheduleAgent` | `ScheduleAgent` | Yes | ✅ PASS |
| `T23` | course_catalog | How many courses are floated in this semester by the Mechanical Engineering department? | `ScheduleAgent` | `ScheduleAgent` | Yes | ✅ PASS |
| `T24` | email | Write an email to the course instructor of MEL3010 that I need leave for 4 days | `EmailAgent` | `EmailAgent` | Yes | ✅ PASS |
| `T25` | refusal | What are the best sightseeing tourist places in Jodhpur city? | `Orchestrator` | `Orchestrator` | Yes | ✅ PASS |

## 5. Inferences & Key Findings
1. **RAG Groundedness:** Every policy and curriculum answer strictly quotes the Senate circulars (e.g. `amendment_attendance_policy_2024.pdf`, `amendment_examination_policy_2024.pdf`, `academic_regulations_iitj_2019.pdf`) and includes explicit page citations.
2. **Zero-Hallucination Out-of-Scope Handling:** The agent achieves a 100% refusal rate on non-academic inquiries (campus dining, city transport, weather) and logs all such instances to `logs/unanswered_questions.jsonl` for human intervention.
3. **Email Generation Accuracy:** Formal email drafts correctly identify course instructors and institutional emails (`rahul.sharma@iitj.ac.in`, `ankit.verma@iitj.ac.in`), formatting polite academic correspondence ready for student review.
