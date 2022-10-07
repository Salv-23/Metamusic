#!/usr/bin/env python3
"""
Author : Salvador <salvador.estrella.ortiz@gmail.com>
Date   : 2022-09-30
Purpose: Query Metadata from MusicBrainz API
"""

import requests
from time import sleep


# --------------------------------------------------
class MusicMetadata:
    artist_endpoit = "http://musicbrainz.org/ws/2/artist/"
    release_groups_endpoint = "http://musicbrainz.org/ws/2/release-group/"
    releases_endpoint = "http://musicbrainz.org/ws/2/release/"

    @classmethod
    def _pick_artist(cls, artist_list: list[dict]):
        # TODO: Deal with artists that don't return a score equal to 100.
        artist = None
        for posible_artist in artist_list:
            if not artist:
                artist = posible_artist
            elif artist["score"] < posible_artist["score"]:
                artist = posible_artist
        if artist and artist["score"] != 100:
            raise NotImplementedError(
                "Selection of artists with lower score than 100 not implemented yet"
            )
        return artist

    @classmethod
    def _artist_lookup(cls, artist_id: str) -> dict:
        artist_lookup = f"{cls.artist_endpoit}{artist_id}?inc=release-groups&fmt=json"
        artist_response = requests.get(artist_lookup)
        artist_info = artist_response.json()
        return artist_info

    @classmethod
    def _query_artist(cls, artist: str) -> dict:
        artist = artist.split()
        artist = "%20".join(artist)
        artist_query = f"{cls.artist_endpoit}?query={artist}&fmt=json"
        response = requests.get(artist_query)
        artist_list = response.json()["artists"]
        return artist_list

    @classmethod
    def _pick_release(cls, release_group: str) -> dict:
        release_id = release_group["id"]
        release_lookup = (
            f"{cls.releases_endpoint}{release_id}?inc=artists+recordings&fmt=json"
        )
        release_response = requests.get(release_lookup)
        release = release_response.json()
        return release

    @classmethod
    def _release_lookup(cls, release_group_id: str) -> dict:
        release_lookup = (
            f"{cls.release_groups_endpoint}{release_group_id}?inc=releases&fmt=json"
        )
        release_response = requests.get(release_lookup)
        release_info = release_response.json()["releases"][0]
        return release_info

    @classmethod
    def get_artist_info(cls, artist: str) -> dict:
        artist_list = cls._query_artist(artist)
        artist_pick = cls._pick_artist(artist_list)
        my_artist = cls._artist_lookup(artist_pick["id"])
        __import__('pprint').pprint(my_artist)
        return my_artist

    @classmethod
    def get_albums(cls, artist: str) -> list:
        release_groups = cls.get_artist_info(artist)["release-groups"]
        albums = []
        for release in release_groups:
            if release["primary-type"] == "Album":
                release_lookup = cls._release_lookup(release["id"])
                release_pick = cls._pick_release(release_lookup)
                albums.append(release_pick)
                sleep(1)
        return albums

    @classmethod
    def get_singles(cls, artist: str) -> list:
        release_groups = cls.get_artist_info(artist)["release-groups"]
        singles = []
        for release in release_groups:
            if release["primary-type"] == "Single":
                release_lookup = cls._release_lookup(release["id"])
                release_pick = cls._pick_release(release_lookup)
                singles.append(release_pick)
                sleep(1)
        return singles

    @classmethod
    def get_episodes(cls, artist: str) -> list:
        release_groups = cls.get_artist_info(artist)["release-groups"]
        episodes = []
        for release in release_groups:
            if release["primary-type"] == "EP":
                release_lookup = cls._release_lookup(release["id"])
                release_pick = cls._pick_release(release_lookup)
                episodes.append(release_pick)
                sleep(1)
        return episodes


# --------------------------------------------------
def main(artist) -> dict:
    """Main function for program"""

    client = MusicMetadata()
    client.get_artist_info(artist)


# --------------------------------------------------
if __name__ == "__main__":
    main("Coldplay")
