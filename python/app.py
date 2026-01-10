from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response
from starlette.templating import Jinja2Templates
from trafikLab import get_transfer_details

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

    global accessToken
    accessToken = await getAccessToken(code)

    response = RedirectResponse(url="/")
    response.set_cookie(
        key="accessToken",
        value=accessToken,
        samesite="lax",
        max_age=8000
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
    trip = await trafikLab.findTrip(fromStop, toStop)
    transfer_details = trafikLab.get_transfer_details(trip)

    totalSeconds = trip.totalSeconds*1000
    totalTime = trip.totalTime

    print(totalTime)

    #accessToken = request.cookies.get("accessToken")
    #print("RETRIEVED ACCESS TOKEN FROM COOKIES" + access_Token)

    return templates.TemplateResponse('index_generated.tpl',
                                      context={'request': request, 'access_token' : accessToken, 'total_seconds' : totalSeconds, 'genre' : genre, 'fromStop' : fromStop, 'toStop' : toStop, 'trip' : trip, 'transfers' : transfer_details})
    #return Response(await trafikLab.findTrip(fromStop, toStop), media_type="application/json")

@app.get("/route_stops")
async def route_stops(request: Request):
    query_params = request.query_params
    fromStop = query_params.get("from")
    toStop = query_params.get("to")

    stops = await trafikLab.findRouteStops(fromStop, toStop)
    return JSONResponse({"stops": stops})