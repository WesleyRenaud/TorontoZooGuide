from __future__ import annotations

from dataclasses import dataclass

from .itinerary_adjustment_reason import ItineraryAdjustmentReason
from .itinerary_adjustment_type import ItineraryAdjustmentType


@dataclass( frozen=True )
class ItineraryAdjustment:
   type: ItineraryAdjustmentType
   field: str
   previous_value: str | None
   value: str | None
   reason: ItineraryAdjustmentReason


   def to_dict( self ) -> dict[ str, str | None ]:
      return {
         'type': self.type.value,
         'field': self.field,
         'previous_value': self.previous_value,
         'value': self.value,
         'reason': self.reason.value,
      }
