from __future__ import annotations

from typing import Any
from typing import TypeVar

from ..data_access.saved_itinerary import SavedItinerary
from ..data_access.validated_itinerary import ValidatedItinerary
from ..domain.itinerary_builder import ItineraryBuilder
from ...models import GuardiansTalk
from ...models import Itinerary
from ...models import WildEncounter
from ...models.guardians_talk_diff import GuardiansTalkDiff
from ...models.wild_encounter_diff import WildEncounterDiff
from ..results.itinerary_result_reason import ItineraryResultReason
from ..results.itinerary_save_issue_item import ItinerarySaveIssueItem
from ..scheduling.core.time_block import TimeBlock
from ..scheduling.core.time_block_builder import TimeBlockBuilder
from ..scheduling.unscheduling.guardians_talk_unschedule_preparer import GuardiansTalkUnschedulePreparer
from ..scheduling.unscheduling.wild_encounter_unschedule_preparer import WildEncounterUnschedulePreparer
from ...shared.calendar_dates import DateValues
from ...shared.constants import MAX_FIXED_TIME_ITEM_WAIT_MINUTES
from ...shared.duration_values import duration_minutes_to_seconds
from ...shared.enums import ItineraryErrorType
from ...shared.enums import ItinerarySaveIssueItemType

ItemT = TypeVar( 'ItemT' )


class FixedTimeItemLongWaitWarningBuilder():
   # Add new fixed-time itinerary item types here as long-wait tracking expands.
   LONG_WAIT_ITEM_TYPES = (
      ItinerarySaveIssueItemType.GUARDIANS_TALK,
      ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   )


   @classmethod
   def time_block_is_isolated(
         cls,
         activity_block: TimeBlock,
         other_blocks: list[ TimeBlock ],
         *,
         max_wait_minutes: int = MAX_FIXED_TIME_ITEM_WAIT_MINUTES ) -> bool:
      """True when every neighboring scheduled block is more than max_wait away.

      `other_blocks` are the other schedule windows to compare against — not the
      activity's own block.
      """
      if not other_blocks:
         return False

      nearest_gap_seconds = min(
         TimeBlockBuilder.gap_seconds( activity_block, other_block )
         for other_block in other_blocks )

      return nearest_gap_seconds > duration_minutes_to_seconds( max_wait_minutes )


   @classmethod
   def time_block_is_isolated_on_schedule(
         cls,
         activity_block: TimeBlock,
         scheduled_blocks: list[ TimeBlock ],
         *,
         max_wait_minutes: int = MAX_FIXED_TIME_ITEM_WAIT_MINUTES ) -> bool:
      """Isolation check when `activity_block` is already one of `scheduled_blocks`."""
      return cls.time_block_is_isolated(
         activity_block,
         cls._other_scheduled_blocks( scheduled_blocks, activity_block ),
         max_wait_minutes=max_wait_minutes )


   @classmethod
   def has_unscheduled_listed_items(
         cls,
         validated_itinerary: ValidatedItinerary ) -> bool:
      for animal in validated_itinerary.animals:
         if not (
               DateValues.normalize_schedule_time_key( animal.start_time )
               and DateValues.normalize_schedule_time_key( animal.end_time ) ):
            return True

      for attraction in validated_itinerary.attractions:
         if not (
               DateValues.normalize_schedule_time_key( attraction.start_time )
               and DateValues.normalize_schedule_time_key( attraction.end_time ) ):
            return True

      for transportation in validated_itinerary.transportations:
         if not (
               DateValues.normalize_schedule_time_key( transportation.start_time )
               and DateValues.normalize_schedule_time_key( transportation.end_time ) ):
            return True

      return False


   @classmethod
   def isolated_from_itinerary(
         cls,
         itinerary: Itinerary,
         item_type: ItinerarySaveIssueItemType ) -> list[ Any ]:
      return cls._isolated_fixed_time_items(
         cls.items_from_itinerary( itinerary, item_type ),
         TimeBlockBuilder.collect_from_itinerary( itinerary ) )


   @classmethod
   def isolated_from_validated_itinerary(
         cls,
         validated_itinerary: ValidatedItinerary,
         item_type: ItinerarySaveIssueItemType ) -> list[ Any ]:
      return cls._isolated_fixed_time_items(
         cls.items_from_validated( validated_itinerary, item_type ),
         TimeBlockBuilder.collect_from_validated_itinerary( validated_itinerary ) )


   @classmethod
   def reasons_from_itinerary(
         cls,
         itinerary: Itinerary ) -> list[ ItineraryResultReason ]:
      issue_items: list[ ItinerarySaveIssueItem ] = []

      for item_type in cls.LONG_WAIT_ITEM_TYPES:
         for item in cls.isolated_from_itinerary( itinerary, item_type ):
            issue_items.append( cls.build_issue_item( item_type, item ) )

      if not issue_items:
         return []

      return [
         ItineraryResultReason(
            code=ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
            items=issue_items ),
      ]


   @classmethod
   def is_isolated_after_adding(
         cls,
         itinerary: Itinerary,
         new_item: ItemT ) -> bool:
      new_item_block = TimeBlockBuilder.from_schedule_times(
         new_item.start_time,
         new_item.end_time )

      if new_item_block is None:
         return False

      return cls.time_block_is_isolated(
         new_item_block,
         TimeBlockBuilder.collect_from_itinerary( itinerary ) )


   @classmethod
   def build_guardians_talk_issue_from_talks(
         cls,
         talks: list[ GuardiansTalk ] | list[ GuardiansTalkDiff ],
         ) -> ItineraryResultReason:
      return cls._long_wait_issue_from_items(
         ItinerarySaveIssueItemType.GUARDIANS_TALK,
         talks )


   @classmethod
   def build_wild_encounter_issue_from_encounters(
         cls,
         encounters: list[ WildEncounter ] | list[ WildEncounterDiff ],
         ) -> ItineraryResultReason:
      return cls._long_wait_issue_from_items(
         ItinerarySaveIssueItemType.WILD_ENCOUNTER,
         encounters )


   @classmethod
   def build_issue_item(
         cls,
         item_type: ItinerarySaveIssueItemType,
         item: Any ) -> ItinerarySaveIssueItem:
      if item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK:
         return ItinerarySaveIssueItem.from_guardians_talk_diff( item )

      if item_type == ItinerarySaveIssueItemType.WILD_ENCOUNTER:
         return ItinerarySaveIssueItem.from_wild_encounter_diff( item )

      raise ValueError( f'Unsupported fixed-time long-wait item type: { item_type }' )


   @classmethod
   def items_from_itinerary(
         cls,
         itinerary: Itinerary,
         item_type: ItinerarySaveIssueItemType ) -> list[ Any ]:
      if item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK:
         return list( itinerary.guardians_talks )

      if item_type == ItinerarySaveIssueItemType.WILD_ENCOUNTER:
         return list( itinerary.wild_encounters )

      return []


   @classmethod
   def items_from_validated(
         cls,
         validated_itinerary: ValidatedItinerary,
         item_type: ItinerarySaveIssueItemType ) -> list[ Any ]:
      if item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK:
         return list( validated_itinerary.guardians_talks )

      if item_type == ItinerarySaveIssueItemType.WILD_ENCOUNTER:
         return list( validated_itinerary.wild_encounters )

      return []


   @classmethod
   def filter_newly_added_items(
         cls,
         saved_itinerary: SavedItinerary,
         items: list[ Any ],
         item_type: ItinerarySaveIssueItemType ) -> list[ Any ]:
      if item_type == ItinerarySaveIssueItemType.GUARDIANS_TALK:
         return GuardiansTalkUnschedulePreparer.newly_added_active( saved_itinerary, items )

      if item_type == ItinerarySaveIssueItemType.WILD_ENCOUNTER:
         return WildEncounterUnschedulePreparer.newly_added_active( saved_itinerary, items )

      return []


   @classmethod
   def propose_guardians_talk_on_itinerary(
         cls,
         itinerary: Itinerary,
         new_talk: GuardiansTalkDiff,
         itinerary_context: dict[ str, Any ] ) -> Itinerary | None:
      talk_details = itinerary_context[ 'guardians_coordinator' ].get_guardians_talk_details(
         [ new_talk.name ] )

      if not talk_details:
         return None

      detail = talk_details[ 0 ]
      proposed_talk = GuardiansTalk(
         name=new_talk.name,
         location=new_talk.location or detail.location,
         x_coord=detail.x_coord,
         y_coord=detail.y_coord,
         maximum_duration=detail.maximum_duration,
         start_time=new_talk.start_time,
         end_time=new_talk.end_time,
         is_deleted=new_talk.is_deleted )
      talks = [
         talk
         for talk in itinerary.guardians_talks
         if talk.name != new_talk.name
      ]
      talks.append( proposed_talk )

      return cls._itinerary_with_fixed_time_items(
         itinerary,
         guardians_talks=talks )


   @classmethod
   def propose_wild_encounter_on_itinerary(
         cls,
         itinerary: Itinerary,
         new_encounter: WildEncounterDiff,
         itinerary_context: dict[ str, Any ] ) -> Itinerary | None:
      encounter_details = itinerary_context[
         'wild_encounter_coordinator'
      ].get_wild_encounter_details( [ new_encounter.name ] )

      if not encounter_details:
         return None

      detail = encounter_details[ 0 ]
      proposed_encounter = WildEncounter(
         name=new_encounter.name,
         meeting_spot=new_encounter.meeting_spot or detail.meeting_spot,
         link=new_encounter.link or detail.link,
         x_coord=detail.x_coord,
         y_coord=detail.y_coord,
         maximum_duration=detail.maximum_duration,
         start_time=new_encounter.start_time,
         end_time=new_encounter.end_time,
         is_deleted=new_encounter.is_deleted )
      encounters = [
         encounter
         for encounter in itinerary.wild_encounters
         if encounter.name != new_encounter.name
      ]
      encounters.append( proposed_encounter )

      return cls._itinerary_with_fixed_time_items(
         itinerary,
         wild_encounters=encounters )


   @classmethod
   def _other_scheduled_blocks(
         cls,
         scheduled_blocks: list[ TimeBlock ],
         activity_block: TimeBlock ) -> list[ TimeBlock ]:
      """Drop the activity's own window so isolation compares only its neighbors."""
      try:
         activity_index = scheduled_blocks.index( activity_block )
      except ValueError:
         return list( scheduled_blocks )

      return [
         *scheduled_blocks[ :activity_index ],
         *scheduled_blocks[ activity_index + 1: ],
      ]


   @classmethod
   def _isolated_fixed_time_items(
         cls,
         items: list[ Any ],
         scheduled_blocks: list[ TimeBlock ] ) -> list[ Any ]:
      if len( scheduled_blocks ) < 2:
         return []

      isolated: list[ Any ] = []

      for item in items:
         if item.is_deleted:
            continue

         item_block = TimeBlockBuilder.from_schedule_times(
            item.start_time,
            item.end_time )

         if item_block is None:
            continue

         if cls.time_block_is_isolated_on_schedule( item_block, scheduled_blocks ):
            isolated.append( item )

      return isolated


   @classmethod
   def _long_wait_issue_from_items(
         cls,
         item_type: ItinerarySaveIssueItemType,
         items: list[ Any ] ) -> ItineraryResultReason:
      return ItineraryResultReason(
         code=ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items=[
            cls.build_issue_item( item_type, item )
            for item in items
         ] )


   @classmethod
   def _itinerary_with_fixed_time_items(
         cls,
         itinerary: Itinerary,
         *,
         guardians_talks: list[ GuardiansTalk ] | None = None,
         wild_encounters: list[ WildEncounter ] | None = None ) -> Itinerary:
      return ItineraryBuilder.build(
         date=itinerary.date,
         selected_exhibits=list( itinerary.selected_exhibits ),
         animals=list( itinerary.animals ),
         attractions=list( itinerary.attractions ),
         transportations=list( itinerary.transportations ),
         transportation_stations=list( itinerary.transportation_stations ),
         guardians_talks=(
            list( itinerary.guardians_talks )
            if guardians_talks is None
            else guardians_talks
         ),
         wild_encounters=(
            list( itinerary.wild_encounters )
            if wild_encounters is None
            else wild_encounters
         ),
         events=list( itinerary.events ),
         arrival_time=itinerary.arrival_time,
         departure_time=itinerary.departure_time )
