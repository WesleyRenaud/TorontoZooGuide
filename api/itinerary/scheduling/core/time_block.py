from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ...data_access.validated_itinerary import ValidatedItinerary
from ....models import Itinerary
from ....shared.calendar_dates import DateValues
from ....types import ScheduleTimeKey


@dataclass( frozen=True )
class TimeBlock:
   start_seconds: int
   end_seconds: int


def time_block_from_seconds(
      start_seconds: int,
      end_seconds: int ) -> TimeBlock | None:
   if start_seconds < 0 or end_seconds <= start_seconds:
      return None

   return TimeBlock(
      start_seconds=start_seconds,
      end_seconds=end_seconds )


def time_block_from_schedule_times(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> TimeBlock | None:
   start_seconds = DateValues.time_value_in_seconds( start_time )
   end_seconds = DateValues.time_value_in_seconds( end_time )

   if start_seconds is None or end_seconds is None:
      return None

   return time_block_from_seconds( start_seconds, end_seconds )


def time_blocks_overlap(
      first: TimeBlock,
      second: TimeBlock ) -> bool:
   return (
      first.start_seconds < second.end_seconds
      and second.start_seconds < first.end_seconds
   )


def time_block_gap_seconds(
      first: TimeBlock,
      second: TimeBlock ) -> int:
   if time_blocks_overlap( first, second ):
      return 0

   if first.end_seconds <= second.start_seconds:
      return second.start_seconds - first.end_seconds

   return first.start_seconds - second.end_seconds


def append_block_from_schedule_times(
      blocks: list[ TimeBlock ],
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> None:
   block = time_block_from_schedule_times( start_time, end_time )

   if block is not None:
      blocks.append( block )


def collect_time_blocks_from_itinerary( itinerary: Itinerary ) -> list[ TimeBlock ]:
   return _collect_time_blocks(
      animals=itinerary.animals,
      attractions=itinerary.attractions,
      transportations=itinerary.transportations,
      events=itinerary.events,
      guardians_talks=itinerary.guardians_talks,
      wild_encounters=itinerary.wild_encounters )


def earliest_scheduled_start_seconds( itinerary: Itinerary ) -> int | None:
   time_blocks = collect_time_blocks_from_itinerary( itinerary )

   if not time_blocks:
      return None

   return min( time_block.start_seconds for time_block in time_blocks )


def latest_scheduled_end_seconds( itinerary: Itinerary ) -> int | None:
   time_blocks = collect_time_blocks_from_itinerary( itinerary )

   if not time_blocks:
      return None

   return max( time_block.end_seconds for time_block in time_blocks )


def collect_time_blocks_from_validated_itinerary(
      validated_itinerary: ValidatedItinerary ) -> list[ TimeBlock ]:
   return _collect_time_blocks(
      animals=validated_itinerary.animals,
      attractions=validated_itinerary.attractions,
      transportations=validated_itinerary.transportations,
      events=validated_itinerary.events,
      guardians_talks=validated_itinerary.guardians_talks,
      wild_encounters=validated_itinerary.wild_encounters )


def _collect_time_blocks(
      *,
      animals: list[ Any ],
      attractions: list[ Any ],
      transportations: list[ Any ],
      events: list[ Any ],
      guardians_talks: list[ Any ],
      wild_encounters: list[ Any ] ) -> list[ TimeBlock ]:
   blocks: list[ TimeBlock ] = []

   for animal in animals:
      if getattr( animal, 'covered_by_talk', False ):
         continue

      append_block_from_schedule_times(
         blocks,
         animal.start_time,
         animal.end_time )

   for attraction in attractions:
      append_block_from_schedule_times(
         blocks,
         attraction.start_time,
         attraction.end_time )

   for transportation in transportations:
      append_block_from_schedule_times(
         blocks,
         transportation.start_time,
         transportation.end_time )

   for event in events:
      append_block_from_schedule_times(
         blocks,
         event.start_time,
         event.end_time )

   for item in guardians_talks:
      if getattr( item, 'is_deleted', False ):
         continue

      append_block_from_schedule_times(
         blocks,
         item.start_time,
         item.end_time )

   for item in wild_encounters:
      if getattr( item, 'is_deleted', False ):
         continue

      append_block_from_schedule_times(
         blocks,
         item.start_time,
         item.end_time )

   return blocks
