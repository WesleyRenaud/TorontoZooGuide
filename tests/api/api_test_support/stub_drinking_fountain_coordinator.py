from __future__ import annotations

from typing import Any

from api_test_support.coordinator_call import CoordinatorCall

from api.models.drinking_fountain import DrinkingFountain


class StubDrinkingFountainCoordinator():
   instances: list[ StubDrinkingFountainCoordinator ] = []
   default_success: bool = True
   drinking_fountains: list[ DrinkingFountain ]
   calls: list[ CoordinatorCall ]
   closed: bool


   def __init__(
         self,
         *,
         drinking_fountains: list[ DrinkingFountain ] ) -> None:
      self.drinking_fountains = drinking_fountains
      self.calls = []
      self.closed = False
      StubDrinkingFountainCoordinator.instances.append( self )


   def close( self ) -> None:
      self.closed = True


   def get_drinking_fountains(
         self,
         *,
         day: int,
         month: str,
         year: int ) -> list[ DrinkingFountain ]:
      self.calls.append(
         CoordinatorCall(
            'get_drinking_fountains',
            {
               'day': day,
               'month': month,
               'year': year,
            },
         )
      )
      return list( self.drinking_fountains )


   def set_drinking_fountains_as_closed( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'set_drinking_fountains_as_closed', kwargs ) )
      return StubDrinkingFountainCoordinator.default_success


   def set_drinking_fountains_as_open( self, **kwargs: Any ) -> bool:
      self.calls.append( CoordinatorCall( 'set_drinking_fountains_as_open', kwargs ) )
      return StubDrinkingFountainCoordinator.default_success
