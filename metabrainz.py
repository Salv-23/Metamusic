#!/usr/bin/env python3
"""
Author : Salvador <salvador.estrella.ortiz@gmail.com>
Date   : 2022-09-30
Purpose: Query Metadata from MusicBrainz API
"""

import argparse
import requests
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Retrieve metadata from MusicBrainz API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-a",
        "--artist",
        help="An artist to search for",
        metavar="str",
        type=str,
        nargs="+",
        required=True,
    )

    return parser.parse_args()


# --------------------------------------------------
class MusicMetadata:
    artist_endpoit = "http://musicbrainz.org/ws/2/artist/"
    release_groups_endpoint = "http://musicbrainz.org/ws/2/release-group/"
    releases_endpoint = "http://musicbrainz.org/ws/2/release/"

    def __init__(self, artist: list[str]):
        self.artist = artist

    def pick_artist(self, artist_list):
        for artist in artist_list:
            if artist["score"] == 100:
                return artist

    def query_artist(self) -> dict:
        endpoint = MusicMetadata.artist_endpoit
        artist_query = "%20".join(self.artist)
        query = f"{endpoint}?query={artist_query}&limit=3&fmt=json"
        response = requests.get(query)
        artist_list = response.json()["artists"]
        my_artist = self.pick_artist(artist_list)
        pprint(my_artist)
        return my_artist


# --------------------------------------------------
def main(artist: list[str]) -> dict:
    """Main function for program"""

    my_artist = MusicMetadata(artist)
    my_artist.query_artist()


# --------------------------------------------------
if __name__ == "__main__":
    arguments = get_args()
    artist_argument = arguments.artist
    main(artist_argument)
