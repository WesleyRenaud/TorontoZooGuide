from __future__ import annotations

from dataclasses import dataclass

from api.models import Restaurant
from .website_page import WebsitePage


@dataclass( frozen=True )
class RestaurantsByTitle:
   restaurants: list[ Restaurant ]


   def restaurant_for( self, title: str ) -> Restaurant | None:
      normalized = WebsitePage.normalize_name( title )

      return min(
         (
            restaurant
            for restaurant in self.restaurants
            if WebsitePage.normalize_name( restaurant.name ) == normalized
         ),
         key=lambda restaurant: restaurant.name.casefold(),
         default=None,
      )
