from __future__ import annotations

from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.warnings.fixed_time_item_long_wait_warning_builder import FixedTimeItemLongWaitWarningBuilder
from api.models import Animal
from api.models import GuardiansTalk
from api.models.animal_diff import AnimalDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItinerarySaveIssueItemType


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
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
   )

   assert FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items( validated )


def Test_HasUnscheduledListedItems_TestAllScheduled_ExpectFalse() -> None:
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
   )

   assert not FixedTimeItemLongWaitWarningBuilder.has_unscheduled_listed_items( validated )


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
         name="Grevy's Zebra",
         location='Africa Savanna',
         x_coord=0.0,
         y_coord=0.0,
         start_time='10:15 AM',
         end_time='10:45 AM' ),
      GuardiansTalk(
         name='Slender-Tailed Meerkat',
         location='African Rainforest Pavilion',
         x_coord=0.0,
         y_coord=0.0,
         start_time='1:00 PM',
         end_time='1:30 PM' ),
   ]

   isolated = FixedTimeItemLongWaitWarningBuilder.isolated_from_itinerary(
      itinerary,
      ItinerarySaveIssueItemType.GUARDIANS_TALK )

   assert [ talk.name for talk in isolated ] == [ 'Slender-Tailed Meerkat' ]


def Test_BuildGuardiansTalkIssueFromTalks_TestTalks_ExpectLongWaitIssue() -> None:
   issue = FixedTimeItemLongWaitWarningBuilder.build_guardians_talk_issue_from_talks(
      [
         GuardiansTalkDiff(
            name="Grevy's Zebra",
            is_deleted=False,
            start_time='1:00 PM',
            end_time='1:30 PM',
            location='Africa Savanna' ),
      ] )

   assert issue.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in issue.items ] == [ "Grevy's Zebra" ]


def Test_BuildWildEncounterIssueFromEncounters_TestEncounters_ExpectLongWaitIssue() -> None:
   issue = FixedTimeItemLongWaitWarningBuilder.build_wild_encounter_issue_from_encounters(
      [
         WildEncounterDiff(
            name='African Rainforest',
            is_deleted=False,
            start_time='1:00 PM',
            end_time='1:45 PM' ),
      ] )

   assert issue.code == ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   assert [ item.name for item in issue.items ] == [ 'African Rainforest' ]
