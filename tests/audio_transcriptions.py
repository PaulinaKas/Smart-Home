import os
from jiwer import wer, cer
from raspberrypi.transcription import transcribe, normalize
from raspberrypi.sessions.session_20260415_203515 import audio_transcription


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
audio_file = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260415_203515", "audio.wav")
test_transcription = transcribe(audio_file)
original_transcription = normalize(audio_transcription.original_audio_transcription)

def validate_original_vs_test(test_txt, original_txt):
    print(f"{original_txt} \n\n {test_txt}")
    print("WER:", wer(original_txt, test_txt))
    print("CER:", cer(original_txt, test_txt))

validate_original_vs_test(original_transcription, test_transcription)