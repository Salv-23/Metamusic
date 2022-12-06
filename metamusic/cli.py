"""
Author : Salvador <Salvador@fedora>
Date   : 2022-10-05
Purpose: Command-line interface for metamusic
"""

import typer
from pprint import pprint as pp
from clients import (
    MusicBrainz,
    high_definition_artwork,
    get_track_tags,
    set_selected_tags,
    set_all_tags,
    set_artwork_locally,
    set_artwork_from_url,
)

app = typer.Typer()


@app.command()
def set_metadata(track_file: str, artist: str, release: str, title: str):
    pass


@app.command()
def set_artwork(track_file: str, artwork_file: str):
    files = find_all_valid_files(directory)
    for file in files:
        handler = FileHandler(file)
        handler.get_artwork = include_artwork
        handler.get_metadata()
        handler.save_metadata()


if __name__ == "__main__":
    app()
