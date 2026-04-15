from faster_whisper import WhisperModel
import re

model = WhisperModel("small",
                     device="cpu",
                     compute_type="int8")  # tiny / base / small / medium / large

def transcribe(audio_file) -> str:
    segments, info = model.transcribe(audio_file, language="pl")

    # print("Detected language:", info.language)

    full_text = ""
    for segment in segments:
        full_text += segment.text + " "

    return normalize(full_text)

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text