from __future__ import annotations

from ..domain.restaurant_menu_link import RestaurantMenuLink
from ...types import Types


class RestaurantMenuLinkMapper():
   @classmethod
   def map_record( cls, row: Types.Row ) -> RestaurantMenuLink:
      return RestaurantMenuLink(
         name=row[ 'NAME' ],
         menu_link=( row[ 'MENU_LINK' ] or '' ).strip() )


   @classmethod
   def map_records( cls, rows: list[ Types.Row ] ) -> list[ RestaurantMenuLink ]:
      return [
         cls.map_record( row )
         for row in rows
      ]
