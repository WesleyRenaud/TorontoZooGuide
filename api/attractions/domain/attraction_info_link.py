from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class AttractionInfoLink:
   name: str
   info_link: str
