import os
import asyncio
import uuid
import wave
import subprocess
import numpy as np
from typing import Tuple, List, Optional
import imageio_ffmpeg

try:
    import edge_tts
    _EDGE_TTS_AVAILABLE = True
except ImportError:
    _EDGE_TTS_AVAILABLE = False

try:
    import pyttsx3
    _PYTTSX3_AVAILABLE = True
except ImportError:
    _PYTTSX3_AVAILABLE = False


class TTSEngine:
    """
    Neural Text-to-Speech synthesizer supporting English and Hindi with audio amplitude analysis.
    """

    VOICES = {
        "en": {
            "female": "en-US-JennyNeural",
            "male": "en-US-GuyNeural"
        },
        "hi": {
            "female": "hi-IN-SwaraNeural",
            "male": "hi-IN-MadhurNeural"
        },
        "hinglish": {
            "female": "en-IN-NeerjaNeural",
            "male": "en-IN-PrabhatNeural"
        }
    }

    def __init__(self, output_dir: str = "media/audio"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    async def _generate_edge_tts(self, text: str, voice: str, output_path: str) -> None:
        communicator = edge_tts.Communicate(text, voice)
        await communicator.save(output_path)

    def _generate_pyttsx3(self, text: str, output_path: str, lang: str = "en") -> None:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        # Select voice if available
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
        engine.save_to_file(text, output_path)
        engine.runAndWait()

    def synthesize(
        self,
        text: str,
        language: str = "en",
        gender: str = "female",
        output_filename: Optional[str] = None
    ) -> Tuple[str, float, List[float]]:
        """
        Synthesizes text into high quality audio, converts to standard 44.1kHz WAV,
        and computes normalized RMS amplitude envelopes per video frame (25 fps).
        Returns: (wav_audio_path, duration_seconds, frame_amplitudes)
        """
        if not text or not text.strip():
            text = "Welcome to this concept lesson."

        lang_lower = language.lower()
        if "hinglish" in lang_lower:
            lang_key = "hinglish"
        elif lang_lower in ["hi", "hindi"]:
            lang_key = "hi"
        else:
            lang_key = "en"

        voice = self.VOICES.get(lang_key, {}).get(gender, "en-US-JennyNeural")

        if not output_filename:
            file_id = f"audio_{uuid.uuid4().hex[:8]}"
        else:
            file_id = output_filename.replace(".wav", "").replace(".mp3", "")

        raw_audio_path = os.path.join(self.output_dir, f"{file_id}_raw.mp3")
        wav_audio_path = os.path.join(self.output_dir, f"{file_id}.wav")

        success = False
        if _EDGE_TTS_AVAILABLE:
            try:
                import concurrent.futures
                async def _timed_gen():
                    await asyncio.wait_for(self._generate_edge_tts(text, voice, raw_audio_path), timeout=6.0)

                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    future = pool.submit(asyncio.run, _timed_gen())
                    future.result(timeout=7.0)

                success = os.path.exists(raw_audio_path) and os.path.getsize(raw_audio_path) > 0
            except Exception as e:
                print(f"[TTSEngine] Edge-TTS error or timeout: {e}. Attempting local fallback.")
                success = False

        if not success and _PYTTSX3_AVAILABLE:
            try:
                self._generate_pyttsx3(text, wav_audio_path, lang=lang_key)
                raw_audio_path = wav_audio_path
                success = True
            except Exception as e:
                print(f"[TTSEngine] pyttsx3 fallback error: {e}")

        # Convert to standard 44.1kHz mono WAV for amplitude analysis & video alignment
        if raw_audio_path != wav_audio_path and os.path.exists(raw_audio_path):
            cmd = [
                self.ffmpeg_exe, "-y",
                "-i", raw_audio_path,
                "-ar", "44100",
                "-ac", "1",
                wav_audio_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            try:
                os.remove(raw_audio_path)
            except OSError:
                pass

        # Calculate duration and per-frame amplitudes (25 fps)
        duration, amplitudes = self._analyze_audio_amplitude(wav_audio_path, fps=25)
        return wav_audio_path, duration, amplitudes

    def _analyze_audio_amplitude(self, wav_path: str, fps: int = 25) -> Tuple[float, List[float]]:
        """
        Reads WAV audio and computes the normalized RMS amplitude per frame at given fps.
        """
        if not os.path.exists(wav_path):
            return 3.0, [0.0] * int(3.0 * fps)

        try:
            with wave.open(wav_path, "rb") as wf:
                sample_rate = wf.getframerate()
                num_samples = wf.getnframes()
                audio_bytes = wf.readframes(num_samples)
                duration = num_samples / float(sample_rate)

            # Convert 16-bit PCM audio bytes to float numpy array
            samples = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
            if len(samples) == 0:
                return max(1.0, duration), [0.0] * max(1, int(duration * fps))

            samples = samples / 32768.0  # Normalize to [-1.0, 1.0]

            samples_per_frame = int(sample_rate / fps)
            total_frames = max(1, int(np.ceil(len(samples) / samples_per_frame)))
            amplitudes = []

            for i in range(total_frames):
                start = i * samples_per_frame
                end = min(start + samples_per_frame, len(samples))
                chunk = samples[start:end]
                if len(chunk) > 0:
                    rms = np.sqrt(np.mean(chunk ** 2))
                    amplitudes.append(float(rms))
                else:
                    amplitudes.append(0.0)

            # Smooth and normalize amplitudes to 0.0 - 1.0 range
            max_amp = max(amplitudes) if amplitudes else 1.0
            if max_amp > 0:
                normalized = [min(1.0, a / (max_amp * 0.85)) for a in amplitudes]
            else:
                normalized = amplitudes

            return max(1.0, duration), normalized
        except Exception as e:
            print(f"[TTSEngine] Amplitude extraction error: {e}")
            return 3.0, [0.1] * (3 * fps)


# Global singleton
tts_engine = TTSEngine()
