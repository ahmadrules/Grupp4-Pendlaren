from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import trafikLab

app = FastAPI()

app.mount("/", StaticFiles(directory="python/static", html=True), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}
