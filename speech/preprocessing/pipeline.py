import os
import logging
from pathlib import Path
import speech.evaluation.transcription as transcription
import speech.speaker_recognition as speaker_rec
import speech.voice_cleaning.noise_reduction as voice_clean

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def evaluate_audiofile(audio_file: str) -> (str, str):
    logging.info("Audio preprocessing...")

    source_transcription = transcription.transcribe(audio_file)
    logging.info("Source audio file transcribed")

    # deep_filter_audiofile = voice_clean.clean(audio_file)
    output_audio_folder = str(Path(audio_file).parent)
    deep_filter_audiofile = os.path.join(output_audio_folder, "audio_DeepFilterNet3.wav")
    deep_filter_transcription = transcription.transcribe(deep_filter_audiofile)
    logging.info("Source audio cleaned with DeepFilter and transcribed")

    return source_transcription, deep_filter_transcription

BASE_DIR = Path(__file__).resolve().parents[2]
source_audiofile = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260508_174743", "audio.wav")
transcription_progress = evaluate_audiofile(source_audiofile)
for t in transcription_progress:
    print(t + '\n')
