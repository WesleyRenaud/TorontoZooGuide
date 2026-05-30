from __future__ import annotations

from dataclasses import dataclass

from ...models import Itinerary
from ...shared.date_values import DateValues
from ...types import ScheduleTimeKey


@dataclass( frozen=True )
class TimeBlock:
   start_minutes: int
   end_minutes: int


def time_block_from_schedule_times(
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> TimeBlock | None:
   start_minutes = DateValues.time_value_in_minutes( start_time )
   end_minutes = DateValues.time_value_in_minutes( end_time )

   if start_minutes is None or end_minutes is None:
      return None

   if end_minutes <= start_minutes:
      return None

   return TimeBlock(
      start_minutes=start_minutes,
      end_minutes=end_minutes )


def time_blocks_overlap(
      first: TimeBlock,
      second: TimeBlock ) -> bool:
   return (
      first.start_minutes < second.end_minutes
      and second.start_minutes < first.end_minutes
   )


def _append_block_from_schedule_times(
      blocks: list[ TimeBlock ],
      start_time: ScheduleTimeKey,
      end_time: ScheduleTimeKey ) -> None:
   block = time_block_from_schedule_times( start_time, end_time )

   if block is not None:
      blocks.append( block )


def collect_time_blocks_from_itinerary( itinerary: Itinerary ) -> list[ TimeBlock ]:
   blocks: list[ TimeBlock ] = []

   for animal in itinerary.animals:
      _append_block_from_schedule_times(
         blocks,
         animal.start_time,
         animal.end_time )

   for attraction in itinerary.attractions:
      _append_block_from_schedule_times(
         blocks,
         attraction.start_time,
         attraction.end_time )

   for event in itinerary.events:
      _append_block_from_schedule_times(
         blocks,
         event.start_time,
         event.end_time )

   for guardians_talk in itinerary.guardians_talks:
      if guardians_talk.is_deleted:
         continue

      _append_block_from_schedule_times(
         blocks,
         guardians_talk.start_time,
         guardians_talk.end_time )

   for wild_encounter in itinerary.wild_encounters:
      if wild_encounter.is_deleted:
         continue

      _append_block_from_schedule_times(
         blocks,
         wild_encounter.start_time,
         wild_encounter.end_time )

   return blocks
