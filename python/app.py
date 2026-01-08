from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import trafikLab
from spotifyTest import fillPlaylist
from spotifyTest import getAccessToken

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/callback")
async def loginSpotify(request: Request):
    code = request.query_params.get("code")
    print(code)
    accessToken = await getAccessToken(code)
    request.session["accessToken"] = accessToken

    return templates.TemplateResponse('index.html', context={'request': request})

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
async def getTrip(request: Request):
    print(request.query_params)
    query_params = request.query_params

    fromStop = query_params.get('from')
    toStop = query_params.get('to')
    genre = query_params.get('genre')

    print(fromStop, toStop)
    trip = await trafikLab.findTrip(fromStop, toStop)

    totalSeconds = trip.totalSeconds*1000
    totalTime = trip.totalTime

    print(totalTime)
    accessToken = request.session.get("accessToken")
    print("Current sessions accessToken: " + accessToken)

    if request.headers.get('Content-Type') == 'application/json':

        

    return templates.TemplateResponse('index_generated.tpl', context={'request': request, 'access_token' : accessToken, 'total_seconds' : totalSeconds, 'genre' : genre, 'fromStop' : fromStop,'toStop' : toStop})

@app.get("/route_stops")
async def route_stops(request: Request):
    query_params = request.query_params
    fromStop = query_params.get("from")
    toStop = query_params.get("to")

    stops = await trafikLab.findRouteStops(fromStop, toStop)
    return JSONResponse({"stops": stops})