#!/usr/bin/env python3
"""
Author : Salvador <salvador.estrella.ortiz@gmail.com>
Date   : 2022-09-14
Purpose: Query artist information from musicbrainz API
"""

import argparse
import requests
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Query artist metadata from MusicBrainz",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-a",
        "--artist",
        help="An artist to search",
        metavar="artist",
        nargs="+",
        type=str,
        required=True,
    )

    return parser.parse_args()


# --------------------------------------------------
def pick_artist(artist_list) -> dict:
    for artist in artist_list:
        if artist["score"] == 100:
            return artist


# --------------------------------------------------
def get_artist(artist: str) -> dict:
    artist_url = "http://musicbrainz.org/ws/2/artist/"
    query = f"{artist_url}?query={artist}&limit=3&fmt=json"
    response = requests.get(query)
    my_artist = pick_artist(response.json()["artists"])
    pprint(my_artist)
    return my_artist


# --------------------------------------------------
def main(artist: list[str]) -> dict:
    artist_query = "%20".join(artist)
    artist_reponse = get_artist(artist_query)
    if not artist_reponse:
        print("No Artist found")
    return artist_reponse


# --------------------------------------------------
if __name__ == "__main__":
    arguments = get_args()
    artist = arguments.artist
    main(artist)
