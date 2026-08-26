from __future__ import annotations

from api.itinerary.animal_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_attraction_record import ItineraryAttractionRecord
from api.itinerary.data_access.itinerary_event_record import ItineraryEventRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.itinerary_wild_encounter_record import ItineraryWildEncounterRecord
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.data_access.saved_itinerary_schedule_item_row_finder import SavedItineraryScheduleItemRowFinder
from api.itinerary.transportation_item_key import TransportationScheduleItemKey
from api.itinerary.wild_encounter_item_key import WildEncounterScheduleItemKey
from api.shared.enums import ItineraryEventType


def test_find_saved_itinerary_schedule_item_row_finds_animal_row() -> None:
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
   schedule_item_key = AnimalScheduleItemKey(
      species='Masai Giraffe',
      exhibit='Africa Savanna',
   )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      schedule_item_key )

   assert row is not None
   assert row.species == 'Masai Giraffe'


def test_find_saved_itinerary_schedule_item_row_finds_attraction_row() -> None:
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
         ),
      ),
      guardians_talk_rows=(),
      wild_encounter_rows=(),
   )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      AttractionScheduleItemKey( name='Conservation Carousel' ),
   )

   assert row is not None
   assert row.attraction == 'Conservation Carousel'


def test_find_saved_itinerary_schedule_item_row_finds_added_as_attraction_transportation_row() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      transportation_rows=(
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True ),
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False ),
      ),
   )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      AttractionScheduleItemKey( name='Zoomobile' ),
   )

   assert isinstance( row, ItineraryTransportationRecord )
   assert row.added_as_attraction is True


def test_find_saved_itinerary_schedule_item_row_ignores_pure_transportation_row() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      transportation_rows=(
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False ),
      ),
   )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      AttractionScheduleItemKey( name='Zoomobile' ),
   )

   assert row is None


def test_find_saved_itinerary_schedule_item_row_finds_pure_transportation_row() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      transportation_rows=(
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True ),
         ItineraryTransportationRecord(
            transportation='Zoomobile',
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False ),
      ),
   )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      TransportationScheduleItemKey(
         name='Zoomobile',
         added_as_attraction=False ),
   )

   assert isinstance( row, ItineraryTransportationRecord )
   assert row.added_as_attraction is False


def test_find_saved_itinerary_schedule_item_row_finds_event_row() -> None:
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

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      ItineraryEventType.LUNCH,
   )

   assert row is not None
   assert row.event_type == ItineraryEventType.LUNCH


def test_find_saved_itinerary_schedule_item_row_matches_wild_encounter_by_name_and_start() -> None:
   saved_itinerary = SavedItinerary(
      date_value='2026-06-15',
      arrival_time=None,
      departure_time=None,
      animal_rows=(),
      attraction_rows=(),
      guardians_talk_rows=(),
      wild_encounter_rows=(
         ItineraryWildEncounterRecord(
            wild_encounter='African Rainforest',
            start_time='3:30 PM',
            end_time='4:15 PM',
            is_deleted=False,
         ),
      ),
   )

   row = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      WildEncounterScheduleItemKey(
         name='African Rainforest',
         start_time='15:30',
      ),
   )

   assert row is not None
   assert row.wild_encounter == 'African Rainforest'
   assert row.end_time == '4:15 PM'

   missing = SavedItineraryScheduleItemRowFinder.find_saved_itinerary_schedule_item_row(
      saved_itinerary,
      WildEncounterScheduleItemKey(
         name='African Rainforest',
         start_time='14:00',
      ),
   )

   assert missing is None
