from __future__ import annotations

from api.itinerary.scheduling.core.available_schedule_slot_finder import AvailableScheduleSlotFinder
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.shared.calendar_dates import DateValues


def Test_FindBeforeOrAfterBounds_TestOpenBeforeWindow_ExpectBeforeSlot() -> None:
   blockers = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   slot = AvailableScheduleSlotFinder.find_before_or_after_bounds(
      blockers,
      8 * 60,
      day_start_seconds=9 * 3600 + 30 * 60,
      day_end_seconds=19 * 3600,
      before_end_seconds=10 * 3600,
      after_start_seconds=10 * 3600 + 30 * 60 )

   assert slot is not None
   assert slot[ 1 ] == DateValues.schedule_time_key_from_seconds( 10 * 3600 )


def Test_FindBeforeOrAfterBounds_TestBeforeBlocked_ExpectAfterSlot() -> None:
   blockers = [
      TimeBlock(
         start_seconds=9 * 3600 + 30 * 60,
         end_seconds=9 * 3600 + 35 * 60 ),
   ]

   slot = AvailableScheduleSlotFinder.find_before_or_after_bounds(
      blockers,
      8 * 60,
      day_start_seconds=9 * 3600 + 30 * 60,
      day_end_seconds=19 * 3600,
      before_end_seconds=9 * 3600 + 30 * 60,
      after_start_seconds=9 * 3600 + 35 * 60 )

   assert slot is not None
   assert slot[ 0 ] == DateValues.schedule_time_key_from_seconds(
      9 * 3600 + 35 * 60 )


def Test_FindBeforeOrAfterBounds_TestNoBlockers_ExpectVisitBoundSlot() -> None:
   slot = AvailableScheduleSlotFinder.find_before_or_after_bounds(
      [],
      8 * 60,
      day_start_seconds=9 * 3600 + 30 * 60,
      day_end_seconds=19 * 3600,
      before_end_seconds=16 * 3600,
      after_start_seconds=16 * 3600 + 5 * 60 )

   assert slot is not None
   assert slot[ 1 ] == DateValues.schedule_time_key_from_seconds( 16 * 3600 )


def Test_FindNext_TestOverlappingBlockers_ExpectSlotAfterBlocker() -> None:
   blockers = [
      TimeBlock(
         start_seconds=9 * 3600 + 30 * 60,
         end_seconds=9 * 3600 + 38 * 60 ),
   ]

   slot = AvailableScheduleSlotFinder.find_next(
      blockers,
      anchor_seconds=9 * 3600 + 30 * 60,
      duration_seconds=8 * 60,
      day_end_seconds=17 * 3600 )

   assert slot == ( '9:38 AM', '9:46 AM' )


def Test_FindNext_TestWindowTooShort_ExpectNone() -> None:
   assert AvailableScheduleSlotFinder.find_next(
      [],
      anchor_seconds=9 * 3600 + 30 * 60,
      duration_seconds=8 * 60,
      day_end_seconds=9 * 3600 + 35 * 60,
   ) is None
