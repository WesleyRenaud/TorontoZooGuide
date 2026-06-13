from __future__ import annotations

from collections.abc import Callable
from datetime import date

from database_console_support import get_animal
from database_console_support import get_animal_status_scopes
from database_console_support import get_animals_for_exhibit

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.shared.enums import AnimalViewingScope
from api.types import Cursor
from conftest import DbControllers


def test_set_animal_as_off_display_changes_visible_animal_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display( 'African Lion', 'Africa Savanna', '2026-06-01', '', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood == 0
   assert lion.off_display_message == 'The African Lion is temporarily off-display.'


def test_set_animal_as_on_display_restores_visible_animal_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AnimalCoordinator.set_animal_as_off_display(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Unavailable.' )

   assert AnimalCoordinator.set_animal_as_on_display( 'African Lion', 'Africa Savanna' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood > 0
   assert lion.off_display_message is None


def test_set_animal_as_off_display_can_scope_to_indoor_viewing(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Indoor unavailable.',
      viewing_scope=AnimalViewingScope.INDOOR )

   penguins = get_animals_for_exhibit( 'African Penguin', 'Africa Savanna' )

   indoor_penguin = next(
      penguin for penguin in penguins
      if penguin.enclosure_type == 'Indoor' )
   outdoor_penguin = next(
      penguin for penguin in penguins
      if penguin.enclosure_type == 'Outdoor' )

   assert indoor_penguin.likelihood == 0
   assert indoor_penguin.off_display_message == 'Indoor unavailable.'
   assert outdoor_penguin.likelihood > 0
   assert outdoor_penguin.off_display_message is None


def test_set_animal_as_off_display_replaces_matching_scopes(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'All unavailable.' )
   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Indoor unavailable.',
      viewing_scope=AnimalViewingScope.INDOOR )

   assert get_animal_status_scopes(
      cursor,
      'African Penguin',
      'Africa Savanna' ) == [ 'indoor' ]


def test_set_animal_as_on_display_can_scope_to_indoor_viewing(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'All unavailable.' )

   assert AnimalCoordinator.set_animal_as_on_display(
      'African Penguin',
      'Africa Savanna',
      viewing_scope=AnimalViewingScope.INDOOR )

   assert get_animal_status_scopes(
      cursor,
      'African Penguin',
      'Africa Savanna' ) == [ 'outdoor' ]


def test_set_animal_as_on_display_removes_matching_scoped_status(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Indoor unavailable.',
      viewing_scope=AnimalViewingScope.INDOOR )
   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Outdoor unavailable.',
      viewing_scope=AnimalViewingScope.OUTDOOR )

   assert AnimalCoordinator.set_animal_as_on_display(
      'African Penguin',
      'Africa Savanna',
      viewing_scope=AnimalViewingScope.INDOOR )

   assert get_animal_status_scopes(
      cursor,
      'African Penguin',
      'Africa Savanna' ) == [ 'outdoor' ]


def test_set_animal_as_off_display_rejects_missing_viewing_scope(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert not AnimalCoordinator.set_animal_as_off_display(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Indoor unavailable.',
      viewing_scope=AnimalViewingScope.INDOOR )
