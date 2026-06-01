from __future__ import annotations

from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from conftest import DbControllers

ANIMAL_KEY = 'African Lion||Africa Savanna'
CAROUSEL = 'Conservation Carousel'
GUARDIANS_TALK = 'African Lion'
AFRICAN_RAINFOREST = 'African Rainforest'


def _set_base_itinerary( db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
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
      guardians_talks=[ { 'name': GUARDIANS_TALK, 'start_time': None, 'end_time': None } ],
      wild_encounters=[ AFRICAN_RAINFOREST ],
   ).success


def test_remove_itinerary_animal_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert ItineraryController.remove_itinerary_item( 'animals', ANIMAL_KEY ).success

   saved = fetch_saved_itinerary( db.conn )

   assert not any(
      row.species == 'African Lion' and row.exhibit == 'Africa Savanna'
      for row in saved.animal_rows )


def test_remove_itinerary_attraction_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert ItineraryController.remove_itinerary_item(
      'attractions',
      CAROUSEL ).success

   saved = fetch_saved_itinerary( db.conn )

   assert not any( row.attraction == CAROUSEL for row in saved.attraction_rows )


def test_remove_itinerary_guardians_talk_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert ItineraryController.remove_itinerary_item(
      'guardians_talks',
      GUARDIANS_TALK ).success

   saved = fetch_saved_itinerary( db.conn )

   assert not any( row.talk_name == GUARDIANS_TALK for row in saved.guardians_talk_rows )


def test_remove_itinerary_wild_encounter_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert ItineraryController.remove_itinerary_item(
      'wild_encounters',
      AFRICAN_RAINFOREST ).success

   saved = fetch_saved_itinerary( db.conn )

   assert not any(
      row.wild_encounter == AFRICAN_RAINFOREST
      for row in saved.wild_encounter_rows )


def test_remove_itinerary_event_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert ItineraryController.schedule_itinerary_item( 'lunch', '' ).success

   saved = fetch_saved_itinerary( db.conn )

   assert len( saved.event_rows ) == 1

   assert ItineraryController.remove_itinerary_item( 'lunch', '' ).success

   saved = fetch_saved_itinerary( db.conn )

   assert len( saved.event_rows ) == 0
