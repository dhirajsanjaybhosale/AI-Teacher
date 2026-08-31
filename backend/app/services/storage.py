import os
from typing import Dict, Any

class StorageService:
    """
    Manages local filesystem paths for uploads, generated audio, and generated videos.
    """

    def __init__(
        self,
        upload_dir: str = "media/uploads",
        audio_dir: str = "media/audio",
        video_dir: str = "media/videos"
    ):
        self.upload_dir = upload_dir
        self.audio_dir = audio_dir
        self.video_dir = video_dir

        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)

    def get_upload_path(self, filename: str) -> str:
        return os.path.join(self.upload_dir, filename)

    def get_audio_path(self, filename: str) -> str:
        return os.path.join(self.audio_dir, filename)

    def get_video_path(self, filename: str) -> str:
        return os.path.join(self.video_dir, filename)


# Global singleton
storage_service = StorageService()
