from __future__ import annotations

from api.itinerary.scheduling.core.available_schedule_slot_finder import AvailableScheduleSlotFinder
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.shared.calendar_dates import DateValues
from api.shared.duration_values import DurationValues
from api.shared.enums.position import Position


def Test_FindBeforeOrAfterBounds_TestOpenBeforeWindow_ExpectBeforeSlot() -> None:
   blocker_start = '10:00 AM'
   blocker_duration_minutes = 30
   duration_minutes = 8
   day_start = '9:30 AM'
   day_end = '7:00 PM'
   blockers = [
      TimeBlock(
         start_seconds=DateValues.time_value_in_seconds( blocker_start ),
         end_seconds=DateValues.time_value_in_seconds( blocker_start )
            + DurationValues.minutes_to_seconds( blocker_duration_minutes ) ),
   ]

   slot = AvailableScheduleSlotFinder.find_before_or_after_bounds(
      blockers,
      DurationValues.minutes_to_seconds( duration_minutes ),
      day_start_seconds=DateValues.time_value_in_seconds( day_start ),
      day_end_seconds=DateValues.time_value_in_seconds( day_end ),
      before_end_seconds=DateValues.time_value_in_seconds( blocker_start ),
      after_start_seconds=DateValues.time_value_in_seconds( blocker_start )
         + DurationValues.minutes_to_seconds( blocker_duration_minutes ) )

   assert slot is not None
   assert slot[ Position.SECOND ] == DateValues.normalize_schedule_time( blocker_start )


def Test_FindBeforeOrAfterBounds_TestBeforeBlocked_ExpectAfterSlot() -> None:
   day_start = '9:30 AM'
   day_end = '7:00 PM'
   blocker_duration_minutes = 5
   duration_minutes = 8
   blockers = [
      TimeBlock(
         start_seconds=DateValues.time_value_in_seconds( day_start ),
         end_seconds=DateValues.time_value_in_seconds( day_start )
            + DurationValues.minutes_to_seconds( blocker_duration_minutes ) ),
   ]
   after_start_seconds = DateValues.time_value_in_seconds( day_start ) + DurationValues.minutes_to_seconds(
      blocker_duration_minutes )

   slot = AvailableScheduleSlotFinder.find_before_or_after_bounds(
      blockers,
      DurationValues.minutes_to_seconds( duration_minutes ),
      day_start_seconds=DateValues.time_value_in_seconds( day_start ),
      day_end_seconds=DateValues.time_value_in_seconds( day_end ),
      before_end_seconds=DateValues.time_value_in_seconds( day_start ),
      after_start_seconds=after_start_seconds )

   assert slot is not None
   assert slot[ Position.FIRST ] == DateValues.schedule_time_key_from_seconds(
      after_start_seconds )


def Test_FindBeforeOrAfterBounds_TestNoBlockers_ExpectVisitBoundSlot() -> None:
   duration_minutes = 8
   day_start = '9:30 AM'
   day_end = '7:00 PM'
   visit_end = '4:00 PM'
   visit_gap_minutes = 5

   slot = AvailableScheduleSlotFinder.find_before_or_after_bounds(
      [],
      DurationValues.minutes_to_seconds( duration_minutes ),
      day_start_seconds=DateValues.time_value_in_seconds( day_start ),
      day_end_seconds=DateValues.time_value_in_seconds( day_end ),
      before_end_seconds=DateValues.time_value_in_seconds( visit_end ),
      after_start_seconds=DateValues.time_value_in_seconds( visit_end )
         + DurationValues.minutes_to_seconds( visit_gap_minutes ) )

   assert slot is not None
   assert slot[ Position.SECOND ] == DateValues.normalize_schedule_time( visit_end )


def Test_FindNext_TestOverlappingBlockers_ExpectSlotAfterBlocker() -> None:
   day_start = '9:30 AM'
   day_end = '5:00 PM'
   blocker_duration_minutes = 8
   duration_minutes = 8
   blockers = [
      TimeBlock(
         start_seconds=DateValues.time_value_in_seconds( day_start ),
         end_seconds=DateValues.time_value_in_seconds( day_start )
            + DurationValues.minutes_to_seconds( blocker_duration_minutes ) ),
   ]
   slot_start_seconds = DateValues.time_value_in_seconds( day_start ) + DurationValues.minutes_to_seconds(
      blocker_duration_minutes )

   slot = AvailableScheduleSlotFinder.find_next(
      blockers,
      anchor_seconds=DateValues.time_value_in_seconds( day_start ),
      duration_seconds=DurationValues.minutes_to_seconds( duration_minutes ),
      day_end_seconds=DateValues.time_value_in_seconds( day_end ) )

   assert slot == (
      DateValues.schedule_time_key_from_seconds( slot_start_seconds ),
      DateValues.schedule_time_key_from_seconds(
         slot_start_seconds + DurationValues.minutes_to_seconds( duration_minutes ) ) )


def Test_FindNext_TestWindowTooShort_ExpectNone() -> None:
   day_start = '9:30 AM'
   duration_minutes = 8
   window_minutes = 5

   slot = AvailableScheduleSlotFinder.find_next(
      [],
      anchor_seconds=DateValues.time_value_in_seconds( day_start ),
      duration_seconds=DurationValues.minutes_to_seconds( duration_minutes ),
      day_end_seconds=DateValues.time_value_in_seconds( day_start )
         + DurationValues.minutes_to_seconds( window_minutes ) )

   assert slot is None


def Test_FindNext_TestAnchorAtDayEnd_ExpectNone() -> None:
   day_end = '5:00 PM'
   duration_minutes = 8

   slot = AvailableScheduleSlotFinder.find_next(
      [],
      anchor_seconds=DateValues.time_value_in_seconds( day_end ),
      duration_seconds=DurationValues.minutes_to_seconds( duration_minutes ),
      day_end_seconds=DateValues.time_value_in_seconds( day_end ) )

   assert slot is None


def Test_FindPrevious_TestFullyBlockedWindow_ExpectNone() -> None:
   day_start = '9:30 AM'
   blocked_until = '12:00 PM'
   duration_minutes = 8
   blockers = [
      TimeBlock(
         start_seconds=DateValues.time_value_in_seconds( day_start ),
         end_seconds=DateValues.time_value_in_seconds( blocked_until ) ),
   ]

   slot = AvailableScheduleSlotFinder.find_previous(
      blockers,
      end_before_seconds=DateValues.time_value_in_seconds( blocked_until ),
      duration_seconds=DurationValues.minutes_to_seconds( duration_minutes ),
      day_start_seconds=DateValues.time_value_in_seconds( day_start ) )

   assert slot is None
