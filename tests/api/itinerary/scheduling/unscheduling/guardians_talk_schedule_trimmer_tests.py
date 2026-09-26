from __future__ import annotations

import pytest

from api.itinerary.scheduling.unscheduling.guardians_talk_schedule_trimmer import GuardiansTalkScheduleTrimmer
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.calendar_dates import DateValues
from api.shared.enums.position import Position


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

   assert trimmed_talks[ Position.FIRST ].start_time == encounter.end_time
   assert trimmed_talks[ Position.FIRST ].end_time == talk.end_time


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

   assert trimmed_talks[ Position.FIRST ].start_time == first_talk.start_time
   assert trimmed_talks[ Position.FIRST ].end_time == first_talk.end_time
   assert trimmed_talks[ Position.SECOND ].start_time == first_talk.end_time
   assert trimmed_talks[ Position.SECOND ].end_time == second_talk.end_time


def Test_TrimRangeAgainstBlocker_TestBlockerCoversStart_ExpectShiftedStart() -> None:
   talk_start = DateValues.time_value_in_minutes( '1:30 PM' )
   talk_end = DateValues.time_value_in_minutes( '3:00 PM' )
   blocker_start = DateValues.time_value_in_minutes( '1:00 PM' )
   blocker_end = DateValues.time_value_in_minutes( '2:15 PM' )

   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=talk_start,
      end=talk_end,
      blocker_start=blocker_start,
      blocker_end=blocker_end )

   assert ( start, end ) == ( blocker_end, talk_end )


def Test_TrimRangeAgainstBlocker_TestBlockerCoversEnd_ExpectShiftedEnd() -> None:
   talk_start = DateValues.time_value_in_minutes( '1:30 PM' )
   talk_end = DateValues.time_value_in_minutes( '3:00 PM' )
   blocker_start = DateValues.time_value_in_minutes( '2:15 PM' )
   blocker_end = DateValues.time_value_in_minutes( '3:30 PM' )

   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=talk_start,
      end=talk_end,
      blocker_start=blocker_start,
      blocker_end=blocker_end )

   assert ( start, end ) == ( talk_start, blocker_start )


def Test_TrimRangeAgainstBlocker_TestNoOverlap_ExpectUnchanged() -> None:
   talk_start = DateValues.time_value_in_minutes( '1:30 PM' )
   talk_end = DateValues.time_value_in_minutes( '3:00 PM' )
   blocker_start = DateValues.time_value_in_minutes( '11:40 AM' )
   blocker_end = DateValues.time_value_in_minutes( '1:00 PM' )

   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=talk_start,
      end=talk_end,
      blocker_start=blocker_start,
      blocker_end=blocker_end )

   assert ( start, end ) == ( talk_start, talk_end )


def Test_TrimRangeAgainstBlocker_TestFullyCovered_ExpectValueError() -> None:
   talk_start = DateValues.time_value_in_minutes( '1:30 PM' )
   talk_end = DateValues.time_value_in_minutes( '3:00 PM' )
   blocker_start = DateValues.time_value_in_minutes( '1:00 PM' )
   blocker_end = DateValues.time_value_in_minutes( '3:30 PM' )

   with pytest.raises( ValueError ):
      GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
         start=talk_start,
         end=talk_end,
         blocker_start=blocker_start,
         blocker_end=blocker_end )


def Test_TrimRangeAgainstBlocker_TestInternalBlocker_ExpectShiftedToAfterBlocker() -> None:
   talk_start = DateValues.time_value_in_minutes( '1:30 PM' )
   talk_end = DateValues.time_value_in_minutes( '3:00 PM' )
   blocker_start = DateValues.time_value_in_minutes( '2:00 PM' )
   blocker_end = DateValues.time_value_in_minutes( '2:30 PM' )

   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=talk_start,
      end=talk_end,
      blocker_start=blocker_start,
      blocker_end=blocker_end )

   assert ( start, end ) == ( blocker_end, talk_end )


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
   talk_start = DateValues.time_value_in_minutes( '1:00 PM' )
   talk_end = DateValues.time_value_in_minutes( '3:00 PM' )
   blocker_start = DateValues.time_value_in_minutes( '1:30 PM' )
   blocker_end = DateValues.time_value_in_minutes( '2:00 PM' )

   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      talk_start,
      talk_end,
      blocker_start=blocker_start,
      blocker_end=blocker_end )

   assert ( start, end ) == ( blocker_end, talk_end )


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
   talk_start = DateValues.time_value_in_minutes( '1:30 PM' )
   talk_end = DateValues.time_value_in_minutes( '3:00 PM' )
   blocker_start = DateValues.time_value_in_minutes( '2:10 PM' )

   start, end = GuardiansTalkScheduleTrimmer.trim_range_against_blocker(
      start=talk_start,
      end=talk_end,
      blocker_start=blocker_start,
      blocker_end=talk_end )

   assert ( start, end ) == ( talk_start, blocker_start )
