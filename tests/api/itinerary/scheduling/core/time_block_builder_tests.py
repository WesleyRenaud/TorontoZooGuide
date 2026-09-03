from __future__ import annotations

from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.core.time_block_builder import TimeBlockBuilder
from api.models import Itinerary
from api.models import WildEncounter

def Test_Overlap_TestAdjacentBlocks_ExpectNoOverlap() -> None:
   first = TimeBlock( start_seconds=9 * 60 * 60, end_seconds=( 9 * 60 + 30 ) * 60 )
   second = TimeBlock( start_seconds=( 9 * 60 + 30 ) * 60, end_seconds=10 * 60 * 60 )

   assert not TimeBlockBuilder.overlap( first, second )


def Test_GapSeconds_TestNonOverlappingBlocks_ExpectGapEitherOrder() -> None:
   morning = TimeBlock( start_seconds=9 * 3600, end_seconds=9 * 3600 + 30 * 60 )
   afternoon = TimeBlock(
      start_seconds=11 * 3600,
      end_seconds=11 * 3600 + 30 * 60 )

   assert TimeBlockBuilder.gap_seconds( morning, afternoon ) == 90 * 60
   assert TimeBlockBuilder.gap_seconds( afternoon, morning ) == 90 * 60


def Test_GapSeconds_TestOverlappingBlocks_ExpectZero() -> None:
   first = TimeBlock( start_seconds=9 * 3600, end_seconds=10 * 3600 )
   second = TimeBlock( start_seconds=9 * 3600 + 30 * 60, end_seconds=10 * 3600 + 30 * 60 )

   assert TimeBlockBuilder.gap_seconds( first, second ) == 0


def Test_CollectFromItinerary_TestDeletedWildEncounter_ExpectSkipped() -> None:
   itinerary = Itinerary(
      date='2026-06-15',
      selected_exhibits=[],
      animals=[],
      attractions=[],
      transportations=[],
      transportation_stations=[],
      guardians_talks=[],
      wild_encounters=[
         WildEncounter(
            name='Kangaroo',
            meeting_spot='Gate',
            link='kangaroo',
            x_coord=0.0,
            y_coord=0.0,
            start_time='1:00 PM',
            end_time='1:45 PM',
            is_deleted=True ),
      ],
      events=[],
      arrival_time=None,
      departure_time=None )

   assert TimeBlockBuilder.collect_from_itinerary( itinerary ) == []
