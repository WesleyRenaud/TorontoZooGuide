from __future__ import annotations

from typing import NamedTuple


class ViewingSpotNameKey( NamedTuple ):
   species: str
   exhibit: str
   enclosure_name: str | None
