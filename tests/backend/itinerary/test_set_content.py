from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
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
