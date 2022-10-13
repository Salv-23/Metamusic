from dataclasses import dataclass
import typing as T


@dataclass
class Track:
    artist: str
    title: str
    album: str
    album_type: T.Optional[str] = None
    track_number: T.Optional[int] = None
    release_date: T.Optional[str] = None
