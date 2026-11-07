from __future__ import annotations

from ..data_access.restaurant_closure_record import RestaurantClosureRecord
from .restaurant_menu_link import RestaurantMenuLink
from .seasonal_restaurant import SeasonalRestaurant
from ...shared.date_values import DateValues


class SeasonalRestaurantBuilder():
   @classmethod
   def build(
         cls,
         restaurants: list[ RestaurantMenuLink ],
         closure_records: list[ RestaurantClosureRecord ] ) -> list[ SeasonalRestaurant ]:
      closures = cls._closures( closure_records )
      return cls._listed( restaurants, closures ) + cls._unlisted( restaurants, closures )


   @classmethod
   def _closures(
         cls,
         closure_records: list[ RestaurantClosureRecord ] ) -> dict[ str, RestaurantClosureRecord ]:
      return {
         record.restaurant: record
         for record in closure_records
         if record.closed_start != None
      }


   @classmethod
   def _listed(
         cls,
         restaurants: list[ RestaurantMenuLink ],
         closures: dict[ str, RestaurantClosureRecord ] ) -> list[ SeasonalRestaurant ]:
      return [
         cls._closure( restaurant.name, closures[ restaurant.name ], restaurant.menu_link )
         if restaurant.name in closures
         else cls._open( restaurant )
         for restaurant in restaurants
      ]


   @classmethod
   def _unlisted(
         cls,
         restaurants: list[ RestaurantMenuLink ],
         closures: dict[ str, RestaurantClosureRecord ] ) -> list[ SeasonalRestaurant ]:
      listed = { restaurant.name for restaurant in restaurants }
      return [
         cls._closure( name, record )
         for name, record in closures.items()
         if name not in listed
      ]


   @classmethod
   def _open( cls, restaurant: RestaurantMenuLink ) -> SeasonalRestaurant:
      return SeasonalRestaurant(
         name=restaurant.name,
         menu_link=restaurant.menu_link,
         is_closed=False,
         start=None,
         end=None,
         closed_for_season=False,
      )


   @classmethod
   def _closure(
         cls,
         name: str,
         record: RestaurantClosureRecord,
         menu_link: str = '' ) -> SeasonalRestaurant:
      return SeasonalRestaurant(
         name=name,
         menu_link=menu_link,
         is_closed=True,
         start=DateValues.parse_date_value( record.closed_start ),
         end=DateValues.parse_date_value( record.closed_end ),
         closed_for_season=record.is_closed_for_season,
      )
