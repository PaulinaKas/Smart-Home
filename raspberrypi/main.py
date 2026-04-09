from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
import subprocess
import os


# uvicorn raspberrypi.main:app --host 127.0.0.1 --port 8000
# uvicorn raspberrypi.main:app --host 0.0.0.0 --port 8000
# http://127.0.0.1:8000/docs

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class Recorder:
    def __init__(self):
        self.process = None

    def start(self):
        if self.process is None:  # checks if recording is already running
            os.makedirs(os.path.join(BASE_DIR, "recordings"), exist_ok=True)

            filename = datetime.now().strftime("%Y%m%d_%H%M%S.wav")
            filepath = f"{BASE_DIR}/recordings/{filename}"

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

@app.get("/ui", response_class=HTMLResponse)
def ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
