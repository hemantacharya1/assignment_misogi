# backend/api/upload.py
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from uuid import uuid4

from backend.services.ffmpeg_utils import extract_audio
from backend.services.whisper_transcriber import transcribe_audio

UPLOAD_DIR = "data/raw"
AUDIO_DIR = "data/audio"
TRANSCRIPT_DIR = "data/transcripts"

router = APIRouter()

@router.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        os.makedirs(AUDIO_DIR, exist_ok=True)
        os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

        # Save uploaded video
        video_id = str(uuid4())
        video_path = os.path.join(UPLOAD_DIR, f"{video_id}_{file.filename}")
        with open(video_path, "wb") as f:
            f.write(await file.read())

        # Extract audio
        audio_path = os.path.join(AUDIO_DIR, f"{video_id}.wav")
        extract_audio(video_path, audio_path)

        # Transcribe
        transcript = transcribe_audio(audio_path)

        # Save transcript
        transcript_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}.json")
        with open(transcript_path, "w") as f:
            import json
            json.dump(transcript, f, indent=2)

        return JSONResponse({
            "video_id": video_id,
            "filename": file.filename,
            "transcript": transcript
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
