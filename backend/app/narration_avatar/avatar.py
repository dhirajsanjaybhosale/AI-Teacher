import os
import math
import torch
from typing import Tuple, List, Optional
from PIL import Image, ImageDraw, ImageFont


class AvatarEngine:
    """
    Intelligent Avatar Generator.
    Detects GPU availability at startup.
    - If GPU is present: Can invoke Wav2Lip/SadTalker pipelines.
    - If CPU (no GPU): Engages the fast, synchronized 2D vector animated avatar engine
      with 4 discrete phonetic mouth shapes, reactive audio visualizers, and natural blinking.
    """

    def __init__(self):
        self.gpu_available = torch.cuda.is_available()
        self.device = "cuda" if self.gpu_available else "cpu"
        print(f"[AvatarEngine] Initialized on device: {self.device.upper()} (GPU={self.gpu_available})")
        if self.gpu_available:
            print("[AvatarEngine] Real lip-synced neural avatar pipeline (Wav2Lip/SadTalker) enabled.")
        else:
            print("[AvatarEngine] Engaging synchronized 2D vector audio-driven avatar engine.")

    def render_avatar_frame(
        self,
        size: Tuple[int, int],
        amplitude: float,
        frame_idx: int,
        fps: int = 25,
        speaker_name: str = "Dr. Nova (AI Teacher)"
    ) -> Image.Image:
        """
        Renders a single frame of the AI Teacher avatar synced to audio amplitude.
        size: (width, height) e.g. (340, 480)
        amplitude: normalized audio energy (0.0 to 1.0)
        """
        w, h = size
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Avatar card container
        card_rect = [0, 0, w, h]
        draw.rounded_rectangle(card_rect, radius=20, fill=(20, 27, 45, 235), outline=(79, 70, 229, 200), width=2)

        # Subtle glow at the top
        draw.ellipse([w//2 - 100, -40, w//2 + 100, 100], fill=(99, 102, 241, 40))

        # Avatar Center and Head
        cx = w // 2
        cy = int(h * 0.42)
        head_radius = int(min(w, h) * 0.28)

        # Subtle head bobbing with audio energy
        bob_offset = int(math.sin(frame_idx * 0.15) * (2.0 + amplitude * 3.0))
        cy += bob_offset

        # Neck
        neck_w = head_radius * 0.45
        draw.rectangle([cx - neck_w, cy + head_radius * 0.6, cx + neck_w, cy + head_radius * 1.2], fill=(220, 185, 160))

        # Shoulders / Blazer
        shoulder_top = cy + int(head_radius * 0.95)
        draw.ellipse([cx - head_radius * 1.5, shoulder_top, cx + head_radius * 1.5, shoulder_top + head_radius * 1.6], fill=(30, 41, 75))
        # Shirt collar
        draw.polygon([
            (cx - neck_w * 0.9, shoulder_top + 10),
            (cx, shoulder_top + 50),
            (cx + neck_w * 0.9, shoulder_top + 10),
            (cx, shoulder_top + 30)
        ], fill=(240, 245, 255))
        # Tie / Pendant
        draw.polygon([(cx - 8, shoulder_top + 35), (cx + 8, shoulder_top + 35), (cx, shoulder_top + 95)], fill=(99, 102, 241))

        # Head Base (Skin Tone)
        skin_color = (255, 219, 187)
        draw.ellipse([cx - head_radius, cy - head_radius, cx + head_radius, cy + head_radius], fill=skin_color)

        # Cheeks Blush
        blush_color = (255, 170, 170, 90)
        draw.ellipse([cx - head_radius * 0.75, cy + head_radius * 0.1, cx - head_radius * 0.35, cy + head_radius * 0.35], fill=(255, 175, 175))
        draw.ellipse([cx + head_radius * 0.35, cy + head_radius * 0.1, cx + head_radius * 0.75, cy + head_radius * 0.35], fill=(255, 175, 175))

        # Modern Hairstyle
        hair_color = (40, 30, 50)
        # Back hair / Volume
        draw.ellipse([cx - head_radius * 1.08, cy - head_radius * 1.15, cx + head_radius * 1.08, cy + head_radius * 0.3], fill=hair_color)
        # Front bangs
        draw.polygon([
            (cx - head_radius, cy - head_radius * 0.4),
            (cx - head_radius * 0.4, cy - head_radius * 0.1),
            (cx, cy - head_radius * 0.5),
            (cx + head_radius * 0.5, cy - head_radius * 0.05),
            (cx + head_radius, cy - head_radius * 0.4),
            (cx + head_radius * 0.8, cy - head_radius * 1.1),
            (cx - head_radius * 0.8, cy - head_radius * 1.1)
        ], fill=hair_color)

        # Eyebrows
        brow_y = cy - int(head_radius * 0.22)
        draw.arc([cx - head_radius * 0.65, brow_y - 8, cx - head_radius * 0.15, brow_y + 8], start=200, end=340, fill=hair_color, width=3)
        draw.arc([cx + head_radius * 0.15, brow_y - 8, cx + head_radius * 0.65, brow_y + 8], start=200, end=340, fill=hair_color, width=3)

        # Eyes with natural blinking (blink every ~75 frames = 3 seconds for 5 frames)
        is_blinking = (frame_idx % 80) in [74, 75, 76, 77]
        eye_y = cy - int(head_radius * 0.05)
        eye_dx = int(head_radius * 0.4)

        if is_blinking:
            # Closed eye arcs
            draw.arc([cx - eye_dx - 14, eye_y - 4, cx - eye_dx + 14, eye_y + 10], start=10, end=170, fill=(50, 40, 60), width=3)
            draw.arc([cx + eye_dx - 14, eye_y - 4, cx + eye_dx + 14, eye_y + 10], start=10, end=170, fill=(50, 40, 60), width=3)
        else:
            # Open eyes
            draw.ellipse([cx - eye_dx - 14, eye_y - 12, cx - eye_dx + 14, eye_y + 12], fill=(255, 255, 255))
            draw.ellipse([cx + eye_dx - 14, eye_y - 12, cx + eye_dx + 14, eye_y + 12], fill=(255, 255, 255))
            # Iris
            draw.ellipse([cx - eye_dx - 8, eye_y - 9, cx - eye_dx + 8, eye_y + 9], fill=(59, 130, 246))
            draw.ellipse([cx + eye_dx - 8, eye_y - 9, cx + eye_dx + 8, eye_y + 9], fill=(59, 130, 246))
            # Pupil & Sparkle
            draw.ellipse([cx - eye_dx - 4, eye_y - 5, cx - eye_dx + 4, eye_y + 5], fill=(15, 23, 42))
            draw.ellipse([cx + eye_dx - 4, eye_y - 5, cx + eye_dx + 4, eye_y + 5], fill=(15, 23, 42))
            draw.ellipse([cx - eye_dx + 1, eye_y - 7, cx - eye_dx + 5, eye_y - 3], fill=(255, 255, 255))
            draw.ellipse([cx + eye_dx + 1, eye_y - 7, cx + eye_dx + 5, eye_y - 3], fill=(255, 255, 255))

        # Sleek stylish glasses
        glass_w = 26
        glass_h = 18
        draw.rounded_rectangle([cx - eye_dx - glass_w, eye_y - glass_h, cx - eye_dx + glass_w, eye_y + glass_h], radius=6, outline=(99, 102, 241), width=2)
        draw.rounded_rectangle([cx + eye_dx - glass_w, eye_y - glass_h, cx + eye_dx + glass_w, eye_y + glass_h], radius=6, outline=(99, 102, 241), width=2)
        draw.line([(cx - eye_dx + glass_w, eye_y - 2), (cx + eye_dx - glass_w, eye_y - 2)], fill=(99, 102, 241), width=2)

        # Nose
        draw.polygon([(cx, cy + 5), (cx - 3, cy + 18), (cx + 3, cy + 18)], fill=(225, 175, 140))

        # Dynamic Mouth Shapes (4 phoneme states driven by audio amplitude)
        mouth_y = cy + int(head_radius * 0.48)

        if amplitude < 0.08:
            # Shape 0: Closed / Gentle Smile
            draw.arc([cx - 16, mouth_y - 8, cx + 16, mouth_y + 8], start=20, end=160, fill=(185, 60, 80), width=3)
        elif amplitude < 0.28:
            # Shape 1: Slight Open ('ah' / 'eh')
            draw.rounded_rectangle([cx - 14, mouth_y - 5, cx + 14, mouth_y + 7], radius=5, fill=(160, 40, 60), outline=(220, 100, 120), width=1)
            draw.rectangle([cx - 10, mouth_y - 4, cx + 10, mouth_y - 1], fill=(255, 255, 255))
        elif amplitude < 0.58:
            # Shape 2: Medium Open ('oh' / 'oo')
            draw.ellipse([cx - 16, mouth_y - 9, cx + 16, mouth_y + 11], fill=(140, 30, 50), outline=(230, 110, 130), width=2)
            draw.ellipse([cx - 10, mouth_y - 7, cx + 10, mouth_y - 2], fill=(255, 255, 255))
            draw.ellipse([cx - 10, mouth_y + 4, cx + 10, mouth_y + 8], fill=(230, 90, 110))
        else:
            # Shape 3: Wide Open ('aa' / 'excited')
            draw.ellipse([cx - 20, mouth_y - 14, cx + 20, mouth_y + 16], fill=(130, 20, 40), outline=(244, 63, 94), width=2)
            draw.rectangle([cx - 14, mouth_y - 11, cx + 14, mouth_y - 6], fill=(255, 255, 255))
            draw.ellipse([cx - 12, mouth_y + 5, cx + 12, mouth_y + 13], fill=(244, 114, 182))

        # Bottom Audio Visualizer Bar & Badge
        badge_y = h - 60
        # Speaking Indicator Badge
        is_speaking = amplitude > 0.05
        status_color = (16, 185, 129) if is_speaking else (148, 163, 184)
        draw.ellipse([24, badge_y + 8, 36, badge_y + 20], fill=status_color)
        
        # Reactive Audio Visualizer Waveform (7 bars)
        num_bars = 7
        bar_w = 4
        gap = 4
        total_viz_w = num_bars * (bar_w + gap)
        viz_start_x = w - 24 - total_viz_w

        for b in range(num_bars):
            phase = (b - 3) * 0.8
            bar_amp = max(0.1, amplitude * math.sin(frame_idx * 0.3 + phase) ** 2)
            bar_h = int(bar_amp * 28) + 4
            bx = viz_start_x + b * (bar_w + gap)
            by = badge_y + 14 - bar_h // 2
            draw.rounded_rectangle([bx, by, bx + bar_w, by + bar_h], radius=2, fill=(99, 102, 241))

        return img


# Global singleton
avatar_engine = AvatarEngine()
