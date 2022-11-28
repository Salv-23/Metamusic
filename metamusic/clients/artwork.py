#!/usr/bin/env python3
"""
Author : root <root@localhost>
Date   : 2022-11-16
Purpose: Program to retrieve and display HD artwork in the terminal.
"""

from term_image.image import from_url
import requests
import re


# --------------------------------------------------
def get_release_information(release: str, artist: str) -> dict:
    """Find release information for a given release-artist name."

    Args:
        release (str): The name of the release to retrieve
        artist (str): The name of the release artist

    Raises:
        ValueError: When the release information is not found

    Returns:
        dict: Useful release information such as URLs for release artwork.
    """

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
    """Fetches an URL for a high-definition artwork.

    Retrieves the release path from a low-definition artwork URL
    and constructs the URL for a high-definition artwork.

    Args:
        release_object (str):
            A release object returned from the get_release_information function.

    Returns:
        str: An URL for the high-definition artwork.
    """

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
        raise ValueError("No artwork found, check release_object and try again.")


# --------------------------------------------------
def main(release: str, artist: str):
    """Display artwork for a given release and artist in the terminal.

    Args:
        release (str): The name of the release.
        artist (str): The name of the artist.
    """

    release_object = get_release_information(release=release, artist=artist)
    artwork_url = get_high_definition_artwork_url(release_object)
    image = from_url(artwork_url)
    image.draw()


# --------------------------------------------------
if __name__ == "__main__":
    main()
