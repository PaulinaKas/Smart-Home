from fastapi import FastAPI
from datetime import datetime
import subprocess
import os

# uvicorn raspberrypi.main:app --host 127.0.0.1 --port 8000
# http://127.0.0.1:8000/docs

app = FastAPI()

os.makedirs("recordings", exist_ok=True)

class Recorder:
    def __init__(self):
        self.process = None

    def start(self):
        if self.process is None:  # checks if recording is already running
            os.makedirs("recordings", exist_ok=True)

            filename = datetime.now().strftime("%Y%m%d_%H%M%S.wav")
            filepath = f"recordings/{filename}"

            self.process = subprocess.Popen([
                "arecord",
                "-D", "plughw:3,0",  # <- my microphone settings (arecord -l)
                "-f", "cd",
                filepath
            ])

            print(f"Recording started: {filepath}")
            return True

        return False

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
            return True
        return False

recorder = Recorder()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/start")
def start():
    success = recorder.start()
    return {"status": "recording_started" if success else "already_recording"}


@app.get("/stop")
def stop():
    success = recorder.stop()
    return {"status": "recording_stopped" if success else "not_recording"}