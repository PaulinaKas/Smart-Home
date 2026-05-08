import subprocess
import os
from pathlib import Path

def normalize_audio(input_audio_file, output_dir):
    normalized_audio = os.path.join(output_dir, "normalized.wav")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i",
        input_audio_file,
        "-ac",
        "1",
        "-ar",
        "16000",
        normalized_audio
    ], check=True)

    return normalized_audio

def clean(file_path: str):
    input_audio_file = file_path
    output_audio_folder = str(Path(file_path).parent)

    if not os.path.exists(input_audio_file):
        raise FileNotFoundError(output_audio_folder)

    normalized_audio = normalize_audio(input_audio_file, output_audio_folder)

    command = [
        "deepFilter",
        normalized_audio,
        "-o",
        output_audio_folder
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

        print("SUCCESS")
        print(result.stdout)

    except subprocess.CalledProcessError as e:

        print("FAILED")
        print(e.stderr)

    return normalized_audio