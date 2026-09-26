from __future__ import annotations

from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.core.time_block_builder import TimeBlockBuilder
from api.models import Itinerary
from api.models import WildEncounter
from api.shared.duration_values import DurationValues


def Test_Overlap_TestAdjacentBlocks_ExpectNoOverlap() -> None:
   morning_start_minutes = 9 * 60
   morning_duration_minutes = 30
   first = TimeBlock(
      start_seconds=DurationValues.minutes_to_seconds( morning_start_minutes ),
      end_seconds=DurationValues.minutes_to_seconds(
         morning_start_minutes + morning_duration_minutes ) )
   second = TimeBlock(
      start_seconds=first.end_seconds,
      end_seconds=DurationValues.minutes_to_seconds(
         morning_start_minutes + morning_duration_minutes + morning_duration_minutes ) )

   overlaps = TimeBlockBuilder.overlap( first, second )

   assert not overlaps


def Test_GapSeconds_TestNonOverlappingBlocks_ExpectGap() -> None:
   morning_start_minutes = 9 * 60
   morning_duration_minutes = 30
   afternoon_start_minutes = 11 * 60
   afternoon_duration_minutes = 30
   morning = TimeBlock(
      start_seconds=DurationValues.minutes_to_seconds( morning_start_minutes ),
      end_seconds=DurationValues.minutes_to_seconds(
         morning_start_minutes + morning_duration_minutes ) )
   afternoon = TimeBlock(
      start_seconds=DurationValues.minutes_to_seconds( afternoon_start_minutes ),
      end_seconds=DurationValues.minutes_to_seconds(
         afternoon_start_minutes + afternoon_duration_minutes ) )

   gap = TimeBlockBuilder.gap_seconds( morning, afternoon )

   assert gap == DurationValues.minutes_to_seconds(
      afternoon_start_minutes - ( morning_start_minutes + morning_duration_minutes ) )


def Test_GapSeconds_TestNonOverlappingBlocksReversed_ExpectSameGap() -> None:
   morning_start_minutes = 9 * 60
   morning_duration_minutes = 30
   afternoon_start_minutes = 11 * 60
   afternoon_duration_minutes = 30
   morning = TimeBlock(
      start_seconds=DurationValues.minutes_to_seconds( morning_start_minutes ),
      end_seconds=DurationValues.minutes_to_seconds(
         morning_start_minutes + morning_duration_minutes ) )
   afternoon = TimeBlock(
      start_seconds=DurationValues.minutes_to_seconds( afternoon_start_minutes ),
      end_seconds=DurationValues.minutes_to_seconds(
         afternoon_start_minutes + afternoon_duration_minutes ) )

   gap = TimeBlockBuilder.gap_seconds( afternoon, morning )

   assert gap == DurationValues.minutes_to_seconds(
      afternoon_start_minutes - ( morning_start_minutes + morning_duration_minutes ) )


def Test_GapSeconds_TestOverlappingBlocks_ExpectZero() -> None:
   first_start_minutes = 9 * 60
   first_duration_minutes = 60
   second_start_minutes = first_start_minutes + 30
   second_duration_minutes = 60
   first = TimeBlock(
      start_seconds=DurationValues.minutes_to_seconds( first_start_minutes ),
      end_seconds=DurationValues.minutes_to_seconds(
         first_start_minutes + first_duration_minutes ) )
   second = TimeBlock(
      start_seconds=DurationValues.minutes_to_seconds( second_start_minutes ),
      end_seconds=DurationValues.minutes_to_seconds(
         second_start_minutes + second_duration_minutes ) )

   gap = TimeBlockBuilder.gap_seconds( first, second )

   assert gap == 0


def Test_CollectFromItinerary_TestDeletedWildEncounter_ExpectSkipped() -> None:
   encounter = WildEncounter(
      name='Kangaroo',
      meeting_spot='Gate',
      link='kangaroo',
      x_coord=0.0,
      y_coord=0.0,
      start_time='1:00 PM',
      end_time='1:45 PM',
      is_deleted=True )
   itinerary = Itinerary(
      date='2026-06-15',
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[ encounter ],
      events=[],
      arrival_time=None,
      departure_time=None )

   blocks = TimeBlockBuilder.collect_from_itinerary( itinerary )

   assert blocks == []
