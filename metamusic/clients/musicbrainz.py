"""
Author : Salvador <salvador.estrella.ortiz@gmail.com>
Date   : 2022-09-30
Purpose: Query Metadata from MusicBrainz API
"""

import requests


# --------------------------------------------------
class MusicBrainz:
    base_url = "http://musicbrainz.org/ws/2/"

    @classmethod
    def _query_artist(cls, artist: str) -> dict:
        artist = artist.split()
        artist = "%20".join(artist)
        artist_query = f"{cls.base_url}artist/?query={artist}&fmt=json"
        response = requests.get(artist_query)
        artist_list = response.json()["artists"]
        return artist_list

    @classmethod
    def _pick_artist(cls, artists_list: list[dict]) -> dict:
        artist = None
        for posible_artist in artists_list:
            if not artist:
                artist = posible_artist
            elif artist["score"] < posible_artist["score"]:
                artist = posible_artist
        if artist and artist["score"] != 100:
            raise ValueError("Artist not found, check your query")
        return artist

    @classmethod
    def _artist_lookup(cls, artist_id: str) -> dict:
        artist_lookup = f"{cls.base_url}artist/{artist_id}?inc=release-groups&fmt=json"
        artist_response = requests.get(artist_lookup)
        artist_info = artist_response.json()
        return artist_info

    @classmethod
    def _pick_release_group(cls, artist: str, release_name: str) -> dict:
        artist_releases = cls.get_artist_info(artist)["release-groups"]
        my_release = {}
        for release in artist_releases:
            if release["title"].lower() == release_name.lower():
                my_release = release
        if not my_release:
            raise ValueError("No release found, check release name.")
        return my_release

    @classmethod
    def _pick_release(cls, release_group_id: str) -> dict:
        lookup = f"{cls.base_url}release-group/{release_group_id}?inc=releases&fmt=json"
        response = requests.get(lookup)
        release_groups = response.json()
        release = release_groups["releases"][0]
        return release

    @classmethod
    def _release_lookup(cls, release_id: str) -> dict:
        lookup = f"{cls.base_url}release/{release_id}?inc=artists+recordings+recording-rels+recording-level-rels+artist-rels&fmt=json"
        response = requests.get(lookup)
        release = response.json()
        return release

    @classmethod
    def _pick_title(cls, titles_list: list, title: str) -> dict:
        title_info = {}
        for item in titles_list:
            if item["title"].lower() == title.lower():
                title_info = item
        if not title_info:
            raise ValueError("No title found, check title name.")
        return title_info

    @classmethod
    def _pick_title_relations(cls, relations_list: list) -> dict:
        relations = {
                "recording engineer": [],
                "engineer": [],
                "producer": [],
                "vocals": [],
                "instruments": []
                }
        for relation in relations_list:
            if relation["type"] == "recording":
                relations["recording engineer"].append(relation)
            elif relation["type"] == "engineer":
                relations["engineer"].append(relation)
            elif relation["type"] == "producer":
                relations["producer"].append(relation)
            elif relation["type"] == "vocal":
                relations["vocals"].append(relation)
            elif relation["type"] == "instrument":
                relations["instruments"].append(relation)
        return relations

    @classmethod
    def get_artist_info(cls, artist: str) -> dict:
        artists_list = cls._query_artist(artist)
        artist_id = cls._pick_artist(artists_list)["id"]
        my_artist = cls._artist_lookup(artist_id)
        return my_artist

    @classmethod
    def get_release(cls, artist: str, release: str) -> dict:
        release_group = cls._pick_release_group(artist=artist, release_name=release)
        release_info = cls._pick_release(release_group_id=release_group["id"])
        release = cls._release_lookup(release_id=release_info["id"])
        return release

    @classmethod
    def get_title(cls, artist: str, release: str, title: str) -> dict:
        release = cls.get_release(artist=artist, release=release)
        release_titles = release["media"][0]["tracks"]
        title = cls._pick_title(titles_list=release_titles, title=title)
        return title

    @classmethod
    def get_title_relations(cls, artist: str, release: str, title: str) -> dict:
        title = cls.get_title(artist=artist, release=release, title=title)
        relations_list = title["recording"]["relations"]
        relations = cls._pick_title_relations(relations_list)
        return relations


# --------------------------------------------------
# def main() -> dict:
#     """Main function for program"""
#
#     client = MusicBrainz()
#     artist = client.get_artist_info("kings of convenience")
#     release = client.get_release(artist="kings of convenience", release="kings of convenience")
#     title = client.get_title(artist="kings of convenience", release="kings of convenience", title="failure")
#     title_relations = client.get_title_relations(artist="kings of convenience", release="kings of convenience", title="failure")
#     breakpoint()
#
#
# if __name__ == "__main__":
#     main()
