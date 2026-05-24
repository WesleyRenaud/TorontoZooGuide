from __future__ import annotations

from dataclasses import dataclass

from .itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.enums import ItinerarySaveIssueType


@dataclass( frozen=True )
class ItinerarySaveIssue:
   issue_type: ItinerarySaveIssueType
   message: str
   items: tuple[ ItinerarySaveIssueItem, ... ] = ()


   def to_dict( self ) -> dict[ str, object ]:
      return {
         'type': self.issue_type,
         'message': self.message,
         'items': [
            item.to_dict() for item in self.items
         ],
      }
