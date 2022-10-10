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
    base_url = "http://musicbrainz.org/ws/2/"

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
        artist_lookup = f"{cls.base_url}artist/{artist_id}?inc=release-groups&fmt=json"
        artist_response = requests.get(artist_lookup)
        artist_info = artist_response.json()
        return artist_info

    @classmethod
    def _query_artist(cls, artist: str) -> dict:
        artist = artist.split()
        artist = "%20".join(artist)
        artist_query = f"{cls.base_url}artist/?query={artist}&fmt=json"
        response = requests.get(artist_query)
        artist_list = response.json()["artists"]
        return artist_list

    @classmethod
    def _pick_release(cls, release_group: str) -> dict:
        release_id = release_group["id"]
        release_lookup = (
            f"{cls.base_url}release/{release_id}?inc=artists+recordings&fmt=json"
        )
        release_response = requests.get(release_lookup)
        release = release_response.json()
        return release

    @classmethod
    def _release_lookup(cls, release_group_id: str) -> dict:
        release_lookup = (
            f"{cls.base_url}release-group/{release_group_id}?inc=releases&fmt=json"
        )
        release_response = requests.get(release_lookup)
        release_info = release_response.json()["releases"][0]
        return release_info

    @classmethod
    def get_artist_info(cls, artist: str) -> dict:
        artist_list = cls._query_artist(artist)
        artist_pick = cls._pick_artist(artist_list)
        my_artist = cls._artist_lookup(artist_pick["id"])
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
        __import__('pprint').pprint(albums)
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

    @classmethod
    def pick_recording(cls, recordings_list: list, artist: str, release: str, title: str) -> dict:
        my_recording = {}
        while not my_recording:
            for recording in recordings_list:
                recording_title = recording["title"].lower()
                recording_artist = recording["artist-credit"][0]["name"].lower()
                release_title = recording["releases"][0]["release-group"]["title"].lower()
                if recording_artist == artist:
                    if release_title == release:
                        if recording_title == title:
                            my_recording = recording
        return my_recording

    @classmethod
    def query_song(cls, song: str) -> dict:
        song = song.split()
        song = "%20".join(song)
        song_search = f"{cls.base_url}recording/?query={song}&fmt=json"
        response = requests.get(song_search)
        response_list = response.json()["recordings"]
        return response_list

    @classmethod
    def lookup_recording(cls, recording: dict) -> dict:
        recording_id = recording["id"]
        recording_lookup = f"{cls.base_url}recording/{recording_id}?inc=artists+releases+isrcs+url-rels&fmt=json"
        lookup_response = requests.get(recording_lookup)
        recording = lookup_response.json()
        return recording

    @classmethod
    def get_recording(cls, artist: str, release: str, title: str):
        recordings_list = cls.query_song(title)
        pick_recording = cls.pick_recording(recordings_list, artist, release, title)
        recording = cls.lookup_recording(pick_recording)
        breakpoint()
        return recording


# --------------------------------------------------
def main() -> dict:
    """Main function for program"""

    client = MusicMetadata()
    client.get_recording(artist="kings of convenience", release="declaration of dependence", title="rule my world")


# --------------------------------------------------
if __name__ == "__main__":
    main()
