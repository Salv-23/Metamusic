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
        required=True,
    )

    return parser.parse_args()


# --------------------------------------------------
class MusicMetadata:
    artist_endpoit = "http://musicbrainz.org/ws/2/artist/"
    release_groups_endpoint = "http://musicbrainz.org/ws/2/release-group/"
    releases_endpoint = "http://musicbrainz.org/ws/2/release/"

    def __init__(self, artist: str):
        self.artist = artist

    def pick_artist(self, artist_list):
        for artist in artist_list:
            if artist["score"] == 100:
                return artist

    def query_artist(self) -> dict:
        endpoint = MusicMetadata.artist_endpoit
        artist = self.artist.split()
        artist = "%20".join(artist)
        artist_query = f"{endpoint}?query={artist}&limit=3&fmt=json"
        response = requests.get(artist_query)
        artist_list = response.json()["artists"]
        my_artist = self.pick_artist(artist_list)
        return my_artist

    def get_release_groups(self) -> dict:
        artist = self.query_artist()
        artist_id = artist['id']
        endpoint = MusicMetadata.artist_endpoit
        artist_lookup = f"{endpoint}{artist_id}?inc=release-groups&fmt=json"
        response = requests.get(artist_lookup)
        release_groups = response.json()["release-groups"]
        return release_groups


# --------------------------------------------------
def main(artist) -> dict:
    """Main function for program"""

    my_artist = MusicMetadata(artist)
    my_artist.get_release_groups()


# --------------------------------------------------
if __name__ == "__main__":
    arguments = get_args()
    artist_argument = arguments.artist
    main(artist_argument)
