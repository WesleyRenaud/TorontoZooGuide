from __future__ import annotations

from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItinerarySaveIssueItemType
from ...shared.enums import ItineraryVisitWindowOverflowEnd
from ...types import Types


class VisitWindowOverflowTimeExpander():
   @classmethod
   def expand(
         cls,
         arrival_time: Types.ScheduleTimeKey,
         departure_time: Types.ScheduleTimeKey,
         kept_items: list[ ItinerarySaveIssueItem ]
         ) -> tuple[ Types.ScheduleTimeKey, Types.ScheduleTimeKey ]:
      expanded_arrival_time = arrival_time
      expanded_departure_time = departure_time
      arrival_item = cls._pinched_item(
         kept_items,
         ItineraryVisitWindowOverflowEnd.ARRIVAL )
      departure_item = cls._pinched_item(
         kept_items,
         ItineraryVisitWindowOverflowEnd.DEPARTURE )

      if arrival_item is not None:
         expanded_arrival_time = cls._expanded_arrival_time( arrival_item )

      if departure_item is not None:
         expanded_departure_time = cls._expanded_departure_time( departure_item )

      return ( expanded_arrival_time, expanded_departure_time )


   @classmethod
   def _pinched_item(
         cls,
         kept_items: list[ ItinerarySaveIssueItem ],
         overflow_end: ItineraryVisitWindowOverflowEnd
         ) -> ItinerarySaveIssueItem | None:
      matching_items = [
         kept_item
         for kept_item in kept_items
         if cls._overflows_end( kept_item, overflow_end )
      ]

      if not matching_items:
         return None

      if overflow_end == ItineraryVisitWindowOverflowEnd.ARRIVAL:
         return min(
            matching_items,
            key=lambda item: DateValues.time_value_in_seconds( item.start_time ) or 0 )

      return max(
         matching_items,
         key=lambda item: DateValues.time_value_in_seconds( item.end_time ) or 0 )


   @classmethod
   def _overflows_end(
         cls,
         kept_item: ItinerarySaveIssueItem,
         overflow_end: ItineraryVisitWindowOverflowEnd ) -> bool:
      if kept_item.overflow_end == overflow_end:
         return True

      return kept_item.overflow_end == ItineraryVisitWindowOverflowEnd.BOTH


   @classmethod
   def _expanded_arrival_time(
         cls,
         kept_item: ItinerarySaveIssueItem ) -> Types.ScheduleTimeKey:
      start_seconds = DateValues.time_value_in_seconds( kept_item.start_time ) or 0
      travel_seconds = (
         ScheduleItemTravelTimeCalculator.entrance_travel_seconds_to_walk_node(
            cls._walk_node_id( kept_item ) ) )

      return DateValues.schedule_time_key_from_seconds(
         max( 0, start_seconds - travel_seconds ) )


   @classmethod
   def _expanded_departure_time(
         cls,
         kept_item: ItinerarySaveIssueItem ) -> Types.ScheduleTimeKey:
      end_seconds = DateValues.time_value_in_seconds( kept_item.end_time ) or 0
      travel_seconds = (
         ScheduleItemTravelTimeCalculator.entrance_travel_seconds_from_walk_node(
            cls._walk_node_id( kept_item ) ) )

      return DateValues.schedule_time_key_from_seconds(
         end_seconds + travel_seconds )


   @classmethod
   def _walk_node_id( cls, kept_item: ItinerarySaveIssueItem ) -> str | None:
      if kept_item.item_type == ItinerarySaveIssueItemType.ATTRACTION:
         return ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction(
            kept_item.name )

      if kept_item.item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK:
         return ScheduleItemTravelTimeCalculator.walk_node_id_for_guardians_talk(
            kept_item.name,
            location=kept_item.location )

      if kept_item.item_type == ItinerarySaveIssueItemType.WILD_ENCOUNTER:
         return ScheduleItemTravelTimeCalculator.walk_node_id_for_wild_encounter(
            kept_item.meeting_spot )

      return None
