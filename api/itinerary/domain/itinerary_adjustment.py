from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ItineraryAdjustmentType( str, Enum ):
   ARRIVAL_TIME_ADJUSTED = 'arrivalTimeAdjusted'
   DEPARTURE_TIME_ADJUSTED = 'departureTimeAdjusted'


@dataclass( frozen=True )
class ItineraryAdjustment:
   type: ItineraryAdjustmentType
   field: str
   previous_value: str | None
   value: str | None
   reason: str


   def to_dict( self ) -> dict[ str, str | None ]:
      return {
         'type': self.type.value,
         'field': self.field,
         'previous_value': self.previous_value,
         'value': self.value,
         'reason': self.reason,
      }
