from pyannote.audio import Pipeline
from config import huggingface_token
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
audio_file_1speaker = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260415_203515", "audio.wav")
audio_file_2speakers = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260507_082323", "audio.wav")
audio_file_2speakers_2 = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260507_082903", "audio.wav")
audio_file_2speakers_3 = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260507_083917", "audio.wav")


def detect_speakers_number(audio_file):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                        use_auth_token=huggingface_token)
    diarization = pipeline(audio_file)
    speakers = set()

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        speakers.add(speaker)

    print("Detected speakers:", speakers)
    print("Number of speakers:", len(speakers))

# detect_speakers_number(audio_file_1speaker) # True
# detect_speakers_number(audio_file_2speakers) # False
# detect_speakers_number(audio_file_2speakers_2) # False
detect_speakers_number(audio_file_2speakers_3) # True
