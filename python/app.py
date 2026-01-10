import jsonpickle
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response
from starlette.templating import Jinja2Templates

from fastapi import Cookie, FastAPI, Request, Form

import trafikLab
from spotifyTest import fillPlaylist
from spotifyTest import getAccessToken
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")

from fastapi.responses import RedirectResponse

@app.get("/callback")
async def loginSpotify(request: Request):
    code = request.query_params.get("code")

    accessToken = await getAccessToken(code)

    response = RedirectResponse(url="/")
    response.set_cookie(
        key="accessToken",
        value=accessToken,
        samesite="lax",
        max_age=3600
    )
    return response


@app.get("/")
async def index(request: Request):
    access_token = request.cookies.get("accessToken")
    spotify_logged_in = access_token is not None

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "spotify_logged_in": spotify_logged_in
        }
    )

class Search(BaseModel):
    fromStop : str
    to: str
    genre : str


@app.post("/search")
async def getTrip(request: Request, fromStop : str = Form(), toStop: str = Form(), genre: str = Form()):
    print(fromStop, toStop)
    print(await request.body())
    trip = await trafikLab.findTrip(fromStop, toStop)
    transfer_stops = trafikLab.get_transfer_stops(trip)

    totalSeconds = trip.totalSeconds*1000
    totalTime = trip.totalTime

    print(totalTime)

    access_token = request.cookies.get("accessToken")
    print("RETRIEVED ACCESS TOKEN FROM COOKIES " + access_token)

    playList = await fillPlaylist(genre, totalSeconds, access_token)

    playlistUrl = playList['url']
    playlistImage = playList['image']

    trip.playlistUrl = playlistUrl
    trip.playlistImage = playlistImage

    print(">>>PLAYLIST URL: " + playList['url'])
    print(jsonpickle.encode(trip))

    if request.headers.get("Content-Type") == "application/json":
        return JSONResponse(jsonpickle.encode(trip))

    else:
        return templates.TemplateResponse('index_generated.tpl',
                                      context={'request': request,
                                               'genre' : genre,
                                               'fromStop' : fromStop,
                                               'toStop' : toStop,
                                               'transfer_stops' : transfer_stops,
                                               'playListUrl' : playlistUrl,
                                               'playlistImage' : playlistImage,})
    #return Response(await trafikLab.findTrip(fromStop, toStop), media_type="application/json")

@app.get("/route_stops")
async def route_stops(request: Request):
    query_params = request.query_params
    fromStop = query_params.get("from")
    toStop = query_params.get("to")

    stops = await trafikLab.findRouteStops(fromStop, toStop)
    return JSONResponse({"stops": stops})