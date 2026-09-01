from __future__ import annotations

from api.itinerary.conflicts.schedule_time_conflict_issue_finder import ScheduleTimeConflictIssueFinder
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryErrorType


def Test_Find_TestOverlappingTalkAndEncounter_ExpectConflictIssue() -> None:
   talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:30 PM',
      location='Africa Savanna' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='12:15 PM',
      end_time='1:00 PM' )

   issues = ScheduleTimeConflictIssueFinder.find( [ talk ], [ encounter ] )

   assert len( issues ) == 1
   assert issues[ 0 ].code == ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT
   assert [ item.name for item in issues[ 0 ].items ] == [
      "Grevy's Zebra",
      'African Rainforest',
   ]


def Test_Find_TestNonOverlapping_ExpectEmpty() -> None:
   talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=False,
      start_time='10:00 AM',
      end_time='10:30 AM' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM' )

   assert ScheduleTimeConflictIssueFinder.find( [ talk ], [ encounter ] ) == []


def Test_Find_TestDeletedOrUntimed_ExpectIgnored() -> None:
   talk = GuardiansTalkDiff(
      name="Grevy's Zebra",
      is_deleted=True,
      start_time='12:00 PM',
      end_time='12:30 PM' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='12:00 PM',
      end_time='12:45 PM' )

   assert ScheduleTimeConflictIssueFinder.find( [ talk ], [ encounter ] ) == []


def Test_Find_TestGroupedMutualOverlap_ExpectSingleConflictGroup() -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:30 PM',
      location='Africa Savanna' )
   rainforest = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:45 PM',
      meeting_spot='Wild Encounter - Africa Meeting Spot' )
   kangaroo = WildEncounterDiff(
      name='Kangaroo',
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:45 PM',
      meeting_spot='Wild Encounter - Eurasia Meeting Spot' )

   issues = ScheduleTimeConflictIssueFinder.find(
      [ talk ],
      [ rainforest, kangaroo ] )

   assert len( issues ) == 1
   assert issues[ 0 ].code == ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT
   assert { item.name for item in issues[ 0 ].items } == {
      'African Lion',
      'African Rainforest',
      'Kangaroo',
   }


def Test_Find_TestOverlappingEncountersOnly_ExpectConflictIssue() -> None:
   rainforest = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM',
      meeting_spot='Wild Encounter - Africa Meeting Spot' )
   kangaroo = WildEncounterDiff(
      name='Kangaroo',
      is_deleted=False,
      start_time='2:30 PM',
      end_time='3:15 PM',
      meeting_spot='Wild Encounter - Eurasia Meeting Spot' )

   issues = ScheduleTimeConflictIssueFinder.find( [], [ rainforest, kangaroo ] )

   assert len( issues ) == 1
   assert { item.name for item in issues[ 0 ].items } == {
      'African Rainforest',
      'Kangaroo',
   }


def Test_Find_TestPartialTalkEncounterOverlap_ExpectConflictIssue() -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='1:30 PM',
      end_time='2:00 PM',
      location='Africa Savanna' )
   encounter = WildEncounterDiff(
      name='Grizzly Bear',
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:45 PM',
      meeting_spot='Wild Encounter - Americas Meeting Spot' )

   issues = ScheduleTimeConflictIssueFinder.find( [ talk ], [ encounter ] )

   assert len( issues ) == 1
   assert issues[ 0 ].code == ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT
   assert { item.name for item in issues[ 0 ].items } == {
      'African Lion',
      'Grizzly Bear',
   }


def Test_Find_TestTurtleTalkRhinoEncounterAt1400_ExpectConflictIssue() -> None:
   talk = GuardiansTalkDiff(
      name='Nile Soft-Shelled Turtle',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:30 PM',
      location='African Rainforest Pavilion' )
   encounter = WildEncounterDiff(
      name='Guardians of White Rhinos',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM',
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      link='https://example.com/rhino' )

   issues = ScheduleTimeConflictIssueFinder.find( [ talk ], [ encounter ] )

   assert len( issues ) == 1
   assert issues[ 0 ].code == ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT
   assert { item.name for item in issues[ 0 ].items } == {
      'Nile Soft-Shelled Turtle',
      'Guardians of White Rhinos',
   }


def Test_Find_TestLionTalkRainforestEncounter_ExpectIssueDict() -> None:
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:30 PM',
      location='Africa Savanna' )
   encounter = WildEncounterDiff(
      name='African Rainforest',
      is_deleted=False,
      start_time='2:00 PM',
      end_time='2:45 PM',
      meeting_spot='Wild Encounter - Africa Meeting Spot',
      link='https://www.torontozoo.com/tickets/weafricarainforest' )

   issues = ScheduleTimeConflictIssueFinder.find( [ talk ], [ encounter ] )

   assert [ issue.to_dict() for issue in issues ] == [
      {
         'code': 'wildEncounterTimeConflict',
         'items': [
            {
               'name': 'African Lion',
               'start_time': '2:00 PM',
               'end_time': '2:30 PM',
               'item_type': 'guardiansTalk',
               'meeting_spot': '',
               'location': 'Africa Savanna',
               'link': '',
            },
            {
               'name': 'African Rainforest',
               'start_time': '2:00 PM',
               'end_time': '2:45 PM',
               'item_type': 'wildEncounter',
               'meeting_spot': 'Wild Encounter - Africa Meeting Spot',
               'location': '',
               'link': 'https://www.torontozoo.com/tickets/weafricarainforest',
            },
         ],
      },
   ]
