from __future__ import annotations

from dataclasses import replace

from ..attraction_schedule_item_key import AttractionScheduleItemKey
from ..data_access.itinerary_guardians_talk_input import ItineraryGuardiansTalkInput
from ..guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from ...models.attraction_diff import AttractionDiff
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ..operations.itinerary_item_remover import ItineraryItemRemover
from ..operations.itinerary_save_context import ItinerarySaveContext
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItinerarySaveIssueItemType
from ...types import Types
from .visit_window_overflow_item_matcher import VisitWindowOverflowItemMatcher
from .visit_window_overflow_keep_item import VisitWindowOverflowKeepItem
from .visit_window_overflow_resolution import VisitWindowOverflowResolution
from .visit_window_overflow_time_expander import VisitWindowOverflowTimeExpander
from ..wild_encounter_schedule_item_key import WildEncounterScheduleItemKey


class VisitWindowOverflowChangeApplier():
   @classmethod
   def overflow_items(
         cls,
         overflow_reasons: list[ ItineraryResultReason ]
         ) -> list[ ItinerarySaveIssueItem ]:
      return [
         overflow_item
         for overflow_reason in overflow_reasons
         for overflow_item in overflow_reason.items
      ]


   @classmethod
   def resolve(
         cls,
         overflow_items: list[ ItinerarySaveIssueItem ],
         kept_items: list[ VisitWindowOverflowKeepItem ],
         arrival_time: Types.ScheduleTimeKey,
         departure_time: Types.ScheduleTimeKey ) -> VisitWindowOverflowResolution:
      kept_overflow_items, dropped_overflow_items = (
         VisitWindowOverflowItemMatcher.partition(
            overflow_items,
            kept_items ) )
      expanded_arrival_time, expanded_departure_time = (
         VisitWindowOverflowTimeExpander.expand(
            arrival_time,
            departure_time,
            kept_overflow_items ) )

      return VisitWindowOverflowResolution(
         kept_items=kept_overflow_items,
         dropped_items=dropped_overflow_items,
         arrival_time=expanded_arrival_time,
         departure_time=expanded_departure_time )


   @classmethod
   def apply_to_context(
         cls,
         context: ItinerarySaveContext,
         overflow_reasons: list[ ItineraryResultReason ],
         kept_items: list[ VisitWindowOverflowKeepItem ] ) -> ItinerarySaveContext:
      resolution = cls.resolve(
         cls.overflow_items( overflow_reasons ),
         kept_items,
         context.save_input.arrival_time,
         context.save_input.departure_time )
      validated_itinerary = context.validated_itinerary
      save_input = context.save_input

      return replace(
         context,
         save_input=replace(
            save_input,
            arrival_time=resolution.arrival_time,
            departure_time=resolution.departure_time,
            attractions=cls._remaining_attraction_names(
               save_input.attractions,
               resolution.dropped_items ),
            guardians_talks=cls._remaining_talk_inputs(
               save_input.guardians_talks,
               resolution.dropped_items ),
            wild_encounters=cls._remaining_encounter_keys(
               save_input.wild_encounters,
               resolution.dropped_items ) ),
         validated_itinerary=replace(
            validated_itinerary,
            arrival_time=resolution.arrival_time,
            departure_time=resolution.departure_time,
            attractions=cls._remaining_attraction_diffs(
               validated_itinerary.attractions,
               resolution.dropped_items ),
            guardians_talks=cls._remaining_talk_diffs(
               validated_itinerary.guardians_talks,
               resolution.dropped_items ),
            wild_encounters=cls._remaining_encounter_diffs(
               validated_itinerary.wild_encounters,
               resolution.dropped_items ) ) )


   @classmethod
   def drop_saved_items(
         cls,
         conn: Types.Connection,
         dropped_items: list[ ItinerarySaveIssueItem ] ) -> None:
      if not dropped_items:
         return

      cur = conn.cursor()

      try:
         for dropped_item in dropped_items:
            schedule_item_key = cls._schedule_item_key( dropped_item )

            if schedule_item_key is None:
               continue

            ItineraryItemRemover.apply( cur, schedule_item_key )

         conn.commit()
      finally:
         cur.close()


   @classmethod
   def _schedule_item_key(
         cls,
         dropped_item: ItinerarySaveIssueItem
         ) -> (
            AttractionScheduleItemKey
            | GuardiansTalkScheduleItemKey
            | WildEncounterScheduleItemKey
            | None ):
      if dropped_item.item_type == ItinerarySaveIssueItemType.ATTRACTION:
         return AttractionScheduleItemKey( name=dropped_item.name )

      if dropped_item.item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK:
         return GuardiansTalkScheduleItemKey(
            name=dropped_item.name,
            start_time=dropped_item.start_time,
            end_time=dropped_item.end_time )

      if dropped_item.item_type == ItinerarySaveIssueItemType.WILD_ENCOUNTER:
         return WildEncounterScheduleItemKey(
            name=dropped_item.name,
            start_time=dropped_item.start_time,
            end_time=dropped_item.end_time )

      return None


   @classmethod
   def _is_dropped(
         cls,
         *,
         name: str,
         item_type: str,
         start_time: Types.ScheduleTimeKey,
         dropped_items: list[ ItinerarySaveIssueItem ] ) -> bool:
      return any(
         dropped_item.name == name
         and dropped_item.item_type == item_type
         and (
            DateValues.time_value_in_seconds( dropped_item.start_time )
            == DateValues.time_value_in_seconds( start_time )
         )
         for dropped_item in dropped_items )


   @classmethod
   def _remaining_attraction_names(
         cls,
         attractions: list[ str ],
         dropped_items: list[ ItinerarySaveIssueItem ] ) -> list[ str ]:
      dropped_names = {
         dropped_item.name
         for dropped_item in dropped_items
         if dropped_item.item_type == ItinerarySaveIssueItemType.ATTRACTION
      }

      return [
         attraction
         for attraction in attractions
         if attraction not in dropped_names
      ]


   @classmethod
   def _remaining_attraction_diffs(
         cls,
         attractions: list[ AttractionDiff ],
         dropped_items: list[ ItinerarySaveIssueItem ] ) -> list[ AttractionDiff ]:
      dropped_names = {
         dropped_item.name
         for dropped_item in dropped_items
         if dropped_item.item_type == ItinerarySaveIssueItemType.ATTRACTION
      }

      return [
         attraction
         for attraction in attractions
         if attraction.name not in dropped_names
      ]


   @classmethod
   def _remaining_talk_inputs(
         cls,
         talks: list[ ItineraryGuardiansTalkInput ],
         dropped_items: list[ ItinerarySaveIssueItem ]
         ) -> list[ ItineraryGuardiansTalkInput ]:
      return [
         talk
         for talk in talks
         if not cls._is_dropped(
            name=talk.name,
            item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
            start_time=talk.start_time,
            dropped_items=dropped_items )
      ]


   @classmethod
   def _remaining_talk_diffs(
         cls,
         talks: list[ GuardiansTalkDiff ],
         dropped_items: list[ ItinerarySaveIssueItem ] ) -> list[ GuardiansTalkDiff ]:
      return [
         talk
         for talk in talks
         if not cls._is_dropped(
            name=talk.name,
            item_type=ItinerarySaveIssueItemType.GUARDIANS_TALK,
            start_time=talk.start_time,
            dropped_items=dropped_items )
      ]


   @classmethod
   def _remaining_encounter_keys(
         cls,
         encounters: list[ WildEncounterScheduleItemKey ],
         dropped_items: list[ ItinerarySaveIssueItem ]
         ) -> list[ WildEncounterScheduleItemKey ]:
      return [
         encounter
         for encounter in encounters
         if not cls._is_dropped(
            name=encounter.name,
            item_type=ItinerarySaveIssueItemType.WILD_ENCOUNTER,
            start_time=encounter.start_time,
            dropped_items=dropped_items )
      ]


   @classmethod
   def _remaining_encounter_diffs(
         cls,
         encounters: list[ WildEncounterDiff ],
         dropped_items: list[ ItinerarySaveIssueItem ] ) -> list[ WildEncounterDiff ]:
      return [
         encounter
         for encounter in encounters
         if not cls._is_dropped(
            name=encounter.name,
            item_type=ItinerarySaveIssueItemType.WILD_ENCOUNTER,
            start_time=encounter.start_time,
            dropped_items=dropped_items )
      ]
