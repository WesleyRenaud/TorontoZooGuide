from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.constants import Constants
from conftest import DbControllers


def test_set_itinerary_persists_selected_exhibits(
      db: DbControllers ) -> None:
   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
   )

   assert result.success is True
   assert result.itinerary.selected_exhibits == [ 'Africa Savanna' ]

   saved_exhibits = db.conn.execute(
      """   SELECT EXHIBIT
            FROM ItineraryExhibit
            ORDER BY EXHIBIT;
      """ ).fetchall()

   assert [ row[ 'EXHIBIT' ] for row in saved_exhibits ] == [ 'Africa Savanna' ]

   fetched = ItineraryCoordinator.get_itinerary()
   assert fetched.selected_exhibits == [ 'Africa Savanna' ]


def test_set_itinerary_same_date_does_not_expand_selected_exhibits(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
   ).success

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
   )

   assert result.success is True
   assert {
      animal.species
      for animal in result.itinerary.animals
   } == { 'African Lion' }
   assert all( not animal.is_added for animal in result.itinerary.animals )


def test_set_itinerary_date_change_adds_animals_from_persisted_selected_exhibits(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 1, 15 ) )
   assert ItineraryCoordinator.set_itinerary(
      date='2026-01-15',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=-10,
   ).success

   freeze_database_today( date( 2026, 6, 15 ) )
   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=28,
   )

   assert result.success is True

   added_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.is_added
   ]
   assert added_animals
   assert all(
      ( animal.likelihood or 0 ) >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
      for animal in added_animals )
   hyena = next(
      animal
      for animal in added_animals
      if animal.species == 'Spotted Hyena' )
   assert hyena.old_likelihood is not None
   assert hyena.old_likelihood < hyena.likelihood
   assert all(
      animal.species != 'African Lion' or animal.exhibit != 'Africa Savanna'
      for animal in added_animals )

   lion = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.is_added is False


def test_set_itinerary_date_change_adds_animals_from_newly_selected_exhibits(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 10, 17 ) )
   assert ItineraryCoordinator.set_itinerary(
      date='2026-10-17',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=18,
   ).success

   freeze_database_today( date( 2026, 10, 31 ) )
   result = ItineraryCoordinator.set_itinerary(
      date='2026-10-31',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[
         'Africa Savanna',
         'Americas Outdoor Mayan Temple Ruins',
      ],
      visit_date_temp=5,
   )

   assert result.success is True
   assert result.itinerary.selected_exhibits == [
      'Africa Savanna',
      'Americas Outdoor Mayan Temple Ruins',
   ]

   americas_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.exhibit == 'Americas Outdoor Mayan Temple Ruins'
   ]
   assert americas_animals
   assert all( animal.is_added is False for animal in americas_animals )
   assert all(
      ( animal.likelihood or 0 ) >= Constants.ITINERARY_ANIMAL_MIN_LIKELIHOOD
      for animal in americas_animals )


def test_set_itinerary_date_change_marks_frontend_rebuilt_animals_as_added(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 10, 31 ) )
   assert ItineraryCoordinator.set_itinerary(
      date='2026-10-31',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=5,
   ).success

   freeze_database_today( date( 2026, 10, 17 ) )
   # Mimic the builder rebuilding already-selected exhibit animals into the finish
   # payload when the date changes.
   result = ItineraryCoordinator.set_itinerary(
      date='2026-10-17',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
         { 'species': 'Southern White Rhinoceros', 'exhibit': 'Africa Savanna' },
         { 'species': 'River Hippopotamus', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=18,
   )

   assert result.success is True

   rhino = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Southern White Rhinoceros' )
   hippo = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'River Hippopotamus' )
   lion = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'African Lion' )

   assert rhino.is_added is True
   assert hippo.is_added is True
   assert lion.is_added is False


def test_set_itinerary_date_change_does_not_flag_newly_selected_exhibit_animals_as_added(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 10, 17 ) )
   assert ItineraryCoordinator.set_itinerary(
      date='2026-10-17',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=18,
   ).success

   freeze_database_today( date( 2026, 10, 31 ) )
   result = ItineraryCoordinator.set_itinerary(
      date='2026-10-31',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
         {
            'species': 'Capybara',
            'exhibit': 'Americas Outdoor Mayan Temple Ruins',
         },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[
         'Africa Savanna',
         'Americas Outdoor Mayan Temple Ruins',
      ],
      visit_date_temp=5,
   )

   assert result.success is True

   americas_animals = [
      animal
      for animal in result.itinerary.animals
      if animal.exhibit == 'Americas Outdoor Mayan Temple Ruins'
   ]
   assert americas_animals
   assert all( animal.is_added is False for animal in americas_animals )


def test_set_itinerary_date_change_does_not_readd_deselected_exhibit_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 10, 31 ) )
   assert ItineraryCoordinator.set_itinerary(
      date='2026-10-31',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
         {
            'species': 'Capybara',
            'exhibit': 'Americas Outdoor Mayan Temple Ruins',
         },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[
         'Africa Savanna',
         'Americas Outdoor Mayan Temple Ruins',
      ],
      visit_date_temp=5,
   ).success

   freeze_database_today( date( 2026, 10, 17 ) )
   result = ItineraryCoordinator.set_itinerary(
      date='2026-10-17',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=18,
   )

   assert result.success is True
   assert result.itinerary.selected_exhibits == [ 'Africa Savanna' ]
   assert all(
      animal.exhibit != 'Americas Outdoor Mayan Temple Ruins'
      for animal in result.itinerary.animals )


def test_set_itinerary_date_change_swaps_giraffe_house_to_outdoor_instead_of_adding(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 10, 31 ) )
   assert ItineraryCoordinator.set_itinerary(
      date='2026-10-31',
      animals=[
         {
            'species': 'Masai Giraffe',
            'exhibit': 'Africa Savanna',
            'enclosure_name': 'Giraffe House',
         },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=5,
   ).success

   freeze_database_today( date( 2026, 10, 17 ) )
   result = ItineraryCoordinator.set_itinerary(
      date='2026-10-17',
      animals=[
         {
            'species': 'Masai Giraffe',
            'exhibit': 'Africa Savanna',
            'enclosure_name': 'Giraffe House',
         },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=18,
   )

   assert result.success is True

   giraffes = [
      animal
      for animal in result.itinerary.animals
      if animal.species == 'Masai Giraffe'
   ]
   assert len( giraffes ) == 1
   assert giraffes[ 0 ].enclosure_name == 'Outdoor'
   assert giraffes[ 0 ].is_added is False


def test_set_itinerary_date_change_keeps_below_min_likelihood_until_accept(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[
         { 'species': 'Spotted Hyena', 'exhibit': 'Africa Savanna' },
         {
            'species': 'Masai Giraffe',
            'exhibit': 'Africa Savanna',
            'enclosure_name': 'Giraffe House',
         },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      visit_date_temp=28,
   ).success

   freeze_database_today( date( 2026, 1, 15 ) )
   result = ItineraryCoordinator.set_itinerary(
      date='2026-01-15',
      animals=[
         { 'species': 'Spotted Hyena', 'exhibit': 'Africa Savanna' },
         {
            'species': 'Masai Giraffe',
            'exhibit': 'Africa Savanna',
            'enclosure_name': 'Giraffe House',
         },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      visit_date_temp=-10,
   )

   assert result.success is True
   species = { animal.species for animal in result.itinerary.animals }
   assert 'Spotted Hyena' in species
   assert 'Masai Giraffe' in species

   assert ItineraryCoordinator.accept_itinerary()
   after_accept = {
      row[ 'SPECIES' ]
      for row in db.conn.execute( 'SELECT SPECIES FROM ItineraryAnimal;' )
   }
   assert 'Spotted Hyena' not in after_accept
   assert 'Masai Giraffe' in after_accept
