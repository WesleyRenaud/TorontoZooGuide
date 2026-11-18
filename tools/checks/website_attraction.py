from __future__ import annotations

from dataclasses import dataclass

from .attraction_hours import AttractionHours


@dataclass( frozen=True )
class WebsiteAttraction:
   href: str
   title: str
   status: str | None
   image: str = ''
   hours: AttractionHours | None = None
