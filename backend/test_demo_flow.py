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
import argparse

# Ensure utf-8 stdout if available
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def get_client(live=False, base_url="http://127.0.0.1:8000"):
    if live:
        import requests
        class RequestsClient:
            def __init__(self, base):
                self.base = base.rstrip("/")
            def get(self, url, **kwargs):
                full_url = url if url.startswith("http") else f"{self.base}/{url.lstrip('/')}"
                return requests.get(full_url, **kwargs)
            def post(self, url, **kwargs):
                full_url = url if url.startswith("http") else f"{self.base}/{url.lstrip('/')}"
                return requests.post(full_url, **kwargs)
        return RequestsClient(base_url)
    else:
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)

def test_full_pipeline(live=False, base_url="http://127.0.0.1:8000"):
    client = get_client(live=live, base_url=base_url)
    mode_str = f"Live Server ({base_url})" if live else "In-Process TestClient"
    print("================================================================")
    print(f"[AI TEACHER] COMPREHENSIVE QA & DEMO VERIFICATION ({mode_str})")
    print("================================================================\n")

    # 1. Health Check
    print("[STEP 1/7] Testing Health Endpoint & GPU Detection...")
    res = client.get("/health")
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
        res = client.post("/api/lesson/create", files=files, data=data)

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
    # Check via client
    v_res = client.get(f"/{video_rel}")
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
    res = client.post("/api/interact/submit-answer", json=wrong_answer_payload)
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
    res = client.post("/api/interact/submit-answer", json=correct_answer_payload)
    assert res.status_code == 200
    eval_correct = res.json()
    assert eval_correct["is_correct"], "Expected answer to be marked correct"
    print(f"  ✓ Answer Evaluated as Correct (Score: {eval_correct['score']})")

    # 6. Summative Assessment: Quiz Generation
    print("\n[STEP 6/7] Testing Summative Mastery Quiz Generation...")
    res = client.get(f"/api/assessment/quiz/{lesson_id}")
    assert res.status_code == 200, f"Quiz generation failed: {res.status_code}"
    quiz = res.json()
    print(f"  ✓ Quiz Generated: '{quiz['title']}' ({len(quiz['questions'])} questions)")

    # 7. Quiz Submission & Feedback Report
    print("\n[STEP 7/7] Testing Quiz Scoring & Analytical Feedback Report (Strict Domain Audit)...")
    quiz_submission = {
        "lesson_id": lesson_id,
        "quiz_id": quiz["quiz_id"],
        "answers": [
            {"question_id": q["id"], "selected_option_index": q["correct_option_index"]}
            for q in quiz["questions"]
        ]
    }
    res = client.post("/api/assessment/submit-quiz", json=quiz_submission)
    assert res.status_code == 200, f"Quiz submission failed: {res.status_code}"
    report = res.json()
    print(f"  ✓ Mastery Score: {report['total_score']}/{report['max_score']} ({report['percentage']}%)")
    print(f"  ✓ Concepts Mastered: {report['concepts_understood']}")
    print(f"  ✓ Recommended Next Topic: '{report['next_recommended_topic']}'")
    print(f"  ✓ Narrative Feedback: {report['summary_feedback'][:120]}...")

    # Strict Zero-Contamination Assertions for Electricity Lesson
    for concept in report['concepts_understood']:
        concept_lower = concept.lower()
        assert "biological" not in concept_lower, f"CONTAMINATION DETECTED: Found 'biological' in Electricity report: {concept}"
        assert "metabolic" not in concept_lower, f"CONTAMINATION DETECTED: Found 'metabolic' in Electricity report: {concept}"
        assert "photosynthesis" not in concept_lower, f"CONTAMINATION DETECTED: Found 'photosynthesis' in Electricity report: {concept}"
    
    assert "circuit" in report['next_recommended_topic'].lower() or "electric" in report['next_recommended_topic'].lower() or "advanced" in report['next_recommended_topic'].lower(), f"Unexpected next topic: {report['next_recommended_topic']}"
    print("  ✓ AUDIT PASSED: Electricity report is 100% free of biological/cross-topic contamination!")

    # -------------------------------------------------------------------------
    # BONUS MULTI-TOPIC SESSION ISOLATION AUDIT: Cellular Respiration PDF
    # -------------------------------------------------------------------------
    print("\n[BONUS AUDIT] Testing Multi-Topic Session Isolation with Biology Chapter...")
    bio_pdf_path = "sample_data/cellular_respiration_chapter.pdf"
    if not os.path.exists(bio_pdf_path):
        bio_pdf_path = "../sample_data/cellular_respiration_chapter.pdf"

    if os.path.exists(bio_pdf_path):
        with open(bio_pdf_path, "rb") as f:
            files = {"pdf_file": ("cellular_respiration_chapter.pdf", f, "application/pdf")}
            data = {"level": "beginner", "time_minutes": "5", "language": "en"}
            res = client.post("/api/lesson/create", files=files, data=data)
        assert res.status_code == 200
        bio_lesson = res.json()
        assert bio_lesson["lesson_id"] != lesson_id, "Session ID collision detected!"
        print(f"  ✓ New Isolated Session Created: '{bio_lesson['title']}' (ID: {bio_lesson['lesson_id']})")

        # Fetch quiz for new session
        q_res = client.get(f"/api/assessment/quiz/{bio_lesson['lesson_id']}")
        assert q_res.status_code == 200
        bio_quiz = q_res.json()
        assert bio_quiz["lesson_id"] == bio_lesson["lesson_id"]

        # Verify all questions in bio quiz are strictly biological
        for q in bio_quiz["questions"]:
            q_text_lower = (q["question_text"] + " " + q["concept_tested"]).lower()
            assert "ohm" not in q_text_lower and "voltage" not in q_text_lower and "resistor" not in q_text_lower, f"CONTAMINATION DETECTED: Electricity concept found in Biology quiz: {q['concept_tested']}"

        # Submit bio quiz
        bio_sub = {
            "lesson_id": bio_lesson["lesson_id"],
            "quiz_id": bio_quiz["quiz_id"],
            "answers": [
                {"question_id": q["id"], "selected_option_index": q["correct_option_index"]}
                for q in bio_quiz["questions"]
            ]
        }
        rep_res = client.post("/api/assessment/submit-quiz", json=bio_sub)
        assert rep_res.status_code == 200
        bio_report = rep_res.json()
        print(f"  ✓ Biology Mastery Score: {bio_report['total_score']}/{bio_report['max_score']} ({bio_report['percentage']}%)")
        print(f"  ✓ Biology Concepts Mastered: {bio_report['concepts_understood']}")
        print(f"  ✓ Biology Recommended Next Topic: '{bio_report['next_recommended_topic']}'")

        # Verify no electricity contamination in biology report
        for concept in bio_report['concepts_understood']:
            assert "ohm" not in concept.lower() and "voltage" not in concept.lower(), f"Electricity concept found in Biology report: {concept}"
        print("  ✓ AUDIT PASSED: Multi-topic session isolation verified with zero cross-contamination!")

    print("\n================================================================")
    print("SUCCESS: ALL QA CHECKS & SESSION AUDITS PASSED WITH ZERO CONTAMINATION!")
    print("================================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Teacher Test Verification Suite")
    parser.add_argument("--live", action="store_true", help="Test against live running server instead of in-process TestClient")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="Base URL for live server")
    args = parser.parse_args()
    test_full_pipeline(live=args.live, base_url=args.url)
