import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes_lesson import router as lesson_router
from app.api.routes_segment import router as segment_router
from app.api.routes_interact import router as interact_router
from app.api.routes_assessment import router as assessment_router

# Ensure media directory exists
os.makedirs("media/videos", exist_ok=True)
os.makedirs("media/audio", exist_ok=True)

app = FastAPI(
    title="AI Teacher API",
    description="Adaptive AI Teacher Platform — AI Innovation Hackathon 2026",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static media files
app.mount("/media", StaticFiles(directory="media"), name="media")

# Include feature routers
app.include_router(lesson_router)
app.include_router(segment_router)
app.include_router(interact_router)
app.include_router(assessment_router)


@app.get("/health")
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint returning system status and device mode.
    """
    import torch
    return {
        "status": "ok",
        "service": "AI Teacher API",
        "gpu_available": torch.cuda.is_available(),
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
