import os
import math
import subprocess
import uuid
import textwrap
from typing import Optional, Dict, Any, List
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

from .tts import tts_engine
from .avatar import avatar_engine
from app.lesson_planning.schemas import Segment


class VideoAssembler:
    """
    Composites synchronized AI Teacher avatar video with dynamic slide graphics,
    typography cards, diagrams, subtitles, and neural narration audio into web-ready MP4.
    """

    def __init__(self, output_dir: str = "media/videos"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        self.fps = 25
        self.width = 1280
        self.height = 720

    def _get_font(self, font_name: str, size: int):
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            try:
                return ImageFont.truetype("segoeui.ttf", size)
            except Exception:
                try:
                    return ImageFont.truetype("arial.ttf", size)
                except Exception:
                    return ImageFont.load_default()

    def assemble_segment_video(
        self,
        segment: Segment,
        lesson_title: str = "AI Teacher Lesson",
        segment_index: int = 1,
        total_segments: int = 2,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generates full MP4 video for a single lesson segment.
        Returns: {
            "video_path": str,
            "duration": float,
            "filename": str,
            "relative_url": str
        }
        """
        is_remediation = getattr(segment, "is_remediation", False)
        seg_id = segment.id or f"seg_{segment_index}"
        unique_suffix = uuid.uuid4().hex[:6]
        filename = f"{seg_id}_{unique_suffix}.mp4"
        output_video_path = os.path.join(self.output_dir, filename)

        # 1. Synthesize Audio
        narration_text = segment.explanation
        if segment.example:
            narration_text += f" For instance: {segment.example}"

        wav_path, duration, amplitudes = tts_engine.synthesize(
            narration_text,
            language=language,
            output_filename=f"audio_{seg_id}_{unique_suffix}"
        )

        total_frames = max(25, int(duration * self.fps))
        # Ensure amplitude list matches total_frames
        if len(amplitudes) < total_frames:
            amplitudes.extend([0.0] * (total_frames - len(amplitudes)))
        else:
            amplitudes = amplitudes[:total_frames]

        # 2. Setup FFmpeg subprocess pipe
        cmd = [
            self.ffmpeg_exe, "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{self.width}x{self.height}",
            "-pix_fmt", "rgb24",
            "-r", str(self.fps),
            "-i", "-",  # Pipe input
            "-i", wav_path,  # Audio input
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            "-movflags", "+faststart",
            output_video_path
        ]

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 3. Pre-render static slide layout components
        title_font = self._get_font("segoeui.ttf", 30)
        heading_font = self._get_font("segoeui.ttf", 20)
        body_font = self._get_font("segoeui.ttf", 18)
        small_font = self._get_font("segoeui.ttf", 14)
        subtitle_font = self._get_font("segoeui.ttf", 16)

        # Prepare narration words for subtitle ticker
        narration_words = narration_text.split()
        words_per_frame = max(0.1, len(narration_words) / float(total_frames))

        try:
            for frame_idx in range(total_frames):
                # Base frame background: Dark cosmic tech gradient
                frame = Image.new("RGB", (self.width, self.height), (11, 15, 25))
                draw = ImageDraw.Draw(frame)

                # Ambient glow background accents
                if is_remediation:
                    draw.ellipse([800, -100, 1400, 400], fill=(245, 158, 11, 20))
                else:
                    draw.ellipse([800, -100, 1400, 400], fill=(99, 102, 241, 25))
                draw.ellipse([100, 400, 600, 900], fill=(59, 130, 246, 20))

                # --- TOP HEADER BAR ---
                header_rect = [30, 20, self.width - 30, 70]
                draw.rounded_rectangle(header_rect, radius=12, fill=(20, 26, 43), outline=(51, 65, 85), width=1)

                # App Logo / Title
                draw.text((48, 33), "🤖 AI TEACHER", font=heading_font, fill=(99, 102, 241))
                draw.line([(190, 32), (190, 58)], fill=(71, 85, 105), width=1)
                
                # Truncate lesson title if long
                disp_lesson_title = (lesson_title[:45] + "...") if len(lesson_title) > 45 else lesson_title
                draw.text((205, 34), disp_lesson_title, font=small_font, fill=(203, 213, 225))

                # Step Tracker / Remediation Badge
                if is_remediation:
                    badge_rect = [self.width - 290, 28, self.width - 48, 62]
                    draw.rounded_rectangle(badge_rect, radius=8, fill=(180, 83, 9), outline=(245, 158, 11), width=1)
                    draw.text((self.width - 275, 34), "🔄 ADAPTIVE RE-EXPLANATION", font=small_font, fill=(254, 243, 199))
                else:
                    badge_rect = [self.width - 180, 28, self.width - 48, 62]
                    draw.rounded_rectangle(badge_rect, radius=8, fill=(30, 41, 59), outline=(99, 102, 241), width=1)
                    draw.text((self.width - 165, 34), f"PART {segment_index} OF {total_segments}", font=small_font, fill=(147, 197, 253))

                # Determine dynamic teaching pose based on lesson progress & pedagogy
                prog = frame_idx / float(total_frames)
                if is_remediation:
                    if prog < 0.18:
                        pose = "remediate"
                    elif prog < 0.52:
                        pose = "point_board"
                    elif prog < 0.82:
                        pose = "explain"
                    else:
                        pose = "welcome"
                else:
                    if prog < 0.15:
                        pose = "welcome"
                    elif prog < 0.48:
                        pose = "point_board"
                    elif prog < 0.82:
                        pose = "explain"
                    else:
                        pose = "welcome"

                # --- LEFT COLUMN: CLASSROOM TEACHER PRESENTATION ---
                avatar_w = 340
                avatar_h = 470
                avatar_x = 30
                avatar_y = 85
                amp = amplitudes[frame_idx]

                avatar_img = avatar_engine.render_avatar_frame(
                    size=(avatar_w, avatar_h),
                    amplitude=amp,
                    frame_idx=frame_idx,
                    fps=self.fps,
                    pose=pose
                )
                frame.paste(avatar_img, (avatar_x, avatar_y), mask=avatar_img)

                # Name Tag on Teacher Podium
                tag_rect = [avatar_x + 20, avatar_y + avatar_h - 48, avatar_x + avatar_w - 20, avatar_y + avatar_h - 16]
                draw.rounded_rectangle(tag_rect, radius=6, fill=(15, 23, 42), outline=(79, 70, 229), width=1)
                pose_label = "Teaching" if pose in ["explain", "welcome"] else "Focus on Board 👉" if pose == "point_board" else "Re-explaining 💡" if pose == "remediate" else "Observing"
                draw.text((avatar_x + 28, avatar_y + avatar_h - 44), f"Dr. Nova • {pose_label}", font=small_font, fill=(226, 232, 240))

                # --- RIGHT COLUMN: SMART TEACHING BOARD ---
                slide_x = 395
                slide_y = 85
                slide_w = self.width - slide_x - 30
                slide_h = 470

                slide_rect = [slide_x, slide_y, slide_x + slide_w, slide_y + slide_h]
                board_outline = (99, 102, 241) if pose == "point_board" else (55, 65, 81)
                draw.rounded_rectangle(slide_rect, radius=18, fill=(17, 24, 39), outline=board_outline, width=2 if pose == "point_board" else 1)

                # Segment Title & Visual Type Badge
                seg_title = segment.title
                if len(seg_title) > 38:
                    seg_title = seg_title[:36] + "..."
                draw.text((slide_x + 28, slide_y + 20), seg_title, font=title_font, fill=(248, 250, 252))

                # Diagram Type Badge
                v_type = (segment.visual_diagram_type or "CONCEPT").upper()
                v_badge_w = len(v_type) * 8 + 16
                v_badge_rect = [slide_x + slide_w - v_badge_w - 28, slide_y + 22, slide_x + slide_w - 28, slide_y + 46]
                draw.rounded_rectangle(v_badge_rect, radius=6, fill=(30, 41, 59), outline=(99, 102, 241), width=1)
                draw.text((slide_x + slide_w - v_badge_w - 20, slide_y + 26), v_type, font=small_font, fill=(165, 180, 252))

                # Decorative underline
                underline_color = (245, 158, 11) if is_remediation else (99, 102, 241)
                draw.rounded_rectangle([slide_x + 28, slide_y + 60, slide_x + 180, slide_y + 64], radius=2, fill=underline_color)

                # Key Points Cards
                kp_y = slide_y + 76
                key_points = segment.key_points if segment.key_points else ["Understand fundamental concept", "Apply practical reasoning", "Verify key mechanism"]
                for k_i, point in enumerate(key_points[:2]):
                    # Card box (Active pulse if teacher is pointing in first half of pointing phase)
                    is_kp_focus = (pose == "point_board" and k_i == 0)
                    card_border = (251, 191, 36) if is_kp_focus else (51, 65, 85)
                    card_r = [slide_x + 28, kp_y, slide_x + slide_w - 28, kp_y + 54]
                    draw.rounded_rectangle(card_r, radius=8, fill=(26, 34, 52), outline=card_border, width=2 if is_kp_focus else 1)

                    # Number badge
                    badge_box = [slide_x + 38, kp_y + 12, slide_x + 66, kp_y + 42]
                    badge_fill = (251, 191, 36) if is_kp_focus else ((99, 102, 241) if not is_remediation else (217, 119, 6))
                    draw.rounded_rectangle(badge_box, radius=5, fill=badge_fill)
                    draw.text((slide_x + 48, kp_y + 16), str(k_i + 1), font=heading_font, fill=(15, 23, 42) if is_kp_focus else (255, 255, 255))

                    # Point text
                    wrapped_point = textwrap.shorten(point, width=62, placeholder="...")
                    draw.text((slide_x + 78, kp_y + 16), wrapped_point, font=body_font, fill=(248, 250, 252) if is_kp_focus else (226, 232, 240))

                    kp_y += 62

                # Subject-Aware Code / Math / Formula / Process Card
                code_or_math = getattr(segment, "visual_code_or_math", "") or getattr(segment, "visual_description", "")
                if code_or_math:
                    is_math_focus = (pose == "point_board")
                    cm_border = (251, 191, 36) if is_math_focus else (79, 70, 229)
                    cm_rect = [slide_x + 28, kp_y, slide_x + slide_w - 28, kp_y + 56]
                    draw.rounded_rectangle(cm_rect, radius=8, fill=(15, 23, 42), outline=cm_border, width=2 if is_math_focus else 1)
                    
                    header_label = f"⚙️ {v_type} SPECIFICATION"
                    if is_math_focus:
                        header_label += "  [👉 TEACHER FOCUS]"
                    draw.text((slide_x + 40, kp_y + 6), header_label, font=small_font, fill=(251, 191, 36) if is_math_focus else (129, 140, 248))
                    cm_snippet = textwrap.shorten(str(code_or_math), width=65, placeholder="...")
                    draw.text((slide_x + 40, kp_y + 26), cm_snippet, font=body_font, fill=(248, 250, 252))

                # Analogy / Example Box at Bottom of Smartboard
                if segment.example:
                    ex_rect = [slide_x + 28, slide_y + slide_h - 96, slide_x + slide_w - 28, slide_y + slide_h - 18]
                    draw.rounded_rectangle(ex_rect, radius=10, fill=(30, 27, 75) if not is_remediation else (69, 26, 3), outline=(129, 140, 248) if not is_remediation else (245, 158, 11), width=1)
                    draw.text((slide_x + 40, slide_y + slide_h - 86), "💡 INTUITIVE REAL-WORLD ANALOGY", font=small_font, fill=(165, 180, 252) if not is_remediation else (252, 211, 77))
                    ex_text = textwrap.shorten(segment.example, width=70, placeholder="...")
                    draw.text((slide_x + 40, slide_y + slide_h - 62), ex_text, font=body_font, fill=(241, 245, 249))

                # --- BOTTOM BAR: SUBTITLE & TIME PROGRESS BAR ---
                bottom_rect = [30, self.height - 145, self.width - 30, self.height - 35]
                draw.rounded_rectangle(bottom_rect, radius=12, fill=(15, 23, 42), outline=(51, 65, 85), width=1)

                # Subtitle Ticker
                current_word_idx = int(frame_idx * words_per_frame)
                start_w = max(0, current_word_idx - 6)
                end_w = min(len(narration_words), current_word_idx + 8)
                sub_snippet = " ".join(narration_words[start_w:end_w])
                if len(sub_snippet) > 85:
                    sub_snippet = sub_snippet[:82] + "..."
                draw.text((50, self.height - 130), "💬 Subtitles:", font=small_font, fill=(148, 163, 184))
                draw.text((140, self.height - 132), sub_snippet, font=subtitle_font, fill=(248, 250, 252))

                # Progress Line
                prog_pct = (frame_idx + 1) / float(total_frames)
                bar_x1 = 50
                bar_x2 = self.width - 50
                bar_y = self.height - 60
                bar_w = bar_x2 - bar_x1

                # Track
                draw.rounded_rectangle([bar_x1, bar_y, bar_x2, bar_y + 8], radius=4, fill=(51, 65, 85))
                # Fill
                fill_w = max(4, int(bar_w * prog_pct))
                bar_color = (245, 158, 11) if is_remediation else (99, 102, 241)
                draw.rounded_rectangle([bar_x1, bar_y, bar_x1 + fill_w, bar_y + 8], radius=4, fill=bar_color)

                # Timestamp
                cur_sec = int(frame_idx / self.fps)
                tot_sec = int(duration)
                time_str = f"{cur_sec//60:02d}:{cur_sec%60:02d} / {tot_sec//60:02d}:{tot_sec%60:02d}"
                draw.text((self.width - 150, self.height - 90), time_str, font=small_font, fill=(148, 163, 184))

                # Write raw RGB frame to ffmpeg stdin
                proc.stdin.write(frame.tobytes())

        finally:
            proc.stdin.close()
            proc.wait()

        # Clean temp WAV
        try:
            os.remove(wav_path)
        except OSError:
            pass

        print(f"[VideoAssembler] Generated video: {output_video_path} (Duration: {duration:.2f}s, Frames: {total_frames})")

        return {
            "video_path": output_video_path,
            "duration": duration,
            "filename": filename,
            "relative_url": f"/media/videos/{filename}"
        }

    def assemble_full_lesson_video(
        self,
        lesson_plan: Any,
        output_filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assembles all segments of a lesson into a single continuous MP4 video.
        Ensures all segment videos are generated, then stitches them using FFmpeg concat protocol.
        """
        if not lesson_plan.segments:
            return {}

        total_segs = len(lesson_plan.segments)
        segment_files = []
        total_duration = 0.0

        for idx, seg in enumerate(lesson_plan.segments):
            seg_video_path = None
            if getattr(seg, "video_url", None):
                local_p = seg.video_url.lstrip("/")
                if os.path.exists(local_p) and os.path.getsize(local_p) > 0:
                    seg_video_path = local_p

            if not seg_video_path:
                v_res = self.assemble_segment_video(
                    segment=seg,
                    lesson_title=lesson_plan.title,
                    segment_index=idx + 1,
                    total_segments=total_segs,
                    language=lesson_plan.target_language
                )
                seg.video_url = v_res["relative_url"]
                seg_video_path = v_res["video_path"]
                total_duration += v_res["duration"]
            else:
                total_duration += getattr(seg, "actual_seconds", 0.0)

            segment_files.append(os.path.abspath(seg_video_path))

        unique_id = output_filename or f"full_{lesson_plan.lesson_id}"
        out_filename = f"{unique_id}.mp4"
        out_path = os.path.join(self.output_dir, out_filename)

        # Build FFmpeg concat list file
        concat_list_path = os.path.join(self.output_dir, f"{unique_id}_list.txt")
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for sf in segment_files:
                clean_path = sf.replace("\\", "/")
                f.write(f"file '{clean_path}'\n")

        # Concat command
        cmd = [
            self.ffmpeg_exe, "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list_path,
            "-c", "copy",
            "-movflags", "+faststart",
            out_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        try:
            os.remove(concat_list_path)
        except OSError:
            pass

        full_url = f"/media/videos/{out_filename}"
        lesson_plan.full_video_url = full_url
        lesson_plan.video_duration_seconds = round(total_duration, 2)

        return {
            "video_path": out_path,
            "duration": total_duration,
            "filename": out_filename,
            "relative_url": full_url
        }


# Global singleton
video_assembler = VideoAssembler()
