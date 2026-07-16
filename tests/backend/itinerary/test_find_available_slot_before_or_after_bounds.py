from __future__ import annotations

from api.itinerary.scheduling.core.find_next_available_slot import find_available_slot_before_or_after_bounds
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.shared.calendar_dates import DateValues


def test_find_available_slot_before_or_after_bounds_prefers_before() -> None:
   blockers = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   slot = find_available_slot_before_or_after_bounds(
      blockers,
      8 * 60,
      day_start_seconds=9 * 3600 + 30 * 60,
      day_end_seconds=19 * 3600,
      before_end_seconds=10 * 3600,
      after_start_seconds=10 * 3600 + 30 * 60 )

   assert slot is not None
   assert slot[ 1 ] == DateValues.schedule_time_key_from_seconds( 10 * 3600 )


def test_find_available_slot_before_or_after_bounds_uses_after_when_before_does_not_fit() -> None:
   blockers = [
      TimeBlock(
         start_seconds=9 * 3600 + 30 * 60,
         end_seconds=9 * 3600 + 35 * 60 ),
   ]

   slot = find_available_slot_before_or_after_bounds(
      blockers,
      8 * 60,
      day_start_seconds=9 * 3600 + 30 * 60,
      day_end_seconds=19 * 3600,
      before_end_seconds=9 * 3600 + 30 * 60,
      after_start_seconds=9 * 3600 + 35 * 60 )

   assert slot is not None
   assert slot[ 0 ] == DateValues.schedule_time_key_from_seconds(
      9 * 3600 + 35 * 60 )


def test_find_available_slot_before_or_after_bounds_uses_visit_bounds_when_empty() -> None:
   slot = find_available_slot_before_or_after_bounds(
      [],
      8 * 60,
      day_start_seconds=9 * 3600 + 30 * 60,
      day_end_seconds=19 * 3600,
      before_end_seconds=16 * 3600,
      after_start_seconds=16 * 3600 + 5 * 60 )

   assert slot is not None
   assert slot[ 1 ] == DateValues.schedule_time_key_from_seconds( 16 * 3600 )
