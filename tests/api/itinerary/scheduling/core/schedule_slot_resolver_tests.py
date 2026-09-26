from __future__ import annotations

from api.itinerary.scheduling.core.schedule_slot_resolver import ScheduleSlotResolver
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.shared.calendar_dates import DateValues
from api.shared.duration_values import DurationValues


ANCHOR_TIME = '9:30 AM'
DAY_END_TIME = '5:00 PM'
DURATION_MINUTES = 8
ANCHOR_SECONDS = DateValues.time_value_in_seconds( ANCHOR_TIME )
DAY_END_SECONDS = DateValues.time_value_in_seconds( DAY_END_TIME )
DURATION_SECONDS = DurationValues.minutes_to_seconds( DURATION_MINUTES )


def Test_Resolve_TestUnsetStartTime_ExpectAnchorSlot() -> None:
   slot = ScheduleSlotResolver.resolve(
      [],
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS )

   assert slot == (
      DateValues.normalize_schedule_time( ANCHOR_TIME ),
      DateValues.add_minutes_to_time( ANCHOR_TIME, DURATION_MINUTES ) )


def Test_Resolve_TestRequestedStartTime_ExpectRequestedSlot() -> None:
   requested_start = '10:00'
   blockers = [
      TimeBlock(
         start_seconds=ANCHOR_SECONDS,
         end_seconds=ANCHOR_SECONDS + DURATION_SECONDS ),
   ]

   slot = ScheduleSlotResolver.resolve(
      blockers,
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time=requested_start )

   assert slot == (
      DateValues.normalize_schedule_time( requested_start ),
      DateValues.add_minutes_to_time( requested_start, DURATION_MINUTES ) )


def Test_Resolve_TestOverlappingRequestedSlot_ExpectNone() -> None:
   requested_start = '10:00'
   blockers = [
      TimeBlock(
         start_seconds=DateValues.time_value_in_seconds( requested_start ),
         end_seconds=DateValues.time_value_in_seconds( requested_start )
            + DURATION_SECONDS ),
   ]

   slot = ScheduleSlotResolver.resolve(
      blockers,
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time=requested_start )

   assert slot is None


def Test_Resolve_TestBlankStartTime_ExpectNone() -> None:
   slot = ScheduleSlotResolver.resolve(
      [],
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time='' )

   assert slot is None
