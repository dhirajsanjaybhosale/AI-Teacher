import os
import sys
import time

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.lesson_planning.schemas import LearnerPreferences
from app.lesson_planning.planner import lesson_planner
from app.narration_avatar.video_assembler import video_assembler

def run_test_case(topic: str, duration_mins: int, language: str):
    print(f"\n================================================================================")
    print(f"RUNNING TEST: Topic='{topic}' | Requested Duration={duration_mins} mins ({duration_mins*60}s) | Language='{language}'")
    print(f"================================================================================")
    
    prefs = LearnerPreferences(
        topic=topic,
        level="intermediate",
        time_minutes=duration_mins,
        language=language,
        goal="understand",
        teaching_style="Visual"
    )

    t0 = time.time()
    lesson = lesson_planner.plan_lesson(preferences=prefs)
    plan_time = time.time() - t0

    target_sec = duration_mins * 60
    total_audio_sec = sum(getattr(s, "actual_seconds", 0.0) for s in lesson.segments)
    total_thinking_sec = sum(getattr(s, "thinking_seconds", 0) for s in lesson.segments)
    total_experience_sec = lesson.actual_duration_seconds or (total_audio_sec + total_thinking_sec)

    tolerance_min = target_sec * 0.90
    tolerance_max = target_sec * 1.10
    is_within_tolerance = tolerance_min <= total_experience_sec <= tolerance_max

    print(f"\n[LESSON PLAN GENERATED in {plan_time:.2f}s]")
    print(f"  Title: {lesson.title}")
    print(f"  Total Modules: {len(lesson.segments)}")
    print(f"  Target Duration: {target_sec}s ({duration_mins} min)")
    print(f"  Actual Audio Duration: {total_audio_sec:.1f}s")
    print(f"  Formative Thinking Time: {total_thinking_sec}s")
    print(f"  Total Experience Duration: {total_experience_sec:.1f}s")
    print(f"  Tolerance Window: [{tolerance_min:.1f}s - {tolerance_max:.1f}s]")
    print(f"  Within ±10% Tolerance: {'PASS [OK]' if is_within_tolerance else 'FAIL [X]'}")

    # Inspect whiteboard data on segments
    for idx, seg in enumerate(lesson.segments):
        wb = getattr(seg, "whiteboard_data", None) or {}
        domain = wb.get("domain", "N/A")
        print(f"    Module {idx+1}: '{seg.title[:35]}' -> Audio: {seg.actual_seconds:.1f}s | WB Domain: {domain}")

    # Generate segment 1 video to verify video engine
    first_seg = lesson.segments[0]
    print(f"\n[VIDEO TEST] Generating video for Module 1 ('{first_seg.title}')...")
    t_v0 = time.time()
    v_res = video_assembler.assemble_segment_video(
        segment=first_seg,
        lesson_title=lesson.title,
        segment_index=1,
        total_segments=len(lesson.segments),
        language=lesson.target_language
    )
    first_seg.video_url = v_res["relative_url"]
    video_gen_time = time.time() - t_v0
    print(f"  Module 1 Video Generated in {video_gen_time:.2f}s: {v_res['video_path']} (Video Duration: {v_res['duration']:.2f}s)")

    return {
        "topic": topic,
        "requested_mins": duration_mins,
        "target_seconds": target_sec,
        "actual_audio_seconds": round(total_audio_sec, 2),
        "actual_experience_seconds": round(total_experience_sec, 2),
        "module_1_video_seconds": round(v_res["duration"], 2),
        "total_modules": len(lesson.segments),
        "within_tolerance": is_within_tolerance
    }


def main():
    print("STARTING COMPLETE DURATION AND PEDAGOGICAL VERIFICATION SUITE...")
    
    test_configs = [
        {"topic": "Explain Black Holes", "duration_mins": 5, "language": "en"},
        {"topic": "How does TCP work?", "duration_mins": 10, "language": "hinglish"},
        {"topic": "Teach me Photosynthesis", "duration_mins": 20, "language": "hi"}
    ]

    results = []
    for cfg in test_configs:
        res = run_test_case(cfg["topic"], cfg["duration_mins"], cfg["language"])
        results.append(res)

    print("\n" + "=" * 80)
    print("                    END-TO-END VERIFICATION SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Requested Duration':<20} | {'Actual Audio (sec)':<20} | {'Actual Exp. (sec)':<20} | {'Status':<10}")
    print("-" * 80)
    for r in results:
        status_str = "PASS [OK]" if r["within_tolerance"] else "FAIL [X]"
        print(f"{r['requested_mins']} minutes ({r['target_seconds']}s)     | {r['actual_audio_seconds']:<20.1f} | {r['actual_experience_seconds']:<20.1f} | {status_str:<10}")
    print("=" * 80)

    all_passed = all(r["within_tolerance"] for r in results)
    if all_passed:
        print("\nALL DURATION ACCURACY TESTS PASSED PERFECTLY WITHIN ±10% TOLERANCE!")
    else:
        print("\nSOME TESTS FAILED TOLERANCE.")

if __name__ == "__main__":
    main()
