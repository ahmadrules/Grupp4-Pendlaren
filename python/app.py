from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response
from starlette.templating import Jinja2Templates

import trafikLab

app = FastAPI()

app.mount("/", StaticFiles(directory="python/static", html=True), name="static")
templates = Jinja2Templates(directory="python/templates")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/?from-stop={fromStop}&to-stop={toStop}")
async def getTrip(fromStop: str, toStop: str):
    print(fromStop, toStop)
    return Response(trafikLab.findTrip(fromStop, toStop), media_type="application/json")