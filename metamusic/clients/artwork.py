#!/usr/bin/env python3
"""
Author : root <root@localhost>
Date   : 2022-11-16
Purpose: Program to retrieve HD artwork from iTunes
"""

from term_image.image import from_url
import requests
import re
import typer


app = typer.Typer()
# --------------------------------------------------
def get_release_object(release: str, artist: str) -> dict:
    release_info = {}
    url = "https://artwork.themoshcrypt.net/api/search?keyword="
    release_query = "%2B".join(release.split()).lower()
    response = requests.get(url + release_query).json()
    for result in response["results"]:
        result_collection = result["collectionCensoredName"].lower().split(" -")[0]
        result_artist = result["artistName"].lower()
        if result_artist == artist.lower():
            if result_collection == release.lower():
                release_info = result
        if not release_info:
            raise ValueError(
                "No release found. check release and artist name and try again."
            )
    return release_info


# --------------------------------------------------
def get_high_definition_artwork_url(release_object: str) -> str:
    high_definition_url = "https://s1.mzstatic.com/us/r1000/063/"
    low_definition_url = release_object["artworkUrl100"]
    pattern = re.compile("Music.+(\.jpg)(?=/)|Music.+(\.png)(?=/)")
    artwork_directory = pattern.search(low_definition_url)
    jpg_artwork_directory = artwork_directory.group(0)
    png_artwork_directory = artwork_directory.group(1)
    if jpg_artwork_directory:
        return high_definition_url + jpg_artwork_directory
    elif png_artwork_directory:
        return high_definition_url + png_artwork_directory
    else:
        raise ValueError("No high definition artwork found")


# --------------------------------------------------
@app.command()
def display_artwork(release: str, artist: str):

    release_object = get_release_object(release=release, artist=artist)
    artwork_url = get_high_definition_artwork_url(release_object)
    image = from_url(artwork_url)
    image.draw()


# --------------------------------------------------
if __name__ == "__main__":
    app()
