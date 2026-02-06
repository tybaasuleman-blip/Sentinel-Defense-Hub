from fastapi import FastAPI

app = FastAPI()

# This is the "Front Door" (/)
@app.get("/")
def home():
    return {
        "message": "Sentinel Defense Hub is ONLINE",
        "status": "Listening for threats",
        "action": "Go to http://127.0.0.1:8000/docs to test"
    }

# This is your scanning tool
@app.get("/scan-live")
def scan_live(url: str = "none"):
    return {"info": f"Scanning started for {url}"}