#!/usr/bin/env python3
"""
Author : Salvador <Salvador@fedora>
Date   : 2022-10-07
Purpose: New program
"""

from .clients import musicbrainz
from .cli import 


# --------------------------------------------------
if __name__ == '__main__':
    musicbrains.main("kings of convenience")
