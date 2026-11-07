from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class WebsiteOffDisplayAnimal:
   section: str
   name: str
