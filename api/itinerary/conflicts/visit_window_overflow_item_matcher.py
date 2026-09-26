from __future__ import annotations

from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.calendar_dates import DateValues
from .visit_window_overflow_keep_item import VisitWindowOverflowKeepItem


class VisitWindowOverflowItemMatcher():
   @classmethod
   def is_kept(
         cls,
         overflow_item: ItinerarySaveIssueItem,
         kept_items: list[ VisitWindowOverflowKeepItem ] ) -> bool:
      return any(
         cls._overflow_item_matches_keep_item( overflow_item, keep_item )
         for keep_item in kept_items )


   @classmethod
   def partition(
         cls,
         overflow_items: list[ ItinerarySaveIssueItem ],
         kept_items: list[ VisitWindowOverflowKeepItem ]
         ) -> tuple[ list[ ItinerarySaveIssueItem ], list[ ItinerarySaveIssueItem ] ]:
      kept_overflow_items: list[ ItinerarySaveIssueItem ] = []
      dropped_overflow_items: list[ ItinerarySaveIssueItem ] = []

      for overflow_item in overflow_items:
         if cls.is_kept( overflow_item, kept_items ):
            kept_overflow_items.append( overflow_item )
            continue

         dropped_overflow_items.append( overflow_item )

      return ( kept_overflow_items, dropped_overflow_items )


   @classmethod
   def _overflow_item_matches_keep_item(
         cls,
         overflow_item: ItinerarySaveIssueItem,
         keep_item: VisitWindowOverflowKeepItem ) -> bool:
      if overflow_item.name != keep_item.name:
         return False

      if overflow_item.item_type != keep_item.item_type:
         return False

      if keep_item.start_time is None:
         return True

      return (
         DateValues.time_value_in_seconds( overflow_item.start_time )
         == DateValues.time_value_in_seconds( keep_item.start_time )
      )
