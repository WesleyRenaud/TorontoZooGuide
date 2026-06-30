from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_saved_itinerary
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.itinerary.scheduling.bulk.bulk_schedule_walk_order import sort_animals_for_bulk_schedule
from api.request_connection import get_connection
from api.shared.calendar_dates import DateValues
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.enclosure_viewing_walk_node_lookup import walk_node_id_by_enclosure_name
from conftest import DbControllers


def _scheduled_animal_order(
      db: DbControllers,
      *,
      freeze_database_today: Callable[ [ date ], None ],
) -> list[ tuple[ str, str | None, str | None, str | None ] ]:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_animals()

   assert result.success

   return sorted(
      [
         (
            animal.species,
            animal.enclosure_name,
            animal.start_time,
            animal.end_time,
         )
         for animal in result.itinerary.animals
         if has_itinerary_schedule_times( animal.start_time, animal.end_time )
      ],
      key=lambda row: DateValues.time_value_in_seconds( row[ 2 ] ) or 0,
   )


def test_bulk_schedule_africa_savanna_groups_savanna_overlook_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   scheduled_order = _scheduled_animal_order(
      db,
      freeze_database_today=freeze_database_today )

   savanna_overlook_rows = [
      row
      for row in scheduled_order
      if row[ 1 ] == 'Savanna Overlook'
   ]

   assert savanna_overlook_rows

   first_savanna_overlook_index = next(
      index
      for index, row in enumerate( scheduled_order )
      if row[ 1 ] == 'Savanna Overlook' )
   last_savanna_overlook_index = len( scheduled_order ) - 1 - next(
      index
      for index, row in enumerate( reversed( scheduled_order ) )
      if row[ 1 ] == 'Savanna Overlook' )

   for index in range(
         first_savanna_overlook_index,
         last_savanna_overlook_index + 1 ):
      assert scheduled_order[ index ][ 1 ] == 'Savanna Overlook'


def test_bulk_schedule_africa_savanna_schedules_null_enclosure_ostrich_after_named_viewing_spots(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   scheduled_order = _scheduled_animal_order(
      db,
      freeze_database_today=freeze_database_today )

   ostrich_rows = [
      row
      for row in scheduled_order
      if row[ 0 ] == 'Ostrich'
   ]

   assert [ row[ 1 ] for row in ostrich_rows ] == [
      'Savanna Overlook',
      'Kesho Park Offshoot',
      'White Rhino Viewing',
      None,
   ]


def test_sort_animals_for_bulk_schedule_does_not_split_savanna_overlook_with_null_enclosure_name(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      selected_exhibits=[ 'Africa Savanna' ],
      confirming_early_admission=True,
   ).success

   saved_itinerary = fetch_saved_itinerary( get_connection() )
   graph = load_walk_graph()
   ordered = sort_animals_for_bulk_schedule(
      graph,
      saved_itinerary.animal_rows,
      start_node_id=str( graph[ 'entrance_node_id' ] ) )

   savanna_overlook_indexes = [
      index
      for index, animal_row in enumerate( ordered )
      if animal_row.enclosure_name == 'Savanna Overlook'
   ]

   assert savanna_overlook_indexes

   first_index = savanna_overlook_indexes[ 0 ]
   last_index = savanna_overlook_indexes[ -1 ]

   for index in range( first_index, last_index + 1 ):
      animal_row = ordered[ index ]
      walk_node_id = walk_node_id_by_enclosure_name().get(
         ( animal_row.species, animal_row.exhibit, animal_row.enclosure_name ) )

      assert animal_row.enclosure_name == 'Savanna Overlook', (
         'Expected Savanna Overlook at index '
         f'{ index }, got { animal_row.species } '
         f'{ animal_row.enclosure_name } walk node { walk_node_id }'
      )
