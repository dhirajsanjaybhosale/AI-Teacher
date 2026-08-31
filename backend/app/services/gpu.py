import torch
from typing import Dict, Any

class GPUService:
    """
    Detects hardware capabilities and GPU availability for AI avatar rendering.
    """

    def __init__(self):
        self.is_cuda_available = torch.cuda.is_available()
        self.device_name = torch.cuda.get_device_name(0) if self.is_cuda_available else "CPU (Neural Engine)"
        self.device_type = "cuda" if self.is_cuda_available else "cpu"
        self.avatar_mode = "GPU Lip-Sync (Wav2Lip/SadTalker)" if self.is_cuda_available else "Lightweight 2D (Amplitude Synced)"

    def get_status(self) -> Dict[str, Any]:
        return {
            "gpu_available": self.is_cuda_available,
            "device": self.device_type,
            "device_name": self.device_name,
            "avatar_mode": self.avatar_mode
        }


# Global singleton
gpu_service = GPUService()
