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
    def _artist_lookup(cls, artist_id: str) -> dict:
        artist_lookup = f"{cls.artist_endpoit}{artist_id}?inc=release-groups&fmt=json"
        artist_response = requests.get(artist_lookup)
        artist_info = artist_response.json()
        return artist_info

    @classmethod
    def get_artist_info(cls, artist: str) -> dict:
        endpoint = cls.artist_endpoit
        artist = artist.split()
        artist = "%20".join(artist)
        artist_query = f"{endpoint}?query={artist}&fmt=json"
        response = requests.get(artist_query)
        artist_list = response.json()["artists"]
        artist_pick = cls._pick_artist(artist_list)
        my_artist = cls._artist_lookup(artist_pick["id"])
        __import__('pprint').pprint(my_artist)
        # logging.info(my_artist)
        return my_artist

    @classmethod
    def get_albums(cls, artist: str) -> list:
        release_groups = cls.get_release_groups(artist)
        albums = []
        for release_group in release_groups:
            release_group_id = release_group["id"]
            endpoint = cls.release_groups_endpoint
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
            endpoint = cls.release_groups_endpoint
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
            endpoint = cls.release_groups_endpoint
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
    main("Kings of convenience")
