from fastapi import FastAPI
from .lib.discogs import DiscogsClient
from .lib.randomizer import AlbumRandomizer
import os


app = FastAPI()

discogs = DiscogsClient(token=os.getenv("DISCOGS_TOKEN",""), username=os.getenv("DISCOGS_USERNAME", ""))
meh = discogs.sync()
randomizer = AlbumRandomizer("./collection.json")

@app.get("/album")
async def get_album():

    await discogs.sync()

    album = randomizer.pick_random()
    return album
