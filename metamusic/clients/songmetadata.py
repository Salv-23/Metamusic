#!/usr/bin/env python3
"""
Author : Salvador <Salvador@fedora>
Date   : 2022-10-15
Purpose: New program
"""
from metamusic.models import Track
import argparse
import eyed3
import requests

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="eyeD3 client to get or update metadata",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-t",
        "--track",
        help="A track file to get or update metadata",
        metavar="str",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-i",
        "--image",
        help="An image file to update album artwork",
        metavar="str",
        type=str,
        required=True,
    )

    return parser.parse_args()


# --------------------------------------------------
def get_track_tags(path: str):
    track = eyed3.load(path)
    track_info = Track(
        artist=track.tag.artist,
        album=track.tag.album,
        title=track.tag.title,
        track_number=track.tag.track_num[0],
        total_tracks=track.tag.track_num[1],
        album_type=track.tag.album_type,
        release_date=track.tag.release_date.year,
    )
    return track_info


# --------------------------------------------------
def set_selected_tags(path: str, metadata: dict, tag_selection: list[str]):
    track = eyed3.load(path)
    if "artist" in tag_selection:
        track.tag.artist = metadata["artist"]
    if "album" in tag_selection:
        track.tag.album = metadata["album"]
    if "title" in tag_selection:
        track.tag.title = metadata["title"]
    if "track_num" in tag_selection:
        track.tag.track_num = (metadata["track_num"], metadata["total_tracks"])
    if "album_type" in tag_selection:
        track.tag.album_type = metadata["album_type"]
    if "release_date" in tag_selection:
        track.tag.original_release_date = metadata["release_date"]
    track.tag.save()


# --------------------------------------------------
def set_all_tags(path: str, metadata: dict):
    track = eyed3.load(path)
    track.tag.artist = metadata["artist"]
    track.tag.album = metadata["album"]
    track.tag.title = metadata["title"]
    track.tag.track_num = (metadata["track_num"], metadata["total_tracks"])
    track.tag.album_type = metadata["album_type"]
    track.tag.original_release_date = metadata["release_date"]
    track.tag.save()


# --------------------------------------------------
def set_artwork_locally(track_path: str, image_path: str):
    track = eyed3.load(track_path)
    with open(image_path, mode="rb") as image_file:
        image_data = image_file.read()
    track.tag.images.set(
        type_=3,
        img_data=image_data,
        mime_type="image/jpeg",
        description="cover",
    )
    track.tag.save(version=eyed3.id3.ID3_V2_3)


# --------------------------------------------------
def set_artwork_from_url(track_path: str, image_url: str):
    track = eyed3.load(track_path)
    web_image = requests.get(image_url)
    track.tag.images.set(
        type_=3,
        img_data=web_image.content(),
        mime_type="image/jpeg",
        description="cover",
    )
    track.tag.save(version=eyed3.id3.ID3_V2_3)


# --------------------------------------------------
def main():
    """Main function for program"""
    arguments = get_args()
    metadata = {
        "artist": "Los Tucanes de Tijuana",
        "title": "La Chona",
        "album": "Me Robastes El Corazón",
        "track_num": 6,
        "total_tracks": 12,
        "album_type": "lp",
        "release_date": 2022,
    }
    tag_selection = ["artist", "album", "title"]
    # Testing functions
    set_all_tags(path=arguments.track, metadata=metadata)
    set_selected_tags(
        path=arguments.track, metadata=metadata, tag_selection=tag_selection
    )


# --------------------------------------------------
if __name__ == "__main__":
    main()
