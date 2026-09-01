import os
import sys
import io
import asyncio

# Configure utf-8 stdout for Windows consoles
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from fastapi.testclient import TestClient
from main import app
from app.ingestion.knowledge_router import knowledge_router
from app.ingestion.search_retriever import search_retriever

client = TestClient(app)

def test_universal_knowledge_router_and_topics():
    print("\n" + "=" * 70)
    print("[TEST SUITE] UNIVERSAL TOPIC & DYNAMIC KNOWLEDGE ROUTING VERIFICATION")
    print("=" * 70)

    # -------------------------------------------------------------
    # TEST CASE 1: "What is photosynthesis?" (Biology -> LLM)
    # -------------------------------------------------------------
    print("\n[TEST 1/10] Testing: 'What is photosynthesis?'")
    res1 = client.post("/api/lesson/create", data={"topic": "What is photosynthesis?", "level": "beginner", "time_minutes": 10, "language": "en"})
    assert res1.status_code == 200, f"Error: {res1.text}"
    data1 = res1.json()
    print(f"  [OK] Lesson Title: '{data1['title']}' | Subject: {data1['subject']}")
    print(f"  [OK] Segments: {len(data1['segments'])} | Route: {data1.get('source_route')}")
    print(f"  [OK] Visual Type: {data1['segments'][0]['visual_diagram_type']}")
    assert "photosynthesis" in data1['title'].lower() or "photosynthesis" in data1['description'].lower()
    assert data1['segments'][0]['visual_diagram_type'] in ["equation", "process", "diagram"]

    # -------------------------------------------------------------
    # TEST CASE 2: "Explain recursion with an example." (Programming -> Code)
    # -------------------------------------------------------------
    print("\n[TEST 2/10] Testing: 'Explain recursion with an example.'")
    res2 = client.post("/api/lesson/create", data={"topic": "Explain recursion with an example.", "level": "beginner", "time_minutes": 10, "language": "en"})
    assert res2.status_code == 200, f"Error: {res2.text}"
    data2 = res2.json()
    print(f"  [OK] Lesson Title: '{data2['title']}' | Subject: {data2['subject']}")
    print(f"  [OK] Segments: {len(data2['segments'])} | Visual: {data2['segments'][0]['visual_diagram_type']}")
    assert data2['segments'][0]['visual_diagram_type'] in ["code", "process", "flowchart"]
    assert "recursion" in data2['title'].lower()

    # -------------------------------------------------------------
    # TEST CASE 3: "What is blockchain?" (Cryptography / Web3)
    # -------------------------------------------------------------
    print("\n[TEST 3/10] Testing: 'What is blockchain?'")
    res3 = client.post("/api/lesson/create", data={"topic": "What is blockchain?", "level": "beginner", "time_minutes": 10, "language": "en"})
    assert res3.status_code == 200, f"Error: {res3.text}"
    data3 = res3.json()
    print(f"  [OK] Lesson Title: '{data3['title']}' | Subject: {data3['subject']}")
    print(f"  [OK] Segments: {len(data3['segments'])} | Visual: {data3['segments'][0]['visual_diagram_type']}")
    assert "blockchain" in data3['title'].lower()

    # -------------------------------------------------------------
    # TEST CASE 4: "Explain Newton's Second Law." (Physics -> F=ma)
    # -------------------------------------------------------------
    print("\n[TEST 4/10] Testing: 'Explain Newton's Second Law.'")
    res4 = client.post("/api/lesson/create", data={"topic": "Explain Newton's Second Law.", "level": "beginner", "time_minutes": 10, "language": "en"})
    assert res4.status_code == 200, f"Error: {res4.text}"
    data4 = res4.json()
    print(f"  [OK] Lesson Title: '{data4['title']}' | Subject: {data4['subject']}")
    print(f"  [OK] Segments: {len(data4['segments'])} | Visual: {data4['segments'][0]['visual_diagram_type']}")
    assert "physics" in data4['subject'].lower() or "newton" in data4['title'].lower()

    # -------------------------------------------------------------
    # TEST CASE 5: "Teach me Machine Learning." (AI / ML)
    # -------------------------------------------------------------
    print("\n[TEST 5/10] Testing: 'Teach me Machine Learning.'")
    res5 = client.post("/api/lesson/create", data={"topic": "Teach me Machine Learning.", "level": "beginner", "time_minutes": 10, "language": "en"})
    assert res5.status_code == 200, f"Error: {res5.text}"
    data5 = res5.json()
    print(f"  [OK] Lesson Title: '{data5['title']}' | Subject: {data5['subject']}")
    print(f"  [OK] Segments: {len(data5['segments'])}")
    assert "machine learning" in data5['title'].lower() or "ai" in data5['subject'].lower()

    # -------------------------------------------------------------
    # TEST CASE 6: "Explain TCP vs UDP." (Networking -> Comparison)
    # -------------------------------------------------------------
    print("\n[TEST 6/10] Testing: 'Explain TCP vs UDP.'")
    res6 = client.post("/api/lesson/create", data={"topic": "Explain TCP vs UDP.", "level": "beginner", "time_minutes": 10, "language": "en"})
    assert res6.status_code == 200, f"Error: {res6.text}"
    data6 = res6.json()
    print(f"  [OK] Lesson Title: '{data6['title']}' | Subject: {data6['subject']}")
    print(f"  [OK] Visual Type: {data6['segments'][0]['visual_diagram_type']}")
    assert data6['segments'][0]['visual_diagram_type'] in ["comparison", "process"]

    # -------------------------------------------------------------
    # TEST CASE 7: "Explain photosynthesis in Hindi." (Multilingual Hindi)
    # -------------------------------------------------------------
    print("\n[TEST 7/10] Testing: 'Explain photosynthesis in Hindi.' (Intent + Language Auto-Detection)")
    res7 = client.post("/api/lesson/create", data={"topic": "Explain photosynthesis in Hindi.", "level": "beginner", "time_minutes": 10, "language": "hi"})
    assert res7.status_code == 200, f"Error: {res7.text}"
    data7 = res7.json()
    print(f"  [OK] Lesson Title: '{data7['title']}' | Language: {data7['target_language']}")
    assert data7['target_language'] == "hi"

    # -------------------------------------------------------------
    # TEST CASE 8: "What are the latest developments in AI agents?" (External Web Retrieval)
    # -------------------------------------------------------------
    print("\n[TEST 8/10] Testing: 'What are the latest developments in AI agents?' (Temporal Search Trigger)")
    res8 = client.post("/api/lesson/create", data={"topic": "What are the latest developments in AI agents?", "level": "beginner", "time_minutes": 10, "language": "en", "force_web_search": "true"})
    assert res8.status_code == 200, f"Error: {res8.text}"
    data8 = res8.json()
    print(f"  [OK] Lesson Title: '{data8['title']}'")
    print(f"  [OK] Route Type: {data8.get('source_route')}")
    print(f"  [OK] Verified Sources Retrieved: {len(data8.get('sources', []))}")
    for s in data8.get('sources', [])[:2]:
        print(f"     - [{s.get('source')}] {s.get('title')} ({s.get('url', '')[:45]}...)")
    assert data8.get('source_route') == "external_web"
    assert len(data8.get('sources', [])) > 0

    # -------------------------------------------------------------
    # TEST CASE 9: "Why is the sky blue?" (Physics / Optics)
    # -------------------------------------------------------------
    print("\n[TEST 9/10] Testing: 'Why is the sky blue?'")
    res9 = client.post("/api/lesson/create", data={"topic": "Why is the sky blue?", "level": "beginner", "time_minutes": 10, "language": "en"})
    assert res9.status_code == 200, f"Error: {res9.text}"
    data9 = res9.json()
    print(f"  [OK] Lesson Title: '{data9['title']}' | Subject: {data9['subject']}")
    assert "sky" in data9['title'].lower() or "rayleigh" in data9['title'].lower()

    # -------------------------------------------------------------
    # TEST CASE 10: Complete Misconception & Adaptive Remediation Verification
    # -------------------------------------------------------------
    print("\n[TEST 10/10] Testing Incorrect Student Answer -> Misconception Detection -> Adaptive Remediation Video")
    lesson_id = data1['lesson_id']
    seg_id = data1['segments'][0]['id']

    # Step A: Student submits incorrect answer
    ans_res = client.post("/api/interact/submit-answer", json={
        "lesson_id": lesson_id,
        "segment_id": seg_id,
        "user_answer": "Oxygen is created because carbon dioxide gas splits directly under atmospheric friction.",
        "language": "en"
    })
    assert ans_res.status_code == 200, f"Error: {ans_res.text}"
    eval_data = ans_res.json()
    print(f"  [OK] Evaluation Result: is_correct={eval_data['is_correct']}")
    print(f"  [OK] Misconception Diagnosed: '{eval_data['misconception_explanation']}'")
    assert eval_data['misconception_detected'] is True
    assert eval_data['adaptation_needed'] is True
    assert eval_data.get('adapted_segment') is not None
    assert eval_data['adapted_segment'].get('video_url') is not None
    print(f"  [OK] Remediation Video Ready: '{eval_data['adapted_segment']['video_url']}'")

    print("\n" + "=" * 70)
    print("SUCCESS: ALL 10 UNIVERSAL TOPIC & KNOWLEDGE ROUTING TESTS PASSED PERFECTLY!")
    print("=" * 70)

if __name__ == "__main__":
    test_universal_knowledge_router_and_topics()
