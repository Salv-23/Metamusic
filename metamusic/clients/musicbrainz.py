#!/usr/bin/env python3
"""
Author : Salvador <salvador.estrella.ortiz@gmail.com>
Date   : 2022-09-30
Purpose: Query Metadata from MusicBrainz API
"""

import requests
import logging
from time import sleep


# --------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(message)s")


# --------------------------------------------------
class MusicMetadata:
    artist_endpoit = "http://musicbrainz.org/ws/2/artist/"
    release_groups_endpoint = "http://musicbrainz.org/ws/2/release-group/"
    releases_endpoint = "http://musicbrainz.org/ws/2/release/"

    @classmethod
    def _pick_artist(cls, artist_list: list[dict]):
        for artist in artist_list:
            if artist["score"] == 100:
                return artist

    @classmethod
    def get_artist_info(cls, artist: str) -> dict:
        endpoint = cls.artist_endpoit
        artist = artist.split()
        artist = "%20".join(artist)
        artist_query = f"{endpoint}?query={artist}&fmt=json"
        response = requests.get(artist_query)
        artist_list = response.json()["artists"]
        my_artist = cls._pick_artist(artist_list)
        logging.info(my_artist)
        return my_artist

    @classmethod
    def get_release_groups(cls, artist: str) -> list:
        artist = cls.get_artist_info(artist)
        artist_id = artist["id"]
        endpoint = cls.artist_endpoit
        artist_lookup = f"{endpoint}{artist_id}?inc=release-groups&fmt=json"
        response = requests.get(artist_lookup)
        release_groups = response.json()["release-groups"]
        logging.info(release_groups)
        return release_groups

    @classmethod
    def get_albums(cls, artist: str) -> list:
        release_groups = cls.get_release_groups(artist)
        albums = []
        for release_group in release_groups:
            release_group_id = release_group["id"]
            endpoint = MusicMetadata.release_groups_endpoint
            lookup = f"{endpoint}{release_group_id}?inc=artists&fmt=json"
            response = requests.get(lookup)
            release = response.json()
            if release["primary-type"] == "Album":
                albums.append(release)
            sleep(1)
        logging.info(albums)
        return albums

    @classmethod
    def get_singles(cls, artist: str) -> list:
        release_groups = cls.get_release_groups(artist)
        singles = []
        for release_group in release_groups:
            release_group_id = release_group["id"]
            endpoint = MusicMetadata.release_groups_endpoint
            lookup = f"{endpoint}{release_group_id}?inc=artists&fmt=json"
            response = requests.get(lookup)
            release = response.json()
            if release["primary-type"] == "Single":
                singles.append(release)
            sleep(1)
        logging.info(singles)
        return singles

    @classmethod
    def get_episodes(cls, artist: str) -> list:
        release_groups = cls.get_release_groups(artist)
        episodes = []
        for release_group in release_groups:
            release_group_id = release_group["id"]
            endpoint = MusicMetadata.release_groups_endpoint
            lookup = f"{endpoint}{release_group_id}?inc=artists&fmt=json"
            response = requests.get(lookup)
            release = response.json()
            if release["primary-type"] == "EP":
                episodes.append(release)
            sleep(1)
        logging.info(episodes)
        return episodes


# --------------------------------------------------
def main(artist) -> dict:
    """Main function for program"""

    client = MusicMetadata()
    client.get_artist_info(artist)


# --------------------------------------------------
if __name__ == "__main__":
    arguments = get_args()
    main(arguments.artist)
