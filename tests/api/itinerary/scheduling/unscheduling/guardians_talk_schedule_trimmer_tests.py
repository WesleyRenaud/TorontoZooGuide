from __future__ import annotations

from api.itinerary.scheduling.unscheduling.guardians_talk_schedule_trimmer import GuardiansTalkScheduleTrimmer
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff


def Test_Apply_TestWildEncounterBlocker_ExpectTalkShiftedAfterEncounter() -> None:
   encounter = WildEncounterDiff(
      name='Grizzly Bear',
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:45 PM',
      meeting_spot='Spot',
      link='' )
   talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='1:30 PM',
      end_time='2:00 PM',
      location='Africa Savanna' )

   trimmed_talks = GuardiansTalkScheduleTrimmer.apply( [ talk ], [ encounter ] )

   assert trimmed_talks[ 0 ].start_time == '1:45 PM'
   assert trimmed_talks[ 0 ].end_time == '2:00 PM'


def Test_Apply_TestEarlierTalkPrecedence_ExpectLaterTalkShifted() -> None:
   first_talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=False,
      start_time='1:30 PM',
      end_time='2:00 PM',
      location='Africa Savanna' )
   second_talk = GuardiansTalkDiff(
      name='Amur Tiger',
      is_deleted=False,
      start_time='1:45 PM',
      end_time='2:15 PM',
      location='Eurasia Wilds' )

   trimmed_talks = GuardiansTalkScheduleTrimmer.apply(
      [ first_talk, second_talk ],
      [],
   )

   assert trimmed_talks[ 0 ].start_time == '1:30 PM'
   assert trimmed_talks[ 0 ].end_time == '2:00 PM'
   assert trimmed_talks[ 1 ].start_time == '2:00 PM'
   assert trimmed_talks[ 1 ].end_time == '2:15 PM'


def Test_TrimRangeAgainstBlocker_TestBlockerCoversStart_ExpectShiftedStart() -> None:
   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=810,
      end=900,
      blocker_start=780,
      blocker_end=855 )

   assert ( start, end ) == ( 855, 900 )


def Test_TrimRangeAgainstBlocker_TestBlockerCoversEnd_ExpectShiftedEnd() -> None:
   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=810,
      end=900,
      blocker_start=855,
      blocker_end=930 )

   assert ( start, end ) == ( 810, 855 )
