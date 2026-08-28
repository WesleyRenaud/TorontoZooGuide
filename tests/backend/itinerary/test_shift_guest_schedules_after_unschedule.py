from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.itinerary.scheduling.unscheduling.guest_schedule_shift_applier import GuestScheduleShiftApplier
from api.shared.enums import ItineraryEventType


def test_shifted_schedule_times_moves_block_earlier() -> None:
   shifted = GuestScheduleShiftApplier.shifted_schedule_times( '10:45 AM', '11:00 AM', -15 * 60 )

   assert shifted == ( '10:30 AM', '10:45 AM' )


def test_shifted_schedule_times_returns_none_for_invalid_shift() -> None:
   assert GuestScheduleShiftApplier.shifted_schedule_times( '10:00 AM', '10:15 AM', -11 * 3600 ) is None


def test_resolve_unscheduled_item_time_block_for_animal() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      animal_rows=(
         ItineraryAnimalRecord(
            species='Masai Giraffe',
            exhibit='Africa Savanna',
            start_time='10:15 AM',
            end_time='10:30 AM',
         ),
      ),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
   )

   block = GuestScheduleShiftApplier.resolve_unscheduled_item_time_block(
      saved_itinerary,
      AnimalScheduleItemKey(
         species='Masai Giraffe',
         exhibit='Africa Savanna',
      ),
   )

   assert block == TimeBlock(
      start_seconds=10 * 3600 + 15 * 60,
      end_seconds=10 * 3600 + 30 * 60,
   )


def test_resolve_unscheduled_item_time_block_for_attraction() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(
         ItineraryAttractionRecord(
            attraction='Conservation Carousel',
            old_likelihood=None,
            new_likelihood=None,
            start_time='1:00 PM',
            end_time='1:15 PM',
         ),
      ),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
   )

   block = GuestScheduleShiftApplier.resolve_unscheduled_item_time_block(
      saved_itinerary,
      AttractionScheduleItemKey( name='Conservation Carousel' ),
   )

   assert block == TimeBlock(
      start_seconds=13 * 3600,
      end_seconds=13 * 3600 + 15 * 60,
   )


def test_resolve_unscheduled_item_time_block_for_event() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
      event_rows=(
         ItineraryEventRecord(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM',
         ),
      ),
   )

   block = GuestScheduleShiftApplier.resolve_unscheduled_item_time_block(
      saved_itinerary,
      ItineraryEventType.LUNCH,
   )

   assert block == TimeBlock(
      start_seconds=12 * 3600,
      end_seconds=12 * 3600 + 30 * 60,
   )
