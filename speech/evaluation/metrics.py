import os
from pathlib import Path
import jiwer
from speech.evaluation.transcription import transcribe

BASE_DIR = Path(__file__).resolve().parents[2]

def validate_original_vs_test(test_txt, original_txt):
    print(f"{original_txt} \n\n {test_txt}")
    print("WER:", jiwer.wer(original_txt, test_txt)) # word error rate
    print("CER:", jiwer.cer(original_txt, test_txt)) # character error rate
    print("MER", jiwer.mer(original_txt, test_txt))  # match error rate
    print("WIL", jiwer.mer(original_txt, test_txt))  # word information lost

# audio_file1 = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260415_203515", "audio.wav")
# test_transcription1 = transcribe(audio_file1)
# original_transcription1 = normalize(session_20260415_203515.audio_transcription.original_audio_transcription)
# validate_original_vs_test(original_transcription1, test_transcription1)

# audio_file2 = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260507_082323", "audio.wav")
# test_transcription2 = transcribe(audio_file2)
# original_transcription2 = normalize(session_20260507_082323.audio_transcription.original_audio_transcription)
# validate_original_vs_test(original_transcription2, test_transcription2)

audio_file3 = os.path.join(BASE_DIR, "raspberrypi", "sessions", "session_20260508_174743", "audio.wav")
test_transcription3 = transcribe(audio_file3)
print(test_transcription3)