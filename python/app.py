from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request

import trafikLab
from spotifyTest import fillPlaylist
from spotifyTest import getAccessToken

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")

accessToken = ""

@app.get("/callback")
async def loginSpotify(request: Request):
    code = request.query_params.get("code")
    print(code)
    global accessToken
    accessToken = await getAccessToken(code)

    return templates.TemplateResponse('index.html', context={'request': request})

@app.post("/spotify/generate_playlist/genre={genre}")
async def spotifyGeneratePlaylist(request: Request, genre: str):
    playlistInfo = await fillPlaylist(genre)
    url = playlistInfo["url"]
    image = playlistInfo["image"]
    return templates.TemplateResponse('index_generated.tpl', context={'request': request, 'url': url, 'image': image})


@app.get("/spotify/login")
async def spotify_login(request: Request):
    return templates.TemplateResponse('spotifylogin.html', context={'request': request})

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

    transfer_stops = trafikLab.get_transfer_stops(trip)

    totalSeconds = trip.totalSeconds*1000
    totalTime = trip.totalTime
    print(totalTime)

    return templates.TemplateResponse('index_generated.tpl',
                                      context={'request': request, 
                                               'access_token' : accessToken, 
                                               'total_seconds' : totalSeconds, 
                                               'genre' : genre, 
                                               'fromStop' : fromStop, 
                                               'toStop' : toStop,
                                               'transfer_stops': transfer_stops})
    #return Response(await trafikLab.findTrip(fromStop, toStop), media_type="application/json")