#!/usr/bin/env python3
"""
Author : Salvador <Salvador@fedora>
Date   : 2022-09-24
Purpose: Query release-groups information from musicbrainz API
"""

import argparse
import requests
from pprint import pprint


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Query release-groups from MusicBrainz",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-a",
        "--artist_id",
        help="Artist id",
        metavar="str",
        type=str,
        required=True,
    )

    # parser.add_argument(
    #     "-r",
    #     "--release_id",
    #     help="Release-group id",
    #     metavar="str",
    #     type=str,
    #     required=True,
    # )
    #
    return parser.parse_args()


# --------------------------------------------------
def get_release_groups(artist_id: str) -> dict:
    url = "http://musicbrainz.org/ws/2/artist"
    release_query = f"{url}/{artist_id}?inc=release-groups&fmt=json"
    response = requests.get(release_query)
    release_groups = response.json()["release-groups"]
    pprint(release_groups)
    return release_groups


# --------------------------------------------------
def pick_release_group(release_id: str):
    release_group_api = "http://musicbrainz.org/ws/2/release-group/"
    query = f"{release_group_api}{release_id}?inc=releases&fmt=json"
    response = requests.get(query)
    release_group = response.json()['releases'][0]
    pprint(release_group)
    return release_group


# --------------------------------------------------
def main(id: str) -> list[dict]:
    """Main function for program"""
    get_release_groups(id)
    # pick_release_group(id)


# --------------------------------------------------
if __name__ == "__main__":
    arguments = get_args()
    id = arguments.id
    main(id)
