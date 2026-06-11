from __future__ import annotations

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.logic.parse_schedule_item_request import parse_schedule_item_request
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers

ANIMAL_KEY = 'African Lion||Africa Savanna'
CAROUSEL = 'Conservation Carousel'


def _set_base_itinerary( db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success


def test_unschedule_itinerary_animal_clears_times_but_keeps_row(
      db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert ItineraryCoordinator.schedule_itinerary_item( 'animals', ANIMAL_KEY ).success

   saved = fetch_saved_itinerary( db.conn )
   animal_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )

   assert animal_row.start_time is not None
   assert animal_row.end_time is not None

   assert ItineraryCoordinator.unschedule_itinerary_item( 'animals', ANIMAL_KEY ).success

   saved = fetch_saved_itinerary( db.conn )
   animal_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )

   assert animal_row.start_time is None
   assert animal_row.end_time is None


def test_unschedule_itinerary_attraction_clears_times(
      db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert ItineraryCoordinator.schedule_itinerary_item(
      'attractions',
      CAROUSEL ).success

   saved = fetch_saved_itinerary( db.conn )
   attraction_row = next(
      row for row in saved.attraction_rows if row.attraction == CAROUSEL )

   assert attraction_row.start_time is not None
   assert attraction_row.end_time is not None

   assert ItineraryCoordinator.unschedule_itinerary_item(
      'attractions',
      CAROUSEL ).success

   saved = fetch_saved_itinerary( db.conn )
   attraction_row = next(
      row for row in saved.attraction_rows if row.attraction == CAROUSEL )

   assert attraction_row.start_time is None
   assert attraction_row.end_time is None


def test_unschedule_itinerary_event_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert ItineraryCoordinator.schedule_itinerary_item( 'lunch', '' ).success

   saved = fetch_saved_itinerary( db.conn )

   assert len( saved.event_rows ) == 1

   assert ItineraryCoordinator.unschedule_itinerary_item( 'lunch', '' ).success

   saved = fetch_saved_itinerary( db.conn )

   assert len( saved.event_rows ) == 0


def test_set_arrival_time_none_clears_arrival_time( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time == '09:30'

   assert ItineraryCoordinator.set_arrival_time( None ).success

   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time is None
   assert itinerary.departure_time == '17:00'


def test_parse_schedule_item_request_guardians_and_wild_kinds() -> None:
   parsed_guardians = parse_schedule_item_request(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      'Gorilla Guardians' )

   assert parsed_guardians is not None
   assert parsed_guardians.kind == ScheduleItemKind.GUARDIANS_TALK
   assert parsed_guardians.talk_name == 'Gorilla Guardians'

   parsed_wild = parse_schedule_item_request(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      'African Rainforest' )

   assert parsed_wild is not None
   assert parsed_wild.kind == ScheduleItemKind.WILD_ENCOUNTER
   assert parsed_wild.wild_encounter_name == 'African Rainforest'
