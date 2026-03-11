from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
def system_status():
    return {"status": "AI surveillance system running"}
