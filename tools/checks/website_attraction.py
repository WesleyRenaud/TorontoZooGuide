from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class WebsiteAttraction:
   href: str
   title: str
   status: str | None
