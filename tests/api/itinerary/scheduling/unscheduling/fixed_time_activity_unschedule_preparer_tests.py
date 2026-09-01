from __future__ import annotations

from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.unscheduling.fixed_time_activity_unschedule_preparer import FixedTimeActivityUnschedulePreparer
from api.models.animal_diff import AnimalDiff
from api.models.itinerary_event import ItineraryEvent
from api.shared.enums import ItineraryEventType


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


def Test_PrepareValidatedForReschedule_TestActivityBlocks_ExpectClearedGuestSchedules() -> None:
   validated = ValidatedItinerary(
      arrival_time='9:00 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species='African Lion',
            exhibit='Africa Savanna',
            old_likelihood=100,
            new_likelihood=100,
            start_time='2:30 PM',
            end_time='2:45 PM' ),
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
      ],
   )
   blocks = [
      TimeBlock( start_seconds=14 * 3600, end_seconds=14 * 3600 + 45 * 60 ),
   ]

   result = FixedTimeActivityUnschedulePreparer.prepare_validated_for_reschedule(
      validated,
      blocks )

   assert result.animals[ 0 ].start_time is None
   assert result.animals[ 0 ].end_time is None
   assert len( result.events ) == 1
