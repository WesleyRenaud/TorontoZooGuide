from __future__ import annotations

from dataclasses import dataclass, field

from .itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.enums import ItineraryErrorType


@dataclass( frozen=True )
class ItineraryResultReason:
   code: ItineraryErrorType
   items: list[ ItinerarySaveIssueItem ] = field( default_factory=list )


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'code': self.code.value,
         'items': [
            item.to_dict() for item in self.items
         ],
      }
