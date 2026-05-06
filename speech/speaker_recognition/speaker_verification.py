from pyannote.audio import Pipeline
from collections import set
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
audio_file = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260415_203515", "audio.wav")

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
diarization = pipeline(audio_file)
speakers = set()

for turn, _, speaker in diarization.itertracks(yield_label=True):
    speakers.add(speaker)

print("Detected speakers:", speakers)
print("Number of speakers:", len(speakers))

if len(speakers) == 1:
    print("Audio contains ONE speaker")
else:
    print("Audio contains MULTIPLE speakers")