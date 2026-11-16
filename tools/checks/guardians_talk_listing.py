from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class GuardiansTalkListing:
   name: str
   location: str
   enclosure_name: str | None = None
