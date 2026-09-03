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
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType

ZEBRA_TALK = "Grevy's Zebra"
MEERKAT_TALK = 'Slender-Tailed Meerkat'
RAINFOREST_ENCOUNTER = 'African Rainforest'
CAROUSEL = 'Conservation Carousel'
ZOOMOBILE = 'Zoomobile'
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


def Test_TimeBlockIsIsolated_TestFarNeighbor_ExpectTrue() -> None:
   activity = TimeBlock( start_seconds=13 * 3600, end_seconds=13 * 3600 + 30 * 60 )
   neighbors = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 8 * 60 ),
   ]

   assert FixedTimeItemLongWaitWarningBuilder.time_block_is_isolated(
      activity,
      neighbors )


def Test_TimeBlockIsIsolated_TestNearNeighbor_ExpectFalse() -> None:
   activity = TimeBlock( start_seconds=10 * 3600 + 15 * 60, end_seconds=10 * 3600 + 45 * 60 )
   neighbors = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 8 * 60 ),
   ]

   assert not FixedTimeItemLongWaitWarningBuilder.time_block_is_isolated(
      activity,
      neighbors )


def Test_TimeBlockIsIsolated_TestNoNeighbors_ExpectFalse() -> None:
   activity = TimeBlock( start_seconds=13 * 3600, end_seconds=13 * 3600 + 30 * 60 )

   assert not FixedTimeItemLongWaitWarningBuilder.time_block_is_isolated( activity, [] )


def Test_HasUnscheduledListedItems_TestMissingAnimalTimes_ExpectTrue() -> None:
   validated = _validated(
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100 ),
      ] )

   assert FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items( validated )


def Test_HasUnscheduledListedItems_TestAllScheduled_ExpectFalse() -> None:
   validated = _validated(
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ] )

   assert not FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items( validated )


def Test_HasUnscheduledListedItems_TestMissingAttractionTimes_ExpectTrue() -> None:
   validated = _validated(
      attractions=[
         AttractionDiff(
            name=CAROUSEL,
            old_likelihood=None,
            new_likelihood=3 ),
      ] )

   assert FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items( validated )


def Test_HasUnscheduledListedItems_TestMissingTransportationTimes_ExpectTrue() -> None:
   validated = _validated(
      transportations=[
         TransportationDiff(
            name=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True ),
      ] )

   assert FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items( validated )


def Test_IsolatedFromItinerary_TestFarTalk_ExpectIsolated() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='10:15 AM',
         end_time='10:45 AM' ),
      GuardiansTalk(
         name=MEERKAT_TALK,
         location='African Rainforest Pavilion',
         x_coord=0.0,
         y_coord=0.0,
         start_time='1:00 PM',
         end_time='1:30 PM' ),
   ]

   isolated = FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.GUARDIANS_TALK )

   assert [ talk.name for talk in isolated ] == [ MEERKAT_TALK ]


def Test_IsolatedFromItinerary_TestFarWildEncounter_ExpectIsolated() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.wild_encounters = [
      WildEncounter(
         name=RAINFOREST_ENCOUNTER,
         meeting_spot=MEETING_SPOT,
         link='african-rainforest',
         x_coord=0.0,
         y_coord=0.0,
         start_time='1:00 PM',
         end_time='1:45 PM' ),
   ]

   isolated = FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.WILD_ENCOUNTER )

   assert [ encounter.name for encounter in isolated ] == [ RAINFOREST_ENCOUNTER ]


def Test_IsolatedFromItinerary_TestDeletedTalk_ExpectSkipped() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=MEERKAT_TALK,
         location='African Rainforest Pavilion',
         x_coord=0.0,
         y_coord=0.0,
         start_time='1:00 PM',
         end_time='1:30 PM',
         is_deleted=True ),
   ]

   assert FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.GUARDIANS_TALK ) == []


def Test_BuildGuardiansTalkIssueFromTalks_TestTalks_ExpectLongWaitIssue() -> None:
   issue = FixedTimeItemLongWaitWarningBuilder.build_guardians_talk_issue_from_talks(
      [
         GuardiansTalkDiff(
            name=ZEBRA_TALK,
            is_deleted=False,
            start_time='1:00 PM',
            end_time='1:30 PM',
            location='Africa Savanna' ),
      ] )

   assert issue.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in issue.items ] == [ ZEBRA_TALK ]


def Test_BuildWildEncounterIssueFromEncounters_TestEncounters_ExpectLongWaitIssue() -> None:
   issue = FixedTimeItemLongWaitWarningBuilder.build_wild_encounter_issue_from_encounters(
      [
         WildEncounterDiff(
            name=RAINFOREST_ENCOUNTER,
            is_deleted=False,
            start_time='1:00 PM',
            end_time='1:45 PM' ),
      ] )

   assert issue.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in issue.items ] == [ RAINFOREST_ENCOUNTER ]


def Test_BuildIssueItem_TestUnsupportedType_ExpectValueError() -> None:
   with pytest.raises( ValueError, match='Unsupported fixed-time long-wait item type' ):
      FixedTimeItemLongWaitWarningBuilder.build_issue_item(
         ItinerarySaveIssueItemType.ANIMAL,
         GuardiansTalkDiff(
            name=ZEBRA_TALK,
            is_deleted=False,
            start_time='1:00 PM',
            end_time='1:30 PM' ) )


def Test_ReasonsFromItinerary_TestIsolatedTalk_ExpectLongWaitReason() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='10:15 AM',
         end_time='10:45 AM' ),
      GuardiansTalk(
         name=MEERKAT_TALK,
         location='African Rainforest Pavilion',
         x_coord=0.0,
         y_coord=0.0,
         start_time='1:00 PM',
         end_time='1:30 PM' ),
   ]

   reasons = FixedTimeItemLongWaitWarningBuilder.reasons_from_itinerary( itinerary )

   assert len( reasons ) == 1
   assert reasons[ 0 ].code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert { item.name for item in reasons[ 0 ].items } == { MEERKAT_TALK }


def Test_ReasonsFromItinerary_TestNoIsolatedItems_ExpectEmptyReasons() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   itinerary.guardians_talks = [
      GuardiansTalk(
         name=ZEBRA_TALK,
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='10:15 AM',
         end_time='10:45 AM' ),
   ]

   assert FixedTimeItemLongWaitWarningBuilder.reasons_from_itinerary( itinerary ) == []


def Test_IsIsolatedAfterAdding_TestFarFromSchedule_ExpectTrue() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   new_talk = GuardiansTalkDiff(
      name=MEERKAT_TALK,
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:30 PM' )

   assert FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding(
      itinerary,
      new_talk )


def Test_IsIsolatedAfterAdding_TestNearSchedule_ExpectFalse() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   new_talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='10:15 AM',
      end_time='10:45 AM' )

   assert not FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding(
      itinerary,
      new_talk )


def Test_IsIsolatedAfterAdding_TestUntimedItem_ExpectFalse() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.animals = [
      Animal(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM' ),
   ]
   new_talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time=None,
      end_time=None )

   assert not FixedTimeItemLongWaitWarningBuilder.is_isolated_after_adding(
      itinerary,
      new_talk )


def Test_FilterNewlyAddedItems_TestNewTalk_ExpectTalk() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   assert FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
      saved,
      [ talk ],
      ItinerarySaveIssueItemType.GUARDIANS_TALK ) == [ talk ]


def Test_FilterNewlyAddedItems_TestAlreadySavedTalk_ExpectEmpty() -> None:
   talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      guardians_talk_rows=[
         ItineraryGuardiansTalkRecord(
            talk_name=ZEBRA_TALK,
            start_time='12:00 PM',
            end_time='12:30 PM',
            is_deleted=False ),
      ],
   )

   assert FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
      saved,
      [ talk ],
      ItinerarySaveIssueItemType.GUARDIANS_TALK ) == []


def Test_FilterNewlyAddedItems_TestNewWildEncounter_ExpectEncounter() -> None:
   encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:45 PM' )
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      wild_encounter_rows=[],
   )

   assert FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
      saved,
      [ encounter ],
      ItinerarySaveIssueItemType.WILD_ENCOUNTER ) == [ encounter ]


def Test_FilterNewlyAddedItems_TestUnsupportedType_ExpectEmpty() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
   )

   assert FixedTimeItemLongWaitWarningBuilder.filter_newly_added_items(
      saved,
      [],
      ItinerarySaveIssueItemType.ANIMAL ) == []


def Test_ProposeGuardiansTalkOnItinerary_TestKnownTalk_ExpectProposedItinerary() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.date = '2026-06-15'
   detail = GuardiansTalk(
      name=ZEBRA_TALK,
      location='Africa Savanna',
      x_coord=11.0,
      y_coord=22.0,
      maximum_duration=30 )

   class GuardiansCoordinatorStub:
      @staticmethod
      def get_guardians_talk_details( names: list[ str ] ) -> list[ GuardiansTalk ]:
         return [ detail ] if names == [ ZEBRA_TALK ] else []

   new_talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )

   proposed = FixedTimeItemLongWaitWarningBuilder.propose_guardians_talk_on_itinerary(
      itinerary,
      new_talk,
      { 'guardians_coordinator': GuardiansCoordinatorStub } )

   assert proposed is not None
   assert len( proposed.guardians_talks ) == 1
   talk = proposed.guardians_talks[ 0 ]
   assert talk.name == ZEBRA_TALK
   assert talk.location == 'Africa Savanna'
   assert talk.x_coord == 11.0
   assert talk.y_coord == 22.0
   assert talk.start_time == '12:00 PM'
   assert talk.end_time == '12:30 PM'


def Test_ProposeGuardiansTalkOnItinerary_TestUnknownTalk_ExpectNone() -> None:
   itinerary = ItineraryBuilder.empty()

   class GuardiansCoordinatorStub:
      @staticmethod
      def get_guardians_talk_details( names: list[ str ] ) -> list[ GuardiansTalk ]:
         return []

   new_talk = GuardiansTalkDiff(
      name=ZEBRA_TALK,
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM' )

   assert FixedTimeItemLongWaitWarningBuilder.propose_guardians_talk_on_itinerary(
      itinerary,
      new_talk,
      { 'guardians_coordinator': GuardiansCoordinatorStub } ) is None


def Test_ProposeWildEncounterOnItinerary_TestKnownEncounter_ExpectProposedItinerary() -> None:
   itinerary = ItineraryBuilder.empty()
   itinerary.date = '2026-06-15'
   detail = WildEncounter(
      name=RAINFOREST_ENCOUNTER,
      meeting_spot=MEETING_SPOT,
      link='african-rainforest',
      x_coord=33.0,
      y_coord=44.0,
      maximum_duration=45 )

   class WildEncounterCoordinatorStub:
      @staticmethod
      def get_wild_encounter_details( names: list[ str ] ) -> list[ WildEncounter ]:
         return [ detail ] if names == [ RAINFOREST_ENCOUNTER ] else []

   new_encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:45 PM' )

   proposed = FixedTimeItemLongWaitWarningBuilder.propose_wild_encounter_on_itinerary(
      itinerary,
      new_encounter,
      { 'wild_encounter_coordinator': WildEncounterCoordinatorStub } )

   assert proposed is not None
   assert len( proposed.wild_encounters ) == 1
   encounter = proposed.wild_encounters[ 0 ]
   assert encounter.name == RAINFOREST_ENCOUNTER
   assert encounter.meeting_spot == MEETING_SPOT
   assert encounter.link == 'african-rainforest'
   assert encounter.x_coord == 33.0
   assert encounter.y_coord == 44.0
   assert encounter.start_time == '1:00 PM'
   assert encounter.end_time == '1:45 PM'


def Test_ProposeWildEncounterOnItinerary_TestUnknownEncounter_ExpectNone() -> None:
   itinerary = ItineraryBuilder.empty()

   class WildEncounterCoordinatorStub:
      @staticmethod
      def get_wild_encounter_details( names: list[ str ] ) -> list[ WildEncounter ]:
         return []

   new_encounter = WildEncounterDiff(
      name=RAINFOREST_ENCOUNTER,
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:45 PM' )

   assert FixedTimeItemLongWaitWarningBuilder.propose_wild_encounter_on_itinerary(
      itinerary,
      new_encounter,
      { 'wild_encounter_coordinator': WildEncounterCoordinatorStub } ) is None


def Test_ItemsFromItinerary_TestUnsupportedType_ExpectEmpty() -> None:
   itinerary = ItineraryBuilder.empty()

   assert FixedTimeItemLongWaitWarningBuilder.items_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.ANIMAL ) == []


def Test_ItemsFromValidated_TestUnsupportedType_ExpectEmpty() -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[] )

   assert FixedTimeItemLongWaitWarningBuilder.items_from_validated(
      validated,
      ItinerarySaveIssueItemType.ANIMAL ) == []


def Test_OtherScheduledBlocks_TestActivityMissing_ExpectAllBlocks() -> None:
   block_a = TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 )
   block_b = TimeBlock( start_seconds=12 * 3600, end_seconds=12 * 3600 + 30 * 60 )
   other = TimeBlock( start_seconds=14 * 3600, end_seconds=14 * 3600 + 30 * 60 )

   assert FixedTimeItemLongWaitWarningBuilder._other_scheduled_blocks(
      [ block_a, block_b ],
      other ) == [ block_a, block_b ]


def Test_IsolatedFixedTimeItems_TestDeletedAndUntimed_ExpectSkipped() -> None:
   deleted = GuardiansTalkDiff(
      name='Deleted Talk',
      is_deleted=True,
      start_time='10:00 AM',
      end_time='10:30 AM',
      location='Africa' )
   untimed = GuardiansTalkDiff(
      name='Untimed Talk',
      is_deleted=False,
      start_time=None,
      end_time=None,
      location='Africa' )
   blocks = [
      TimeBlock( start_seconds=9 * 3600, end_seconds=9 * 3600 + 30 * 60 ),
      TimeBlock( start_seconds=15 * 3600, end_seconds=15 * 3600 + 30 * 60 ),
   ]

   assert FixedTimeItemLongWaitWarningBuilder._isolated_fixed_time_items(
      [ deleted, untimed ],
      blocks ) == []

