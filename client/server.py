from fastapi import FastAPI
from config import ssh_path
import subprocess
import os

# uvicorn client.server:app --host 0.0.0.0 --port 8001

app = FastAPI()

@app.post("/pull")
def pull(data: dict):
    session = data["session_path"]
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    session_path = os.path.join(BASE_DIR, "raspberrypi", "sessions")

    print("Downloading:", session)

    result = subprocess.run([
        "scp",
        "-i",
        ssh_path,
        "-r",
        f"pi@raspberrypi:{session}",
        session_path
    ])

    if result.returncode == 0:
        print("Downloading finished")
        return {"status": "success"}
    else:
        print("Downloading failed")
        return {"status": "error"}