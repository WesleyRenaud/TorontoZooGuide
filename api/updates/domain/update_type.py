from __future__ import annotations

from enum import Enum

_ORDER_BY_TYPE: dict[ 'UpdateType', int ] = {}
_ALIASES_BY_TYPE: dict[ 'UpdateType', frozenset[ str ] ] = {}


class UpdateType( str, Enum ):
   CLOSURE = 'Closure'
   ANIMAL_BIRTH = 'Animal Birth'
   ANIMAL_PASSING = 'Animal Passing'
   NEW_ARRIVAL = 'New Arrival'
   DEPARTURE = 'Departure'


   @property
   def order( self ) -> int:
      return _ORDER_BY_TYPE[ self ]


   @classmethod
   def normalize( cls, value: str | None ) -> 'UpdateType | None':
      if value is None:
         return None

      normalized_key = value.strip().lower()

      for update_type in cls:
         if normalized_key == update_type.value.lower():
            return update_type

         if normalized_key in _ALIASES_BY_TYPE.get( update_type, frozenset() ):
            return update_type

      return None


_ORDER_BY_TYPE.update( {
   UpdateType.CLOSURE: 0,
   UpdateType.ANIMAL_BIRTH: 1,
   UpdateType.ANIMAL_PASSING: 2,
   UpdateType.NEW_ARRIVAL: 3,
   UpdateType.DEPARTURE: 4,
} )

_ALIASES_BY_TYPE.update( {
   UpdateType.ANIMAL_BIRTH: frozenset( { 'animal_birth' } ),
   UpdateType.ANIMAL_PASSING: frozenset( { 'animal_passing' } ),
   UpdateType.NEW_ARRIVAL: frozenset( { 'new_arrival' } ),
} )
