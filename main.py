from fastapi import FastAPI
from .lib.discogs import DiscogsClient
from .lib.randomizer import AlbumRandomizer
import os
import uvicorn

app = FastAPI()

discogs = DiscogsClient(token=os.getenv("DISCOGS_TOKEN",""), username=os.getenv("DISCOGS_USERNAME", ""))
meh = discogs.sync()
meh.close()
randomizer = AlbumRandomizer("./collection.json")

@app.get("/album")
async def get_album():

    await discogs.sync()

    album = randomizer.pick_random()

    return {
        "artists": [artist.name for artist in album.basic_information.artists],
        "album": album.basic_information.title
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
