import typing as T
from dataclasses import dataclass


@dataclass
class Track:
    artist: str
    title: str
    release: str
    release_type: T.Optional[str] = None
    track_number: T.Optional[int] = None
    total_tracks: T.Optional[int] = None
    recording_date: T.Optional[str] = None
