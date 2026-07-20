from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.shared.constants import ITINERARY_ANIMAL_MIN_LIKELIHOOD
from conftest import DbControllers


def test_set_itinerary_expands_selected_exhibits_into_viewable_animals(
      db: DbControllers ) -> None:
   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
   )

   assert result.success is True

   saved_animals = db.conn.execute(
      """   SELECT SPECIES, EXHIBIT
            FROM ItineraryAnimal
            WHERE EXHIBIT = 'Africa Savanna'
            ORDER BY SPECIES;
      """ ).fetchall()

   assert saved_animals
   assert {
      row[ 'EXHIBIT' ]
      for row in saved_animals
   } == { 'Africa Savanna' }


def test_set_itinerary_exhibit_expand_excludes_animals_below_min_likelihood(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 1, 15 ) )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-01-15',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      visit_date_temp=-10,
   )

   assert result.success is True
   saved_species = {
      animal.species
      for animal in result.itinerary.animals
   }
   assert 'Spotted Hyena' not in saved_species
   assert 'Watusi Cattle' not in saved_species
   assert 'African Lion' in saved_species

   for animal in result.itinerary.animals:
      assert ( animal.likelihood or 0 ) >= ITINERARY_ANIMAL_MIN_LIKELIHOOD


def test_set_itinerary_marks_exhibit_expanded_animals_as_added_on_update(
      db: DbControllers ) -> None:
   ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[],
   )

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

   added_rows = db.conn.execute(
      """   SELECT SPECIES, EXHIBIT, IS_ADDED
            FROM ItineraryAnimal
            WHERE IS_ADDED = 1
            ORDER BY SPECIES;
      """ ).fetchall()

   assert added_rows
   assert all( row[ 'IS_ADDED' ] == 1 for row in added_rows )
   assert {
      ( row[ 'SPECIES' ], row[ 'EXHIBIT' ] )
      for row in added_rows
   } != { ( 'African Lion', 'Africa Savanna' ) }

   added_in_response = [
      animal
      for animal in result.itinerary.animals
      if animal.is_added
   ]
   assert added_in_response
   assert all(
      animal.species != 'African Lion' or animal.exhibit != 'Africa Savanna'
      for animal in added_in_response )


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
