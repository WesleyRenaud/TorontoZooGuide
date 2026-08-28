from __future__ import annotations

from typing import Any

from ...data_access.validated_itinerary import ValidatedItinerary
from ....models import Itinerary
from ....shared.calendar_dates import DateValues
from .time_block import TimeBlock
from ....types import Types


class TimeBlockBuilder():
   @classmethod
   def from_seconds(
         cls,
         start_seconds: int,
         end_seconds: int ) -> TimeBlock | None:
      if start_seconds < 0 or end_seconds <= start_seconds:
         return None

      return TimeBlock(
         start_seconds=start_seconds,
         end_seconds=end_seconds )


   @classmethod
   def from_schedule_times(
         cls,
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> TimeBlock | None:
      start_seconds = DateValues.time_value_in_seconds( start_time )
      end_seconds = DateValues.time_value_in_seconds( end_time )

      if start_seconds is None or end_seconds is None:
         return None

      return cls.from_seconds( start_seconds, end_seconds )


   @classmethod
   def overlap(
         cls,
         first: TimeBlock,
         second: TimeBlock ) -> bool:
      return (
         first.start_seconds < second.end_seconds
         and second.start_seconds < first.end_seconds
      )


   @classmethod
   def gap_seconds(
         cls,
         first: TimeBlock,
         second: TimeBlock ) -> int:
      if cls.overlap( first, second ):
         return 0

      if first.end_seconds <= second.start_seconds:
         return second.start_seconds - first.end_seconds

      return first.start_seconds - second.end_seconds


   @classmethod
   def append_from_schedule_times(
         cls,
         blocks: list[ TimeBlock ],
         start_time: Types.ScheduleTimeKey,
         end_time: Types.ScheduleTimeKey ) -> None:
      block = cls.from_schedule_times( start_time, end_time )

      if block is not None:
         blocks.append( block )


   @classmethod
   def collect_from_itinerary( cls, itinerary: Itinerary ) -> list[ TimeBlock ]:
      return cls._collect(
         animals=itinerary.animals,
         attractions=itinerary.attractions,
         transportations=itinerary.transportations,
         events=itinerary.events,
         guardians_talks=itinerary.guardians_talks,
         wild_encounters=itinerary.wild_encounters )


   @classmethod
   def earliest_start_seconds( cls, itinerary: Itinerary ) -> int | None:
      time_blocks = cls.collect_from_itinerary( itinerary )

      if not time_blocks:
         return None

      return min( time_block.start_seconds for time_block in time_blocks )


   @classmethod
   def latest_end_seconds( cls, itinerary: Itinerary ) -> int | None:
      time_blocks = cls.collect_from_itinerary( itinerary )

      if not time_blocks:
         return None

      return max( time_block.end_seconds for time_block in time_blocks )


   @classmethod
   def collect_from_validated_itinerary(
         cls,
         validated_itinerary: ValidatedItinerary ) -> list[ TimeBlock ]:
      return cls._collect(
         animals=validated_itinerary.animals,
         attractions=validated_itinerary.attractions,
         transportations=validated_itinerary.transportations,
         events=validated_itinerary.events,
         guardians_talks=validated_itinerary.guardians_talks,
         wild_encounters=validated_itinerary.wild_encounters )


   @classmethod
   def _collect(
         cls,
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

         cls.append_from_schedule_times(
            blocks,
            animal.start_time,
            animal.end_time )

      for attraction in attractions:
         cls.append_from_schedule_times(
            blocks,
            attraction.start_time,
            attraction.end_time )

      for transportation in transportations:
         cls.append_from_schedule_times(
            blocks,
            transportation.start_time,
            transportation.end_time )

      for event in events:
         cls.append_from_schedule_times(
            blocks,
            event.start_time,
            event.end_time )

      for item in guardians_talks:
         if getattr( item, 'is_deleted', False ):
            continue

         cls.append_from_schedule_times(
            blocks,
            item.start_time,
            item.end_time )

      for item in wild_encounters:
         if getattr( item, 'is_deleted', False ):
            continue

         cls.append_from_schedule_times(
            blocks,
            item.start_time,
            item.end_time )

      return blocks
