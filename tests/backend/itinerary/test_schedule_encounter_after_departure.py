from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import LION_ITINERARY_ENTRY, LION_KEY, schedule_itinerary_item, set_wild_encounter_schedule, WILD_ENCOUNTER, wild_encounter_key

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


def test_set_itinerary_keeps_wild_encounter_after_departure_without_reschedule(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   set_wild_encounter_schedule( encounter_time='15:30' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='12:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success
   assert schedule_itinerary_item(
      ScheduleItemKind.ANIMAL.item_type,
      LION_KEY,
      confirming_schedule_item_not_on_itinerary=True,
   ).success

   before_times = _scheduled_animal_times( ItineraryCoordinator.get_itinerary() )

   result = ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='12:00',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[
         wild_encounter_key( WILD_ENCOUNTER, start_time='15:30' ),
      ],
   )

   assert result.success
   assert result.itinerary is not None

   encounter = next(
      saved_encounter
      for saved_encounter in result.itinerary.wild_encounters
      if saved_encounter.name == WILD_ENCOUNTER )
   assert encounter.start_time == '3:30 PM'
   assert encounter.end_time is not None
   assert DateValues.time_value_is_at_or_after(
      result.itinerary.departure_time,
      encounter.end_time )
   assert _scheduled_animal_times( result.itinerary ) == before_times
