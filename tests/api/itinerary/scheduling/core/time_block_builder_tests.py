from __future__ import annotations

from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.core.time_block_builder import TimeBlockBuilder


def Test_Overlap_TestAdjacentBlocks_ExpectNoOverlap() -> None:
   first = TimeBlock( start_seconds=9 * 60 * 60, end_seconds=( 9 * 60 + 30 ) * 60 )
   second = TimeBlock( start_seconds=( 9 * 60 + 30 ) * 60, end_seconds=10 * 60 * 60 )

   assert not TimeBlockBuilder.overlap( first, second )
