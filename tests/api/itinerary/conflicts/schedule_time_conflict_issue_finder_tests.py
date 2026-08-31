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
