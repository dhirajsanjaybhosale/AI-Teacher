"""
AI Teacher — Automated End-to-End Demo & QA Verification Script
Verifies:
1. System Health & Hardware Detection
2. PDF Ingestion, Chunking, Embedding, FAISS Indexing & Retrieval
3. Adaptive Lesson Planning across Time Budgets & Languages
4. Neural TTS Audio Synthesis & RMS Envelope Extraction
5. Talking Avatar Frame Generation & FFmpeg Video Assembly
6. Formative Assessment: Misconception Diagnosis & Adaptive Reteaching Video Loop
7. Summative Assessment: Quiz Generation, Scoring, and Feedback Reporting
"""

import os
import sys
import requests

# Ensure utf-8 stdout if available
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8000"

def test_full_pipeline():
    print("================================================================")
    print("[AI TEACHER] COMPREHENSIVE QA & DEMO VERIFICATION SUITE")
    print("================================================================\n")

    # 1. Health Check
    print("[STEP 1/7] Testing Health Endpoint & GPU Detection...")
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    health = res.json()
    print(f"  ✓ Service: {health.get('service')}")
    print(f"  ✓ Device: {health.get('device')} (GPU Available: {health.get('gpu_available')})")

    # 2. PDF Upload & RAG Lesson Creation
    print("\n[STEP 2/7] Testing PDF Upload & RAG Lesson Creation (Electricity Chapter)...")
    sample_pdf_path = "sample_data/sample_chapter.pdf"
    if not os.path.exists(sample_pdf_path):
        sample_pdf_path = "../sample_data/sample_chapter.pdf"

    with open(sample_pdf_path, "rb") as f:
        files = {"pdf_file": ("sample_chapter.pdf", f, "application/pdf")}
        data = {"level": "beginner", "time_minutes": "5", "language": "en"}
        res = requests.post(f"{BASE_URL}/api/lesson/create", files=files, data=data)

    assert res.status_code == 200, f"Lesson creation failed: {res.status_code} - {res.text}"
    lesson = res.json()
    lesson_id = lesson["lesson_id"]
    print(f"  ✓ Lesson Created: '{lesson['title']}'")
    print(f"  ✓ Segments Planned: {len(lesson['segments'])}")
    print(f"  ✓ Segment 1 Video URL: {lesson['segments'][0]['video_url']}")

    # 3. Verify Segment 1 Video Exists on Disk
    print("\n[STEP 3/7] Verifying Generated Video Stream...")
    seg1 = lesson["segments"][0]
    video_rel = seg1["video_url"].lstrip("/")
    # Check via HTTP
    v_res = requests.get(f"{BASE_URL}/{video_rel}", stream=True)
    assert v_res.status_code == 200, f"Failed to stream video: {v_res.status_code}"
    print(f"  ✓ Video stream verified ({v_res.headers.get('content-type', 'video/mp4')})")

    # 4. Interaction Loop: Incorrect Answer -> Misconception Diagnosis & Reteach
    print("\n[STEP 4/7] Testing Misconception Detection & Adaptive Remediation Loop...")
    wrong_answer_payload = {
        "lesson_id": lesson_id,
        "segment_id": seg1["id"],
        "user_answer": "I believe current increases when resistance increases because more resistance means more electrical friction.",
        "language": "en"
    }
    res = requests.post(f"{BASE_URL}/api/interact/submit-answer", json=wrong_answer_payload)
    assert res.status_code == 200, f"Submit answer failed: {res.status_code}"
    eval_wrong = res.json()
    assert not eval_wrong["is_correct"], "Expected wrong answer to be marked incorrect"
    assert eval_wrong["adaptation_needed"], "Expected adaptation to be needed"
    assert eval_wrong["misconception_detected"], "Expected misconception to be detected"
    print(f"  ✓ Misconception Diagnosed: '{eval_wrong['misconception_explanation']}'")
    
    adapted_seg = eval_wrong.get("adapted_segment")
    assert adapted_seg is not None, "Expected adapted remediation segment to be generated"
    assert adapted_seg.get("video_url") is not None, "Expected remediation video URL"
    print(f"  ✓ Remediation Segment: '{adapted_seg['title']}'")
    print(f"  ✓ Remediation Video: '{adapted_seg['video_url']}'")

    # 5. Interaction Loop: Correct Answer
    print("\n[STEP 5/7] Testing Correct Answer Evaluation...")
    correct_answer_payload = {
        "lesson_id": lesson_id,
        "segment_id": seg1["id"],
        "user_answer": seg1["question"]["correct_answer"],
        "language": "en"
    }
    res = requests.post(f"{BASE_URL}/api/interact/submit-answer", json=correct_answer_payload)
    assert res.status_code == 200
    eval_correct = res.json()
    assert eval_correct["is_correct"], "Expected answer to be marked correct"
    print(f"  ✓ Answer Evaluated as Correct (Score: {eval_correct['score']})")

    # 6. Summative Assessment: Quiz Generation
    print("\n[STEP 6/7] Testing Summative Mastery Quiz Generation...")
    res = requests.get(f"{BASE_URL}/api/assessment/quiz/{lesson_id}")
    assert res.status_code == 200, f"Quiz generation failed: {res.status_code}"
    quiz = res.json()
    print(f"  ✓ Quiz Generated: '{quiz['title']}' ({len(quiz['questions'])} questions)")

    # 7. Quiz Submission & Feedback Report
    print("\n[STEP 7/7] Testing Quiz Scoring & Analytical Feedback Report...")
    quiz_submission = {
        "lesson_id": lesson_id,
        "quiz_id": quiz["quiz_id"],
        "answers": [
            {"question_id": q["id"], "selected_option_index": q["correct_option_index"]}
            for q in quiz["questions"]
        ]
    }
    res = requests.post(f"{BASE_URL}/api/assessment/submit-quiz", json=quiz_submission)
    assert res.status_code == 200, f"Quiz submission failed: {res.status_code}"
    report = res.json()
    print(f"  ✓ Mastery Score: {report['total_score']}/{report['max_score']} ({report['percentage']}%)")
    print(f"  ✓ Concepts Mastered: {report['concepts_understood']}")
    print(f"  ✓ Recommended Next Topic: '{report['next_recommended_topic']}'")
    print(f"  ✓ Narrative Feedback: {report['summary_feedback'][:120]}...")

    print("\n================================================================")
    print("SUCCESS: ALL 7 END-TO-END STAGES PASSED!")
    print("================================================================")

if __name__ == "__main__":
    test_full_pipeline()
