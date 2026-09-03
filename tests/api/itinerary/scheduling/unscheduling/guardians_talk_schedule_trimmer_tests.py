from __future__ import annotations

import pytest

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


def Test_TrimRangeAgainstBlocker_TestNoOverlap_ExpectUnchanged() -> None:
   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=810,
      end=900,
      blocker_start=700,
      blocker_end=780 )

   assert ( start, end ) == ( 810, 900 )


def Test_TrimRangeAgainstBlocker_TestFullyCovered_ExpectValueError() -> None:
   with pytest.raises( ValueError ):
      GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
         start=810,
         end=900,
         blocker_start=780,
         blocker_end=930 )


def Test_TrimRangeAgainstBlocker_TestInternalBlocker_ExpectShiftedToAfterBlocker() -> None:
   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=810,
      end=900,
      blocker_start=840,
      blocker_end=870 )

   assert ( start, end ) == ( 870, 900 )


def Test_TrimTimes_TestFullyConsumed_ExpectNoRemainingTimeError() -> None:
   encounter = WildEncounterDiff(
      name='Grizzly Bear',
      is_deleted=False,
      start_time='1:00 PM',
      end_time='2:00 PM',
      meeting_spot='Spot',
      link='' )

   with pytest.raises( ValueError ):
      GuardiansTalkScheduleTrimmer.trim_times(
         '1:15 PM',
         '1:45 PM',
         [ encounter ] )


def Test_Apply_TestDeletedTalk_ExpectPassthrough() -> None:
   deleted_talk = GuardiansTalkDiff(
      name='African Lion',
      is_deleted=True,
      start_time='1:30 PM',
      end_time='2:00 PM',
      location='Africa Savanna' )

   trimmed_talks = GuardiansTalkScheduleTrimmer.apply( [ deleted_talk ], [] )

   assert trimmed_talks == [ deleted_talk ]


def Test_TrimRangeAgainstBlocker_TestMiddleOverlap_ExpectLaterSegment() -> None:
   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      780,
      900,
      blocker_start=810,
      blocker_end=840 )

   assert ( start, end ) == ( 840, 900 )


def Test_TrimTimes_TestEmptyRangeAfterTrim_ExpectNoRemainingTimeError(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      GuardiansTalkScheduleTrimmer,
      'trim_range_against_blocker',
      lambda start, end, blocker_start, blocker_end: ( end, end ) )

   encounter = WildEncounterDiff(
      name='Grizzly Bear',
      is_deleted=False,
      start_time='1:00 PM',
      end_time='1:45 PM',
      meeting_spot='Spot',
      link='' )

   with pytest.raises( ValueError ):
      GuardiansTalkScheduleTrimmer.trim_times(
         '1:30 PM',
         '2:00 PM',
         [ encounter ] )


def Test_TrimRangeAgainstBlocker_TestBlockerEndsAtTalkEnd_ExpectEarlierSegment() -> None:
   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=810,
      end=900,
      blocker_start=850,
      blocker_end=900 )

   assert ( start, end ) == ( 810, 850 )
