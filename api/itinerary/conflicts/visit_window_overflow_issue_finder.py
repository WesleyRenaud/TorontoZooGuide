from __future__ import annotations

from ...models import Itinerary
from ...models.attraction_diff import AttractionDiff
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.core.time_block_builder import TimeBlockBuilder
from ...shared.calendar_dates import DateValues
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItineraryVisitWindowOverflowEnd
from ...types import Types


class VisitWindowOverflowIssueFinder():
   @classmethod
   def find(
         cls,
         arrival_time: Types.ScheduleTimeKey,
         departure_time: Types.ScheduleTimeKey,
         *,
         guardians_talks: list[ GuardiansTalkDiff ],
         wild_encounters: list[ WildEncounterDiff ],
         attractions: list[ AttractionDiff ] ) -> list[ ItineraryResultReason ]:
      arrival_seconds = DateValues.time_value_in_seconds( arrival_time )
      departure_seconds = DateValues.time_value_in_seconds( departure_time )

      if arrival_seconds is None or departure_seconds is None:
         return []

      overflow_items = cls._overflow_issue_items(
         arrival_seconds,
         departure_seconds,
         guardians_talks=guardians_talks,
         wild_encounters=wild_encounters,
         attractions=attractions )

      if not overflow_items:
         return []

      return [
         ItineraryResultReason(
            code=ItineraryErrorType.SCHEDULED_ITEM_OUTSIDE_VISIT_HOURS,
            items=overflow_items )
      ]


   @classmethod
   def find_from_itinerary(
         cls,
         arrival_time: Types.ScheduleTimeKey,
         departure_time: Types.ScheduleTimeKey,
         itinerary: Itinerary ) -> list[ ItineraryResultReason ]:
      return cls.find(
         arrival_time,
         departure_time,
         guardians_talks=cls._talks_from_itinerary( itinerary ),
         wild_encounters=cls._encounters_from_itinerary( itinerary ),
         attractions=cls._attractions_from_itinerary( itinerary ) )


   @classmethod
   def _talks_from_itinerary(
         cls,
         itinerary: Itinerary ) -> list[ GuardiansTalkDiff ]:
      return [
         GuardiansTalkDiff(
            name=talk.name,
            is_deleted=talk.is_deleted,
            start_time=talk.start_time,
            end_time=talk.end_time,
            location=talk.location )
         for talk in itinerary.guardians_talks
      ]


   @classmethod
   def _encounters_from_itinerary(
         cls,
         itinerary: Itinerary ) -> list[ WildEncounterDiff ]:
      return [
         WildEncounterDiff(
            name=encounter.name,
            is_deleted=encounter.is_deleted,
            start_time=encounter.start_time,
            end_time=encounter.end_time,
            meeting_spot=encounter.meeting_spot )
         for encounter in itinerary.wild_encounters
      ]


   @classmethod
   def _attractions_from_itinerary(
         cls,
         itinerary: Itinerary ) -> list[ AttractionDiff ]:
      return [
         AttractionDiff(
            name=attraction.name,
            old_likelihood=attraction.old_likelihood,
            new_likelihood=attraction.likelihood,
            start_time=attraction.start_time,
            end_time=attraction.end_time )
         for attraction in itinerary.attractions
      ]


   @classmethod
   def _schedule_time_range(
         cls,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> tuple[ int, int ] | None:
      time_block = TimeBlockBuilder.from_schedule_times( start_time, end_time )

      if time_block is None:
         return None

      return ( time_block.start_seconds, time_block.end_seconds )


   @classmethod
   def _overflow_end(
         cls,
         start_seconds: int,
         end_seconds: int,
         arrival_seconds: int,
         departure_seconds: int ) -> ItineraryVisitWindowOverflowEnd | None:
      overflows_arrival = start_seconds < arrival_seconds
      overflows_departure = end_seconds > departure_seconds

      if overflows_arrival and overflows_departure:
         return ItineraryVisitWindowOverflowEnd.BOTH

      if overflows_arrival:
         return ItineraryVisitWindowOverflowEnd.ARRIVAL

      if overflows_departure:
         return ItineraryVisitWindowOverflowEnd.DEPARTURE

      return None


   @classmethod
   def _issue_item_for_scheduled(
         cls,
         scheduled_item: GuardiansTalkDiff | WildEncounterDiff | AttractionDiff,
         overflow_end: ItineraryVisitWindowOverflowEnd ) -> ItinerarySaveIssueItem:
      if isinstance( scheduled_item, GuardiansTalkDiff ):
         return ItinerarySaveIssueItem.from_guardians_talk_diff(
            scheduled_item,
            overflow_end=overflow_end )

      if isinstance( scheduled_item, WildEncounterDiff ):
         return ItinerarySaveIssueItem.from_wild_encounter_diff(
            scheduled_item,
            overflow_end=overflow_end )

      return ItinerarySaveIssueItem.from_attraction_diff(
         scheduled_item,
         overflow_end=overflow_end )


   @classmethod
   def _collect_scheduled_items(
         cls,
         *,
         guardians_talks: list[ GuardiansTalkDiff ],
         wild_encounters: list[ WildEncounterDiff ],
         attractions: list[ AttractionDiff ]
         ) -> list[ GuardiansTalkDiff | WildEncounterDiff | AttractionDiff ]:
      scheduled_items: list[
         GuardiansTalkDiff | WildEncounterDiff | AttractionDiff
      ] = []

      for talk in guardians_talks:
         if talk.is_deleted:
            continue

         scheduled_items.append( talk )

      for encounter in wild_encounters:
         if encounter.is_deleted:
            continue

         scheduled_items.append( encounter )

      scheduled_items.extend( attractions )

      return scheduled_items


   @classmethod
   def _overflow_issue_items(
         cls,
         arrival_seconds: int,
         departure_seconds: int,
         *,
         guardians_talks: list[ GuardiansTalkDiff ],
         wild_encounters: list[ WildEncounterDiff ],
         attractions: list[ AttractionDiff ] ) -> list[ ItinerarySaveIssueItem ]:
      overflow_items: list[ ItinerarySaveIssueItem ] = []

      for scheduled_item in cls._collect_scheduled_items(
            guardians_talks=guardians_talks,
            wild_encounters=wild_encounters,
            attractions=attractions ):
         schedule_range = cls._schedule_time_range(
            scheduled_item.start_time,
            scheduled_item.end_time )

         if schedule_range is None:
            continue

         start_seconds, end_seconds = schedule_range
         overflow_end = cls._overflow_end(
            start_seconds,
            end_seconds,
            arrival_seconds,
            departure_seconds )

         if overflow_end is None:
            continue

         overflow_items.append(
            cls._issue_item_for_scheduled( scheduled_item, overflow_end ) )

      return sorted(
         overflow_items,
         key=lambda issue_item: (
            DateValues.time_value_in_minutes( issue_item.start_time ) or 0,
            issue_item.name,
         ) )
