from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CHEETAH_INDO_MALAYA_ITINERARY_ENTRY, entrance_travel_seconds_to_animal, expected_departure_time_for_itinerary, LION_ITINERARY_ENTRY, LION_KEY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, schedule_itinerary_item, schedule_time_after_seconds, schedule_time_before_seconds

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.walk_travel_time import travel_time_seconds_between_nodes
from api.itinerary.scheduling.core.guest_item_schedule_status_checker import GuestItemScheduleStatusChecker
from api.shared.calendar_dates import DateValues
from api.shared.enums import ItineraryErrorType
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.walk_node_id_for_viewing_spot import walk_node_id_for_viewing_spot
from conftest import DbControllers

LION_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='African Lion',
   exhibit='Africa Savanna',
)
CHEETAH_INDO_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='Cheetah',
   exhibit='Indo-Malaya Outdoor',
)


def _travel_seconds_between_animals(
      *,
      from_species: str,
      from_exhibit: str,
      to_species: str,
      to_exhibit: str,
      from_enclosure_name: str | None = None,
      to_enclosure_name: str | None = None ) -> int:
   walk_graph = load_walk_graph()
   from_node_id = walk_node_id_for_viewing_spot(
      from_species,
      from_exhibit,
      from_enclosure_name )
   to_node_id = walk_node_id_for_viewing_spot(
      to_species,
      to_exhibit,
      to_enclosure_name )
   assert from_node_id is not None
   assert to_node_id is not None

   return travel_time_seconds_between_nodes(
      walk_graph,
      from_node_id,
      to_node_id )


def test_bulk_schedule_itinerary_schedules_animals_in_travel_efficient_order(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_INDO_MALAYA_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []
   assert result.itinerary.arrival_time == '9:30 AM'

   cheetah = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'Cheetah' )
   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )

   expected_cheetah_start = schedule_time_after_seconds(
      '9:30 AM',
      CHEETAH_INDO_TRAVEL_SECONDS )
   expected_cheetah_end = schedule_time_after_seconds( expected_cheetah_start, 5 * 60 )
   expected_lion_start = schedule_time_after_seconds(
      expected_cheetah_end,
      _travel_seconds_between_animals(
         from_species='Cheetah',
         from_exhibit='Indo-Malaya Outdoor',
         to_species='African Lion',
         to_exhibit='Africa Savanna' ) )
   expected_lion_end = schedule_time_after_seconds( expected_lion_start, 8 * 60 )

   assert cheetah.start_time == expected_cheetah_start
   assert cheetah.end_time == expected_cheetah_end
   assert lion.start_time == expected_lion_start
   assert lion.end_time == expected_lion_end
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


def test_bulk_schedule_itinerary_sets_arrival_time_to_zoo_open_when_unset(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   itinerary_before = ItineraryCoordinator.get_itinerary()
   assert itinerary_before.arrival_time is None
   assert itinerary_before.departure_time is None

   result = ItineraryCoordinator.bulk_schedule_itinerary()
   expected_start = schedule_time_after_seconds( '9:30 AM', LION_TRAVEL_SECONDS )
   expected_end = schedule_time_after_seconds( expected_start, 8 * 60 )

   assert result.success
   assert result.itinerary.arrival_time == '9:30 AM'
   assert result.itinerary.animals[ 0 ].start_time == expected_start
   assert result.itinerary.animals[ 0 ].end_time == expected_end
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


def test_bulk_schedule_itinerary_uses_early_admission_when_warning_suppressed(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   assert ItineraryCoordinator.suppress_itinerary_warning(
      ItineraryErrorType.EARLY_ADMISSION_REQUIRES_MEMBERSHIP.value ).success

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()
   expected_start = schedule_time_after_seconds( '9:00 AM', LION_TRAVEL_SECONDS )
   expected_end = schedule_time_after_seconds( expected_start, 8 * 60 )

   assert result.success
   assert result.itinerary.arrival_time == '9:00 AM'
   assert result.itinerary.animals[ 0 ].start_time == expected_start
   assert result.itinerary.animals[ 0 ].end_time == expected_end
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


def test_bulk_schedule_itinerary_sets_departure_to_last_animal_end_when_departure_was_set(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()
   expected_end = schedule_time_after_seconds(
      schedule_time_after_seconds( '9:30 AM', LION_TRAVEL_SECONDS ),
      8 * 60 )

   assert result.success
   assert result.reasons == []
   assert result.itinerary.animals[ 0 ].end_time == expected_end
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


def test_bulk_schedule_itinerary_rebuild_reschedules_already_scheduled_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.reasons == []

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin' )

   assert lion.start_time is not None
   assert lion.end_time is not None
   assert penguin.start_time is not None
   assert penguin.end_time is not None
   assert lion.start_time != '09:00'

   lion_start_seconds = DateValues.time_value_in_seconds( lion.start_time )
   penguin_start_seconds = DateValues.time_value_in_seconds( penguin.start_time )
   assert lion_start_seconds is not None
   assert penguin_start_seconds is not None
   earliest_animal = (
      lion
      if lion_start_seconds <= penguin_start_seconds
      else penguin )
   earliest_travel_seconds = entrance_travel_seconds_to_animal(
      species=earliest_animal.species,
      exhibit=earliest_animal.exhibit,
      enclosure_name=earliest_animal.enclosure_name )
   assert result.itinerary.arrival_time == schedule_time_before_seconds(
      earliest_animal.start_time,
      earliest_travel_seconds )

   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )


def test_bulk_schedule_itinerary_rebuild_reschedules_when_all_animals_are_already_scheduled(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=PENGUIN_KEY,
   ).success

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success
   assert result.status == ItineraryErrorType.SUCCESS
   assert result.reasons == []
   assert {
      animal.species
      for animal in result.itinerary.animals
      if GuestItemScheduleStatusChecker.has_schedule_times( animal.start_time, animal.end_time )
   } == { 'African Lion', 'African Penguin' }


def test_bulk_schedule_itinerary_preserves_custom_animal_duration(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      animals=[
         LION_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   scheduled = schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='10:00',
      duration_minutes=20 )

   assert scheduled.success
   lion_before = next(
      animal for animal in scheduled.itinerary.animals
      if animal.species == 'African Lion' )
   custom_duration_seconds = (
      DateValues.time_value_in_seconds( lion_before.end_time )
      - DateValues.time_value_in_seconds( lion_before.start_time )
   )
   assert custom_duration_seconds == 20 * 60

   result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert result.success

   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   penguin = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Penguin' )

   lion_duration_seconds = (
      DateValues.time_value_in_seconds( lion.end_time )
      - DateValues.time_value_in_seconds( lion.start_time )
   )
   penguin_duration_seconds = (
      DateValues.time_value_in_seconds( penguin.end_time )
      - DateValues.time_value_in_seconds( penguin.start_time )
   )

   assert lion_duration_seconds == custom_duration_seconds
   # Unscheduled companion still gets the enclosure default (5 minutes).
   assert penguin_duration_seconds == 5 * 60
