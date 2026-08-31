from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.unscheduling.fixed_time_activity_unschedule_preparer import FixedTimeActivityUnschedulePreparer


def Test_OverlapsAnyTimeBlock_TestOverlappingTimes_ExpectTrue() -> None:
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert FixedTimeActivityUnschedulePreparer.overlaps_any_time_block(
      '10:15 AM',
      '10:45 AM',
      blocks )


def Test_OverlapsAnyTimeBlock_TestAdjacentTimes_ExpectFalse() -> None:
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert not FixedTimeActivityUnschedulePreparer.overlaps_any_time_block(
      '10:30 AM',
      '11:00 AM',
      blocks )


def Test_SavedItineraryHasOverlap_TestOverlappingAnimal_ExpectTrue() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=10 * 3600, end_seconds=10 * 3600 + 30 * 60 ),
   ]

   assert FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap( saved, blocks )


def Test_SavedItineraryHasOverlap_TestNoOverlap_ExpectFalse() -> None:
   saved = SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animal_rows=[
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=None,
            new_likelihood=100,
            start_time='10:00 AM',
            end_time='10:08 AM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=13 * 3600, end_seconds=13 * 3600 + 30 * 60 ),
   ]

   assert not FixedTimeActivityUnschedulePreparer.saved_itinerary_has_overlap( saved, blocks )
