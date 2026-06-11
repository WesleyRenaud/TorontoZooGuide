from __future__ import annotations

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
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

