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
def get_release_object_substring(release_object: dict) -> str:
    """Use regular expression to retrieve substring."""

    pattern = re.compile("Music.+(\.jpg)(?=/)|Music.+(\.png)(?=/)")
    string = release_object["artworkUrl100"]
    match = pattern.search(string)
    if match:
        if match.group(0):
            return match.group(0)
        elif match.group(1):
            return match.group(1)
    else:
        raise ValueError("No match found for artwork url")


# --------------------------------------------------
def main():
    """Main function for program"""

    args = get_args()
    release_object = get_release_object(release=args.release, artist=args.artist)
    substring = get_release_object_substring(release_object=release_object)
    print(substring)
    return substring


# --------------------------------------------------
if __name__ == "__main__":
    main()

