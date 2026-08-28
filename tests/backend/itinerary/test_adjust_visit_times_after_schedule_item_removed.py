from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import CHEETAH_ITINERARY_ENTRY, CHEETAH_KEY, entrance_travel_seconds_to_animal, expected_departure_time_for_itinerary, guardians_talk_save_entry, LION_ITINERARY_ENTRY, LION_KEY, PENGUIN_ITINERARY_ENTRY, PENGUIN_KEY, remove_itinerary_item, schedule_itinerary_item, schedule_time_after_seconds, schedule_time_before_seconds, set_guardians_talk_schedule, set_wild_encounter_schedule, unschedule_itinerary_item, WILD_ENCOUNTER, wild_encounter_wire

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.shared.calendar_dates import DateValues
from api.shared.enums import ScheduleItemKind
from api.walk_graph.data_access.load_walk_graph import load_walk_graph
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver
from conftest import DbControllers

GUARDIANS_TALK = 'African Lion'
LION_TRAVEL_SECONDS = entrance_travel_seconds_to_animal(
   species='African Lion',
   exhibit='Africa Savanna',
)
CHEETAH_START = schedule_time_after_seconds(
   '10:15 AM',
   WalkTravelTimeCalculator.seconds_between_nodes(
      load_walk_graph(),
      ViewingSpotWalkNodeIdResolver.resolve( 'African Lion', 'Africa Savanna', None ),
      ViewingSpotWalkNodeIdResolver.resolve( 'Cheetah', 'Africa Savanna', None ),
   ),
)
PENGUIN_START = schedule_time_after_seconds(
   schedule_time_after_seconds( CHEETAH_START, 15 * 60 ),
   WalkTravelTimeCalculator.seconds_between_nodes(
      load_walk_graph(),
      ViewingSpotWalkNodeIdResolver.resolve( 'Cheetah', 'Africa Savanna', None ),
      ViewingSpotWalkNodeIdResolver.resolve( 'African Penguin', 'Africa Savanna', 'Outdoor' ),
   ),
)


def test_remove_last_wild_encounter_sets_departure_to_previous_last_end(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   set_wild_encounter_schedule( encounter_time='15:30' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   bulk_result = ItineraryCoordinator.bulk_schedule_itinerary()

   assert bulk_result.success
   assert bulk_result.reasons == []

   latest_animal_end = max(
      (
         animal.end_time
         for animal in bulk_result.itinerary.animals
         if animal.end_time is not None
      ),
      key=lambda end_time: DateValues.time_value_in_seconds( end_time ) or -1,
   )
   assert DateValues.time_value_is_at_or_after(
      expected_departure_time_for_itinerary( bulk_result.itinerary ),
      latest_animal_end )

   schedule_result = schedule_itinerary_item(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      wild_encounter_wire( WILD_ENCOUNTER, start_time='15:30' ),
   )

   assert schedule_result.success
   encounter = next(
      saved_encounter
      for saved_encounter in schedule_result.itinerary.wild_encounters
      if saved_encounter.name == WILD_ENCOUNTER )
   assert encounter.end_time is not None
   assert DateValues.time_value_is_at_or_after(
      schedule_result.itinerary.departure_time,
      encounter.end_time )

   remove_result = remove_itinerary_item(
      ScheduleItemKind.WILD_ENCOUNTER.item_type,
      wild_encounter_wire(
         WILD_ENCOUNTER,
         start_time='15:30',
         end_time=encounter.end_time ),
   )

   assert remove_result.success
   assert remove_result.itinerary.departure_time == (
      expected_departure_time_for_itinerary( remove_result.itinerary ) )
   assert remove_result.adjustments == []


def test_remove_first_guardians_talk_sets_arrival_to_new_first_start(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   set_guardians_talk_schedule( talk_time='10:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[ guardians_talk_save_entry( GUARDIANS_TALK, start_time='10:00' ) ],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='11:00',
   ).success

   before = ItineraryCoordinator.get_itinerary()
   talk = next(
      saved_talk
      for saved_talk in before.guardians_talks
      if saved_talk.name == GUARDIANS_TALK )
   lion_before = next(
      animal
      for animal in before.animals
      if animal.species == 'African Lion' )

   assert talk.start_time is not None
   assert lion_before.start_time == '11:00 AM'
   assert DateValues.time_value_is_before(
      talk.start_time,
      lion_before.start_time )

   remove_result = remove_itinerary_item(
      ScheduleItemKind.GUARDIANS_TALK.item_type,
      f'{ GUARDIANS_TALK }||10:00',
   )

   assert remove_result.success
   lion_after = next(
      animal
      for animal in remove_result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion_after.start_time is not None
   assert remove_result.itinerary.arrival_time == schedule_time_before_seconds(
      lion_after.start_time,
      LION_TRAVEL_SECONDS )
   assert remove_result.adjustments == []


def test_unschedule_middle_animal_clears_visit_times_when_day_becomes_incomplete(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='10:00',
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      CHEETAH_KEY,
      start_time='10:30',
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      PENGUIN_KEY,
      start_time='11:00',
   ).success

   before = ItineraryCoordinator.get_itinerary()
   lion = next(
      animal
      for animal in before.animals
      if animal.species == 'African Lion' )
   penguin = next(
      animal
      for animal in before.animals
      if animal.species == 'African Penguin' )

   assert lion.start_time is not None
   assert penguin.end_time is not None
   assert before.arrival_time == schedule_time_before_seconds(
      lion.start_time,
      LION_TRAVEL_SECONDS )
   assert before.departure_time == expected_departure_time_for_itinerary( before )

   result = unschedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      CHEETAH_KEY,
   )

   assert result.success
   assert result.itinerary.arrival_time is None
   assert result.itinerary.departure_time is None
   assert result.adjustments == []


def test_unschedule_middle_animal_clears_pinned_departure_when_day_becomes_incomplete(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
         PENGUIN_ITINERARY_ENTRY,
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='10:00',
      duration_minutes=15,
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      CHEETAH_KEY,
      start_time=CHEETAH_START,
      duration_minutes=15,
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      PENGUIN_KEY,
      start_time=PENGUIN_START,
      duration_minutes=15,
   ).success

   scheduled = ItineraryCoordinator.get_itinerary()
   penguin_before = next(
      animal
      for animal in scheduled.animals
      if animal.species == 'African Penguin' )
   assert penguin_before.end_time is not None
   assert ItineraryCoordinator.set_departure_time(
      penguin_before.end_time,
      confirming_short_visit=True,
   ).success

   before = ItineraryCoordinator.get_itinerary()
   assert before.departure_time == penguin_before.end_time

   result = unschedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      CHEETAH_KEY,
   )

   assert result.success
   assert result.itinerary.arrival_time is None
   assert result.itinerary.departure_time is None
   assert result.adjustments == []
