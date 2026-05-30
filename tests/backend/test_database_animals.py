from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.controllers.animal_controller import AnimalController
from api.exhibits.controllers.exhibit_controller import ExhibitController
from api.types import Cursor
from conftest import DbControllers


def test_get_animals_viewable_on_day_returns_animals_from_seeded_database( db: DbControllers ) -> None:
   animals = AnimalController.get_animals_viewable_on_day( day=15, month='June', year=2026, temp=22 )

   assert animals
   assert all( animal.species for animal in animals )
   assert all( animal.likelihood > 0 for animal in animals )


def test_get_animals_viewable_on_day_filters_by_exhibit( db: DbControllers ) -> None:
   animals = AnimalController.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      exhibits_to_include=[ 'Africa Savanna' ]
   )

   assert animals
   assert { animal.exhibit for animal in animals } == { 'Africa Savanna' }


def test_off_display_animals_are_excluded_or_included_by_flag(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   AnimalController.set_animal_as_off_display(
      species='African Lion',
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Lions are resting.'
   )

   without_closed = AnimalController.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=False
   )
   with_closed = AnimalController.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   assert all( animal.species != 'African Lion' for animal in without_closed )
   lion = next( animal for animal in with_closed if animal.species == 'African Lion' )
   assert lion.likelihood == 0
   assert lion.off_display_message == 'Lions are resting.'


def test_limited_viewing_and_alert_messages_are_returned(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AnimalController.set_animal_limited_viewing_schedule(
      species='African Penguin',
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      daily_start_time='09:00',
      daily_end_time='11:00',
      message='Morning viewing only.'
   )
   assert AnimalController.set_animal_viewing_alert(
      species='African Penguin',
      exhibit='Africa Savanna',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Penguins may be harder to spot.'
   )

   animals = AnimalController.get_animals_viewable_on_day( day=15, month='June', year=2026, temp=22 )
   penguin = next( animal for animal in animals if animal.species == 'African Penguin' )

   assert penguin.has_limited_viewing_schedule is True
   assert penguin.limited_viewing_message == 'Morning viewing only.'
   assert penguin.has_viewing_alert is True
   assert penguin.viewing_alert_message == 'Penguins may be harder to spot.'


def test_setting_animal_viewing_alert_twice_updates_existing_alert(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AnimalController.set_animal_viewing_alert(
      species='African Penguin',
      exhibit='Africa Savanna',
      alert_start_date='2026-06-01',
      alert_end_date='2026-06-30',
      message='Penguins may be harder to spot.'
   )
   assert AnimalController.set_animal_viewing_alert(
      species='African Penguin',
      exhibit='Africa Savanna',
      alert_start_date='2026-06-15',
      alert_end_date='2026-07-15',
      message='Penguin viewing has moved.'
   )

   alert_rows = cursor.execute(
      """ SELECT
             ALERT_MESSAGE,
             ALERT_START_DATE,
             ALERT_END_DATE
          FROM AnimalViewingAlert
          WHERE SPECIES = ?
          AND EXHIBIT = ?;
      """,
      ( 'African Penguin', 'Africa Savanna' )
   ).fetchall()
   animals = AnimalController.get_animals_viewable_on_day( day=15, month='June', year=2026, temp=22 )
   penguin = next( animal for animal in animals if animal.species == 'African Penguin' )

   assert len( alert_rows ) == 1
   assert dict( alert_rows[ 0 ] ) == {
      'ALERT_MESSAGE': 'Penguin viewing has moved.',
      'ALERT_START_DATE': '2026-06-15',
      'ALERT_END_DATE': '2026-07-15'
   }
   assert penguin.has_viewing_alert is True
   assert penguin.viewing_alert_message == 'Penguin viewing has moved.'


def test_exhibit_closure_sets_animal_likelihood_to_zero(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   ExhibitController.set_exhibit_as_closed(
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Savanna is closed.'
   )

   animals = AnimalController.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True,
      exhibits_to_include=[ 'Africa Savanna' ]
   )

   assert animals
   assert all( animal.likelihood == 0 for animal in animals )
   assert all( animal.off_display_message == 'Savanna is closed.' for animal in animals )


def test_animal_query_matches_species_not_exhibit( db: DbControllers ) -> None:
   species_matches = AnimalController.get_animals_matching_query(
      query='cheetah',
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   assert species_matches
   assert all(
      'cheetah' in ( animal.species or '' ).lower()
      for animal in species_matches
   )

   exhibit_matches = AnimalController.get_animals_matching_query(
      query='africa savanna',
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   assert exhibit_matches == []


def test_animal_query_helpers_dedupe_and_sort( db: DbControllers ) -> None:
   animals = AnimalController.get_animals_matching_query(
      query='african',
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   species_exhibits = [ ( animal.species, animal.exhibit ) for animal in animals ]

   assert species_exhibits == sorted(
      species_exhibits,
      key=lambda pair: ( pair[ 0 ].lower(), ( pair[ 1 ] or '' ).lower() ) )
   assert len( species_exhibits ) == len( set( species_exhibits ) )
   assert all(
      'african' in ( animal.species or '' ).lower()
      for animal in animals
   )


def test_animal_query_returns_same_species_in_multiple_exhibits( db: DbControllers ) -> None:
   animals = AnimalController.get_animals_matching_query(
      query='cheetah',
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True
   )

   exhibits = { animal.exhibit for animal in animals if animal.species == 'Cheetah' }

   assert exhibits == { 'Africa Savanna', 'Indo-Malaya Outdoor' }


def test_basic_animal_lookup_methods( db: DbControllers ) -> None:
   assert 'African Lion' in ExhibitController.get_names_of_animals_in_exhibit( 'Africa Savanna' )

   information = AnimalController.get_animal_information( 'African Lion' )

   assert information.species == 'African Lion'
   assert information.exhibit == 'Africa Savanna'
