from __future__ import annotations

from enum import Enum

from .shared_enum_values import SharedEnumValues


ItinerarySaveIssueItemType = Enum(
   'ItinerarySaveIssueItemType',
   SharedEnumValues.load( 'itinerarySaveIssueItemType.json' ),
   type=str,
)
