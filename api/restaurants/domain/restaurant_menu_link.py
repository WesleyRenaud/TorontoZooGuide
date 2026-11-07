from __future__ import annotations

from dataclasses import dataclass


@dataclass( frozen=True )
class RestaurantMenuLink:
   name: str
   menu_link: str
