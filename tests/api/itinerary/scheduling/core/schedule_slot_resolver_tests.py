from __future__ import annotations

from api.itinerary.scheduling.core.schedule_slot_resolver import ScheduleSlotResolver
from api.itinerary.scheduling.core.time_block import TimeBlock


ANCHOR_SECONDS = 9 * 3600 + 30 * 60
DAY_END_SECONDS = 17 * 3600
DURATION_SECONDS = 8 * 60


def Test_Resolve_TestUnsetStartTime_ExpectAnchorSlot() -> None:
   slot = ScheduleSlotResolver.resolve(
      [],
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS )

   assert slot == ( '9:30 AM', '9:38 AM' )


def Test_Resolve_TestRequestedStartTime_ExpectRequestedSlot() -> None:
   blockers = [
      TimeBlock(
         start_seconds=9 * 3600 + 30 * 60,
         end_seconds=9 * 3600 + 38 * 60 ),
   ]

   slot = ScheduleSlotResolver.resolve(
      blockers,
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time='10:00' )

   assert slot == ( '10:00 AM', '10:08 AM' )


def Test_Resolve_TestOverlappingRequestedSlot_ExpectNone() -> None:
   blockers = [
      TimeBlock(
         start_seconds=10 * 3600,
         end_seconds=10 * 3600 + 8 * 60 ),
   ]

   assert ScheduleSlotResolver.resolve(
      blockers,
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time='10:00',
   ) is None


def Test_Resolve_TestBlankStartTime_ExpectNone() -> None:
   assert ScheduleSlotResolver.resolve(
      [],
      anchor_seconds=ANCHOR_SECONDS,
      duration_seconds=DURATION_SECONDS,
      day_end_seconds=DAY_END_SECONDS,
      start_time='',
   ) is None
