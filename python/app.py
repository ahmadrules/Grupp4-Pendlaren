from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates

import requests

import trafikLab
from spotifyTest import fillPlaylist, getAccessToken

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")

accessToken = ""


@app.get("/callback")
async def loginSpotify(request: Request):
    global accessToken

    accessToken = await getAccessToken()

    profile_response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={
            "Authorization": f"Bearer {accessToken}"
        }
    )
    profile = profile_response.json()

    username = profile.get("display_name", "")
    image_url = ""

    if profile.get("images"):
        image_url = profile["images"][0]["url"]

    # Redirect till startsidan + sätt cookies
    response = RedirectResponse(url="/")

    response.set_cookie("spotify_logged_in", "true", httponly=False)
    response.set_cookie("spotify_username", username, httponly=False)
    response.set_cookie("spotify_image", image_url, httponly=False)

    return response

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/search")
async def getTrip(request: Request):
    query_params = request.query_params

    fromStop = query_params.get("from")
    toStop = query_params.get("to")
    genre = query_params.get("genre")

    trip = await trafikLab.findTrip(fromStop, toStop)

    totalSeconds = trip.totalSeconds * 1000
    totalTime = trip.totalTime

    return templates.TemplateResponse(
        "index_generated.tpl",
        {
            "request": request,
            "access_token": accessToken,
            "total_seconds": totalSeconds,
            "genre": genre,
            "fromStop": fromStop,
            "toStop": toStop
        }
    )

@app.post("/spotify/generate_playlist/genre={genre}")
async def spotifyGeneratePlaylist(request: Request, genre: str):
    playlistInfo = await fillPlaylist(genre)
    url = playlistInfo["url"]
    image = playlistInfo["image"]

    return templates.TemplateResponse(
        "index_generated.tpl",
        {
            "request": request,
            "url": url,
            "image": image
        }
    )

@app.get("/spotify/login")
async def spotify_login(request: Request):
    return templates.TemplateResponse("spotifylogin.html", {"request": request})
