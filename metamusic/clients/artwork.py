#!/usr/bin/env python3
"""
Author : root <root@localhost>
Date   : 2022-11-16
Purpose: Program to retrieve HD artwork from iTunes
"""

import argparse
import requests
import re


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="New Program",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-r",
        "--release",
        help="Name of the release",
        metavar="str",
        type=str,
    )

    parser.add_argument(
        "-a",
        "--artist",
        help="Name of the artist",
        metavar="str",
        type=str,
    )

    return parser.parse_args()


# --------------------------------------------------
def get_release_object(release: str, artist: str) -> dict:
    """Search and return a release object"""

    release_object = {}
    url = "https://artwork.themoshcrypt.net/api/search?keyword="
    release = "%2B".join(release.split()).lower()
    response = requests.get(url + release).json()
    for result in response["results"]:
        if result["artistName"].lower() == artist.lower():
            release_object = result
    if not release_object:
        raise ValueError(
            "No release found. check release and artist name and try again."
        )
    return release_object


# --------------------------------------------------
def get_high_definition_artwork_url(release_object: dict) -> str:
    """Find the url for a high-definition artwork"""

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
        raise ValueError("No match found for artwork url")


# --------------------------------------------------
def main():
    """Main function for program"""

    args = get_args()
    release_object = get_release_object(release=args.release, artist=args.artist)
    artwork_url = get_high_definition_artwork_url(release_object=release_object)
    breakpoint()
    return artwork_url


# --------------------------------------------------
if __name__ == "__main__":
    main()
