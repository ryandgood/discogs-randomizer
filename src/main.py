from fastapi import FastAPI
from .lib.discogs import DiscogsClient
from .lib.randomizer import AlbumRandomizer
import os
import uvicorn
import re

app = FastAPI()

discogs = DiscogsClient(token=os.getenv("DISCOGS_TOKEN",""), username=os.getenv("DISCOGS_USERNAME", ""))
randomizer = AlbumRandomizer("./collection.json")

@app.get("/album")
async def get_album():

    await discogs.sync()

    album = randomizer.pick_random()

    # create a list of artists, but strip out any digits in parenthesis which discogs adds for some reaso
    artists = [re.sub(r'\s*\(\d+\)\s*', ' ', artist.name) for artist in album.basic_information.artists]

    return {
        "artists": artists,
        "album": album.basic_information.title
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
