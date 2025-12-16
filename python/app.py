from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/", StaticFiles(directory="python/static", html=True), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}
