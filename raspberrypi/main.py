from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from config import ip_address
import subprocess
import os
import requests


# uvicorn raspberrypi.main:app --host 127.0.0.1 --port 8000
# uvicorn raspberrypi.main:app --host 0.0.0.0 --port 8000
# http://127.0.0.1:8000/docs

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class Recorder:
    def __init__(self):
        self.process = None
        self.current_session = None

    def start(self):
        if self.process is None:
            sessions_dir = os.path.join(BASE_DIR, "sessions")
            os.makedirs(sessions_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_path = os.path.join(sessions_dir, f"session_{timestamp}")
            os.makedirs(session_path, exist_ok=True)

            audio_path = os.path.join(session_path, "audio.wav")

            self.process = subprocess.Popen([
                "arecord",
                "-D", "plughw:3,0", # my microphone settings (arecord -l)
                "-f", "cd",
                audio_path
            ])

            self.current_session = session_path

            print(f"Recording started in: {session_path}")
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

    if success and recorder.current_session:
        requests.post(
            f"http://{ip_address}:8001/pull",
            json={"session_path": recorder.current_session}
        )

    return {
        "status": "recording_stopped" if success else "not_recording",
        "session_path": recorder.current_session
    }

@app.get("/ui", response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/status")
def status():
    return {
        "recording": recorder.process is not None,
        "session_path": recorder.current_session
    }
