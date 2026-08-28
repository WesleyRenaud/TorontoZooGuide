from __future__ import annotations

from typing import Any

from api.models.restaurant import Restaurant


class StubRestaurantCoordinator():
   instances: list[ StubRestaurantCoordinator ] = []
   default_success: bool = True


   def __init__(
         self,
         *,
         restaurant_names: list[ str ],
         restaurants: list[ Restaurant ] ) -> None:
      self.restaurant_names = restaurant_names
      self.restaurants = restaurants
      self.calls: list[ tuple[ str, dict[ str, Any ] ] ] = []
      self.closed = False
      StubRestaurantCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_restaurant_names( self ) -> list[ str ]:
      self.calls.append( ( 'get_restaurant_names', {} ) )
      return list( self.restaurant_names )


   def get_restaurants(
         self,
         *,
         day: int,
         month: str,
         year: int,
         include_closed_restaurants: bool | None = None,
         restaurants_to_include: list[ str ] | None = None ) -> list[ Restaurant ]:
      self.calls.append(
         (
            'get_restaurants',
            {
               'day': day,
               'month': month,
               'year': year,
               'include_closed_restaurants': include_closed_restaurants,
               'restaurants_to_include': restaurants_to_include,
            }
         )
      )
      return list( self.restaurants )


   def set_restaurant_as_closed( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_restaurant_as_closed', kwargs ) )
      return StubRestaurantCoordinator.default_success


   def set_restaurant_closure_override( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_restaurant_closure_override', kwargs ) )
      return StubRestaurantCoordinator.default_success


   def set_restaurant_opening_schedule( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'set_restaurant_opening_schedule', kwargs ) )
      return StubRestaurantCoordinator.default_success


   def replace_restaurant_opening_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'replace_restaurant_opening_schedule_overlaps', kwargs ) )
      return StubRestaurantCoordinator.default_success


   def trim_restaurant_opening_schedule_overlaps( self, **kwargs: Any ) -> bool:
      self.calls.append( ( 'trim_restaurant_opening_schedule_overlaps', kwargs ) )
      return StubRestaurantCoordinator.default_success
