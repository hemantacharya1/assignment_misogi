 # backend/services/whisper_transcriber.py
import os
from faster_whisper import WhisperModel

USE_FAST_WHISPER = os.getenv("USE_FAST_WHISPER", "True") == "True"

if USE_FAST_WHISPER:
    model = WhisperModel("base", compute_type="int8")
else:
    import whisper
    model = whisper.load_model("base")

def transcribe_audio(audio_path: str):
    if USE_FAST_WHISPER:
        segments, _ = model.transcribe(audio_path, beam_size=5)
        result = {
            "segments": [
                {
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text.strip()
                } for seg in segments
            ]
        }
    else:
        result = model.transcribe(audio_path)
        result = {
            "segments": [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip()
                } for seg in result["segments"]
            ]
        }
    return result
