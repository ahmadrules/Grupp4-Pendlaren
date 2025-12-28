from fastapi.staticfiles import StaticFiles
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request

import trafikLab

app = FastAPI()

app.mount("/static", StaticFiles(directory="python/static", html=True), name="static")
templates = Jinja2Templates(directory="python/templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/from={fromStop}&to={toStop}")
async def getTrip(request: Request, fromStop: str, toStop: str):
    print(fromStop, toStop)
    return Response(await trafikLab.findTrip(fromStop, toStop), media_type="application/json")