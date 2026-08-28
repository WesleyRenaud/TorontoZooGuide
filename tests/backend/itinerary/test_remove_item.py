from __future__ import annotations

from itinerary.support import CHEETAH_ITINERARY_ENTRY, CHEETAH_KEY, LION_ITINERARY_ENTRY, LION_KEY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, remove_itinerary_item, schedule_itinerary_item, schedule_time_after_seconds, wild_encounter_key, wild_encounter_wire
from wild_encounter_schedule_support import wire_schedule_row, wire_schedule_rows

from api.guardians.coordinators.guardians_coordinator import GuardiansCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver
from conftest import DbControllers

ANIMAL_KEY = 'African Lion||Africa Savanna'
CAROUSEL = 'Conservation Carousel'
GUARDIANS_TALK = 'African Lion'
AFRICAN_RAINFOREST = 'African Rainforest'
CHEETAH_START = schedule_time_after_seconds(
   '10:15 AM',
   WalkTravelTimeCalculator.seconds_between_nodes(
      load_walk_graph(),
      ViewingSpotWalkNodeIdResolver.resolve( 'African Lion', 'Africa Savanna', None ),
      ViewingSpotWalkNodeIdResolver.resolve( 'Cheetah', 'Africa Savanna', None ),
   ),
)
PENGUIN_START_WITH_15_MIN_GAP = schedule_time_after_seconds(
   schedule_time_after_seconds( CHEETAH_START, 15 * 60 ),
   15 * 60,
)


def _set_base_itinerary( db: DbControllers ) -> None:
   assert GuardiansCoordinator.set_guardians_talk_schedule(
      talk=GUARDIANS_TALK,
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      schedule_rows=wire_schedule_rows( '10:00', monday=True, tuesday=False, wednesday=False, thursday=False, friday=False, saturday=False, sunday=False ),
      message=None,
   )

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
      guardians_talks=[ {
         'name': GUARDIANS_TALK,
         'start_time': '10:00',
         'end_time': None,
      } ],
      wild_encounters=[ wild_encounter_key( AFRICAN_RAINFOREST ) ],
   ).success


def test_remove_itinerary_animal_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert remove_itinerary_item( 'animals', ANIMAL_KEY ).success

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )

   assert not any(
      row.species == 'African Lion' and row.exhibit == 'Africa Savanna'
      for row in saved.animal_rows )


def test_remove_itinerary_attraction_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert remove_itinerary_item(
      'attractions',
      CAROUSEL ).success

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )

   assert not any( row.attraction == CAROUSEL for row in saved.attraction_rows )


def test_remove_itinerary_guardians_talk_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert remove_itinerary_item(
      'guardians_talks',
      f'{ GUARDIANS_TALK }||10:00' ).success

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )

   assert not any( row.talk_name == GUARDIANS_TALK for row in saved.guardians_talk_rows )


def test_remove_itinerary_wild_encounter_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert remove_itinerary_item(
      'wild_encounters',
      wild_encounter_wire( AFRICAN_RAINFOREST ) ).success

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )

   assert not any(
      row.wild_encounter == AFRICAN_RAINFOREST
      for row in saved.wild_encounter_rows )


def test_remove_itinerary_event_deletes_row( db: DbControllers ) -> None:
   _set_base_itinerary( db )

   assert schedule_itinerary_item( 'lunch', '' ).success

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )

   assert len( saved.event_rows ) == 1

   assert remove_itinerary_item( 'lunch', '' ).success

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )

   assert len( saved.event_rows ) == 0


def test_remove_middle_animal_shifts_later_items_by_removed_duration(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      'animals',
      LION_KEY,
      start_time='10:00 AM',
      duration_minutes=15,
   ).success
   assert schedule_itinerary_item(
      'animals',
      CHEETAH_KEY,
      start_time=CHEETAH_START,
      duration_minutes=15,
   ).success
   assert schedule_itinerary_item(
      'animals',
      PENGUIN_KEY,
      start_time=PENGUIN_START_WITH_15_MIN_GAP,
      duration_minutes=15,
   ).success

   assert remove_itinerary_item( 'animals', CHEETAH_KEY ).success

   saved = ItineraryProvider.fetch_saved_itinerary( db.conn )
   animals_by_key = {
      ( row.species, row.exhibit, row.enclosure_name ): row
      for row in saved.animal_rows
   }

   lion = animals_by_key[ ( 'African Lion', 'Africa Savanna', None ) ]
   penguin = animals_by_key[ ( 'African Penguin', 'Africa Savanna', 'Outdoor' ) ]

   assert lion.start_time == '10:00 AM'
   assert lion.end_time == '10:15 AM'
   assert ( 'Cheetah', 'Africa Savanna', None ) not in animals_by_key
   assert penguin.start_time == '10:32 AM'
   assert penguin.end_time == '10:47 AM'
