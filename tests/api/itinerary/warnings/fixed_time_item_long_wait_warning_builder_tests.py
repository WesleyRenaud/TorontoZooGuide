from __future__ import annotations

import pytest

from api.itinerary.data_access.itinerary_guardians_talk_record import ItineraryGuardiansTalkRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.warnings.fixed_time_item_long_wait_warning_builder import FixedTimeItemLongWaitWarningBuilder
from api.models import Animal
from api.models import GuardiansTalk
from api.models import WildEncounter
from api.models.animal_diff import AnimalDiff
from api.models.attraction_diff import AttractionDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.transportation_diff import TransportationDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.calendar_dates import DateValues
from api.shared.constants import Constants
from api.shared.duration_values import DurationValues
from api.shared.enums import ItineraryErrorType, Position
from api.shared.enums import ItinerarySaveIssueItemType
from api.shared.enums.transportation_name import TransportationName


ZEBRA_TALK = "Grevy's Zebra"
MEERKAT_TALK = 'Slender-Tailed Meerkat'
RAINFOREST_ENCOUNTER = 'African Rainforest'
CAROUSEL = 'Conservation Carousel'
MEETING_SPOT = 'Wild Encounter - Africa Meeting Spot'


def _validated(
      *,
      animals: list[ AnimalDiff ] | None = None,
      attractions: list[ AttractionDiff ] | None = None,
      transportations: list[ TransportationDiff ] | None = None,
      guardians_talks: list[ GuardiansTalkDiff ] | None = None,
      wild_encounters: list[ WildEncounterDiff ] | None = None ) -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=animals or [],
      attractions=attractions or [],
      guardians_talks=guardians_talks or [],
      wild_encounters=wild_encounters or [],
      events=[],
      transportations=transportations or [] )


def _time_block( start_minutes: int, duration_minutes: int ) -> TimeBlock:
   return TimeBlock(
      start_seconds=DurationValues.minutes_to_seconds( start_minutes ),
      end_seconds=DurationValues.minutes_to_seconds(
         start_minutes + duration_minutes ) )


class _GuardiansTalkDetailsStub:
   def __init__( self, talks: list[ GuardiansTalk ] ) -> None:
      self._talks = talks


   def get_guardians_talk_details( self, names: list[ str ] ) -> list[ GuardiansTalk ]:
      return [
         talk
         for talk in self._talks
         if talk.name in names
      ]


class _WildEncounterDetailsStub:
   def __init__( self, encounters: list[ WildEncounter ] ) -> None:
      self._encounters = encounters


   def get_wild_encounter_details( self, names: list[ str ] ) -> list[ WildEncounter ]:
      return [
         encounter
         for encounter in self._encounters
         if encounter.name in names
      ]


def Test_TimeBlockIsIsolated_TestFarNeighbor_ExpectTrue() -> None:
   neighbor_start_minutes = 10 * 60
   neighbor_duration_minutes = 8
   activity_duration_minutes = 30
   activity_start_minutes = (
      neighbor_start_minutes
      + neighbor_duration_minutes
      + Constants.MAX_FIXED_TIME_ITEM_WAIT_MINUTES
      + 1 )
   activity = _time_block( activity_start_minutes, activity_duration_minutes )
   neighbors = [ _time_block( neighbor_start_minutes, neighbor_duration_minutes ) ]

   isolated = FixedTimeItemLongWaitWarningBuilder.time_block_is_isolated(
      activity,
      neighbors )

   assert isolated is True


def Test_TimeBlockIsIsolated_TestNearNeighbor_ExpectFalse() -> None:
   neighbor_start_minutes = 10 * 60
   neighbor_duration_minutes = 8
   activity_duration_minutes = 30
   activity_start_minutes = (
      neighbor_start_minutes
      + neighbor_duration_minutes
      + Constants.MAX_FIXED_TIME_ITEM_WAIT_MINUTES
      - 1 )
   activity = _time_block( activity_start_minutes, activity_duration_minutes )
   neighbors = [ _time_block( neighbor_start_minutes, neighbor_duration_minutes ) ]

   isolated = FixedTimeItemLongWaitWarningBuilder.time_block_is_isolated(
      activity,
      neighbors )

   assert isolated is False


def Test_TimeBlockIsIsolated_TestNoNeighbors_ExpectFalse() -> None:
   activity_start_minutes = 13 * 60
   activity_duration_minutes = 30
   activity = _time_block( activity_start_minutes, activity_duration_minutes )
   neighbors: list[ TimeBlock ] = []

   isolated = FixedTimeItemLongWaitWarningBuilder.time_block_is_isolated(
      activity,
      neighbors )

   assert isolated is False


def Test_HasUnscheduledListedItems_TestMissingAnimalTimes_ExpectTrue() -> None:
   validated = _validated(
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100 ),
      ] )

   unscheduled = FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items(
      validated )

   assert unscheduled is True


def Test_HasUnscheduledListedItems_TestAllScheduled_ExpectFalse() -> None:
   start_time = '10:00 AM'
   duration_minutes = 8
   validated = _validated(
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time=start_time,
            end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) ),
      ] )

   unscheduled = FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items(
      validated )

   assert unscheduled is False


def Test_HasUnscheduledListedItems_TestMissingAttractionTimes_ExpectTrue() -> None:
   validated = _validated(
      attractions=[
         AttractionDiff(
            name=CAROUSEL,
            old_likelihood=None,
            new_likelihood=3 ),
      ] )

   unscheduled = FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items(
      validated )

   assert unscheduled is True


def Test_HasUnscheduledListedItems_TestMissingTransportationTimes_ExpectTrue() -> None:
   validated = _validated(
      transportations=[
         TransportationDiff(
            name=TransportationName.ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True ),
      ] )

   unscheduled = FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items(
      validated )

   assert unscheduled is True


def Test_IsolatedFromItinerary_TestFarTalk_ExpectIsolated() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   nearby_start = '10:15 AM'
   nearby_duration_minutes = 30
   far_start = '1:00 PM'
   far_duration_minutes = 30
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   nearby = GuardiansTalk(
      name=ZEBRA_TALK,
      location='Africa Savanna',
      x_coord=0.0,
      y_coord=0.0,
      start_time=nearby_start,
      end_time=DateValues.add_minutes_to_time( nearby_start, nearby_duration_minutes ) )
   far = GuardiansTalk(
      name=MEERKAT_TALK,
      location='African Rainforest Pavilion',
      x_coord=0.0,
      y_coord=0.0,
      start_time=far_start,
      end_time=DateValues.add_minutes_to_time( far_start, far_duration_minutes ) )
   itinerary.guardians_talks = [ nearby, far ]

   isolated = FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.GUARDIANS_TALK )

   assert [ talk.name for talk in isolated ] == [ far.name ]


def Test_IsolatedFromItinerary_TestFarWildEncounter_ExpectIsolated() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   encounter_start = '1:00 PM'
   encounter_duration_minutes = 45
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   encounter = WildEncounter(
      name=RAINFOREST_ENCOUNTER,
      meeting_spot=MEETING_SPOT,
      link='african-rainforest',
      x_coord=0.0,
      y_coord=0.0,
      start_time=encounter_start,
      end_time=DateValues.add_minutes_to_time(
         encounter_start,
         encounter_duration_minutes ) )
   itinerary.wild_encounters = [ encounter ]

   isolated = FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.WILD_ENCOUNTER )

   assert [ item.name for item in isolated ] == [ encounter.name ]


def Test_IsolatedFromItinerary_TestDeletedTalk_ExpectSkipped() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   talk_start = '1:00 PM'
   talk_duration_minutes = 30
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=MEERKAT_TALK,
         location='African Rainforest Pavilion',
         x_coord=0.0,
         y_coord=0.0,
         start_time=talk_start,
         end_time=DateValues.add_minutes_to_time( talk_start, talk_duration_minutes ),
         is_deleted=True ),
   ]

   isolated = FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.GUARDIANS_TALK )

   assert isolated == []


def Test_BuildGuardiansTalkIssueFromTalks_TestTalks_ExpectLongWaitIssue() -> None:
   start_time = '1:00 PM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      location='Africa Savanna' )
   talks = [ talk ]

   issue = FixedTimeItemLongWaitWarningBuilder.build_guardians_talk_issue_from_talks(
      talks )

   assert issue.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in issue.items ] == [ talk.name ]


def Test_BuildWildEncounterIssueFromEncounters_TestEncounters_ExpectLongWaitIssue() -> None:
   start_time = '1:00 PM'
   duration_minutes = 45
   encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   encounters = [ encounter ]

   issue = FixedTimeItemLongWaitWarningBuilder.build_wild_encounter_issue_from_encounters(
      encounters )

   assert issue.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in issue.items ] == [ encounter.name ]


def Test_BuildIssueItem_TestUnsupportedType_ExpectValueError() -> None:
   start_time = '1:00 PM'
   duration_minutes = 30
   item_type = ItinerarySaveIssueItemType.ANIMAL
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )

   with pytest.raises( ValueError, match='Unsupported fixed-time long-wait item type' ):
      FixedTimeItemLongWaitWarningBuilder.build_issue_item( item_type, talk )


def Test_ReasonsFromItinerary_TestIsolatedTalk_ExpectLongWaitReason() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   nearby_start = '10:15 AM'
   nearby_duration_minutes = 30
   far_start = '1:00 PM'
   far_duration_minutes = 30
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   nearby = GuardiansTalk(
      name=ZEBRA_TALK,
      location='Africa Savanna',
      x_coord=0.0,
      y_coord=0.0,
      start_time=nearby_start,
      end_time=DateValues.add_minutes_to_time( nearby_start, nearby_duration_minutes ) )
   far = GuardiansTalk(
      name=MEERKAT_TALK,
      location='African Rainforest Pavilion',
      x_coord=0.0,
      y_coord=0.0,
      start_time=far_start,
      end_time=DateValues.add_minutes_to_time( far_start, far_duration_minutes ) )
   itinerary.guardians_talks = [ nearby, far ]

   reasons = FixedTimeItemLongWaitWarningBuilder.reasons_from_itinerary( itinerary )

   assert [ reason.code for reason in reasons ] == [
      ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
   ]
   assert [ item.name for item in reasons[ Position.FIRST ].items ] == [ far.name ]


def Test_ReasonsFromItinerary_TestNoIsolatedItems_ExpectEmptyReasons() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   talk_start = '10:15 AM'
   talk_duration_minutes = 30
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time=talk_start,
         end_time=DateValues.add_minutes_to_time( talk_start, talk_duration_minutes ) ),
   ]

   reasons = FixedTimeItemLongWaitWarningBuilder.reasons_from_itinerary( itinerary )

   assert reasons == []


def Test_IsIsolatedAfterAdding_TestFarFromSchedule_ExpectTrue() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   talk_start = '1:00 PM'
   talk_duration_minutes = 30
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   new_talk = GuardiansTalkDiff(
      name=MEERKAT_TALK,
      is_deleted=False,
      start_time=talk_start,
      end_time=DateValues.add_minutes_to_time( talk_start, talk_duration_minutes ) )

   isolated = FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding(
      itinerary,
      new_talk )

   assert isolated is True


def Test_IsIsolatedAfterAdding_TestNearSchedule_ExpectFalse() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   talk_start = '10:15 AM'
   talk_duration_minutes = 30
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   new_talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=talk_start,
      end_time=DateValues.add_minutes_to_time( talk_start, talk_duration_minutes ) )

   isolated = FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding(
      itinerary,
      new_talk )

   assert isolated is False


def Test_IsIsolatedAfterAdding_TestUntimedItem_ExpectFalse() -> None:
   lion_start = '10:00 AM'
   lion_duration_minutes = 8
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time=lion_start,
         end_time=DateValues.add_minutes_to_time( lion_start, lion_duration_minutes ) ),
   ]
   new_talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=None,
      end_time=None )

   isolated = FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding(
      itinerary,
      new_talk )

   assert isolated is False


def Test_FilterNewlyAddedItems_TestNewTalk_ExpectTalk() -> None:
   start_time = '12:00 PM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )
   talks = [ talk ]

   newly_added = FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
      saved,
      talks,
      ItinerarySaveIssueItemType.GUARDIANS_TALK )

   assert newly_added == talks


def Test_FilterNewlyAddedItems_TestAlreadySavedTalk_ExpectEmpty() -> None:
   start_time = '12:00 PM'
   duration_minutes = 30
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=talk.name,
            start_time=talk.start_time,
            end_time=talk.end_time,
            is_deleted=False ),
      ],
   )

   newly_added = FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
      saved,
      [ talk ],
      ItinerarySaveIssueItemType.GUARDIANS_TALK )

   assert newly_added == []


def Test_FilterNewlyAddedItems_TestNewWildEncounter_ExpectEncounter() -> None:
   start_time = '1:00 PM'
   duration_minutes = 45
   encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      wild_encounter_rows=[],
   )
   encounters = [ encounter ]

   newly_added = FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
      saved,
      encounters,
      ItinerarySaveIssueItemType.WILD_ENCOUNTER )

   assert newly_added == encounters


def Test_FilterNewlyAddedItems_TestUnsupportedType_ExpectEmpty() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )
   items: list = []

   newly_added = FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
      saved,
      items,
      ItinerarySaveIssueItemType.ANIMAL )

   assert newly_added == []


def Test_ProposeGuardiansTalkOnItinerary_TestKnownTalk_ExpectProposedItinerary() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.date = '2026-06-15'
   start_time = '12:00 PM'
   duration_minutes = 30
   detail = GuardiansTalk(
      name=ZEBRA_TALK,
      location='Africa Savanna',
      x_coord=11.0,
      y_coord=22.0,
      maximum_duration=duration_minutes )
   new_talk = GuardiansTalkDiff(
      name=detail.name,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   itinerary_context = {
      'guardians_coordinator': _GuardiansTalkDetailsStub( [ detail ] ),
   }

   proposed = FixedTimeItemLongWaitWarningBuilder.propose_guardians_talk_on_itinerary(
      itinerary,
      new_talk,
      itinerary_context )

   assert proposed is not None
   talk = proposed.guardians_talks[ Position.FIRST ]
   assert talk.name == new_talk.name
   assert talk.location == detail.location
   assert talk.x_coord == detail.x_coord
   assert talk.y_coord == detail.y_coord
   assert talk.start_time == new_talk.start_time
   assert talk.end_time == new_talk.end_time


def Test_ProposeGuardiansTalkOnItinerary_TestUnknownTalk_ExpectNone() -> None:
   itinerary = ItineraryBuilder.empty()
   start_time = '12:00 PM'
   duration_minutes = 30
   new_talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   itinerary_context = {
      'guardians_coordinator': _GuardiansTalkDetailsStub( [] ),
   }

   proposed = FixedTimeItemLongWaitWarningBuilder.propose_guardians_talk_on_itinerary(
      itinerary,
      new_talk,
      itinerary_context )

   assert proposed is None


def Test_ProposeWildEncounterOnItinerary_TestKnownEncounter_ExpectProposedItinerary() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.date = '2026-06-15'
   start_time = '1:00 PM'
   duration_minutes = 45
   detail = WildEncounter(
      name=RAINFOREST_ENCOUNTER,
      meeting_spot=MEETING_SPOT,
      link='african-rainforest',
      x_coord=33.0,
      y_coord=44.0,
      maximum_duration=duration_minutes )
   new_encounter = WildEncounterDiff(
      name=detail.name,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   itinerary_context = {
      'wild_encounter_coordinator': _WildEncounterDetailsStub( [ detail ] ),
   }

   proposed = FixedTimeItemLongWaitWarningBuilder.propose_wild_encounter_on_itinerary(
      itinerary,
      new_encounter,
      itinerary_context )

   assert proposed is not None
   encounter = proposed.wild_encounters[ Position.FIRST ]
   assert encounter.name == new_encounter.name
   assert encounter.meeting_spot == detail.meeting_spot
   assert encounter.link == detail.link
   assert encounter.x_coord == detail.x_coord
   assert encounter.y_coord == detail.y_coord
   assert encounter.start_time == new_encounter.start_time
   assert encounter.end_time == new_encounter.end_time


def Test_ProposeWildEncounterOnItinerary_TestUnknownEncounter_ExpectNone() -> None:
   itinerary = ItineraryBuilder.empty()
   start_time = '1:00 PM'
   duration_minutes = 45
   new_encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ) )
   itinerary_context = {
      'wild_encounter_coordinator': _WildEncounterDetailsStub( [] ),
   }

   proposed = FixedTimeItemLongWaitWarningBuilder.propose_wild_encounter_on_itinerary(
      itinerary,
      new_encounter,
      itinerary_context )

   assert proposed is None


def Test_ItemsFromItinerary_TestUnsupportedType_ExpectEmpty() -> None:
   itinerary = ItineraryBuilder.empty()
   item_type = ItinerarySaveIssueItemType.ANIMAL

   items = FixedTimeItemLongWaitWarningBuilder.items_from_itinerary(
      itinerary,
      item_type )

   assert items == []


def Test_ItemsFromValidated_TestUnsupportedType_ExpectEmpty() -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[] )
   item_type = ItinerarySaveIssueItemType.ANIMAL

   items = FixedTimeItemLongWaitWarningBuilder.items_from_validated(
      validated,
      item_type )

   assert items == []


def Test_OtherScheduledBlocks_TestActivityMissing_ExpectAllBlocks() -> None:
   duration_minutes = 30
   block_a = _time_block( 10 * 60, duration_minutes )
   block_b = _time_block( 12 * 60, duration_minutes )
   other = _time_block( 14 * 60, duration_minutes )
   scheduled_blocks = [ block_a, block_b ]

   other_blocks = FixedTimeItemLongWaitWarningBuilder._other_scheduled_blocks(
      scheduled_blocks,
      other )

   assert other_blocks == scheduled_blocks


def Test_IsolatedFixedTimeItems_TestDeletedAndUntimed_ExpectSkipped() -> None:
   start_time = '10:00 AM'
   duration_minutes = 30
   deleted = GuardiansTalkDiff(
      name='Deleted Talk',
      is_deleted=True,
      start_time=start_time,
      end_time=DateValues.add_minutes_to_time( start_time, duration_minutes ),
      location='Africa' )
   untimed = GuardiansTalkDiff(
      name='Untimed Talk',
      is_deleted=False,
      start_time=None,
      end_time=None,
      location='Africa' )
   blocks = [
      _time_block( 9 * 60, duration_minutes ),
      _time_block( 15 * 60, duration_minutes ),
   ]

   isolated = FixedTimeItemLongWaitWarningBuilder._isolated_fixed_time_items(
      [ deleted, untimed ],
      blocks )

   assert isolated == []
