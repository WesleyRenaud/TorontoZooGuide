from __future__ import annotations

from itinerary.support import schedule_itinerary_item, unschedule_itinerary_item

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.guardians_talk_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.scheduling.items.map_schedule_item_key_from_wire import map_schedule_item_key_from_wire
from api.itinerary.wild_encounter_item_key import WildEncounterScheduleItemKey
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

   assert schedule_itinerary_item( 'animals', ANIMAL_KEY ).success

   saved = fetch_saved_itinerary( db.conn )
   animal_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )

   assert animal_row.start_time is not None
   assert animal_row.end_time is not None

   assert unschedule_itinerary_item( 'animals', ANIMAL_KEY ).success

   saved = fetch_saved_itinerary( db.conn )
   animal_row = next(
      row for row in saved.animal_rows
      if row.species == 'African Lion' and row.exhibit == 'Africa Savanna' )

   assert animal_row.start_time is None
   assert animal_row.end_time is None


def test_unschedule_itinerary_attraction_clears_times(
      db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert schedule_itinerary_item(
      'attractions',
      CAROUSEL ).success

   saved = fetch_saved_itinerary( db.conn )
   attraction_row = next(
      row for row in saved.attraction_rows if row.attraction == CAROUSEL )

   assert attraction_row.start_time is not None
   assert attraction_row.end_time is not None

   assert unschedule_itinerary_item(
      'attractions',
      CAROUSEL ).success

   saved = fetch_saved_itinerary( db.conn )
   attraction_row = next(
      row for row in saved.attraction_rows if row.attraction == CAROUSEL )

   assert attraction_row.start_time is None
   assert attraction_row.end_time is None


def test_unschedule_itinerary_event_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert schedule_itinerary_item( 'lunch', '' ).success

   saved = fetch_saved_itinerary( db.conn )

   assert len( saved.event_rows ) == 1

   assert unschedule_itinerary_item( 'lunch', '' ).success

   saved = fetch_saved_itinerary( db.conn )

   assert len( saved.event_rows ) == 0


def test_set_arrival_time_none_clears_arrival_time( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time == '9:30 AM'

   assert ItineraryCoordinator.set_arrival_time( None ).success

   itinerary = ItineraryCoordinator.get_itinerary()

   assert itinerary.arrival_time is None
   assert itinerary.departure_time == '5:00 PM'


def test_map_schedule_item_key_from_wire_guardians_and_wild_kinds() -> None:
   guardians_key = map_schedule_item_key_from_wire(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      'Gorilla Guardians' )

   assert guardians_key == GuardiansTalkScheduleItemKey( name='Gorilla Guardians' )

   wild_key = map_schedule_item_key_from_wire(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      'African Rainforest||14:00' )

   assert wild_key == WildEncounterScheduleItemKey(
      name='African Rainforest',
      start_time='2:00 PM' )
