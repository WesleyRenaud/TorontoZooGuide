from __future__ import annotations

from api.animals.search.viewing_spot_key_builder import ViewingSpotKeyBuilder
from api.guardians.data_access.guardians_talk_animal_provider import GuardiansTalkAnimalProvider
from api.guardians.scheduling.guardians_talk_loop_schedule_pin import resolve_guardians_talk_loop_pin
from api.guardians.scheduling.guardians_talk_loop_schedule_pin import viewing_spot_index_for_talk_in_loop
from api.itinerary.data_access.itinerary import fetch_itinerary_animal_rows
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.routing.itinerary_stop import ItineraryStop
from api.itinerary.routing.loop_schedule_pin import LoopSchedulePin
from api.itinerary.scheduling.bulk.guardians_talk_covered_animals import apply_covered_by_talk_schedules
from api.itinerary.scheduling.bulk.guardians_talk_covered_animals import restore_covered_animals_after_talk_removed
from api.itinerary.scheduling.bulk.guardians_talk_covered_animals import viewing_spot_keys_to_cover_for_loop_pins
from api.itinerary.scheduling.core.time_block import TimeBlock
from api.models import GuardiansTalk
from api.shared.enums import ScheduleItemKind
from api.walk_graph.domain.master_route_stop import is_animal_route_stop
from api.walk_graph.master_route import default_master_route_loop_by_id
from conftest import DbControllers


EXPECTED_TALK_ENCLOSURE_LINKS = {
   ( 'African Penguin', 'African Penguin' ): 'Outdoor',
   ( 'Aldabra Tortoise', 'Aldabra Tortoise' ): 'Outdoor',
   ( 'Babirusa', 'Babirusa' ): 'Outdoor',
   ( 'Masai Giraffe', 'Masai Giraffe' ): 'Outdoor',
   ( 'Western Lowland Gorilla', 'Western Lowland Gorilla' ): 'Indoor',
   ( 'Wood Bison', 'Wood Bison' ): 'Female Herd',
   ( 'North American River Otter', 'North American River Otter' ): 'Indoor',
   ( 'New World Primates', 'Golden Lion Tamarin' ): 'Indoor',
   ( 'New World Primates', 'Two-Toed Sloth' ): 'Indoor',
   ( 'New World Primates', 'White-Faced Saki' ): 'Indoor',
   ( 'African Lion', 'African Lion' ): None,
}


def _guardians_talk(
      *,
      name: str,
      location: str,
      start_time: str = '11:00 AM',
      end_time: str = '11:30 AM' ) -> GuardiansTalk:
   return GuardiansTalk(
      name=name,
      location=location,
      x_coord=0.0,
      y_coord=0.0,
      start_time=start_time,
      end_time=end_time )


def _talk_stop(
      *,
      name: str,
      start_time: str = '11:00 AM',
      end_time: str = '11:30 AM' ) -> ItineraryStop:
   return ItineraryStop(
      schedule_item_kind=ScheduleItemKind.GUARDIANS_TALK,
      item_key=name,
      walk_node_ids=( 'v-0001', ),
      is_fixed_time=True,
      start_time=start_time,
      end_time=end_time )


def _insert_itinerary_animal(
      db: DbControllers,
      *,
      species: str,
      exhibit: str,
      enclosure_name: str | None,
      covered_by_talk: bool = False,
      start_time: str | None = None,
      end_time: str | None = None ) -> None:
   assert db.conn is not None
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               IS_ADDED,
               COVERED_BY_TALK,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, NULL, 100, 0, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         enclosure_name,
         int( covered_by_talk ),
         start_time,
         end_time,
      ),
   )
   db.conn.commit()


def _viewing_spot_index(
      *,
      loop_id: str,
      species: str,
      exhibit: str,
      enclosure_name: str | None ) -> int:
   master_route_loop = default_master_route_loop_by_id()[ loop_id ]

   for index, viewing_spot in enumerate( master_route_loop.viewing_spots ):
      # Guardians-talk enclosure pins resolve against animal stops only.
      if not is_animal_route_stop( viewing_spot ):
         continue

      if (
            viewing_spot.species == species
            and viewing_spot.exhibit == exhibit
            and viewing_spot.name == enclosure_name ):
         return index

   raise AssertionError(
      'Viewing spot not found: %s / %s / %s'
      % ( repr( species ), repr( exhibit ), repr( enclosure_name ) )
   )


def test_seeded_guardians_talk_animal_enclosure_links( db: DbControllers ) -> None:
   assert db.conn is not None

   for ( talk_name, species ), enclosure_name in EXPECTED_TALK_ENCLOSURE_LINKS.items():
      links = GuardiansTalkAnimalProvider.fetch_animal_links( db.conn, talk_name )
      matching = [
         link
         for link in links
         if link.species == species
      ]

      assert matching, (
         'Missing link for %s / %s' % ( repr( talk_name ), repr( species ) )
      )
      assert matching[ 0 ].enclosure_name == enclosure_name


def test_resolve_pin_prefers_seeded_outdoor_penguin_enclosure(
      db: DbControllers ) -> None:
   loop_pin = resolve_guardians_talk_loop_pin(
      db.conn,
      _guardians_talk(
         name='African Penguin',
         location='Africa Savanna' ),
      _talk_stop( name='African Penguin' ) )

   assert loop_pin is not None
   assert loop_pin.loop_id == 'africa_savanna_canadian_domain'
   assert loop_pin.viewing_spot_index == _viewing_spot_index(
      loop_id='africa_savanna_canadian_domain',
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )

   indoor_index = _viewing_spot_index(
      loop_id='africa_savanna_canadian_domain',
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Indoor' )
   assert loop_pin.viewing_spot_index != indoor_index


def test_resolve_pin_prefers_seeded_indoor_gorilla_enclosure(
      db: DbControllers ) -> None:
   loop_pin = resolve_guardians_talk_loop_pin(
      db.conn,
      _guardians_talk(
         name='Western Lowland Gorilla',
         location='African Rainforest Pavilion' ),
      _talk_stop( name='Western Lowland Gorilla' ) )

   assert loop_pin is not None
   assert loop_pin.loop_id == 'african_rainforest_giraffe'
   assert loop_pin.viewing_spot_index == _viewing_spot_index(
      loop_id='african_rainforest_giraffe',
      species='Western Lowland Gorilla',
      exhibit='African Rainforest Pavilion',
      enclosure_name='Indoor' )


def test_resolve_pin_uses_null_enclosure_name_for_african_lion(
      db: DbControllers ) -> None:
   loop_pin = resolve_guardians_talk_loop_pin(
      db.conn,
      _guardians_talk(
         name='African Lion',
         location='Africa Savanna' ),
      _talk_stop( name='African Lion' ) )

   assert loop_pin is not None
   assert loop_pin.viewing_spot_index == _viewing_spot_index(
      loop_id='africa_savanna_canadian_domain',
      species='African Lion',
      exhibit='Africa Savanna',
      enclosure_name=None )


def test_cover_keys_only_match_seeded_penguin_enclosure(
      db: DbControllers ) -> None:
   assert db.conn is not None

   animal_rows = [
      ItineraryAnimalRecord(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Indoor',
         new_likelihood=100 ),
      ItineraryAnimalRecord(
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor',
         new_likelihood=100 ),
   ]
   loop_pin = LoopSchedulePin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=_viewing_spot_index(
         loop_id='africa_savanna_canadian_domain',
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor' ),
      stop=_talk_stop( name='African Penguin' ),
      start_seconds=11 * 3600,
      end_seconds=11 * 3600 + 30 * 60 )

   covered = viewing_spot_keys_to_cover_for_loop_pins(
      db.conn,
      [ loop_pin ],
      animal_rows )

   assert set( covered ) == {
      ViewingSpotKeyBuilder.from_values(
         'African Penguin',
         'Africa Savanna',
         'Outdoor' ),
   }


def test_apply_and_uncover_penguin_outdoor_leaves_indoor_untouched(
      db: DbControllers ) -> None:
   assert db.conn is not None

   _insert_itinerary_animal(
      db,
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Indoor' )
   _insert_itinerary_animal(
      db,
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )

   loop_pin = LoopSchedulePin(
      loop_id='africa_savanna_canadian_domain',
      viewing_spot_index=_viewing_spot_index(
         loop_id='africa_savanna_canadian_domain',
         species='African Penguin',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor' ),
      stop=_talk_stop( name='African Penguin' ),
      start_seconds=11 * 3600,
      end_seconds=11 * 3600 + 30 * 60 )
   covered = viewing_spot_keys_to_cover_for_loop_pins(
      db.conn,
      [ loop_pin ],
      fetch_itinerary_animal_rows( db.conn ) )

   apply_covered_by_talk_schedules( db.conn, covered )
   rows_by_enclosure = {
      row.enclosure_name: row
      for row in fetch_itinerary_animal_rows( db.conn )
   }

   assert rows_by_enclosure[ 'Outdoor' ].covered_by_talk is True
   assert rows_by_enclosure[ 'Outdoor' ].start_time == '11:00 AM'
   assert rows_by_enclosure[ 'Outdoor' ].end_time == '11:30 AM'
   assert rows_by_enclosure[ 'Indoor' ].covered_by_talk is False
   assert rows_by_enclosure[ 'Indoor' ].start_time is None

   cur = db.conn.cursor()

   try:
      restored = restore_covered_animals_after_talk_removed(
         cur,
         db.conn,
         talk_name='African Penguin',
         talk_block=TimeBlock(
            start_seconds=11 * 3600,
            end_seconds=11 * 3600 + 30 * 60 ),
         animal_rows=fetch_itinerary_animal_rows( db.conn ) )
      db.conn.commit()
   finally:
      cur.close()

   assert len( restored.animals ) == 1
   assert restored.animals[ 0 ].enclosure_name == 'Outdoor'
   assert restored.replacement_end_seconds == 11 * 3600 + 5 * 60

   rows_by_enclosure = {
      row.enclosure_name: row
      for row in fetch_itinerary_animal_rows( db.conn )
   }

   assert rows_by_enclosure[ 'Outdoor' ].covered_by_talk is False
   assert rows_by_enclosure[ 'Outdoor' ].start_time == '11:00 AM'
   assert rows_by_enclosure[ 'Outdoor' ].end_time == '11:05 AM'
   assert rows_by_enclosure[ 'Indoor' ].covered_by_talk is False


def test_viewing_spot_index_for_talk_uses_linked_enclosure_before_talk_name_match(
      db: DbControllers ) -> None:
   assert db.conn is not None
   links = GuardiansTalkAnimalProvider.fetch_animal_links( db.conn, 'African Penguin' )
   master_route_loop = default_master_route_loop_by_id()[
      'africa_savanna_canadian_domain'
   ]

   index = viewing_spot_index_for_talk_in_loop(
      master_route_loop,
      talk_name='African Penguin',
      talk_location='Africa Savanna',
      linked_animals=links )

   assert index == _viewing_spot_index(
      loop_id='africa_savanna_canadian_domain',
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )
