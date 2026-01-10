import jsonpickle
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from fastapi import FastAPI, Request, Form

import trafikLab
from spotifyTest import fillPlaylist
from spotifyTest import getAccessToken

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


@app.post("/search")
async def getTrip(request: Request, fromStop: str = Form(), toStop: str = Form(), genre: str = Form(),
                  contentType: str = Form()):
    trip = await trafikLab.findTrip(fromStop, toStop)
    transfer_details = trafikLab.get_transfer_details(trip)

    totalSeconds = trip.totalSeconds * 1000
    totalTime = trip.totalTime

    access_token = request.cookies.get("accessToken")
    print("RETRIEVED ACCESS TOKEN FROM COOKIES " + access_token)

    playList = await fillPlaylist(genre, totalSeconds, access_token, fromStop, toStop)

    playlistUrl = playList['url']
    playlistImage = playList['image']

    trip.playlistUrl = playlistUrl
    trip.playlistImage = playlistImage

    if contentType == "application/json":
        return jsonpickle.encode(trip)

    else:
        return templates.TemplateResponse('index_generated.tpl',
                                          context={'request' : request,
                                                   'playlistUrl': playlistUrl,
                                                   'playlistImage': playlistImage,
                                                   'trip': trip,
                                                   'transfers': transfer_details})
