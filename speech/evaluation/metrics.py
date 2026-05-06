import os
import jiwer
from raspberrypi.transcription import transcribe, normalize
from raspberrypi.sessions.session_20260415_203515 import audio_transcription


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
audio_file = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260415_203515", "audio.wav")
test_transcription = transcribe(audio_file)
original_transcription = normalize(audio_transcription.original_audio_transcription)

def validate_original_vs_test(test_txt, original_txt):
    print(f"{original_txt} \n\n {test_txt}")
    print("WER:", jiwer.wer(original_txt, test_txt)) # word error rate
    print("CER:", jiwer.cer(original_txt, test_txt)) # character error rate
    print("MER", jiwer.mer(original_txt, test_txt))  # match error rate
    print("WIL", jiwer.mer(original_txt, test_txt))  # word information lost

validate_original_vs_test(original_transcription, test_transcription)