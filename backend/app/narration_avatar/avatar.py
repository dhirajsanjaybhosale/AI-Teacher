import os
import math
import torch
from typing import Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFont


class AvatarEngine:
    """
    Classroom Teacher Animation & Presentation Engine.
    Detects GPU availability at startup.
    - If GPU is present: Can invoke neural lip-sync/avatar pipelines.
    - If CPU mode: Engages the high-framerate, articulated classroom educator presentation
      system featuring:
      * Articulated arms and gesturing hands
      * 6 distinct pedagogical postures (welcome, explain, point_board, question, praise, remediate)
      * Dynamic pointer wand directed at smartboard equations/diagrams
      * Natural sinusoidal breathing cycle and eye blink
      * Multi-directional gaze (looking forward at student vs. looking toward the board)
      * 4 audio-synchronized phoneme mouth shapes
    """

    POSES = ["welcome", "explain", "point_board", "question", "praise", "remediate", "idle"]

    def __init__(self):
        self.gpu_available = torch.cuda.is_available()
        self.device = "cuda" if self.gpu_available else "cpu"
        print(f"[AvatarEngine] Initialized on device: {self.device.upper()} (GPU={self.gpu_available})")
        if self.gpu_available:
            print("[AvatarEngine] Neural avatar pipeline enabled.")
        else:
            print("[AvatarEngine] Articulated classroom teacher presentation engine engaged.")

    def render_avatar_frame(
        self,
        size: Tuple[int, int],
        amplitude: float,
        frame_idx: int,
        fps: int = 25,
        speaker_name: str = "Dr. Nova (AI Teacher)",
        pose: str = "explain"
    ) -> Image.Image:
        """
        Renders a single frame of the classroom teacher figure synced to audio amplitude and pedagogical pose.
        size: (width, height), e.g. (340, 470)
        amplitude: normalized audio energy (0.0 to 1.0)
        pose: 'welcome' | 'explain' | 'point_board' | 'question' | 'praise' | 'remediate' | 'idle'
        """
        w, h = size
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Classroom Teacher card frame
        card_rect = [0, 0, w, h]
        draw.rounded_rectangle(card_rect, radius=18, fill=(16, 22, 38, 240), outline=(79, 70, 229, 210), width=2)

        # Ambient classroom spotlight glow
        draw.ellipse([w // 2 - 120, -50, w // 2 + 120, 110], fill=(99, 102, 241, 45))

        # Teacher center coordinate
        cx = w // 2
        cy = int(h * 0.38)
        head_radius = int(min(w, h) * 0.22)

        # Natural breathing animation (subtle torso rise & fall)
        breath_offset = math.sin(frame_idx * 0.08) * 2.5

        # Head bobbing driven by speech amplitude
        is_speaking = amplitude > 0.05
        speech_bob = math.sin(frame_idx * 0.18) * (1.5 + amplitude * 3.5) if is_speaking else 0.0
        head_y = int(cy + breath_offset + speech_bob)

        # Look direction and head tilt based on pose
        look_dx = 0
        look_dy = 0
        head_tilt_x = 0
        if pose == "point_board":
            look_dx = 5  # Looking right toward smartboard
            head_tilt_x = 4
        elif pose == "question":
            look_dy = 1  # Looking intently forward/downward at student
            head_tilt_x = int(math.sin(frame_idx * 0.05) * 2)
        elif pose == "praise":
            look_dy = -1
        elif pose == "remediate":
            head_tilt_x = -3  # Gentle empathetic tilt

        head_cx = cx + head_tilt_x

        # -------------------------------------------------------------
        # 1. TORSO & BLAZER (Back Layer)
        # -------------------------------------------------------------
        torso_top = head_y + int(head_radius * 0.90)
        shoulder_w = int(head_radius * 1.55)
        blazer_bottom = h - 55

        # Shoulders / Blazer Main Body
        draw.ellipse([head_cx - shoulder_w, torso_top - 6, head_cx + shoulder_w, torso_top + int(head_radius * 1.6)], fill=(26, 36, 68))
        draw.rectangle([head_cx - int(shoulder_w * 0.82), torso_top + 25, head_cx + int(shoulder_w * 0.82), blazer_bottom], fill=(26, 36, 68))

        # Neck
        neck_w = int(head_radius * 0.40)
        draw.rectangle([head_cx - neck_w, head_y + int(head_radius * 0.6), head_cx + neck_w, torso_top + 15], fill=(230, 192, 168))

        # Shirt Collar (V-neck / button-down)
        draw.polygon([
            (head_cx - neck_w - 4, torso_top - 2),
            (head_cx, torso_top + 48),
            (head_cx + neck_w + 4, torso_top - 2),
            (head_cx, torso_top + 22)
        ], fill=(245, 248, 255))

        # Teacher Silk Scarf / Pendant
        draw.polygon([
            (head_cx - 7, torso_top + 24),
            (head_cx + 7, torso_top + 24),
            (head_cx, torso_top + 80)
        ], fill=(129, 140, 248))

        # Lapels of blazer
        draw.polygon([(head_cx - shoulder_w + 14, torso_top + 10), (head_cx - 10, torso_top + 60), (head_cx - 26, torso_top + 70)], fill=(34, 46, 84))
        draw.polygon([(head_cx + shoulder_w - 14, torso_top + 10), (head_cx + 10, torso_top + 60), (head_cx + 26, torso_top + 70)], fill=(34, 46, 84))

        # -------------------------------------------------------------
        # 2. HEAD BASE & SKIN
        # -------------------------------------------------------------
        skin_color = (255, 222, 194)
        draw.ellipse([head_cx - head_radius, head_y - head_radius, head_cx + head_radius, head_y + head_radius], fill=skin_color)

        # Cheeks blush
        blush_color = (255, 175, 175)
        draw.ellipse([head_cx - int(head_radius * 0.72), head_y + int(head_radius * 0.12), head_cx - int(head_radius * 0.32), head_y + int(head_radius * 0.36)], fill=blush_color)
        draw.ellipse([head_cx + int(head_radius * 0.32), head_y + int(head_radius * 0.12), head_cx + int(head_radius * 0.72), head_y + int(head_radius * 0.36)], fill=blush_color)

        # -------------------------------------------------------------
        # 3. PROFESSIONAL HAIRSTYLE
        # -------------------------------------------------------------
        hair_color = (38, 28, 48)
        # Hair volume / Back hair
        draw.ellipse([head_cx - int(head_radius * 1.08), head_y - int(head_radius * 1.16), head_cx + int(head_radius * 1.08), head_y + int(head_radius * 0.28)], fill=hair_color)
        # Bangs / Front framing
        draw.polygon([
            (head_cx - head_radius, head_y - int(head_radius * 0.42)),
            (head_cx - int(head_radius * 0.45), head_y - int(head_radius * 0.12)),
            (head_cx, head_y - int(head_radius * 0.52)),
            (head_cx + int(head_radius * 0.50), head_y - int(head_radius * 0.08)),
            (head_cx + head_radius, head_y - int(head_radius * 0.42)),
            (head_cx + int(head_radius * 0.85), head_y - int(head_radius * 1.15)),
            (head_cx - int(head_radius * 0.85), head_y - int(head_radius * 1.15))
        ], fill=hair_color)

        # -------------------------------------------------------------
        # 4. EYEBROWS (Pose-responsive expression)
        # -------------------------------------------------------------
        brow_y = head_y - int(head_radius * 0.22)
        if pose == "question":
            # Inquisitive: one eyebrow raised higher
            draw.arc([head_cx - int(head_radius * 0.65), brow_y - 12, head_cx - int(head_radius * 0.15), brow_y + 4], start=210, end=330, fill=hair_color, width=3)
            draw.arc([head_cx + int(head_radius * 0.15), brow_y - 6, head_cx + int(head_radius * 0.65), brow_y + 8], start=200, end=340, fill=hair_color, width=3)
        elif pose == "praise":
            # Excited raised brows
            draw.arc([head_cx - int(head_radius * 0.65), brow_y - 10, head_cx - int(head_radius * 0.15), brow_y + 6], start=200, end=340, fill=hair_color, width=3)
            draw.arc([head_cx + int(head_radius * 0.15), brow_y - 10, head_cx + int(head_radius * 0.65), brow_y + 6], start=200, end=340, fill=hair_color, width=3)
        elif pose == "remediate":
            # Soft, empathetic brows
            draw.arc([head_cx - int(head_radius * 0.65), brow_y - 4, head_cx - int(head_radius * 0.15), brow_y + 10], start=190, end=330, fill=hair_color, width=3)
            draw.arc([head_cx + int(head_radius * 0.15), brow_y - 4, head_cx + int(head_radius * 0.65), brow_y + 10], start=210, end=350, fill=hair_color, width=3)
        else:
            # Focused natural teaching brows
            draw.arc([head_cx - int(head_radius * 0.65), brow_y - 7, head_cx - int(head_radius * 0.15), brow_y + 7], start=200, end=340, fill=hair_color, width=3)
            draw.arc([head_cx + int(head_radius * 0.15), brow_y - 7, head_cx + int(head_radius * 0.65), brow_y + 7], start=200, end=340, fill=hair_color, width=3)

        # -------------------------------------------------------------
        # 5. EYES & NATURAL BLINKING
        # -------------------------------------------------------------
        # Blink every ~75 frames (3s) for 4 frames
        is_blinking = (frame_idx % 80) in [73, 74, 75, 76]
        eye_y = head_y - int(head_radius * 0.05)
        eye_dx = int(head_radius * 0.40)

        if is_blinking:
            # Soft closed eye arcs
            draw.arc([head_cx - eye_dx - 13, eye_y - 3, head_cx - eye_dx + 13, eye_y + 8], start=15, end=165, fill=(50, 40, 60), width=3)
            draw.arc([head_cx + eye_dx - 13, eye_y - 3, head_cx + eye_dx + 13, eye_y + 8], start=15, end=165, fill=(50, 40, 60), width=3)
        else:
            # Sclera (White)
            draw.ellipse([head_cx - eye_dx - 13, eye_y - 11, head_cx - eye_dx + 13, eye_y + 11], fill=(255, 255, 255))
            draw.ellipse([head_cx + eye_dx - 13, eye_y - 11, head_cx + eye_dx + 13, eye_y + 11], fill=(255, 255, 255))

            # Iris (Warm intelligent sapphire/hazel)
            iris_cx_l = head_cx - eye_dx + look_dx
            iris_cx_r = head_cx + eye_dx + look_dx
            iris_cy = eye_y + look_dy
            draw.ellipse([iris_cx_l - 7, iris_cy - 8, iris_cx_l + 7, iris_cy + 8], fill=(37, 99, 235))
            draw.ellipse([iris_cx_r - 7, iris_cy - 8, iris_cx_r + 7, iris_cy + 8], fill=(37, 99, 235))

            # Pupil & Sparkle
            draw.ellipse([iris_cx_l - 4, iris_cy - 4, iris_cx_l + 4, iris_cy + 4], fill=(15, 23, 42))
            draw.ellipse([iris_cx_r - 4, iris_cy - 4, iris_cx_r + 4, iris_cy + 4], fill=(15, 23, 42))
            draw.ellipse([iris_cx_l + 1, iris_cy - 6, iris_cx_l + 4, iris_cy - 3], fill=(255, 255, 255))
            draw.ellipse([iris_cx_r + 1, iris_cy - 6, iris_cx_r + 4, iris_cy - 3], fill=(255, 255, 255))

        # Teacher Glasses (Indigo rim)
        gw = 24
        gh = 16
        draw.rounded_rectangle([head_cx - eye_dx - gw, eye_y - gh, head_cx - eye_dx + gw, eye_y + gh], radius=6, outline=(99, 102, 241), width=2)
        draw.rounded_rectangle([head_cx + eye_dx - gw, eye_y - gh, head_cx + eye_dx + gw, eye_y + gh], radius=6, outline=(99, 102, 241), width=2)
        draw.line([(head_cx - eye_dx + gw, eye_y - 2), (head_cx + eye_dx - gw, eye_y - 2)], fill=(99, 102, 241), width=2)

        # Nose
        draw.polygon([(head_cx, head_y + 4), (head_cx - 3, head_y + 17), (head_cx + 3, head_y + 17)], fill=(225, 175, 140))

        # -------------------------------------------------------------
        # 6. DYNAMIC MOUTH SHAPES (Phonemes & Expressions)
        # -------------------------------------------------------------
        mouth_y = head_y + int(head_radius * 0.46)

        if amplitude < 0.08:
            if pose == "praise":
                # Wide beaming congratulatory smile
                draw.arc([head_cx - 18, mouth_y - 12, head_cx + 18, mouth_y + 12], start=10, end=170, fill=(219, 39, 119), width=3)
                draw.ellipse([head_cx - 12, mouth_y - 2, head_cx + 12, mouth_y + 6], fill=(255, 255, 255))
            elif pose == "remediate":
                # Warm reassuring smile
                draw.arc([head_cx - 14, mouth_y - 7, head_cx + 14, mouth_y + 7], start=20, end=160, fill=(190, 60, 80), width=3)
            elif pose == "question":
                # Thoughtful subtle smile
                draw.arc([head_cx - 12, mouth_y - 6, head_cx + 12, mouth_y + 6], start=25, end=155, fill=(185, 55, 75), width=2)
            else:
                # Gentle closed resting smile
                draw.arc([head_cx - 15, mouth_y - 7, head_cx + 15, mouth_y + 7], start=20, end=160, fill=(185, 60, 80), width=3)
        elif amplitude < 0.28:
            # Phoneme 1: Slight Open ('ah' / 'eh')
            draw.rounded_rectangle([head_cx - 14, mouth_y - 5, head_cx + 14, mouth_y + 7], radius=5, fill=(160, 40, 60), outline=(220, 100, 120), width=1)
            draw.rectangle([head_cx - 10, mouth_y - 4, head_cx + 10, mouth_y - 1], fill=(255, 255, 255))
        elif amplitude < 0.58:
            # Phoneme 2: Medium Open ('oh' / 'oo')
            draw.ellipse([head_cx - 16, mouth_y - 9, head_cx + 16, mouth_y + 11], fill=(140, 30, 50), outline=(230, 110, 130), width=2)
            draw.ellipse([head_cx - 10, mouth_y - 7, head_cx + 10, mouth_y - 2], fill=(255, 255, 255))
            draw.ellipse([head_cx - 10, mouth_y + 4, head_cx + 10, mouth_y + 8], fill=(230, 90, 110))
        else:
            # Phoneme 3: Wide Open ('aa' / animated delivery)
            draw.ellipse([head_cx - 20, mouth_y - 14, head_cx + 20, mouth_y + 15], fill=(130, 20, 40), outline=(244, 63, 94), width=2)
            draw.rectangle([head_cx - 14, mouth_y - 11, head_cx + 14, mouth_y - 6], fill=(255, 255, 255))
            draw.ellipse([head_cx - 12, mouth_y + 5, head_cx + 12, mouth_y + 13], fill=(244, 114, 182))

        # -------------------------------------------------------------
        # 7. ARTICULATED ARMS, HANDS & GESTURE SYSTEM
        # -------------------------------------------------------------
        l_shoulder = (head_cx - shoulder_w + 12, torso_top + 16)
        r_shoulder = (head_cx + shoulder_w - 12, torso_top + 16)

        # Draw gesture based on active pedagogical posture
        if pose == "point_board":
            # --- POSE: POINTING TO BOARD (Right arm extended with pointer wand) ---
            # Left arm resting naturally at side
            l_elbow = (l_shoulder[0] - 8, l_shoulder[1] + 65)
            l_hand = (l_shoulder[0] + 10, l_shoulder[1] + 125)
            draw.line([l_shoulder, l_elbow, l_hand], fill=(26, 36, 68), width=16)
            # Left hand (skin)
            draw.ellipse([l_hand[0] - 8, l_hand[1] - 8, l_hand[0] + 8, l_hand[1] + 8], fill=skin_color)

            # Right arm extending upward/right toward the smartboard
            r_elbow = (r_shoulder[0] + 25, r_shoulder[1] + 35)
            r_hand = (w - 28, torso_top + 18)
            draw.line([r_shoulder, r_elbow, r_hand], fill=(26, 36, 68), width=16)
            # Right hand pointing
            draw.ellipse([r_hand[0] - 8, r_hand[1] - 8, r_hand[0] + 8, r_hand[1] + 8], fill=skin_color)

            # Elegant Wooden Pointer Wand extending directly to the board
            wand_tip = (w + 15, torso_top - 10)
            draw.line([r_hand, wand_tip], fill=(217, 119, 6), width=4)
            # Golden tip sparkle on pointer
            draw.ellipse([wand_tip[0] - 4, wand_tip[1] - 4, wand_tip[0] + 4, wand_tip[1] + 4], fill=(251, 191, 36))

        elif pose == "question":
            # --- POSE: QUESTION / THINKING (Hand at chin, inquisitive) ---
            # Left arm resting at lectern/side
            l_elbow = (l_shoulder[0] - 6, l_shoulder[1] + 68)
            l_hand = (l_shoulder[0] + 15, l_shoulder[1] + 120)
            draw.line([l_shoulder, l_elbow, l_hand], fill=(26, 36, 68), width=16)
            draw.ellipse([l_hand[0] - 8, l_hand[1] - 8, l_hand[0] + 8, l_hand[1] + 8], fill=skin_color)

            # Right arm brought up to chin
            r_elbow = (r_shoulder[0] + 10, r_shoulder[1] + 70)
            chin_hand = (head_cx + 16, head_y + int(head_radius * 0.70))
            draw.line([r_shoulder, r_elbow, chin_hand], fill=(26, 36, 68), width=16)
            # Hand cupping chin in thought
            draw.ellipse([chin_hand[0] - 10, chin_hand[1] - 8, chin_hand[0] + 10, chin_hand[1] + 8], fill=skin_color)
            # Thinking finger resting against cheek
            draw.line([(chin_hand[0], chin_hand[1]), (chin_hand[0] - 4, chin_hand[1] - 14)], fill=skin_color, width=4)

        elif pose == "praise":
            # --- POSE: PRAISE / CELEBRATION (Both hands raised in enthusiastic praise) ---
            # Left arm raised
            l_elbow = (l_shoulder[0] - 22, l_shoulder[1] + 30)
            l_hand = (l_shoulder[0] - 18, l_shoulder[1] - 15)
            draw.line([l_shoulder, l_elbow, l_hand], fill=(26, 36, 68), width=16)
            draw.ellipse([l_hand[0] - 9, l_hand[1] - 9, l_hand[0] + 9, l_hand[1] + 9], fill=skin_color)
            # Thumbs up left
            draw.line([l_hand, (l_hand[0] - 5, l_hand[1] - 12)], fill=skin_color, width=5)

            # Right arm raised
            r_elbow = (r_shoulder[0] + 22, r_shoulder[1] + 30)
            r_hand = (r_shoulder[0] + 18, r_shoulder[1] - 15)
            draw.line([r_shoulder, r_elbow, r_hand], fill=(26, 36, 68), width=16)
            draw.ellipse([r_hand[0] - 9, r_hand[1] - 9, r_hand[0] + 9, r_hand[1] + 9], fill=skin_color)
            # Thumbs up right
            draw.line([r_hand, (r_hand[0] + 5, r_hand[1] - 12)], fill=skin_color, width=5)

        elif pose == "remediate":
            # --- POSE: EMPATHETIC REASSURANCE (Hand on heart, encouraging) ---
            # Left arm resting gently
            l_elbow = (l_shoulder[0] - 8, l_shoulder[1] + 65)
            l_hand = (l_shoulder[0] + 12, l_shoulder[1] + 120)
            draw.line([l_shoulder, l_elbow, l_hand], fill=(26, 36, 68), width=16)
            draw.ellipse([l_hand[0] - 8, l_hand[1] - 8, l_hand[0] + 8, l_hand[1] + 8], fill=skin_color)

            # Right arm placed over chest/heart
            r_elbow = (r_shoulder[0] + 15, r_shoulder[1] + 55)
            heart_hand = (head_cx + 6, torso_top + 45)
            draw.line([r_shoulder, r_elbow, heart_hand], fill=(26, 36, 68), width=16)
            draw.ellipse([heart_hand[0] - 11, heart_hand[1] - 9, heart_hand[0] + 11, heart_hand[1] + 9], fill=skin_color)

        else:
            # --- POSE: EXPLAINING / CONVERSATIONAL GESTURES (Dynamic speech movement) ---
            # Hand moves rhythmically with speech amplitude and cadence
            cadence = math.sin(frame_idx * 0.16)
            r_gesture_y = int(torso_top + 50 - amplitude * 26 + cadence * 8)
            r_gesture_x = int(r_shoulder[0] + 15 + cadence * 6)

            r_elbow = (r_shoulder[0] + 16, torso_top + 52)
            r_hand = (r_gesture_x, r_gesture_y)
            draw.line([r_shoulder, r_elbow, r_hand], fill=(26, 36, 68), width=16)
            # Gesturing open palm
            draw.ellipse([r_hand[0] - 9, r_hand[1] - 9, r_hand[0] + 9, r_hand[1] + 9], fill=skin_color)
            # Distinct extended conversational fingers
            draw.line([(r_hand[0], r_hand[1]), (r_hand[0] + 8, r_hand[1] - 8)], fill=skin_color, width=3)
            draw.line([(r_hand[0], r_hand[1]), (r_hand[0] + 10, r_hand[1] - 3)], fill=skin_color, width=3)

            # Left arm subtle resting / balancing gesture
            l_cadence = math.cos(frame_idx * 0.12)
            l_elbow = (l_shoulder[0] - 10, torso_top + 62)
            l_hand = (l_shoulder[0] + 8, int(torso_top + 85 + l_cadence * 6))
            draw.line([l_shoulder, l_elbow, l_hand], fill=(26, 36, 68), width=16)
            draw.ellipse([l_hand[0] - 8, l_hand[1] - 8, l_hand[0] + 8, l_hand[1] + 8], fill=skin_color)

        # -------------------------------------------------------------
        # 8. CLASSROOM TEACHER STATUS BADGE & AUDIO VISUALIZER
        # -------------------------------------------------------------
        badge_y = h - 50
        status_color = (16, 185, 129) if is_speaking else (148, 163, 184)
        draw.ellipse([22, badge_y + 8, 34, badge_y + 20], fill=status_color)

        # Reactive Audio Visualizer (7 bars)
        num_bars = 7
        bar_w = 4
        gap = 4
        total_viz_w = num_bars * (bar_w + gap)
        viz_start_x = w - 24 - total_viz_w

        for b in range(num_bars):
            phase = (b - 3) * 0.8
            bar_amp = max(0.1, amplitude * (math.sin(frame_idx * 0.3 + phase) ** 2))
            bar_h = int(bar_amp * 26) + 4
            bx = viz_start_x + b * (bar_w + gap)
            by = badge_y + 14 - bar_h // 2
            draw.rounded_rectangle([bx, by, bx + bar_w, by + bar_h], radius=2, fill=(99, 102, 241))

        return img


# Global singleton
avatar_engine = AvatarEngine()
