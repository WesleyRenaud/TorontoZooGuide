from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import itinerary_animals_for_exhibits

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.scheduling.bulk.bulk_schedule_animals import has_itinerary_schedule_times
from api.shared.calendar_dates import DateValues
from conftest import DbControllers


def _scheduled_animal_order(
      db: DbControllers,
      *,
      freeze_database_today: Callable[ [ date ], None ],
) -> list[ tuple[ str, str | None, str | None, str | None ] ]:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=itinerary_animals_for_exhibits(
         [ 'Africa Savanna' ],
         visit_date='2026-06-20' ),
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


def test_bulk_schedule_africa_savanna_has_no_savanna_overlook_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   scheduled_order = _scheduled_animal_order(
      db,
      freeze_database_today=freeze_database_today )

   pavilion_routed_species = {
      'Greater Kudu',
      'Marabou Stork',
      'Ostrich',
      'Southern Ground Hornbill',
      'White-Headed Vulture',
   }

   assert not any(
      row[ 0 ] in pavilion_routed_species and row[ 1 ] == 'Savanna Overlook'
      for row in scheduled_order )


def test_bulk_schedule_africa_savanna_has_no_savanna_grasslands_zebra(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ],
) -> None:
   scheduled_order = _scheduled_animal_order(
      db,
      freeze_database_today=freeze_database_today )

   assert not any(
      row[ 0 ] == "Grevy's Zebra" and row[ 1 ] == 'Savanna Grasslands'
      for row in scheduled_order )


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
      None,
      'White Rhino Viewing',
      'Kesho Park Offshoot',
   ]
