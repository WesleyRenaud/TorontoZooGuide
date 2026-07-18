from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import GUARDIANS_TALK, guardians_talk_save_entry, LION_ITINERARY_ENTRY, LION_KEY, schedule_itinerary_item, set_guardians_talk_schedule, set_wild_encounter_schedule, WILD_ENCOUNTER, wild_encounter_key

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.models import Itinerary
from api.shared.calendar_dates import DateValues
from api.shared.enums import ScheduleItemKind
from conftest import DbControllers


def _scheduled_animal_times(
      itinerary: Itinerary ) -> list[ tuple[ str, str | None, str | None ] ]:
   return [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ]


def test_set_itinerary_removing_wild_encounter_preserves_animal_schedules(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   set_wild_encounter_schedule( encounter_time='15:30' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='15:30' ),
      ],
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='10:00',
   ).success

   before_times = _scheduled_animal_times( ItineraryCoordinator.get_itinerary() )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary is not None
   assert result.itinerary.wild_encounters == []
   assert _scheduled_animal_times( result.itinerary ) == before_times


def test_set_itinerary_removing_guardians_talk_preserves_animal_schedules(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   set_guardians_talk_schedule( talk_time='11:00' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[
         guardians_talk_save_entry( GUARDIANS_TALK, start_time='11:00' ),
      ],
      wild_encounters=[],
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='10:00',
   ).success

   before_times = _scheduled_animal_times( ItineraryCoordinator.get_itinerary() )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary is not None
   assert result.itinerary.guardians_talks == []
   assert _scheduled_animal_times( result.itinerary ) == before_times


def test_set_itinerary_removing_first_talk_updates_arrival_to_next_start(
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
      guardians_talks=[
         guardians_talk_save_entry( GUARDIANS_TALK, start_time='10:00' ),
      ],
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

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time=before.arrival_time,
      departure_time=before.departure_time,
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary is not None
   assert result.itinerary.guardians_talks == []
   lion_after = next(
      animal
      for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion_after.start_time == '11:00 AM'
   assert result.itinerary.arrival_time == lion_after.start_time
   assert result.adjustments == []


def test_set_itinerary_later_arrival_without_cutoff_preserves_animal_schedules(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='11:00',
   ).success

   before_times = _scheduled_animal_times( ItineraryCoordinator.get_itinerary() )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='10:00',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary is not None
   assert result.itinerary.arrival_time == '10:00 AM'
   assert _scheduled_animal_times( result.itinerary ) == before_times


def test_set_itinerary_later_arrival_that_cuts_off_items_reschedules_animals(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      start_time='10:00',
   ).success

   before_times = _scheduled_animal_times( ItineraryCoordinator.get_itinerary() )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='10:30',
      departure_time='17:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   )

   assert result.success
   assert result.itinerary is not None
   assert _scheduled_animal_times( result.itinerary ) != before_times
   lion = next(
      animal for animal in result.itinerary.animals
      if animal.species == 'African Lion' )
   assert lion.start_time is not None
   assert lion.end_time is not None
   assert not (
      lion.start_time == '10:00 AM'
      and lion.end_time == '10:08 AM'
   )
